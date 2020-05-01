from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pusher

app = Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)
migrate=Migrate(app, db)

pusher_client = pusher.Pusher(
  app_id='983636',
  key='ff61f4ea6365adab4736',
  secret='27490296aa9ef7371930',
  cluster='us2',
  ssl=True
)

if __name__ == '__main__':
    app.run()

import models, routes
