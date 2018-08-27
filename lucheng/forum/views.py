"""
lucheng.forum.views.

This module handles the  forum logic like creating and viewing
topics and post.
"""
from flask import Blueprint, render_template

forum = Blueprint("forum", __name__)


@forum.route("/")
def index():
    """Forum index route function."""
    return render_template('forum/index.html')
