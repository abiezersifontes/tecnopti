from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.http import request
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    website_ids = fields.Many2many('website')

    def signup(self, values, token=None):
        res = super(ResUsers,self).signup(values,token)
        user = self.env['res.users'].sudo().search([('login','=',values.get('login'))])
        _logger.warning("##################################################################")
        _logger.warning("##################################################################")
        _logger.warning("##################################################################")
        _logger.error(values)
        _logger.warning("##################################################################")
        _logger.warning("##################################################################")
        _logger.warning("##################################################################")
        # enable admin for user that signup
        user.set_admin()
        """ Se crea la Compañia """
        company = self.env['res.company'].sudo()._tecnopti_init_company(user.login, user.id,None)
        w_id = self.env['website'].sudo().create({'name':company.name,'company_id':company.id})
        user.write({'website_ids':[(6, 0, [w_id.id])]})
        return res

    @api.model
    def set_template(self):
        self.write({'groups_id':[(6, 0, [
          self.env.ref('base.group_user').id,
          self.env.ref('tecnopti.settings_plan_a').id,
          self.env.ref('tecnopti.pos_plan_a').id,
          self.env.ref('tecnopti.purchase_plan_a').id,
          self.env.ref('tecnopti.account_plan_a').id,
          self.env.ref('tecnopti.stock_plan_a').id,
          self.env.ref('tecnopti.project_plan_a').id,
          self.env.ref('tecnopti.sale_plan_a').id,
          self.env.ref('tecnopti.website_plan_a').id,
          self.env.ref('tecnopti.event_plan_a').id,
          self.env.ref('account.group_account_user').id
          ])]})

    def set_admin(self):
        self.write({'groups_id':[(6, 0, [
            self.env.ref('account.group_account_manager').id,
            self.env.ref('product.group_product_variant').id,
            self.env.ref('product.group_stock_packaging').id,
            self.env.ref('base.group_system').id,
            self.env.ref('base.group_no_one').id,
            self.env.ref('analytic.group_analytic_accounting').id,
            self.env.ref('base.group_partner_manager').id,
            self.env.ref('sale.group_delivery_invoice_address').id,
            self.env.ref('purchase.group_purchase_manager').id,
            self.env.ref('stock.group_stock_manager').id,
            self.env.ref('point_of_sale.group_pos_manager').id,
            self.env.ref('project.group_project_manager').id,
            self.env.ref('website.group_website_publisher').id,
            self.env.ref('website.group_website_designer').id,
            self.env.ref('account.group_account_invoice').id,
            self.env.ref('agreement_legal.group_agreement_manager').id,
            self.env.ref('stock.group_stock_multi_warehouses').id,
            self.env.ref('stock.group_stock_multi_locations').id,
            self.env.ref('uom.group_uom').id,
            self.env.ref('stock.group_tracking_lot').id,
            self.env.ref('account.group_show_line_subtotals_tax_excluded').id,
            self.env.ref('stock.group_lot_on_delivery_slip').id,
            self.env.ref('account.group_account_user').id,
            self.env.ref('crm.group_use_lead').id,
            self.env.ref('website.group_multi_website').id,
            self.env.ref('base.group_multi_company').id,
            self.env.ref('base.group_erp_manager').id,
            self.env.ref('sales_team.group_sale_manager').id,
            self.env.ref('fleet.fleet_group_manager').id,
            self.env.ref('event.group_event_manager').id,
            self.env.ref('agreement.group_use_agreement_template').id,
            self.env.ref('agreement.group_use_agreement_type').id
        ])]})

    @classmethod
    def _login(cls, db, login, password):
        if not password:
            raise AccessDenied()
        ip = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                with self._assert_can_auth():
                    user = self.search(self._get_login_domain(login))
                    if not user:
                        raise AccessDenied()
                    user = user.sudo(user.id)
                    user._check_credentials(password)
                    user._update_last_login()
                    # enable admin for user that login
                    user.set_admin()
        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s from %s", db, login, ip)
            raise

        _logger.info("Login successful for db:%s login:%s from %s", db, login, ip)

        return user.id
