from time import sleep
from flask import request, redirect, url_for
from flask_socketio import join_room, leave_room
from pymongo import ReturnDocument
from app import socketio
from mongo.connection import room_collection, player_collection

import random


@socketio.on("disconnect")
def disconnect():
    """
    handles when a socket connection disconnects
    """
    room = room_collection.find_one({"host_socketid": request.sid})
    if room:
        # delete if the disconnected user is host
        if not room['live_room']:
            room_collection.delete_one({"host_socketid": room})
            player_collection.delete_many({"host_id": room["host_socketid"]})
            socketio.emit("host-disconnect", to=room['pin'])
            leave_room(room['pin'])
    else:
        # delete if the disconnected user is player
        player = player_collection.find_one(
            {"player_socketid": request.sid}, {"_id": False})
        if player:
            room = room_collection.find_one(
                {"pin": int(player['pin'])})

            if not room['live_room']:
                player_collection.delete_one({"player_socketid": request.sid})
                players_in_game = player_collection.find(
                    {"host_id": player['host_id']}, {"_id": False})

                socketio.emit("update-lobby", {
                    "players_in_game": list(players_in_game)
                }, to=room['pin'])
                leave_room(room['pin'])


@socketio.on("host-join")
def host_join(data):
    # TODO: update new host socketid
    """
    host create room with form data and join lobby of the created room
    """
    room = room_collection.find_one({"id": int(data['id'])}, {"_id": False})
    if room:
        # room = room_collection.find_one_and_update({"id": int(data['id'])}, {
        #                                            "$set": {"host_socketid": request.sid}}, return_document=ReturnDocument.AFTER)

        room_collection.update_one({"id": int(data['id'])}, {"$set": {"live_room": True}})

        pin = room['pin']
        join_room(pin)

        socketio.emit("show-game-pin", {"pin": pin})
    else:
        socketio.emit("no-game-found")


@socketio.on("host-join-game")
def host_join_game(data):
    """
    start the game from host's view
    """
    host_socketid = data['id']

    room = room_collection.find_one({"host_socketid": host_socketid})

    if room:
        # update room and players in room with new host socketid
        room = room_collection.find_one_and_update(
            {"pin": room['pin']}, {"$set": {"host_socketid": request.sid}, "$set": {"live_room": True}, "$set": {"game_data.live_question": True}})

        join_room(room['pin'])

        player_collection.update_many({"pin": int(room['pin'])}, {
                                      "$set": {"host_socketid": request.sid}})

        # send first question to players
        first_question = room['questions'][0]
        first_question['players-in-game'] = player_collection.count_documents(
            {"pin": room['pin']})

        socketio.emit("game-questions", first_question)

        socketio.emit("game-started-player", to=room['pin'])
    else:
        # socketio.emit("no-game-found")
        print("no room found")


@socketio.on("player-join")
def player_join(data):
    """
    player enter lobby with game pin
    """
    room = room_collection.find_one({"pin": int(data['pin'])})
    if room:
        new_player = player_collection.insert_one(
            {
                "player_socketid": request.sid,
                "host_id": room['host_socketid'],
                "pin": room['pin'],
                "name": data['name'],
                "game_data": {
                    "score": 0,
                    "choice": 0
                }
            }
        )
        join_room(room['pin'])
        # update lobby with list of players in room
        players_in_game = player_collection.find(
            {"pin": room['pin']}, {"_id": False})
        socketio.emit("update-lobby",
                      {"players_in_game": list(players_in_game)}, to=room['pin'])

    else:
        socketio.emit("no-game-found")


@socketio.on("player-join-game")
def player_join_game(data):
    """
    player join live game from lobby
    """
    # update player socketid when join game from lobby
    # get old socketid from path, find player that match with socketid and update to current socketid

    player = player_collection.find_one_and_update({"player_socketid": data['player_socketid']}, {
        "$set": {"player_socketid": request.sid}}, return_document=ReturnDocument.AFTER)

    join_room(player['pin'])

    players_in_game = player_collection.find(
        {"pin": player['pin']}, {"_id": False})
    socketio.emit("player-game-data", list(players_in_game))


@socketio.on("player-answer")
def player_answer(data):
    player = player_collection.find_one({"player_socketid": data['id']})
    room = room_collection.find_one({"pin": player['pin']})

    choice = str(data['choice'])

    if room:
        if room['game_data']['live_question']:
            player_collection.update_one({"player_socketid": request.sid}, {
                                         "$set": {"game_data.choice": choice}})
            room_collection.update_one({"pin": room['pin']}, {
                                       "$inc": {"game_data.answered_players": 1}})

            current_question = room['game_data']['current_question']
            # game_id = room['game_data']['game_id']

            print("checking current question ", current_question)

            correct_answer = room['questions'][current_question]['correct']

            if correct_answer == choice:
                print("player answered correctly")
                # increase score by 100 for correct answer plus time bonus
                player_collection.update_one({"player_socketid": request.sid}, {
                                             "$inc": {"game_data.score": 100}})
                socketio.emit("get-time", request.sid, to=room['pin'])
                socketio.emit("answer-result", True)

            # if all players answered, set current question to inactive move to next question
            players_in_room = player_collection.find(
                {"pin": room['pin']}, {"_id": False})
            num_players_in_room = len(list(players_in_room))
            
            if num_players_in_room == room['game_data']['answered_players']:

                # room['game_data']['live_question'] = False
                room_collection.update_one({"pin": room['pin']}, {
                                           "$set": {"game_data.live_question": False}})
                socketio.emit("question-over", {
                    "players": list(players_in_room),
                    "correct_answer": correct_answer
                }, to=room['pin'])
            else:
                socketio.emit("update-answered-players", {
                    "players_in_game": num_players_in_room,
                    "answered_players": room['game_data']['answered_players']
                }, to=room['pin'])
    else:
        print("player asnwer room not found")


@socketio.on("get-score")
def get_score():
    player = player_collection.find_one({"player_socketid": request.sid})
    socketio.emit("update-display-score", player['game_data']['score'])


@socketio.on("time-score")
def time_score(data):
    # score = remaining_time as a percentage of total time (remaining_time)
    score = (data['time'] / 10) * 100
    # update score
    player_collection.update_one({"player_socketid": request.sid}, {
        "$inc": {"score": score}})


@socketio.on("question-time-up")
def question_time_up(data):
    """
    when time up or all players have answered, broadcast correct answer to all players in room
    """
    room = room_collection.find_one_and_update({"host_socketid": data['id']},
                                               {"$set": {"game_data.live_question": False}}, return_document=ReturnDocument.AFTER)

    players_in_room = player_collection.find(
        {"pin": room['pin']}, {"_id": False})

    if room:
        current_question = room['game_data']['current_question']

        print("[debug] current question: ", current_question)

        correct_answer = room['questions'][current_question]['correct']

        print("[debug] correct answer: ", correct_answer)

        socketio.emit("question-over", {
            "players": list(players_in_room),
            "correct_answer": correct_answer
        }, to=room['pin'])


@socketio.on("next-question")
def next_question(data):
    """
    move to next question in quiz if available, reset all players in room answer to 0 and broadcast new question
    """
    room = room_collection.find_one({"host_socketid": data['id']})
    player = player_collection.find_one({"pin": room['pin']})

    num_players_in_room = player_collection.update_many({"pin": player['pin']}, {
        "$set": {"game_data.choice": 0}})

    room = room_collection.find_one({"pin": player['pin']})
    if room:
        current_question_num = room["game_data"]['current_question'] + 1

        if (current_question_num < len(room['questions'])):
            question = room['questions'][current_question_num]
            question['players_in_game'] = num_players_in_room.matched_count

            room_collection.update_one({"pin": int(room['pin'])}, {"$inc": {"game_data.current_question": 1}, "$set": {"game_data.live_question": True}})

            print("next question: ", question)

            socketio.emit("game-questions", question)
        else:
            # no more question available, game is over, rank players
            print("no more question")

            top_three = list(player_collection.find({"pin": room['pin']}).sort(
                "game_data.score", -1).limit(3))
            
            while len(top_three) < 3:
                top_three.append({"name": ""})
            
            socketio.emit("game-over", {
                "first": top_three[0]['name'],
                "second": top_three[1]['name'],
                "third": top_three[2]['name'],
            }, to=room['pin'])

    socketio.emit("next-question-player", to=room['pin'])


@socketio.on("start-game")
def start_game(data):
    """
    start game from host view
    """
    room = room_collection.find_one_and_update(
        {"pin": int(data['pin'])}, {"$set": {"live_room": True}, "$set": {"host_socketid": request.sid}}, return_document=ReturnDocument.AFTER)

    socketio.emit("game-started", room['host_socketid'])


@socketio.on("new-game")
def new_game(data):
    """
    host choose to create a room, add quiz questions to database
    """
    # new room's id = len(existing_room) + 1
    if room_collection.count_documents({}) == 0:
        id = 0
    else:
        latest_room = room_collection.find({}).sort("id", -1).limit(1)
        id = latest_room[0]['id'] + 1

    host_socketid = data['socketid']
    data.pop("socketid")

    # extract questions from form data
    questions = []
    question = {'answers': []}

    for index in enumerate(data, 1):
        if index[0] % 6 == 1:
            question['question'] = data[index[1]]
        elif index[0] % 6 == 0:
            question['correct'] = data[index[1]]
            questions.append(question)
            question = {'answers': []}
        else:
            question['answers'].append(data[index[1]])

    new_room = {
        "host_socketid": host_socketid,
        "id": id,
        "pin": random.randrange(100000, 1000000),
        "questions": questions,
        "live_room": False,
        "game_data": {
            "current_question": 0,
            "live_question": False,
            "answered_players": 0
        }
    }
    room = room_collection.insert_one(new_room)
    socketio.emit("start-game-from-host", {"id": id})
