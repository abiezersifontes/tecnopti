 # -*- coding: utf-8 -*-
import logging
import werkzeug
import re

from odoo import http,_
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.main import Website
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo.http import request
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class TecnoptiAuthSignUpHome(AuthSignupHome):

    def get_auth_signup_qcontext(self):
        qcontext = super(TecnoptiAuthSignUpHome,self).get_auth_signup_qcontext()
        if qcontext.get('login'):
            if not bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", qcontext.get("login"))):
                qcontext['error'] = _("invalid email format")

        return qcontext

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        if qcontext.get('company'):
            values['company_name'] = qcontext.get('company')
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

class TecnoptiWebsite(Website):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        resp = super(TecnoptiWebsite,self).web_login(redirect=redirect, *args, **kw)

        if request.params.get('login_success'):
            user = request.env['res.users'].sudo().search([('id','=',request.uid)])
            website_id = user.website_ids[0]

            request.params.update({'redirect':'/?fw='+str(website_id.id)})

            if not user.id in [1,2]:
                # disable admin for user that signup or only login oly if don't admin
                user.set_template()
            return http.redirect_with_hash(request.params.get('redirect'))
        return resp
