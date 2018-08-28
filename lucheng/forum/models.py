"""
forum model define file.

Forum Category and so on
"""
from lucheng.extensions import db


class Forum(db.Model):
    """Forum model define."""

    __table__ = "forums"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    position = db.Column(db.Integer, default=1, nullable=False)

    category_id = db.Column(
        db.Integer, db.Foreignkey("categories.id"),
        nullable=False
    )


class Category(db.Model):
    """Category model define."""

    __table__ = "categories"

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
