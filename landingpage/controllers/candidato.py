# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import werkzeug


class WebsiteForm(http.Controller):

    @http.route('/candidato/', type='http', auth='public', website=True)
    def index_page(self, **kw):
        return request.render('landingpage.candidato', {})

    @http.route(['/candidato/submit'], csrf=False, type='http', auth="public", website=True)
    def contact_form_submit(self, **post):
        request.env['candidato.candidato'].sudo().create({
            'nome': post.get('nome'),
            'apelido': post.get('apelido'),
            'profissao': post.get('profissao'),
            'email': post.get('email'),
            'telefone': post.get('telefone'),

        })
        return request.render("landingpage.on_sucess_submit", {})

