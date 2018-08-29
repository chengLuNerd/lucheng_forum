from lucheng.user.models import Group

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

