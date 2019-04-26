import logging

from jass.player_service.player_service_app import PlayerServiceApp
from jass.player.random_player_schieber import RandomPlayerSchieber
from my_jass.imcts.my_imcts_player_random_trump import MyIMCTSPlayerRandomTrump
from my_jass.imcts.my_imcts_deep_player import MyIMCTSDeepPlayer
from my_jass.ml_player.ml_player import MyMLPlayer
from my_jass.player.my_player_deep_trump import MyPlayerDeepTrump


def main():
    create_app()


def create_app():
    """
    This is the factory method for flask. It is automatically detected when flask is run, but we must tell flask
    what python file to use:

        export FLASK_APP=my_player_service.py
        export FLASK_ENV=development
        flask run --host=0.0.0.0 --port=8888
    """
    logging.basicConfig(level=logging.DEBUG)

    # create and configure the app
    app = PlayerServiceApp('my_player_service')

    # you could use a configuration file to load additional variables
    # app.config.from_pyfile('my_player_service.cfg', silent=False)

    # add some players
    app.add_player('my_player', MyMLPlayer())
    app.add_player('random', MyIMCTSPlayerRandomTrump())

    return app


if __name__ == '__main__':
    main()
