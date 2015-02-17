# -*- coding: utf-8 -*-

import random

from google.appengine.ext import ndb


class Player(ndb.Model):
    name = ndb.StringProperty()
    power = ndb.IntegerProperty()
    medals = ndb.IntegerProperty()
    money = ndb.IntegerProperty()
    in_attack = ndb.BooleanProperty(default=False)

    def get_group(self):
        query = self.query(ancestor=self.key.parent()).order(Player.power)
        group, cursor, more = query.fetch_page(50)

        if self in group:
            return group

        while more and cursor:
            group, cursor, more = query.fetch_page(50, start_cursor=cursor)
            if self in group:
                return group

        return []

    def find_opponent(self):
        opponents = self.get_group()

        opponent = self
        while opponent.in_attack or opponent == self:
            opponent = opponents[random.randint(0, 49)]

        return opponent


class Tournament(ndb.Model):
    start = ndb.DateTimeProperty()
    stop = ndb.DateTimeProperty()
