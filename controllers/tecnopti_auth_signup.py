# -*- coding: utf-8 -*-
import logging
import werkzeug
import re

from odoo import http,_
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo.http import request
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class TecnoptiAuthSignUpHome(AuthSignupHome):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(TecnoptiAuthSignUpHome, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())

        # comprueba que el usuario sea un usuario por portar y tenga una session activa
        # y ejecuta los permisos de usuarios necesarios y crea la compañia
        if request.session.uid and request.session.user_tecnopti:
            request.session['user_tecnopti'] = False
            if request.session.company:
                company = request.session.company
            else:
                company = None
            self._register_default_company_of_user(request.session.login, request.session.uid,company)

        return response

    @http.route()
    def web_auth_signup(self, *args, **kw):
        if super(TecnoptiAuthSignUpHome, self).get_auth_signup_qcontext().get('company'):
            request.session['company'] = super(TecnoptiAuthSignUpHome, self).get_auth_signup_qcontext().get('company')
            request.session['user_tecnopti'] = True
        resp = super(TecnoptiAuthSignUpHome, self).web_auth_signup(*args, **kw)
        return resp


    def get_auth_signup_qcontext(self):
        qcontext = super(TecnoptiAuthSignUpHome,self).get_auth_signup_qcontext()
        if qcontext.get('login'):
            if not bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", qcontext.get("login"))):
                qcontext['error'] = _("invalid email format")

        return qcontext


    def _register_default_company_of_user(self,user_login=None,user_id=None,Company=None):
        """ Se crea la Compañia """
        request.env['res.company']._tecnopti_init_company(user_login, user_id,Company)
        return True
