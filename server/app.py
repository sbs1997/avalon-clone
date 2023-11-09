#!/usr/bin/env python3
from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, api, socket_io, random, or_
from models import User, Player, Game, ChatMessage, Round, Quester, Vote
from flask_socketio import join_room, leave_room


# takes the user and game id and returns the info for the game that the user should have
def game_info(game_id, user_id):
    game = Game.query.filter(Game.id == game_id).first()
    player = Player.query.filter(Player.game_id == game_id).filter(Player.user_id == user_id).first()
    response_game = game.to_dict(only=('id', 'title', 'size', 'phase', 'rounds', 'round', 'room_code', 'percival', 'mordred', 'oberon', 'morgana', 'players.user.username', 'players.user.id', 'players.leader', 'players.id', 'players.role', 'winner'))
    if not player:
        response_game["role"] = 'imposter'
    else: 
        if player.role == "Good":
            pass
        if player.role == 'Evil' or player.role == 'Merlin' or player.role == 'Assassin':
            evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(or_(Player.role == "Evil", Player.role == 'Assassin')).all()]
            response_game['baddies'] = evil_players
        response_game["role"] = player.role
        if player.owner:
            response_game["owner"] = True
        if player.leader:
            response_game["leader"] = True
        # print(response_game)
        if game.phase == "over":
            evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(or_(Player.role == "Evil", Player.role == 'Assassin')).all()]
            response_game['baddies'] = evil_players
        else:
            for player in response_game['players']:
                player['role'] = 'unknown' 
    return response_game

# Move the leader to the next player
def move_leader(game):
    last_leader = Player.query.filter(Player.game_id == game.id).filter(Player.leader).first()

    # print(len(game.players))
    # print(game.players.index(last_leader)+1)
    if len(game.players) > game.players.index(last_leader)+1:
        new_leader = game.players[game.players.index(last_leader)+1]
    else:
        new_leader = game.players[0]
    last_leader.leader = False
    new_leader.leader = True

    db.session.add(last_leader, new_leader)
    db.session.commit()


# starts the quest_team selection phase
def quest_team_start(game):
    'start a new round'
    move_leader(game)
    # messages = ChatMessage.query.join(Player).filter(Player.game_id == id).all()
    # db.session.delete(messages)
    # db.session.commit()
    # socket_io.emit('messages-fetched', [])
    for player in game.players:
        for message in player.chat_messages:
            db.session.delete(message)
    db.session.commit()
    quest_size_dict = {
        5 : [2,3,2,3,3],
        6 : [2,3,4,3,4],
        7 : [2,3,3,4,4],
        8 : [3,4,4,5,5],
        9 : [3,4,4,5,5],
        10: [3,4,4,5,5]
    }

    game.phase = 'team_building'
    game.round += 1
    # print(f"quest_size: {quest_size_dict[game.size][game.round-1]}")
    # create round
    new_round= Round(
        game_id = game.id,
        number = game.round,
        quest_size = quest_size_dict[game.size][game.round-1],
        winner = None,
        team_votes_failed = 0
    )

    # print(new_round.quest_size)
    
    db.session.add(new_round)
    db.session.add(game)
    db.session.commit()

    socket_io.emit('qt-submitted', room = f"game{game.id}")

    # (number of people on quest, round number)
    # socket_io.emit('new quest voting', new_round.to_dict())

def check_victory(game):
    print('checking the game')
    good_wins = Round.query.filter(Round.game_id == game.id).filter(Round.winner == "Pass").all()
    print(good_wins)
    print(len(good_wins))
    evil_wins = Round.query.filter(Round.game_id == game.id).filter(Round.winner == "Fail").all()
    print(evil_wins)
    print(len(evil_wins))
    if len(good_wins) == 3:
        game.phase = "merlin_assassination"
        db.session.add(game)
        db.session.commit()
        socket_io.emit('merlin-assassination', room = f"game{game.id}")
    elif len(evil_wins) == 3:
        game.phase = "over"
        game.winner = "Evil"
        db.session.add(game)
        db.session.commit()
        socket_io.emit('game-over', room = f"game{game.id}")
    else:
        print('starting the next quest!')
        quest_team_start(game)
    


###################################################################################
################################### SOCKET STUFF ##################################
###################################################################################

@socket_io.on('connect')
def handle_connect():
    print('new connection')


# client sends a message, add that message to the DB and emit the message to everyone in the same room
@socket_io.on('client-message')
def chat_message(playerID, message, room):
    # print(playerID)
    new_message = ChatMessage(player_id = playerID, message = message)
    db.session.add(new_message)
    # print(new_message.to_dict())
    db.session.commit()
    # print(new_message.to_dict())
    
    socket_io.emit('server-message', new_message.to_dict(), room = room)
    
# listen for requests for game info
@socket_io.on('info-req')
def info_request(game_id, user_id, socket_id):
        print('info request')
        socket_io.emit('update-game', game_info(game_id, user_id), room = socket_id)
    
    
# listen for client request to be set to a room
@socket_io.on('set-room')
def change_room(game_id, user_id, socket_id):
    # print(socket_id)
    room = f'game{game_id}'
    join_room(room)

    socket_io.emit('update-game', game_info(game_id, user_id), room = socket_id)


# listen for client request to be added to a game
@socket_io.on('join-game')
def add_player(player_info):
    # print(player_info)
    try:
        new_player = Player(
            user_id = player_info['userID'],
            game_id = player_info['gameID'],
            role = None,
            owner = False,
            winner = False
        )
        db.session.add(new_player)
        db.session.commit()

        socket_io.emit('update-game', game_info(new_player.game_id, new_player.user_id), room = player_info['socketID'])

        players = [p.to_dict() for p in Player.query.filter(Player.game_id == player_info['gameID']).all()]
        # print(players)

        socket_io.emit('player-change', players, room= player_info['gameID'])

    except ValueError:
        socket_io.emit('join-error', room = player_info['socketID'])

# listen for client request to leave game
@socket_io.on('leave-game')
def remove_player(game_id, user_id, sender_socket):
    player = Player.query.filter(Player.user_id == user_id).filter(Player.game_id == game_id).first()

    db.session.delete(player)
    db.session.commit()

    # send the client the new game info that they should have
    socket_io.emit('update-game', game_info(game_id, user_id), room = sender_socket)

    # send the other players in the game the new player list
    players = [p.to_dict() for p in Player.query.filter(Player.game_id == game_id).all()]
    # print(players)

    socket_io.emit('player-change', players, room=f'game{game_id}')


# delete the game
@socket_io.on('delete-game')
def delete_game(game_id):
    game = Game.query.filter(Game.id == game_id).first()
    db.session.delete(game)
    db.session.commit()

# listen for requests from a client for messages in a room
@socket_io.on('message-request')
def messages_by_game_id(game_id, socket_id):
    messages = [m.to_dict() for m in ChatMessage.query.join(Player).filter(Player.game_id == game_id).all()]
    socket_io.emit('messages-fetched', messages, room = socket_id)


# START THE GAME! EXCITING!
@socket_io.on('start-game')
def start_game(game_id):
    print('starting!')
    game = Game.query.filter(Game.id==game_id).first()
    game.winner = None
    # number of evil players in a game based on total size
    evil_size_dict = {
        5 : 2,
        6 : 2,
        7 : 3,
        8 : 3,
        9 : 3,
        10: 4,
    }

    # 
    # assign roles
    # first get/set the size of the game:
    # print(game.players)
    game.size=len(game.players)
    game.round = 0

    # clear rounds
    game_rounds = Round.query.filter(Round.game_id == game.id).all()
    for round in game_rounds:
        db.session.delete(round)
    db.session.commit()

    # set all the players roles to good and then add them to our list of good players
    good_players = []
    baddies = []
    assassin_selected = False
    for player in game.players:
        player.role = 'Good'
        good_players.append(player)

    # pick the appropriate number of players and make them evil. the first one will be the assassin
    for baddie in random.sample(game.players, evil_size_dict[game.size]):
        # print(f'{baddie.id} is an')
        if not assassin_selected:
            # print('assassin')
            assassin_selected = True
            baddie.role = 'Assassin'
            # print(f'i said {baddie.role}')
        else:
            # print('evil')
            baddie.role = 'Evil'

        good_players.remove(baddie)
        baddies.append(baddie)

    # print(good_players)
    # print(baddies)
    merlin = random.choice(good_players)
    merlin.role = "Merlin"

    for player in good_players:
        player.leader = None
        # print(f'{player} is {player.role}')
        db.session.add(player)
    for player in baddies:
        player.leader = None
        # print(f'{player} is {player.role}')
        db.session.add(player)

    

    db.session.commit()

    prefirst_leader = random.choice(game.players)
    prefirst_leader.leader = True
    db.session.add(prefirst_leader)
    db.session.commit()

    quest_team_start(game)
    
    socket_io.emit('game-started', room = f"game{game.id}")




# listen for changes to the proposed quest team
@socket_io.on('update-qt')
def update_qt(player_id, round_num, game_id):
    round = Round.query.filter(Round.game_id == game_id).filter(Round.number == round_num).first()
    quester = Quester.query.filter(Quester.player_id == player_id).filter(Quester.round_id == round.id).first()
    # print(quester)
    if quester:
        print('deletem')
        db.session.delete(quester)
        db.session.commit()

        questers = [q.to_dict() for q in Quester.query.filter(Quester.round_id == round.id).all()]
        socket_io.emit('updated-qt', questers, room = f"game{game_id}")
    else:
        if len(round.questers) < round.quest_size:
            print(f"{len(round.questers)} < {round.quest_size}")
            new_quester = Quester(
                player_id = player_id,
                round_id = round.id
            )
            db.session.add(new_quester)
            db.session.commit()
            questers = [q.to_dict() for q in Quester.query.filter(Quester.round_id == round.id).all()]
            socket_io.emit('updated-qt', questers, room = f"game{game_id}")
        else:
            print("didn't update :) ")
            socket_io.emit('not-updated-qt', room = f"game{game_id}")


@socket_io.on('submit-qt')
def qt_submitted(game_id):
    game = Game.query.filter(Game.id == game_id).first()
    game.phase = 'qt_voting'
    db.session.add(game)
    db.session.commit()
    
    socket_io.emit('qt-submitted', room = f"game{game_id}")

@socket_io.on('qt-request')
def qt_request(game_id, round_num):
    round = Round.query.filter(Round.game_id == game_id).filter(Round.number == round_num).first()
    questers = [q.to_dict() for q in Quester.query.filter(Quester.round_id == round.id).all()]
    print(round)
    print(questers)
    socket_io.emit('updated-qt', questers, room = f"game{game_id}")


# check the quest team votes helper func
def check_qt_votes(round):
    if len(round.votes) == len(round.game.players):
        threshold = len(round.game.players)/2
        approve_votes = Vote.query.filter(Vote.round_id == round.id).filter(Vote.voted_for).all()
        if len(approve_votes) > threshold:
            round.game.phase = "quest_voting"
            round.last_votes_for = len(approve_votes)
            db.session.add(round.game)
            db.session.commit()
            socket_io.emit('all-qt-votes-in', True, room=f"game{round.game.id}")

        else:
            round.last_votes_for = len(approve_votes)
            round.team_votes_failed += 1
            questers = Quester.query.filter(Quester.round_id == round.id).all()
            print(questers)
            for vote in Vote.query.filter(Vote.round_id == round.id).all():
                db.session.delete(vote)
            for quester in questers:
                db.session.delete(quester)
            move_leader(round.game)
            round.game.phase = "team_building"
            db.session.add(round.game)
            db.session.add(round)
            db.session.commit()
            print('i should be emittin')
            socket_io.emit('all-qt-votes-in', False, room=f"game{round.game.id}")





@socket_io.on('quest-team-vote')
def quest_team_vote(value, user_id, game_id, socket_id):
    game = Game.query.filter(Game.id == game_id).first()
    round = Round.query.filter(Round.game_id == game_id).filter(Round.number == game.round).first()
    player = Player.query.filter(Player.user_id == user_id).filter(Player.game_id == game_id).first()
    vote = Vote.query.filter(Vote.player_id == player.id).filter(Vote.round_id == round.id).first()
    
    if not vote:
        vote = Vote(
            player_id = player.id,
            round_id = round.id,
            vote_type = "team",
            voted_for = value
        )
        db.session.add(vote)
        db.session.commit()
        socket_io.emit('quest-vote-reciept', vote.to_dict(), room = socket_id)
        voted = [u.id for u in User.query.join(Player).join(Vote).filter(Vote.round_id == round.id).all()]
        socket_io.emit('quest-vote-cast', voted, room = f'game{game_id}')
        check_qt_votes(round)
    else:
        voted = [u.id for u in User.query.join(Player).join(Vote).filter(Vote.round_id == round.id).all()]
        socket_io.emit('quest-vote-cast', voted, room = socket_id)
        socket_io.emit('quest-vote-reciept', vote.to_dict(), room = socket_id)


def check_quest(round):
    print('checking quest')
    quest_votes = Vote.query.filter(Vote.round_id == round.id).filter(Vote.vote_type == "quest").all()
    # print(f'{len(quest_votes)} == {round.quest_size} ?')
    if round.quest_size == len(quest_votes):
        print('ending quest')
        votes_against = Vote.query.filter(Vote.round_id == round.id).filter(Vote.vote_type == "quest").filter(Vote.voted_for == False).all()
        # print(votes_against)
        # print(len(votes_against))
        if len(votes_against) > 0:
            print('evil votes')
            round.winner = "Fail"
            socket_io.emit('quest-failed', len(quest_votes), room=f"game{round.game_id}")
        else:
            print('success')
            round.winner = "Pass"
            socket_io.emit('quest-success', room=f"game{round.game_id}")
        db.session.add(round)
        db.session.commit()

        check_victory(round.game)
        


@socket_io.on('quest-vote')
def quest_vote(value, user_id, game_id, socket_id):
    game = Game.query.filter(Game.id == game_id).first()
    round = Round.query.filter(Round.game_id == game_id).filter(Round.number == game.round).first()
    player = Player.query.filter(Player.user_id == user_id).filter(Player.game_id == game_id).first()
    vote = Vote.query.filter(Vote.player_id == player.id).filter(Vote.round_id == round.id).filter(Vote.vote_type == "quest").first()
    
    if not vote:
        print('make vote')
        vote = Vote(
            player_id = player.id,
            round_id = round.id,
            vote_type = "quest",
            voted_for = value
        )
        db.session.add(vote)
        db.session.commit()
    socket_io.emit('quest-reciept', vote.to_dict(), room = socket_id)
    check_quest(round)
    
@socket_io.on('assassinate')
def assassinate(target_id):
    target = Player.query.filter(Player.id == target_id).first()
    game = target.game
    if target.role == "Merlin":
        game.phase = "over"
        game.winner = "Evil"
    else:
        game.phase = "over"
        game.winner = "Good"
    db.session.add(game)
    db.session.commit()
    socket_io.emit('game-over', room = f"game{game.id}")


@socket_io.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")

################################################################
################################################################
######################### ROUTES!!!!! ##########################
################################################################
################################################################
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
                password_hash = data.get("password")
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 200)
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
                title = data.get("title"),
                size = data.get("size"),
                round = 0,
                phase = "pregame",
                # room_code = data.get('roomCode'),
                # percival = data.get('percival'),
                # mordred = data.get('mordred'),
                # oberon = data.get('oberon'),
                # morgana = data.get('morgana')
            )
            db.session.add(new_game)
            db.session.commit()

            return make_response(new_game.to_dict(), 200)
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
            if player.role == "Good":
                pass
            if player.role == 'Evil' or player.role == 'Merlin':
                evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(Player.role == "Evil").all()]
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