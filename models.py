from app import db

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), index=True, unique=True)
    users = db.relationship('Users', backref='currentgame', lazy='dynamic' )
    cards = db.relationship('Cards', backref='deck', lazy='dynamic' )
    currentPlayerIndex = db.Column(db.Integer)
    def __repr__(self):
        return '<Game {}>'.format(self.code)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    cards = db.relationship('Cards', backref='hand', lazy='dynamic')
    usingDownCards=db.Column(db.Boolean)
    isAdmin=db.Column(db.Boolean)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suit = db.Column(db.String(1))
    value = db.Column(db.Integer)
    name = db.Column(db.String(3))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    #null means its in the pile, deck, or discarded
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    #location can be 'uphand', 'downhand', 'hand', 'pile', 'deck', 'None (discarded)'
    location = db.Column(db.String(10))
    def __repr__(self):
        return '<Card {}>'.format(self.name)
