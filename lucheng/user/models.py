
class Group(db.Model):
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
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {} {}>".format(self.__class__.__name__, self.id, self.name)
