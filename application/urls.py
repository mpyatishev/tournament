from application import app
from application import views

player_view = views.PlayerView.as_view('player_api')
app.add_url_rule('/player/', defaults={'id': None},
                 view_func=player_view, methods=['GET'])
app.add_url_rule('/player/',
                 view_func=player_view, methods=['POST'])
app.add_url_rule('/player/<int:id>',
                 view_func=player_view, methods=['GET'])

tournament_view = views.TournamentView.as_view('tournament_api')
app.add_url_rule('/tournament/', defaults={'id': None},
                 view_func=tournament_view, methods=['GET'])
app.add_url_rule('/tournament/',
                 view_func=tournament_view, methods=['POST'])
app.add_url_rule('/tournament/<int:id>',
                 view_func=tournament_view, methods=['GET'])

game_view = views.GameView.as_view('game_api')
app.add_url_rule('/opponent/',
                 view_func=game_view, methods=['GET'])
app.add_url_rule('/attack/',
                 view_func=game_view, methods=['POST'])
