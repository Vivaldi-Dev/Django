import json

from odoo import http
from odoo.http import request


class MeuController(http.Controller):

    @http.route('/recruitment/', auth='public', type="json", methods=['POST'] )
    def meu_endpoint(self):

        registros = request.env['recrutamento.recrutamento'].sudo().search([])


        dados_registros = []


        for registro in registros:
            dados_registros.append({
                'id': registro.id,
                'name': registro.job_name,
                'description': registro.job_description,

            })


        return dados_registros
