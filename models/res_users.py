from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    website_id = fields.Many2one('website')

    def signup(self, values, token=None):
        res = super(ResUsers,self).signup(values,token)
        user_id = self.env['res.users'].sudo().search([('login','=',values.get('login'))])
        user_id.set_admin()
        """ Se crea la Compañia """
        self.env['res.company'].sudo()._tecnopti_init_company(user_id.login, user_id.id,None)
        user_id.set_template()
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
