# -*- coding: utf-8 -*-

import json
import mock
import unittest

from tournament import (
    generate_players,
    create_tournament,
)


class read_wrapper:
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content


class TournamentTest(unittest.TestCase):
    @mock.patch('tournament.urllib2.urlopen')
    def test_generate_players(self, mock):
        mock.side_effect = [read_wrapper(json.dumps({'id': i})) for i in xrange(1, 201)]
        players = generate_players(tournament_id=1, num_players=200)
        self.assertEqual(len(players), 200)

    @mock.patch('tournament.urllib2.urlopen')
    def test_create_tournament(self, mock):
        mock.return_value = read_wrapper(json.dumps({'id': 1}))
        tournament_id = create_tournament()
        self.assertEqual(tournament_id, 1)


if __name__ == '__main__':
    unittest.main()
