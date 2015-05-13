# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from tekton.gae.middleware import Middleware
from gaegraph.model import Arc

class ModifiedMiddleware(Middleware):
    def set_up(self):
        query = Game.query()
        game_list = query.fetch()
        game_form = GameFormTable()
        game_list = [game_form.fill_with_model(game) for game in game_list]
        self.dependencies['_game_list'] = game_list

class Game(Node):
    name = ndb.StringProperty(required=True)
    nickname = ndb.StringProperty(required=True)
    game_page = ndb.StringProperty()
    steam_link = ndb.StringProperty()
    notes = ndb.StringProperty()
    game_community = ndb.StringProperty()
    active = ndb.BooleanProperty()

class GameForm(ModelForm):
    _model_class = Game
    _include = [Game.name, Game.nickname, Game.game_page, Game.steam_link, Game.notes, Game.game_community, Game.active]

class GameFormTable(ModelForm):
    _model_class = Game
    _include = [Game.name, Game.nickname, Game.game_page, Game.steam_link, Game.notes, Game.game_community, Game.active]

class ArcGen(Arc):
    origin = ndb.KeyProperty(required = True)
    destination = ndb.KeyProperty(Game, required = True)