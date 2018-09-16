"""
summary: populate.py create data tool.

description: xxx
"""
from lucheng.user.models import (Group, User)
from lucheng.forum.models import (Forum, Category, Topic, Post)


def create_default_groups():
    """Create the 5 default groups."""
    from lucheng.fixtures.groups import group_fixture
    result = []
    for key, value in group_fixture.items():
        group = Group(name=key)

        for k, v in value.items():
            setattr(group, k, v)

        group.save()
        result.append(group)

    return result


def create_user(username, password, email, groupname):
    """
    Create a user.

    Returns the created user.
    :param username: The username of the user.
    :param password: The password of the user.
    :param email: The email address of the user.
    :param groupname: The name of the group to which the user
                      should belong to.
    """
    # group = Group.query.filter(name==groupname)
    group = Group.query.filter(getattr(Group, groupname) == True).first()
    """
    user = User.create(
            username=username, password=password, email=email,
            primary_group_id=group.id, activate=True)
    """
    user = User(username=username, password=password, email=email,
                primary_group_id=group.id, activated=True)
    user.save()

    return user


def create_welcome_forum():
    """
    Create the 'welcome forum' with a welcome topic.

    Returns True if it's created succesfully
    """
    if User.query.count() < 1:
        return False

    user = User.query.filter_by(id=1).first()

    category = Category(title="My Category", position=1)
    category.save()

    forum = Forum(title="welcome", description="Your first forum",
                  category_id=category.id)
    forum.save()

    topic = Topic(title="Welcome!")
    post = Post(content="Have fun with your new lucheng Forum!")

    topic.save(user=user, forum=forum, post=post)

    return True
