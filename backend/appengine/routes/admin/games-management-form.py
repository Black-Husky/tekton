# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from gaecookie.decorator import no_csrf
from gaeforms import base
from gaeforms.base import Form
from gaepermission.decorator import login_not_required, permissions, login_required
from config.template_middleware import TemplateResponse
from permission_app.model import ADMIN
from routes.admin.home import GameForm, GameFormTable
from routes.admin.home import Game
from routes.admin.home import ArcGen
from tekton import router
from routes.login import passwordless, facebook
from routes.permission import home as permission_home, admin
from tekton.gae.middleware.redirect import RedirectResponse


#@permissions(ADMIN)
@login_required
@no_csrf
def index(_resp, id=None, context={}):
    if id:
        game = Game.get_by_id(int(id))
        if not game: return RedirectResponse(router.to_path(index))
        game_form = GameFormTable()
        game_form.fill_with_model(game)
        context = {'properties': game_form, 'edit': True, 'id' : id}
        return TemplateResponse(context, template_path="/admin/games-management-form.html")
    return TemplateResponse(context, template_path="admin/games-management-form.html")


#@permissions(ADMIN)
@login_required
def save(_resp, _logged_user, **properties):
    errors = {}
    game_form = GameForm(**properties)
    errors = game_form.validate()
    if errors:
        context = {'errors': errors,
                   'properties': properties}
        # return RedirectResponse(router.to_path(index(context)))
        return TemplateResponse(context, "/admin/games-management-form.html")
    else:
        game = game_form.fill_model()
        game_key = game.put()
        gen_arc = ArcGen(origin=_logged_user.key, destination=game_key)
        gen_arc.put()
        return RedirectResponse("/admin/games-management")


#@permissions(ADMIN)
@login_required
def delete(_resp, _logged_user, id):
    key = ndb.Key(Game, int(id))
    key.delete()
    query = ArcGen.find_origins(key)
    arc_keys = query.fetch(keys_only=True)
    ndb.delete_multi(arc_keys)
    return RedirectResponse("/admin/games-management")


#@permissions(ADMIN)
@login_required
def edit(_resp, _logged_user, id, **properties):
    errors = {}
    game = Game.get_by_id(int(id))
    game_form = GameForm(**properties)
    errors = game_form.validate()
    if errors:
        temp = {'id': id}
        properties.update(temp)
        context = {'errors': errors,
                   'properties': properties,
                   'edit': True,
                   'id': id}
        return TemplateResponse(context, template_path="/admin/games-management-form.html")
    else:
        game_form.fill_model(game)
        game.put()
        return RedirectResponse("/admin/games-management")