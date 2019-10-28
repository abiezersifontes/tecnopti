# -*- coding: utf-8 -*-
{
    'name': "tecnopti",

    'summary': """
        This module are destine for made all modification for tecnopti's odoo instance""",

    'description': """
        This module permit add html edit to blog post
    """,

    'author': "Tecnopti",
    'website': "http://www.tecnopti.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_blog','portal','website'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/website_blog_post.xml',
        'views/website_blog_cover_template.xml',
        'views/tecnopti_website_base_view_company_form.xml',
        'views/tecnopti_website_homepage_s_comparisons_template.xml',
        'views/tecnopti_res_company_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
