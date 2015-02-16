# -*- conding: utf-8 -*-

import random

from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from google.appengine.ext import ndb

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
        if 'name' in args and 'power' in args and 'medals' in args and 'money' in args\
                and 'tournament_id' in args:
            player = Player(
                parent=ndb.Key(Tournament, args['tournament_id']),
                name=args['name'], power=args['power'],
                medals=args['medals'], money=args['money']
            )
            player_key = player.put()
            return jsonify({'id': player_key.id()})
        return 'error'


class TournamentView(MethodView):
    def get(self, id):
        if id is None:
            return 'error'

        return 'not implemented'

    def post(self):
        try:
            args = request.get_json()
        except BadRequest:
            args = None

        if args is None:
            tournament = Tournament()
            tournament_key = tournament.put()
            return jsonify({'id': tournament_key.id()})
        elif 'id' in args and 'start_timestamp' in args and 'duration' in args:
            tournament = Tournament.get_by_id(args['id'])
            if tournament:
                tournament.start = datetime.fromtimestamp(args['start_timestamp'])
                tournament.stop = datetime.fromtimestamp(
                    args['start_timestamp'] + args['duration'])
                tournament.put()

                return 'tournament %s started' % tournament.key.id()

        return 'error'


class GameView(MethodView):
    def get(self):
        player_id = request.args.get('player_id', None)
        tournament_id = request.args.get('tournament_id', None)
        if player_id is None or tournament_id is None:
            return 'error'

        player_id = int(player_id)
        tournament_id = int(tournament_id)

        tournament = Tournament.get_by_id(tournament_id)

        player = Player.get_by_id(player_id, parent=tournament.key)
        opponents = Player.query(ancestor=tournament.key).order(Player.power).fetch()

        groups = []
        player_group = None
        prev_i = 0
        for i in xrange(49, 200, 50):
            group = opponents[prev_i:i]
            # print(prev_i, i, group)
            groups.append(group)
            prev_i = i + 1

            if player in group:
                player_group = group

        # print(player)
        # print(player_group)

        opponent = player
        while opponent.in_attack or player == opponent:
            print('here')
            opponent = player_group[random.randint(0, 49)]

        return '%s' % opponent.key.id()
