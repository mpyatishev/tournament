# -*- conding: utf-8 -*-

from flask import jsonify, request
from flask.views import MethodView

from models import (
    Player,
    Tournament
)


class PlayerView(MethodView):
    def get(self, id):
        if id is None:
            return 'error'

        player = Player.get_by_id(id=id)
        return jsonify(player.to_dict())

    def post(self):
        args = request.get_json()
        player = Player(**args)
        player_key = player.put()
        return jsonify({'id': player_key.id()})


class TournamentView(MethodView):
    model = Tournament
