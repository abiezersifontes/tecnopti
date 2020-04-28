import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):

    _inherit = 'res.company'

    @api.model
    def _tecnopti_init_company(self,nameUser=None, idUser=None,Company=None):

        if Company != None and Company != '':
            companyName = Company
        else:
            companyName = self._create_nombre_company(nameUser)

        company = self._create_company_default(companyName)
        self._update_users_set_company_id(idUser, company.id)
        self._consultar_res_company_users_rel_ids(idUser)

    def _create_nombre_company(self, nameUser = None):
        companyName = 'Company '
        if nameUser:
            companyName += nameUser.capitalize()
        return companyName

    @api.model
    def _create_company_default(self, companyName = None):
        # llamando  al metodo create del model company del modulo base
        # el cual crea una compania
        company = self.create({'name': companyName})
        return company

    @api.model
    def _update_users_set_company_id(self, idUser=None, idCompany=None):
        usuario = self.env['res.users'].search([('id', '=', idUser)])
        idPartner = usuario.partner_id.id
        usuario.write({'company_id':idCompany})

        self._update_res_partner_company_id(idPartner,idCompany)


    @api.model
    def _update_res_partner_company_id(self,idPartner=None, idCompany=None):
        partner = self.env['res.partner'].search([('id','=',idPartner)])
        partner.write({'company_id':idCompany})



    @api.model
    def _consultar_res_company_users_rel_ids(self, idUser=None):
        sql = "select cid from res_company_users_rel where cid=%s and user_id=%s;"

        """extrae el id del a compania por defecto
        llamando al metodo _company_default_get
        del modulo base"""
        idCompany = self._company_default_get().id
        self.env.cr.execute(sql,(idCompany, idUser))
        data = self.env.cr.fetchone()
        if len(data) == 1:
            self._delete_res_company_user_rel(idCompany, idUser)


    @api.model
    def _delete_res_company_user_rel(self,idCompany=None,idUser=None):
        self.env.cr.execute("delete from res_company_users_rel where not cid=%s and user_id=%s;",(idCompany,idUser))
