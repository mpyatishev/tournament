from google.appengine.ext import ndb


class Player(ndb.Model):
    name = ndb.StringProperty()
    power = ndb.IntegerProperty()
    medals = ndb.IntegerProperty()
    money = ndb.IntegerProperty()
    in_attack = ndb.BooleanProperty(default=False)


class Tournament(ndb.Model):
    start = ndb.DateTimeProperty()
    stop = ndb.DateTimeProperty()
