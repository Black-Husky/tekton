# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from blob_app import blob_facade
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required, login_not_required
from tekton import router
from routes.updown import upload
from routes.updown import download


# @permissions(ADMIN)
from tekton.gae.middleware.redirect import RedirectResponse


@login_required
@no_csrf
def index(_handler):
    com= blob_facade.list_blob_files_cmd()
    archives=com()
    download_path= router.to_path(download)
    delete_path = router.to_path(delete)

    for arc in archives:
        arc.delete_path = router.to_path(delete_path, arc.key.id(), arc.filename)
        arc.download_path= router.to_path(download_path, arc.key.id(), arc.filename)

    upload_path = router.to_path(upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(upload_path, gs_bucket_name=bucket)
    ctx = {'save_path': url, 'archives':archives}
    return TemplateResponse(ctx, '/admin/reports-management.html')

@login_not_required
@no_csrf
def delete(_handler, id, file_name):
    cmd = blob_facade.delete_blob_file_cmd(id)
    cmd.execute()
    return RedirectResponse(index)