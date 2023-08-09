from __main__ import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request

users = {}

@socketio.on("connect")
def handle_connect():
    print(request.sid + " - Client connected to the server.")
    users[request.sid] = 'Default'
    print(users)

@socketio.on('updatevideo')
def handle_video_update(data):
    print(request.sid + " - Received video ID: " + data['videoId'])
    print(request.sid + " - Room ID: " + data['roomId'])

    if(users[request.sid] == data['roomId']):
        emit("updatevideoresponse", data['videoId'], broadcast=True, to=data['roomId'])
        print("Success!")

@socketio.on('joinroom')
def handle_room_join(data):
    print(request.sid + " - Client connected to room: " + data['roomId'])
    join_room(data['roomId'])
    users[request.sid] = data['roomId']
    print(users)

@socketio.on('leaveroom')
def handle_room_leave(data):
    print(request.sid + " - Client disconnected from room: " + data['roomId'])
    
    if(users[request.sid] == data['roomId']):
        leave_room(data['roomId'])

@socketio.on('disconnect')
def handle_disconnect():
    print(request.sid + " - Client disconnected from the server.")
    del users[request.sid]
    print(users)

@socketio.on('clientpauserequest')
def handle_pause(data):
    print(request.sid + " - Client paused video at time " + str(data['playbackTime']))
    emit('updatecurrentvideotime', data['playbackTime'], broadcast=True, to=data['roomId']) 
    emit('pausevideo', broadcast=True, to=data['roomId'])

@socketio.on('clientplayrequest')
def handle_play(data):
    print(request.sid + " - Client played video at time " + str(data['playbackTime']))
    emit('updatecurrentvideotime', data['playbackTime'], broadcast=True, to=data['roomId'])
    emit('playvideo', broadcast=True, to=data['roomId'])