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

class TecnoptiWebsite(Website):

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        resp =  super(TecnoptiWebsite,self).web_login(redirect=redirect, *args, **kw)
        user_id = request.env['res.users'].sudo().search([('id','=',request.uid)])
        user_id.set_admin()
        if request.params.get('login_success') and request.params.get('redirect') == '':
            user = request.env['res.users'].search([('id','=',request.uid)])
            website_id = user.website_ids[0]
            request.params.update({'redirect':'/?fw='+str(website_id.id)})
            user_id.set_template()
            return http.redirect_with_hash(request.params.get('redirect'))
        return resp
