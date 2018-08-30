"""
summary: populate.py create data tool.

description: xxx
"""
from lucheng.user.models import (Group, User)


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
