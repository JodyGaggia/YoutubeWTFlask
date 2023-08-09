from flask import jsonify, make_response
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
from requests import get


# Server validation of video ID
class ValidateVideoID(Resource):
    @use_kwargs({"videoId": fields.Str()}, location="json")
    def post(self, videoId):
        # Check if video is valid
        pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
        request = get('https://www.youtube.com/watch?v=' + videoId, allow_redirects=False)

        if pattern in request.text:
            return make_response(jsonify({"videoId":"Invalid Video ID"}), 400)

        # This isn't needed but respond with a success when the video ID is valid
        return make_response(jsonify({"videoId":videoId}), 200)

