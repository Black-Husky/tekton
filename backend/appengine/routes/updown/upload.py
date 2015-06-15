# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blob_app import blob_facade
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
def index(_handler, files):
    blob_infos = _handler.get_uploads('files[]')
    blob_facade.save_blob_files_cmd(blob_infos).execute()
    return RedirectResponse('/admin/reports-management')