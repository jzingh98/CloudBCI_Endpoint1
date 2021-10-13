import eventlet
import socketio
import time
from helpers import authenticateUser

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ, auth):
    authenticated = authenticateUser(auth)
    if not authenticated:
        return False
    else:
        print('connect ', sid)
        sio.emit('on_ping_client', {'data': 'foo'}, room=sid)


@sio.event
def ping_server(sid, data):
    print('Server Pinged by: ', sid)
    print(data)


@sio.on('*')
def catch_all(event, sid, data):
    print("unrecognized event")


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
