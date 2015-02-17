# -*- coding: utf-8 -*-

import random
import time
import unittest
import webtest

from datetime import datetime

from google.appengine.ext import testbed

from application import app
from application.models import Player, Tournament


class TestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.testapp = webtest.TestApp(app)

    def tearDown(self):
        self.testbed.deactivate()


class PlayerViewTest(TestCase):
    def setUp(self):
        super(PlayerViewTest, self).setUp()

        self.player = Player(name='player', power=100, medals=1000, money=0)
        self.player_key = self.player.put()

    def test_get_player_without_id(self):
        resp = self.testapp.get('/player/')

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.normal_body, 'error')

    def test_get_player_by_id(self):
        resp = self.testapp.get('/player/%s' % self.player_key.id())

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.json, self.player.to_dict())

    def test_post_to_player_creates_new_entity(self):
        tournament = Tournament()
        tournament_key = tournament.put()

        resp = self.testapp.post_json(
            '/player/',
            {
                'name': 'player2',
                'power': 100,
                'medals': 1000,
                'money': 0,
                'tournament_id': tournament_key.id(),
            }
        )

        self.assertEqual(resp.status_int, 200)

        players = Player.query(Player.name == 'player2').fetch()
        self.assertEqual(len(players), 1)

        player = players[0]
        self.assertEqual(resp.json, {'id': player.key.id()})
        self.assertEqual(player.key.parent(), tournament_key)


class TournamentViewTest(TestCase):
    def test_post_with_empty_body_creates_new_tournament(self):
        resp = self.testapp.post_json(
            '/tournament/',
        )

        self.assertEqual(resp.status_int, 200)

        tournaments = Tournament.query().fetch()
        self.assertEqual(len(tournaments), 1)

        tournament = tournaments[0]
        self.assertEqual(resp.json, {'id': tournament.key.id()})

    def test_post_with_args_starts_tournament(self):
        tournament = Tournament()
        tournament_key = tournament.put()

        start = time.time()
        two_minutes = 120
        resp = self.testapp.post_json(
            '/tournament/',
            {
                'id': tournament_key.id(),
                'start_timestamp': start,
                'duration': two_minutes,
            }
        )

        self.assertEqual(resp.status_int, 200)

        tournament = Tournament.get_by_id(tournament_key.id())
        self.assertEqual(tournament.start, datetime.fromtimestamp(start))

        self.assertEqual(tournament.stop, datetime.fromtimestamp(start + two_minutes))

    def test_get_results(self):
        tournament = Tournament()
        tournament_key = tournament.put()

        for i in xrange(200):
            player = Player(
                parent=tournament_key,
                name='player%s' % i,
                power=random.randint(1, 1000),
                medals=1000,
                money=0,
            )
            player.put()

        resp = self.testapp.get('/tournament/%s' % tournament_key.id())

        self.assertEqual(resp.status_int, 200)

        results = resp.json
        self.assertEqual(len(results.keys()), 4)


class GameViewTest(TestCase):
    def setUp(self):
        super(GameViewTest, self).setUp()
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
        self.player = self.players[random.randint(0, 199)]
        self.tournament_key = tournament_key

    def test_opponent_returns_player_from_same_tournament_group(self):
        self._prepare_data()
        resp = self.testapp.get(
            '/opponent/?player_id=%s&tournament_id=%s' % (self.player.key.id(),
                                                          self.tournament_key.id()),
        )

        self.assertEqual(resp.status_int, 200)
        self.assertTrue(int(resp.normal_body))

        opponent = Player.get_by_id(int(resp.normal_body), parent=self.tournament_key)
        self.assertNotEqual(opponent, self.player)
        self.assertIn(opponent, self.player.get_group())

    def test_attack(self):
        opponent = self.player.find_opponent()

        resp = self.testapp.post_json(
            '/attack/',
            {
                'from_player_id': self.player.key.id(),
                'to_player_id': opponent.key.id(),
                'tournament_id': self.tournament_key.id(),
            }
        )

        self.assertNotEqual(self.player.medals, 1000)
        self.assertNotEqual(opponent.medals, 1000)


if __name__ == '__main__':
    unittest.main()
