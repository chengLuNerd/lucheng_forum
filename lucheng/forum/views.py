"""
lucheng.forum.views.

This module handles the  forum logic like creating and viewing
topics and post.
"""
from flask import Blueprint, render_template

from lucheng.forum.models import Category
from lucheng.user.models import User


forum = Blueprint("forum", __name__)


@forum.route("/")
def index():
    """Forum index route function."""
    categories = Category.get_all()
    user_count = 1
    topic_count = 1
    post_count = 1

    return render_template('forum/index.html',
                           categories=categories,
                           user_count=user_count,
                           topic_count=topic_count,
                           post_count=post_count)


@forum.route("/memberlist")
def memberlist():
    """Memberlist show logic view."""
    users = User.query.all()
    return render_template("forum/memberlist.html", users=users)
