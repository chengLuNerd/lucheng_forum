"""
summary: models.py.

description: xxx
"""
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_login import UserMixin
from lucheng.extensions import db

groups_users = db.Table(
    'groups_users',
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')))


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


class User(db.Model, UserMixin):
    """User define."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    def _get_password(self):
        """Return the hashed password."""
        return self._password

    def _set_password(self, password):
        """Check password, If password match it returns True, else False."""
        if password is None:
            return False
        self._password = generate_password_hash(password)

    _password = db.Column('password', db.String(120), nullable=False)
    password = db.synonym('_password',
                          descriptor=property(_get_password, _set_password))
    activated = db.Column(db.Boolean, default=False)

    primary_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'),
                                 nullable=False)
    secondary_groups = db.relationship(
        'Group',
        secondary=groups_users,
        primaryjoin=(groups_users.c.user_id == id),
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic')

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.

        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.username)

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false."""
        if self.password is None:
            return False
        print("-------------------------------------")
        print(password)
        return check_password_hash(self.password, password)

    '''
    @classmethod
    def authenticate(cls, username, password):
        """Check user legal."""
        user = cls.query().filter(db.or_(User.username == username,
                                         User.email == username)).first()
        if user is not None:
            if user.check_password(password):
                return user
    '''
