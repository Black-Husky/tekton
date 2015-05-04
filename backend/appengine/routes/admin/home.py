# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaepermission.decorator import login_not_required, permissions, login_required
from config.template_middleware import TemplateResponse
from gaegraph.model import Arc
from permission_app.model import ADMIN
from tekton import router
from routes.login import passwordless, facebook
from routes.permission import home as permission_home, admin
from google.appengine.ext import ndb
from gaegraph.model import Node

#@permissions(ADMIN)
@login_required
@no_csrf
def index():
    return TemplateResponse({'security_table_path': router.to_path(permission_home.index),
                             'permission_admin_path': router.to_path(admin),
                             'passwordless_admin_path': router.to_path(passwordless.form),
                             'facebook_admin_path': router.to_path(facebook.form)})

class Game(Node):
    name = ndb.StringProperty(required=True)
    nick_name = ndb.StringProperty(required=True)
    game_page = ndb.StringProperty()
    steam_link = ndb.StringProperty()
    notes = ndb.StringProperty()
    game_community = ndb.StringProperty()
    active = ndb.StringProperty()

class GameForm(ModelForm):
    _model_class = Game
    _include = [Game.name, Game.nick_name, Game.game_page, Game.steam_link, Game.steam_link, Game.notes, Game.game_community, Game.active]

class GameFormTable(ModelForm):
    _model_class = Game
    _include = [Game.name, Game.nick_name, Game.game_page, Game.steam_link, Game.steam_link, Game.notes, Game.game_community, Game.active]

class ArcGen(Arc):
    origin = ndb.KeyProperty(required = True)
    destination = ndb.KeyProperty(Game, required = True)