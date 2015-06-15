# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blob_app import blob_facade
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index(_handler,id,filename):
    comando=blob_facade.get_blob_file_cmd(id)
    arquivo=comando()
    _handler.send_blob(arquivo.blob_key)