# -*- coding: utf-8 -*-

import random

from google.appengine.ext import ndb


class Player(ndb.Model):
    name = ndb.StringProperty()
    power = ndb.IntegerProperty()
    medals = ndb.IntegerProperty()
    money = ndb.IntegerProperty()
    in_attack = ndb.BooleanProperty(default=False)
    attacked = ndb.KeyProperty(repeated=True)

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
        while opponent.in_attack or opponent == self or opponent.key in self.attacked:
            opponent = opponents[random.randint(0, 49)]

        return opponent

    def attack(self, opponent):
        attack = random.randint(-10, 10)
        self.medals += attack
        opponent.medals -= attack

        self.attacked.append(opponent.key)


class Tournament(ndb.Model):
    start = ndb.DateTimeProperty()
    stop = ndb.DateTimeProperty()

    def _make_money(self, champions, money=300):
        for champ in champions:
            champ.money += money
            money -= 100
        ndb.put_multi(champions)

    def calc_scores(self):
        query = Player.query(ancestor=self.key).order(Player.power)

        group, cursor, more = query.fetch_page(50)

        champions = sorted(group, key=lambda x: x.medals, reverse=True)[0:3]
        self._make_money(champions)
        while more and cursor:
            group, cursor, more = query.fetch_page(50, start_cursor=cursor)
            champions = sorted(group, key=lambda x: x.medals, reverse=True)[0:3]
            self._make_money(champions)
