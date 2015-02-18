# -*- coding: utf-8 -*-

import random
import unittest

import mock

from google.appengine.ext import testbed

from application.models import Player, Tournament


class TestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()


class PlayerTest(TestCase):
    def setUp(self):
        super(PlayerTest, self).setUp()
        self._prepare_data()

    def _prepare_data(self):
        tournament = Tournament()
        tournament_key = tournament.put()

        players = []
        for i in xrange(1, 201):
            player = Player(
                parent=tournament_key,
                name='player%s' % i,
                power=random.randint(1, 1000),
                medals=1000,
                money=0
            )
            player.put()
            players.append(player)
        players.sort(key=lambda p: p.power)

        groups = []
        prev_i = 0
        for i in xrange(50, 200, 50):
            group = players[prev_i:i]
            groups.append(group)
            prev_i = i + 1

        self.players = players
        self.groups = groups
        self.tournament_key = tournament_key

    def test_get_group(self):
        player = self.groups[0][5]

        group = player.get_group()

        self.assertEqual(len(group), len(self.groups[0]))
        self.assertEqual(group, self.groups[0])

    def test_find_opponent(self):
        player = self.groups[0][5]

        opponent = player.find_opponent()

        self.assertNotEqual(opponent, player)
        self.assertIn(opponent, self.groups[0])
        self.assertFalse(opponent.in_attack)

    def test_attack(self):
        player = self.groups[0][5]
        opponent = player.find_opponent()

        player.attack(opponent)

        self.assertNotEqual(player.medals, 1000)
        self.assertNotEqual(opponent.medals, 1000)

        self.assertIn(opponent.key, player.attacked)

    @mock.patch('application.models.random.randint')
    def test_attack_increases_player_medals(self, mock):
        mock.return_value = 10

        player = self.groups[0][5]
        opponent = player.find_opponent()

        player.attack(opponent)

        self.assertEqual(player.medals - opponent.medals, 20)

    @mock.patch('application.models.random.randint')
    def test_attack_decreases_player_medals(self, mock):
        mock.return_value = -10

        player = self.groups[0][5]
        opponent = player.find_opponent()

        player.attack(opponent)

        self.assertEqual(player.medals - opponent.medals, -20)
