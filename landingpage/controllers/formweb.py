# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import werkzeug


class WebsiteForm(http.Controller):

    @http.route('/formuweb/', type='http', auth='public', website=True)
    def index_page(self, **kw):
        return request.render('landingpage.formweb', {})

    @http.route(['/formuweb/submit'], csrf=False, type='http', auth="public", website=True)
    def contact_form_submit(self, **post):
        request.env['formweb.formweb'].sudo().create({
            'nome': post.get('nome'),
            'apelido': post.get('apelido'),
            'email': post.get('email'),
            'numero_celular': post.get('numero_celular'),
            'mensagem': post.get('mensagem'),

        })
        return request.render("landingpage.on_sucess_submit", {})

