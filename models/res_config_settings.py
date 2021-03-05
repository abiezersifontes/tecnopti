from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ip = fields.Char(string="IP")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('tecnopti.ip',self.ip)
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ips = ICPSudo.get_param('tecnopti.ip')
        res.update(
            ip=ips
        )
        return res

