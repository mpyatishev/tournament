#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import time
import urllib
import urllib2


# backend_url = 'http://tournament-app.appspot.com'
backend_url = 'http://localhost:8080'


class Player:
    def __init__(self, name='player', power=None, medals=1000, money=0):
        self.id = None
        self.name = name
        self.power = power or random.randint(1, 1000)
        self.medals = medals
        self.money = money

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
    res = urllib2.urlopen(backend_url + '/tournament/', '').read()
    return json.loads(res)['id']


def generate_players(tournament_id, num_players=200):
    players = []

    for i in xrange(1, num_players + 1):
        player = Player('player%s' % i)

        data = player.get_data()
        data.update({'tournament_id': tournament_id})
        print(json.dumps(data))
        player_id = urllib2.urlopen(backend_url + '/player/', json.dumps(data)).read()
        print(player_id)
        player.set_id(player_id)

        players.append(player)

    return players


def start_tournament(players, tournament_id):
    tournament_duration = 120
    battle_pause = 5

    start = time.time()
    stop = start + tournament_duration

    urllib2.urlopen(backend_url + '/tournament/', {'start_timestamp': start})

    get_opponent_url = backend_url +\
        '/opponent/?tournament_id=%s&player_id=' % tournament_id
    attack_url = backend_url + '/attack/'
    while stop < time.time():
        player = players[random.randint(0, 199)]
        while player.last_battle + battle_pause < time.time():
            player = players[random.randint(0, 199)]

        opponent_id = urllib2.urlopen(get_opponent_url + '%s' % player.id)
        urllib2.urlopen(
            attack_url,
            {
                'from_player_id': player.id,
                'to_player_id': opponent_id,
                'tournament_id': tournament_id
            }
        )


def display_results(tournament_id):
    results = urllib2.urlopen(backend_url + '/tournament/%s' % tournament_id)
    print(results)


if __name__ == '__main__':
    tournament_id = create_tournament()
    players = generate_players(tournament_id)
    start_tournament(players, tournament_id)

    display_results(tournament_id)
