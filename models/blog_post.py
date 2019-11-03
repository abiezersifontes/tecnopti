# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BlogPost2(models.Model):
    _inherit = 'blog.post'
    img_blog = fields.Binary("Image", attachment=True)
