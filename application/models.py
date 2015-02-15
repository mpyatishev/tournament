from google.appengine.ext import ndb


class Player(ndb.Model):
    name = ndb.StringProperty()
    power = ndb.IntegerProperty()
    medals = ndb.IntegerProperty()
    money = ndb.IntegerProperty()


class Tournament(ndb.Model):
    pass
