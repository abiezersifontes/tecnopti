# -*- coding: utf-8 -*-
import logging
import werkzeug
from odoo import http,_
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo.http import request
from odoo.exceptions import UserError

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
            self._register_default_company_of_user(request.session.login, request.session.uid)

        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))
        return super(TecnoptiAuthSignUpHome, self).web_login(*args, **kw)

    @http.route()
    def web_auth_signup(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                """creando una variable de session
                 para utilizarla como bandera en
                 los filtros del metodo login """
                request.session['user_tecnopti'] = True
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        #response = request.render('auth_signup.signup', qcontext)
        #esponse.headers['X-Frame-Options'] = 'DENY'
        return super(TecnoptiAuthSignUpHome, self).web_auth_signup(*args, **kw)


    def _register_default_company_of_user(self,user_login=None,user_id=None):

        request.env['res.users']._set_user_table_res_groups_users_rel(user_id)
        request.env['res.company']._tecnopti_init_company(user_login, user_id)
