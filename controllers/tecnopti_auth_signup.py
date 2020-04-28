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
        request.session['user_tecnopti'] = True
        if super(TecnoptiAuthSignUpHome, self).get_auth_signup_qcontext().get('company'):
            request.session['company'] = super(TecnoptiAuthSignUpHome, self).get_auth_signup_qcontext().get('company')
        resp = super(TecnoptiAuthSignUpHome, self).web_auth_signup(*args, **kw)
        return resp


    def get_auth_signup_qcontext(self):
        qcontext = super(TecnoptiAuthSignUpHome,self).get_auth_signup_qcontext()
        if qcontext.get('login'):
            if not bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", qcontext.get("login"))):
                qcontext['error'] = _("invalid email format")

        return qcontext


    def _register_default_company_of_user(self,user_login=None,user_id=None,Company=None):
        """ _Establece Permisos para que pueda ser creada una compañia
        no son necesarios siempre y cuando la plantilla de usuario """
        """
        Añadir Usuario a Grupo de Ajustess
        """
        #TODO: Crear un metodo que quite y añada permisiso solo pasandole el nombre de esos permisos
        group_id = request.env['ir.model.data'].get_object('base', 'group_system')
        group_id.sudo().write({'users': [(4, request.session.uid)]})
        request.env.cr.commit()
        # request.env['res.users']._set_user_table_res_groups_users_rel(user_id)
        """ Se crea la Compañia """
        request.env['res.company']._tecnopti_init_company(user_login, user_id,Company)

        """
        Sacar al usuario de los grupos de Ajustes y Perisos de Acceso
        """
        #TODO: Crear un metodo que quite y añada permisiso solo pasandole el nombre de esos permisos
        group_id.sudo().write({'users': [(3, request.session.uid)]})
        group_id_manager = request.env['ir.model.data'].get_object('base', 'group_erp_manager')
        group_id_manager.sudo().write({'users': [(3, request.session.uid)]})
        request.env.cr.commit()

        return True
