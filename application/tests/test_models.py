# -*- coding: utf-8 -*-

import random
import unittest

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
        self._prepare_data()

        player = self.groups[0][5]

        group = player.get_group()

        self.assertEqual(len(group), len(self.groups[0]))
        self.assertEqual(group, self.groups[0])
