# -*- coding: utf-8 -*-
from odoo import http

# class Tecnopti(http.Controller):
#    @http.route('/tecnopti/', auth='user')
#    def index(self, **kw):
#        return "Hello, world"

#     @http.route('/tecnopti/tecnopti/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tecnopti.listing', {
#             'root': '/tecnopti/tecnopti',
#             'objects': http.request.env['tecnopti.tecnopti'].search([]),
#         })

#     @http.route('/tecnopti/tecnopti/objects/<model("tecnopti.tecnopti"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tecnopti.object', {
#             'object': obj
#         })
