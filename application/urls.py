from application import app
from application import views

player_view = views.PlayerView.as_view('player_api')

app.add_url_rule('/player/', defaults={'id': None},
                 view_func=player_view, methods=['GET'])
app.add_url_rule('/player/',
                 view_func=player_view,
                 methods=['POST'])
app.add_url_rule('/player/<int:id>',
                 view_func=player_view, methods=['GET'])
