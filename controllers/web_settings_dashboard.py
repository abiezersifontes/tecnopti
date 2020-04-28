
import logging

from datetime import datetime, timedelta

from odoo import _, fields, http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo import release
from odoo.addons.web_settings_dashboard.controllers.main import WebSettingsDashboard
_logger = logging.getLogger(__name__)

class WebSettingsDashboardCustom(WebSettingsDashboard):
    @http.route('/web_settings_dashboard/data', type='json', auth='user')
    def web_settings_dashboard_data(self, **kw):
        response = super(WebSettingsDashboardCustom, self).web_settings_dashboard_data(**kw)
        _logger.warning("################################################################")
        _logger.warning("################################################################")
        _logger.warning(response['share'])
        _logger.warning("################################################################")
        _logger.warning("################################################################")
        return response
