"""
forum model define file.

Forum Category and so on
"""
import itertools
import operator
from sqlalchemy.orm import aliased

from lucheng.extensions import db

# m2m table for group-forum permission mapping
forumgroups = db.Table(
    'forumgroups',
    db.Column(
        'group_id',
        db.Integer(),
        db.ForeignKey('groups.id'),
        nullable=False
    ),
    db.Column(
        'forum_id',
        db.Integer(),
        db.ForeignKey('forums.id', use_alter=True, name="fk_forum_id"),
        nullable=False
    )
)


class Forum(db.Model):
    """Forum model define."""

    __tablename__ = "forums"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    position = db.Column(db.Integer, default=1, nullable=False)

    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"),
        nullable=False
    )

    groups = db.relationship(
        "Group",
        secondary=forumgroups,
        primaryjoin=(forumgroups.c.forum_id == id),
        backref="forumgroups",
        lazy="joined",
    )

    def save(self, groups=None):
        """Save the object to the database."""
        from lucheng.user.models import Group
        if groups is None:
            self.groups = Group.query.order_by(Group.name.asc()).all()
        db.session.add(self)
        db.session.commit()
        return self


class Category(db.Model):
    """Category model define."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    position = db.Column(db.Integer, default=1, nullable=False)

    # one to many
    forums = db.relationship(
        "Forum", backref="category", lazy="dynamic",
        primaryjoin='Forum.category_id == Category.id',
        order_by='asc(Forum.position)',
        cascade='all, delete-orphan'
    )

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_all(cls, user):
        """Get all categories with all associated forums.

        It returns a list with tuples. Those tuples are containing the category
        and their associated forums (whose are stored in a list).

        For example::

            [(<Category 1>, [(<Forum 2>, <ForumsRead>), (<Forum 1>, None)]),
             (<Category 2>, [(<Forum 3>, None), (<Forum 4>, None)])]

        :param user: The user object is needed to check if we also need their
                     forumsread object.
        """
        if user.is_authenticated:
            from lucheng.user.models import Group
            # forums = Forum.query.subquery()
            # get list of user group ids
            user_groups = [group.id for group in user.groups]
            # filter forums by user groups
            user_forums = Forum.query.\
                filter(Forum.groups.any(Group.id.in_(user_groups))).subquery()
            forum_alias = aliased(Forum, user_forums)

            query_result = cls.query.\
                join(forum_alias, cls.id == forum_alias.category_id).\
                add_entity(forum_alias).\
                all()
            # print(query_result)
        else:
            query_result = cls.query.join(Forum, cls.id == Forum.category_id).\
                add_entity(Forum).\
                all()

        forums = []
        it = itertools.groupby(query_result, operator.itemgetter(0))

        for key, value in it:
            forums.append((key, [item[1] for item in value]))

        return forums


class Topic(db.Model):
    """Topic model define."""

    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer,
                         db.ForeignKey("forums.id",
                                       use_alter=True,
                                       name="fk_topic_forum_id"),
                         nullable=False)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String(200), nullable=False)

    def save(self, user=None, forum=None, post=None):
        """
        Save a topic and returns the topic object.

        If no parameters are given, it will only update the topic.

        :param user: The user who has created the topic
        :param forum: The forum where the topic is stored
        :param post: The post object which is connected to the topic
        """
        # Updates the topic
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # Set the forum and user id
        self.forum_id = forum.id
        self.user_id = user.id
        self.username = user.username

        # Insert and commit the topic
        db.session.add(self)
        db.session.commit()

        # Create the topic post
        post.save(user, self)


class Post(db.Model):
    """Post model define."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer,
                         db.ForeignKey("topics.id",
                                       use_alter=True,
                                       name="fk_post_topic_id",
                                       ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    username = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def save(self, user=None, topic=None):
        """Save a new post.

        If no parameters are passed we assume that
        you will just update an existing post. It returns the object after the
        operation was successful.

        :param user: The user who has created the post
        :param topic: The topic in which the post was created
        """
        self.user_id = user.id
        self.username = user.username
        self.topic_id = topic.id
        db.session.add(self)
        db.session.commit()
