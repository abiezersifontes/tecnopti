# -*- coding: utf-8 -*-

import logging
import werkzeug

from odoo import http,_
from odoo.addons.auth_signup.controllers.main import  AuthSignupHome
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo.http import request
from odoo.exceptions import UserError

class TecnoptiAuthSignUpHome(AuthSignupHome, CustomerPortal):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(TecnoptiAuthSignUpHome, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))
        if request.session.uid:
            request.env['res.users']._set_user_table_res_groups_users_rel(request.session.uid)
        return response

    @http.route()
    def home(self, **kw):
        super(TecnoptiAuthSignUpHome, self).home(**kw)
        values = self._prepare_portal_layout_values()
        base_url = request.httprequest.url_root + 'web#menu_id=54'
        return request.render("portal.portal_my_home", {'values': values, 'base_url':base_url })
