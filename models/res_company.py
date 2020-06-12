import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)
from odoo.addons.base.models.res_company import Company
from odoo.addons.account_multicompany_easy_creation.wizards.multicompany_easy_creation import AccountMulticompanyEasyCreationWiz

class ResCompany(models.Model):

    _inherit = 'res.company'

    @api.model
    def _tecnopti_init_company(self,nameUser=None, idUser=None,companyName=None):
        company = self._create_company_default(companyName,nameUser)
        self._update_users_set_company_id(idUser, company.id)
        # self._consultar_res_company_users_rel_ids(idUser)
        # self.sudo().env['website'].sudo().create({'name':company.name,'company_id':company.id})

    @api.model
    def _create_company_default(self, companyName=None, nameUser=None):

        if companyName == None or companyName == '':
            companyName = 'Company '+nameUser.capitalize()

        # llamando  al metodo create del model company del modulo base
        # el cual crea una compania
        accountPlan = self.env['account.chart.template'].search([('name','=','Chile - Plan de Cuentas SII')])
        preCompany = self.env['account.multicompany.easy.creation.wiz'].create({'name':companyName,'chart_template_id':accountPlan.id})
        action = preCompany.action_accept()
        company = self.env['res.company'].search([('id','=',action['res_id'])])
        return company

    @api.model
    def _update_users_set_company_id(self, idUser=None, idCompany=None):
        usuario = self.sudo().env['res.users'].search([('id', '=', idUser)])
        self.sudo().env['res.users'].search([('id', '=', 2)]).write({'company_ids':[(4,idCompany)]})
        idPartner = usuario.partner_id.id
        usuario.write({'company_id':idCompany,'company_ids':[(6,0,[int(idCompany)])]})

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
