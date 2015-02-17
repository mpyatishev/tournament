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


class Tournament(ndb.Model):
    start = ndb.DateTimeProperty()
    stop = ndb.DateTimeProperty()
