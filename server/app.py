#!/usr/bin/env python3
from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, api, socket_io
from models import User, Player, Game, ChatMessage
from flask_socketio import join_room, leave_room



def game_info(game_id, user_id):
    game = Game.query.filter(Game.id == game_id).first()
    player = Player.query.filter(Player.game_id == game_id).filter(Player.user_id == user_id).first()
    response_game = game.to_dict(only=('id', 'title', 'size', 'round', 'phase', 'room_code', 'percival', 'mordred', 'oberon', 'morgana', 'players.user.username', 'players.user.id', 'players.leader', 'players.id'))
    if not player:
        response_game["role"] = 'imposter'
    else:
        if player.role == "good":
            pass
        if player.role == 'evil' or player.role == 'merlin':
            evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(Player.role == "evil").all()]
            response_game['evils'] = evil_players
        response_game["role"] = player.role
        if player.owner:
            response_game["owner"] = True
    socket_io.emit('update-game', response_game)

####################### SOCKET STUFF #########################

@socket_io.on('connect')
def handle_connect():
    print('new connection')
    # print(request.sid)
    # session["user"] = request.sid

@socket_io.on('client-message')
def chat_message(playerID, message, room):
    new_message = ChatMessage(player_id = playerID, message = message)
    db.session.add(new_message)
    db.session.commit()
    
    socket_io.emit('server-message', new_message.to_dict(), room = room)
    
@socket_io.on('set-room')
def change_room(game_id, user_id):
    room = f'game{game_id}'
    join_room(room)
    game_info(game_id, user_id)

@socket_io.on('message-request')
def messages_by_game_id(game_id):
    messages = [m.to_dict() for m in ChatMessage.query.join(Player).filter(Player.game_id == id).all()]
    socket_io.emit('messages-fetched', messages)



@socket_io.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")



######################### ROUTES!!!!! ##########################
@app.route('/')
def index():
    return '<h1>Avalon Server!</h1>'

######################## USER ROUTES ###########################


class UserById(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        return make_response(user.to_dict(), 200)
    
    def patch(self, id):
        user = User.query.filter(User.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(user, field, data[field])
            db.session.add(user)
            db.session.commit()
            
            return make_response(user.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(UserById, '/users/<int:id>')
    
class Users(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_user = User(
                username = data.get("username"),
                _password_hash = data.get("password")
            )
            db.session.add(new_user)
            db.session.commit()
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Users, '/users')

class PlayersByUser(Resource):
    def get(self, user_id):
        players = [p.to_dict() for p in Player.query.filter(Player.user_id == user_id).all()]
        make_response(players, 200)

api.add_resource(PlayersByUser, '/users/<int:id>/players')


####################### Games routes ######################
class GameById(Resource):
    def get(self, id):
        game = Game.query.filter(Game.id == id).first()
        if not game:
            return make_response(({"error": "game not found"}),404)
        return make_response(game.to_dict(), 200)
    
    def patch(self, id):
        game = Game.query.filter(Game.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(game, field, data[field])
            db.session.add(game)
            db.session.commit()
            
            return make_response(game.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        game = Game.query.filter(Game.id == id).first()
        db.session.delete(game)
        db.session.commit()

        return make_response({}, 204)

api.add_resource(GameById, '/games/<int:id>')


class Games(Resource):
    def get (self):
        games = [g.to_dict() for g in Game.query.all()]
        return make_response(games, 200)
    
    def post(self):
        data = request.get_json()

        try:
            new_game = Game(
                size = data.get("size"),
                round = 0,
                phase = "pregame",
                room_code = data.get('roomCode'),
                percival = data.get('percival'),
                mordred = data.get('mordred'),
                oberon = data.get('oberon'),
                morgana = data.get('morgana')
            )
            db.session.add(new_game)
            db.session.commit()
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Games, '/games')

# class PlayersByGame(Resource):
#     def get(self, game_id):
#         players = [p.to_dict() for p in Player.query.filter(Player.game_id == game_id).all()]
#         make_response(players, 200)

# api.add_resource(PlayersByGame, '/games/<int:id>/players')

class GameForPlayer(Resource):
    def get(self, game_id, user_id):
        game = Game.query.filter(Game.id == game_id).first()
        player = Player.query.filter(Player.game_id == game_id).filter(Player.user_id == user_id).first()
        response_game = game.to_dict(only=('id', 'title', 'size', 'round', 'phase', 'room_code', 'percival', 'mordred', 'oberon', 'morgana', 'players.user.username', 'players.user.id', 'players.leader', 'players.id'))
        if not player:
            response_game["role"] = 'imposter'
        else:
            if player.role == "good":
                pass
            if player.role == 'evil' or player.role == 'merlin':
                evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(Player.role == "evil").all()]
                response_game['evils'] = evil_players
            response_game["role"] = player.role
            if player.owner:
                response_game["owner"] = True
        return make_response(response_game, 200)
    
api.add_resource(GameForPlayer, '/games/<int:game_id>/<int:user_id>')


######################################## player routes ############################################

class PlayerById(Resource):
    def get(self, id):
        player = Player.query.filter(Player.id == id).first()
        return make_response(player.to_dict(), 200)
    
    def patch(self, id):
        player = Player.query.filter(Player.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(player, field, data[field])
            db.session.add(player)
            db.session.commit()
            
            return make_response(player.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        player = Player.query.filter(Player.id == id).first()
        db.session.delete(player)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(PlayerById, '/players/<int:id>')


class Players(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_player = Player(
                user_id = data.get('userID'),
                game_id = data.get('gameID'),
                role = data.get('role'),
                owner = data.get('owner'),
                winner = False
            )
            db.session.add(new_player)
            db.session.commit()

            return make_response(new_player.to_dict(), 201)

        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Players, '/players')



################################ Chat Messages ###########################

class MessageById(Resource):
    def get(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        return make_response(message.to_dict(), 200)
    
    def patch(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(message, field, data[field])
            db.session.add(message)
            db.session.commit()
            
            return make_response(message.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        db.session.delete(message)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(MessageById, '/messages/<int:id>')


class Messages(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_message = ChatMessage(
                player_id = data.get('playerID'),
                message = data.get('message')
            )
            db.session.add(new_message)
            db.session.commit()
            return make_response(new_message.to_dict(), 201)
        
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Messages, '/messages')


class MessagesByRoom(Resource):
    def get(self, id):
        messages = [m.to_dict() for m in ChatMessage.query.join(Player).filter(Player.game_id == id).all()]
        return make_response(messages, 200)

api.add_resource(MessagesByRoom, '/messages/game/<int:id>')


########################################### log in stuff #######################################
class Login(Resource):
    def post(self):
        data = request.get_json()
        username= data['username']
        password= data['password']
        user = User.query.filter(User.username == username).first()
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
            else:
                return {"Error": "password is wrong"}, 401
        return {"Error": "User doesn't exist"}, 401

api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(only=('username', 'id'))
        else:
            return {'message': 'Not Authorized'}, 401
        
api.add_resource(CheckSession, '/check_session')


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204
    
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    # app.run(port=5555, debug=True)
    socket_io.run(app, port=5555)