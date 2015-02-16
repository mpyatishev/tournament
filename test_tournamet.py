# -*- coding: utf-8 -*-

import mock
import unittest

from tournament import (
    generate_players,
    create_tournament,
    start_tournament,
)


class TournamentTest(unittest.TestCase):
    @mock.patch('tournament.urllib2.urlopen')
    def test_generate_players(self, mock):
        mock.side_effect = [i for i in xrange(1, 201)]
        players = generate_players(tournament_id=1, num_players=200)
        self.assertEqual(len(players), 200)

    @mock.patch('tournament.urllib2.urlopen')
    def test_create_tournament(self, mock):
        mock.return_value = 1
        tournament_id = create_tournament()
        self.assertEqual(tournament_id, 1)

    @mock.patch('tournament.urllib2.urlopen')
    def test_start_tournament(self, mock):
        players = generate_players(tournament_id=1)
        start_tournament(players)


if __name__ == '__main__':
    unittest.main()
