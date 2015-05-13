# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, permissions, login_required
from config.template_middleware import TemplateResponse
from permission_app.model import ADMIN
from google.appengine.ext import ndb
from routes.middleware.home import GameForm, GameFormTable, Game, ArcGen
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse
from tekton.gae.middleware.redirect import RedirectResponse

# @permissions(ADMIN)
@login_required
@no_csrf
def index():
    return TemplateResponse()


@login_required
@no_csrf
def list(_resp):
    query = Game.query()
    game_list = query.fetch()
    game_form = GameFormTable()
    game_list = [game_form.fill_with_model(game) for game in game_list]
    context = {'game_list': game_list}
    return JsonUnsecureResponse(context)


# @permissions(ADMIN)
@login_required
@no_csrf
def save(_resp, _logged_user, **properties):
    errors = {}
    game_form = GameForm(**properties)
    errors = game_form.validate()
    if errors:
        context = {'errors': errors,
                   'properties': properties}
        # return RedirectResponse(router.to_path(index(context)))
        # return TemplateResponse(context, "/admin/games-management-form.html")
        return JsonUnsecureResponse(context)
    else:
        game = game_form.fill_model()
        game_key = game.put()
        response = game_form.fill_with_model(game)
        gen_arc = ArcGen(origin=_logged_user.key, destination=game_key)
        gen_arc.put()
        # return RedirectResponse("/admin/games-management")
        return JsonUnsecureResponse(response)


# @permissions(ADMIN)
@login_required
@no_csrf
def delete(_resp, _logged_user, **properties):
    key = ndb.Key(Game, int(properties['id']))
    key.delete()
    query = ArcGen.find_origins(key)
    arc_keys = query.fetch(keys_only=True)
    ndb.delete_multi(arc_keys)


# @permissions(ADMIN)
@login_required
@no_csrf
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