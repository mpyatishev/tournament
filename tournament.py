#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import urllib2


backend_url = 'http://tournament-app.appspot.com'


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
    return urllib2.urlopen(backend_url + '/tournament/', {})


def generate_players(tournament_id, num_players=200):
    players = []

    for i in xrange(1, num_players + 1):
        player = Player('player%s' % i)

        data = player.get_data()
        data.update({'tournament_id': tournament_id})
        player_id = urllib2.urlopen(backend_url + '/player/', data)
        player.set_id(player_id)

        players.append(player)

    return players


def start_tournament(players):
    pass


if __name__ == '__main__':
    tournament_id = create_tournament()
    players = generate_players(tournament_id)
    start_tournament(players)
