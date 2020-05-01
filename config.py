import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class Constants(object):
  PUSHER_CHANNEL = 'danish-channel'
  PUSHER_APP_ID = 'ff61f4ea6365adab4736'

  def JOIN_EVENT(game_id):
      return 'joining-game-' + str(game_id)

  def INIT_EVENT(game_id):
      return 'init-game-' + str(game_id)

  def CHANGE_TURN_EVENT(game_id):
      return 'change-turn-' +str(game_id)

  def WIN_EVENT(game_id):
      return 'game-won-' + str(game_id)
