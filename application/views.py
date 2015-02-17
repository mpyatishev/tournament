# -*- conding: utf-8 -*-

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
        try:
            args = request.get_json()
        except BadRequest as e:
            print(e, request.data)
            return 'error'
        if args and 'name' in args and 'power' in args and 'medals' in args\
                and 'money' in args and 'tournament_id' in args:
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

        tournament = Tournament.get_by_id(int(id))
        query = Player.query(ancestor=tournament.key).order(Player.power, Player.medals)

        group, cursor, more = query.fetch_page(50)

        groups = []
        groups.append(group)

        while more and cursor:
            group, cursor, more = query.fetch_page(50, start_cursor=cursor)
            groups.append(group)

        result = {
            'group%s' % groups.index(group): [(_.key.id(), _.name, _.medals)
                                              for _ in group]
            for group in groups
        }

        return jsonify(result)

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
        opponent = player.find_opponent()

        return '%s' % opponent.key.id()

    def post(self):
        args = request.get_json()

        if 'from_player_id' not in args or 'to_player_id' not in args\
                or 'tournament_id' not in args:
            return 'error'

        player_id = int(args['from_player_id'])
        opponent_id = int(args['to_player_id'])
        tournament_id = int(args['tournament_id'])

        tournament = Tournament.get_by_id(tournament_id)
        player = Player.get_by_id(player_id, parent=tournament.key)
        opponent = Player.get_by_id(opponent_id, parent=tournament.key)

        player.in_attack = True
        player.put()
        opponent.in_attack = True
        opponent.put()

        player.attack(opponent)

        player.in_attack = False
        player.put()
        opponent.in_attack = False
        opponent.put()

        return jsonify({
            'from_player': player.medals,
            'to_player': opponent.medals
        })
