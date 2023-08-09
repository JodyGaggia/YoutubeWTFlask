from flask import request
from flask_restful import Resource
from hashlib import sha256
from datetime import datetime
import secrets

active_sessions = {}

def GetCurrentUnixTimestamp():
    return (datetime.now() - datetime(1970, 1, 1)).total_seconds()

def Get24HourUnixTimestamp():
    unix_timestamp = GetCurrentUnixTimestamp()
    session_expiry = round(unix_timestamp + 86400) # Expires in 24 hours
    return session_expiry

def UpdateActiveSessions(session_token):
    hashed_session_token = sha256(session_token.encode('utf-8')).hexdigest()
    active_sessions.update({hashed_session_token: str(Get24HourUnixTimestamp())})


class ValidateSessionToken(Resource):
    # Grabs expiry time of token from server
    def GetTokenExpiryTime(token):
        if token in active_sessions:
            return active_sessions.get(token)
        else:
            return 0
        
    def post(self):
        # Fail if session token is not included in header
        if 'sessiontoken' not in request.headers:
            return "Invalid session token.", 400
        
        # Grab session token expiry time from server
        session_token = request.headers.get('sessiontoken')
        server_expiry_time = ValidateSessionToken.GetTokenExpiryTime(session_token)
        
        # Fail if session token is not registered on server or if session token has expired
        # TODO: Delete token if time has expired
        if server_expiry_time == 0 or server_expiry_time < GetCurrentUnixTimestamp():
            return "Invalid session token.", 400
        else:
            UpdateActiveSessions(session_token)
            return "Validated", 200
            

class GetSessionToken(Resource):
    def get(self):
        isvalidtoken = False

        while not isvalidtoken:
            # Generate session token
            session_token = str(secrets.token_bytes(16))

            # We don't want duplicate tokens
            if session_token not in active_sessions:
                isvalidtoken = True

        # Hash session token and store in database along with expiry for the session
        UpdateActiveSessions(session_token)

        # Return session token to client
        return {'sessiontoken':session_token}, 200
    