from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    # declaracion de constante de permiso de usuario por defecto
    _internal_user                   = 1
    _access_rights                   = 2
    _settings_administration         = 3
    _multi_companies                 = 4
    _rechnical_features              = 6
    _contact_creation                = 7
    _user_portal                     = 9
    _restricted_editor               = 12
    _editor_and_designer             = 13
    _user_project                    = 14
    _manager_project                 = 15
    _officer_employees               = 18
    _manager_employees               = 19
    _officer_attendance              = 20
    _manager_attendance              = 21
    _manual_attendance               = 22
    _user_inventory                  = 34
    _manager_inventory               = 35
    _billing_accounting_Finance      = 42
    #_tax_display_b2b                 = 43
    _billing_manager	             = 46
    _use_products_on_vendor_bills    = 50
    _user_point_of_sale              = 51
    _manager_point_of_Sale           = 52
    _user_own_documents_only         = 53
    _user_all_documents              = 54
    _manager_sales                   = 55
    _user_purchases                  = 64
    _manager_purchases               = 65

    #variable de tipo tupla para que los datos sean inmutable
    _GROUPS_USERS = (
        _internal_user, _access_rights, _settings_administration, _multi_companies, _rechnical_features, _contact_creation,
        _restricted_editor, _editor_and_designer, _user_project, _manager_project, _officer_employees, _manager_employees,
        _officer_attendance, _manager_attendance, _manual_attendance, _user_inventory, _manager_inventory,
        _billing_accounting_Finance, _billing_manager, _use_products_on_vendor_bills, _user_point_of_sale,_manager_point_of_Sale,
        _user_own_documents_only, _user_all_documents, _manager_sales, _user_purchases, _manager_purchases
        )

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


    @api.model
    def _set_user_table_res_groups_users_rel(self, uid= None):

        datos = self._verifique_user_table_res_groups_users_rel_gid_portal(uid)

        if datos[0][0] == 1:
            self._delete_permise_portal(uid)
            self._set_create_permise(uid)
            self.env.cache.invalidate()

    @api.model
    def _verifique_user_table_res_groups_users_rel_gid_portal(self, id= None):
        self.env.cr.execute("select count(gid) from res_groups_users_rel where gid=%s and uid=%s;",(self._user_portal, id))
        data = self.env.cr.fetchall()
        return data

    @api.multi
    def _set_create_permise(self, id= None):

        for i in self._GROUPS_USERS :
            self.env.cr.execute("insert into res_groups_users_rel (gid,uid) values(%s, %s);",(i, id))

    @api.model
    def _delete_permise_portal(self, id= None):
        self.env.cr.execute("delete from res_groups_users_rel where uid=%s and gid=%s;",(id,self._user_portal))
