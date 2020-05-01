from app import db
from models import Users, Games, Cards

for u in Users.query.all():
    db.session.delete(u)

for g in Games.query.all():
    db.session.delete(g)

for c in Cards.query.all():
    db.session.delete(c)

db.session.commit()

print('reset db successfully')
