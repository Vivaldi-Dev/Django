from odoo import http
from odoo.http import request
import werkzeug


class WebsiteForm(http.Controller):
    @http.route('/teste/<int:id>/', type='http', auth='public', website=True)
    def function_name(self, id):

        record = request.env['customblog.customblog'].sudo().search([('id', '=', id)])

        values = {
            'key_value': record
        }
        return request.render(
            'landingpage.teste', values)