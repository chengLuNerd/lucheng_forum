"""
lucheng.forum.forms .

It provides the forms that are needed for the auth views.

:copyright: (c) 2014 by the FlaskBB Team.
:license: BSD, see LICENSE for more details.
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField)
from wtforms.validators import (DataRequired, Optional, Length)

class UserSearchForm(FlaskForm):
    """memberlist Search Form define."""
    search_query = StringField("Search",validators=[
        Optional(), Length(min=3, max=50)])

    submit = SubmitField("Search")
