#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import random
import time
import urllib2

PLAYERS_NUM = 200
backend_url = 'http://tournament-app.appspot.com'
# backend_url = 'http://localhost:8080'

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class Player:
    def __init__(self, name='player', power=None, medals=1000, money=0):
        self.id = None
        self.name = name
        self.power = power or random.randint(1, 1000)
        self.medals = medals
        self.money = money
        self.last_battle = 0

    def get_data(self):
        return {
            'name': self.name,
            'power': self.power,
            'medals': self.medals,
            'money': self.money,
        }

    def set_id(self, id):
        self.id = id


def create_tournament():
    logger.info('creating tournament')

    resp = urllib2.urlopen(backend_url + '/tournament/', '').read()
    tournament_id = json.loads(resp)['id']

    logger.info('tournament created with id: %s' % tournament_id)

    return tournament_id


def generate_players(tournament_id, num_players=PLAYERS_NUM):
    logger.info('creating players')

    players = []
    player_url = backend_url + '/player/'
    for i in xrange(1, num_players + 1):
        player = Player('player%s' % i)

        data = player.get_data()
        data.update({'tournament_id': tournament_id})
        request = urllib2.Request(player_url, json.dumps(data),
                                  headers={'Content-Type': 'application/json'})
        try:
            resp = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            print(e)
        else:
            player_id = int(json.loads(resp)['id'])
            player.set_id(player_id)
            players.append(player)

    logger.info('created %s players' % num_players)

    return players


def start_tournament(players, tournament_id):
    logger.info('tournament started')

    tournament_duration = 120
    battle_pause = 5
    players_dir = {_.id: _ for _ in players}

    start = time.time()
    stop = start + tournament_duration

    request = urllib2.Request(backend_url + '/tournament/',
                              json.dumps({
                                  'id': tournament_id,
                                  'start_timestamp': start,
                              }),
                              headers={'Content-Type': 'application/json'})
    urllib2.urlopen(request)

    get_opponent_url = backend_url +\
        '/opponent/?tournament_id=%s&player_id=' % tournament_id
    attack_url = backend_url + '/attack/'
    has_attacked = set()
    while time.time() < stop:
        has_attacked_full = len(has_attacked) >= PLAYERS_NUM
        while True:
            player = players[random.randint(0, PLAYERS_NUM - 1)]
            if has_attacked_full and time.time() < player.last_battle + battle_pause:
                break
            elif player not in has_attacked:
                has_attacked.add(player)
                break

        resp = urllib2.urlopen(get_opponent_url + '%s' % player.id).read()
        opponent_id = json.loads(resp)

        data = {
            'from_player_id': player.id,
            'to_player_id': opponent_id,
            'tournament_id': tournament_id
        }
        request = urllib2.Request(attack_url, json.dumps(data),
                                  headers={'Content-Type': 'application/json'})
        player.last_battle = time.time()
        result = urllib2.urlopen(request).read()

        opponent = players_dir[opponent_id]
        logger.info('%s attacked %s' % (player.name, opponent.name))
        logger.debug(result)


def stop_tournament(tournament_id):
    request = urllib2.Request(backend_url + '/tournament/',
                              json.dumps({
                                  'id': tournament_id,
                                  'stop_timestamp': time.time(),
                              }),
                              headers={'Content-Type': 'application/json'})
    urllib2.urlopen(request)


def display_results(tournament_id):
    resp = urllib2.urlopen(backend_url + '/tournament/%s' % tournament_id).read()
    groups = json.loads(resp)

    name = 1
    medals = 2
    money = 3
    for group in sorted(groups.keys()):
        print(group)
        for player in groups[group]:
            print('%s %s %s' % (player[name], player[medals], player[money]))


if __name__ == '__main__':
    tournament_id = create_tournament()
    players = generate_players(tournament_id)

    start_tournament(players, tournament_id)
    stop_tournament(tournament_id)

    display_results(tournament_id)
