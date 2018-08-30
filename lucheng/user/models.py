"""
summary: models.py.

description: xxx
"""
from lucheng.extensions import db

groups_users = db.Table(
    'groups_users',
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
    )


class Group(db.Model):
    """Group define."""

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Group types
    admin = db.Column(db.Boolean, default=False, nullable=False)
    super_mod = db.Column(db.Boolean, default=False, nullable=False)
    mod = db.Column(db.Boolean, default=False, nullable=False)
    guest = db.Column(db.Boolean, default=False, nullable=False)
    banned = db.Column(db.Boolean, default=False, nullable=False)

    # Moderator permissions (only available when the user a moderator)
    mod_edituser = db.Column(db.Boolean, default=False, nullable=False)
    mod_banuser = db.Column(db.Boolean, default=False, nullable=False)

    # User permissions
    editpost = db.Column(db.Boolean, default=True, nullable=False)
    deletepost = db.Column(db.Boolean, default=False, nullable=False)
    deletetopic = db.Column(db.Boolean, default=False, nullable=False)
    posttopic = db.Column(db.Boolean, default=True, nullable=False)
    postreply = db.Column(db.Boolean, default=True, nullable=False)

    # Methods
    def __repr__(self):
        """
        Set to a unique key specific to the object in the database.

        Required for cache.memoize() to work across requests.
        """
        return "<{} {} {}>".format(self.__class__.__name__, self.id, self.name)

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self


class User(db.Model):
    """User define."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)

    activated = db.Column(db.Boolean, default=False)

    primary_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'),
                                 nullable=False)
    secondary_groups = db.relationship(
                        'Group',
                        secondary=groups_users,
                        primaryjoin=(groups_users.c.user_id == id),
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self
