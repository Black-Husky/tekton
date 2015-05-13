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
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse
from permission_app.model import ADMIN
from routes.middleware.home import GameForm, GameFormTable, Game, ArcGen
from tekton import router
from routes.login import passwordless, facebook
from routes.permission import home as permission_home, admin
from tekton.gae.middleware.redirect import RedirectResponse


# @permissions(ADMIN)
@login_required
@no_csrf
def index(_resp, id=None, context={}):
    if id:
        game = Game.get_by_id(int(id))
        if not game: return RedirectResponse(router.to_path(index))
        game_form = GameFormTable()
        game_form.fill_with_model(game)
        context = {'properties': game_form, 'edit': True, 'id': id}
        return TemplateResponse(context, template_path="/admin/games-management-form-dialog.html")
    return TemplateResponse(context, template_path="admin/games-management-form-dialog.html")