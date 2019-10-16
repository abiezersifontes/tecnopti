from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    # declaracion de constante de permiso de usuario por defecto
    _GROUPS_INTERNAL                    = 1
    _GROUPS_ACCESS_RIGHTS               = 2
    _GROUPS_SETTINGS                    = 3
    _GROUPS_MULTI_COMPANIE              = 4
    _GROUPS_MULTI_CURRENCIES            = 5
    _GROUPS_TECHNICAL_FEATURES          = 6
    _GROUPS_CONTACT_CREATION            = 7
    _GROUPS_ACCESS_PRIVATE              = 8
    _GROUPS_PORTAL                      = 9
    _GROUPS_MULTI_WEBSITE               = 11
    _GROUPS_SALES_PRINCELISTS           = 27
    _GROUPS_PRINCELIST_ON_PRODUCT       = 29
    _GROUPS_INVENTORY_MANAGER           = 35
    _GROUPS_BILLING                     = 42
    _GROUPS_BILLING_MANAGER             = 46
    _GROUPS_USE_PRODUCT_ON_VENDOR_BILLS = 50

    #variable de tipo tupla para que los datos sean inmutable
    _GROUPS_USERS = (
        _GROUPS_INTERNAL, _GROUPS_ACCESS_RIGHTS, _GROUPS_SETTINGS, _GROUPS_MULTI_COMPANIE,
        _GROUPS_MULTI_CURRENCIES, _GROUPS_TECHNICAL_FEATURES, _GROUPS_CONTACT_CREATION,
        _GROUPS_ACCESS_PRIVATE ,_GROUPS_MULTI_WEBSITE, _GROUPS_SALES_PRINCELISTS,
        _GROUPS_PRINCELIST_ON_PRODUCT,_GROUPS_INVENTORY_MANAGER,_GROUPS_BILLING,_GROUPS_BILLING_MANAGER ,
        _GROUPS_USE_PRODUCT_ON_VENDOR_BILLS
        )


    @api.model
    def _set_user_table_res_groups_users_rel(self, uid= None):

        datos = self._verifique_user_table_res_groups_users_rel_gid_portal(uid)

        if datos[0][0] == 1:
            self._delete_permise_portal(uid)
            self._set_create_permise(uid)
            self.env.cache.invalidate()

    @api.model
    def _verifique_user_table_res_groups_users_rel_gid_portal(self, id= None):
        self.env.cr.execute("select count(gid) from res_groups_users_rel where gid=%s and uid=%s;",(self._GROUPS_PORTAL, id))
        data = self.env.cr.fetchall()
        return data

    @api.multi
    def _set_create_permise(self, id= None):

        for i in self._GROUPS_USERS :
            self.env.cr.execute("insert into res_groups_users_rel (gid,uid) values(%s, %s);",(i, id))

    @api.model
    def _delete_permise_portal(self, id= None):
        self.env.cr.execute("delete from res_groups_users_rel where uid=%s and gid=%s;",(id,self._GROUPS_PORTAL))
