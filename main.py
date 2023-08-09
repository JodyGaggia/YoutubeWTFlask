from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS
from SessionTokenAPI import GetSessionToken, ValidateSessionToken
from VideoAPI import ValidateVideoID

hostName = "192.168.0.100"
serverPort = 7700

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
app.config['SECRET_KEY'] = 'secret!'
api = Api(app)

socketio = SocketIO(app,cors_allowed_origins="*", async_mode='eventlet')
import SocketEvents

api.add_resource(GetSessionToken, '/session')
api.add_resource(ValidateSessionToken, '/session/validate')
api.add_resource(ValidateVideoID, '/validate')

if __name__ == "__main__":
    socketio.run(app, debug=True, host=hostName, port=serverPort)
    
    
