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