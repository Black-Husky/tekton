# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, permissions, login_required
from config.template_middleware import TemplateResponse
from permission_app.model import ADMIN
import routes.admin.home as home


#@permissions(ADMIN)
@login_required
@no_csrf
def index():
    query = home.Game.query()
    game_list = query.fetch()
    game_form = home.GameFormTable()
    game_list = [game_form.fill_with_model(game) for game in game_list]
    context = {'game_list' : game_list}
    return TemplateResponse(context, template_path="/admin/games-management.html")