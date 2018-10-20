from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    """客户离开房间时发送的信息。
    该状态消息被广播给房间中的所有人。"""
    room = message['msg']
    join_room(room)
    session['room'] = room
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """用户在输入新消息时由客户端发送。
    该消息将发送给聊天室中的所有人。"""
    print("room", session.get("room"))
    room = message.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """客户离开房间时发送的信息。
    该状态消息被广播给房间中的所有人"""
    room = session.get('room')
    session.pop('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

