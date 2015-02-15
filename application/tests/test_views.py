# -*- coding: utf-8 -*-

import webtest
import unittest

from google.appengine.ext import testbed

from application import app
from application.models import Player


class PlayerViewTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.testapp = webtest.TestApp(app)

        self.player = Player(name='player', power=100, medals=1000, money=0)
        self.player_key = self.player.put()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_player_without_id(self):
        resp = self.testapp.get('/player/')

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.normal_body, 'error')

    def test_get_player_by_id(self):
        resp = self.testapp.get('/player/%s' % self.player_key.id())

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.json, self.player.to_dict())

    def test_post_to_player_creates_new_entity(self):
        resp = self.testapp.post_json(
            '/player/',
            {
                'name': 'player2',
                'power': 100,
                'medals': 1000,
                'money': 0,
            }
        )

        self.assertEqual(resp.status_int, 200)

        players = Player.query(Player.name == 'player2').fetch()
        self.assertEqual(len(players), 1)

        player = players[0]
        self.assertEqual(resp.json, {'id': player.key.id()})


if __name__ == '__main__':
    unittest.main()
