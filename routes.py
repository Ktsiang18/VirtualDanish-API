from app import app, pusher_client
from controller import *
import json
from flask import request, render_template
from config import Constants

@app.route('/')
def hello():
    return render_template('./pusherTest.html')

#--------- USER INIT -------------
@app.route("/nameForm", methods=['POST'])
def nameForm():
    data = json.loads(request.data)
    [user, message] = createUserByName(data['name'])
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'is_admin': user.isAdmin,
            'message': message
        }
    }


@app.route("/joinGame", methods=['POST'])
def joinGame():
    data = json.loads(request.data)
    [game, message] = addUserToGame(data['code'], data['user_id'])

    if not game:
        return {'game_id': None, 'message': message}

    game_users = [{'id': u.id, 'username': u.username, 'isAdmin': u.isAdmin } for u in game.users]
    pusher_client.trigger(Constants.PUSHER_CHANNEL, Constants.JOIN_EVENT(game.id), \
                {'message': message, 'game_users': game_users})

    return {
            'game_id': game.id,
            'game_code': game.code,
            'game_users': game_users,
            'message': message,
        }

#--------- GAME INIT -------------
@app.route("/fetchGame/<game_id>", methods=['GET'])
def fetchGame(game_id):
    g = getGame(game_id)
    users = list({'id': u.id, 'username': u.username, 'isAdmin': u.isAdmin} for u in g.users)
    return {
        'game': {
            'id': g.id,
            'code': g.code,
            'users': users
        }
    }

@app.route("/fetchUser/<user_id>", methods=['GET'])
def fetchUser(user_id):
    u = getUser(user_id)
    return {
        'user': {
            'id': u.id,
            'username': u.username,
            'isAdmin': u.isAdmin,
            'game_id': u.game_id
        }
    }


@app.route("/createGame", methods=['POST'])
def createGame():
    data = json.loads(request.data)
    [game, message] = createNewGame(data['user_id'])
    print(message)

    return {
        'game_id': game.id,
        'game_code': game.code,
        'game_users': [ {'id': u.id, 'username': u.username } for u in game.users],
        'message': message,
    }

@app.route("/initGame", methods=['POST'])
def initGame():
    data=json.loads(request.data)
    initializeGame(data['game_id'])
    pusher_client.trigger(Constants.PUSHER_CHANNEL, Constants.INIT_EVENT(data['game_id']), {})
    return {
        'message': 'success'
    }

#----CARDS----
@app.route("/getUsersCards/<user_id>/", methods=['GET'])
def getUsersCards(user_id):
    [result, message] = getCards(user_id)

    if result['gameWon']:
        pusher_client.trigger(Constants.PUSHER_CHANNEL, Constants.WIN_EVENT(result['gameId']), {'winner_id': user_id})
    return result

@app.route("/setUsersCards", methods=['POST'])
def setUsersCards():
    data = json.loads(request.data)
    for type in ['hand', 'uphand', 'downhand']:
        if type in data['cards']:
            setUsersCardsByType(type, data['cards'][type], data['user_id'])
    return {
        'message' : 'successfully updated cards'
    }

#---GAME STATE-----
@app.route("/getPileTop/<user_id>/", methods=['GET'])
def getPileTop(user_id):
    [card, message] = getPileTopByUser(user_id)
    if card:
        serialized = {
            'id': card.id,
            'suit': card.suit,
            'value': card.value,
            'name':card.name,
        }
    else:
        serialized = {'name': None}
    serialized['message'] = message
    return serialized

@app.route("/clearPile", methods=['POST'])
def clearPileCards():
    data=json.loads(request.data)
    clearPile(data['user_id'])

@app.route("/getDeckSize/<user_id>", methods=['GET'])
def getDeckSize(user_id):
    size = getDeckLength(user_id)
    return {
        'deck_size': size
    }

@app.route("/getCurrentPlayer/<user_id>/", methods=['GET'])
def getCurrentPlayer(user_id):
    [player, message] = getCurrentPlayerByUser(user_id)
    return {
        'player_id': player.id,
        'player_username': player.username,
        'message': message
    }

#---Players turn----
@app.route("/validatePlayableCards", methods=['POST'])
def validatePlayableCards():
    data = json.loads(request.data)
    [validated, message] = validateCards(data['card_ids'], data['user_id'])
    return {
        'valid': validated,
        'message': message
    }

@app.route("/playCards", methods=['POST'])
def playCards():
    data = json.loads(request.data)
    message = playValidatedCards(data['card_ids'], data['user_id'])
    return message

@app.route("/pickUpPile", methods=['POST'])
def pickUpPile():
    data = json.loads(request.data)
    message = addPileToUser(data['user_id'])
    return message


@app.route("/refillHand", methods=['POST'])
def refillHand():
    data = json.loads(request.data)
    [newCards, message] = refillUsersHand(data['user_id'])
    return {
        'new_cards': [c.name for c in newCards],
        'message': message
    }

@app.route("/updateCurrentPlayer", methods=['POST'])
def updateCurrentPlayer():
    data = json.loads(request.data)
    [currentPlayer, message] = changeToNextPlayer(data['user_id'])
    [topCard, _] =  getPileTopByUser(data['user_id'])

    serialized= {'id':None}
    if topCard:
        serialized = {
            'id': topCard.id,
            'suit': topCard.suit,
            'value': topCard.value,
            'name':topCard.name,
        }

    result = {
        'top_card': serialized,
        'current_player_id': currentPlayer.id,
        'current_player_username': currentPlayer.username,
        'message': message,
        'last_player': data['user_id']
    }
    pusher_client.trigger(Constants.PUSHER_CHANNEL, Constants.CHANGE_TURN_EVENT(currentPlayer.game_id), result)
    return result

#----- end game -----
@app.route("/clearGame", methods=['POST'])
def clearGame():
    data = json.loads(request.data)
    clearGameFromDB(user_id)
