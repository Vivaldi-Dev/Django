# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import werkzeug


class WebsiteForm(http.Controller):

    @http.route('/form/', type='http', auth='public', website=True)
    def index_page(self, **kw):
        return request.render('landingpage.empresa', {})

    @http.route(['/form/submit'], csrf=False, type='http', auth="public", website=True)
    def contact_form_submit(self, **post):
        request.env['empresa.empresa'].sudo().create({
            'nome_empresa': post.get('nome_empresa'),
            'email': post.get('email'),
            'numero': post.get('numero'),
            'nuit': post.get('nuit'),


        })
        return request.render("landingpage.on_sucess_submit", {})

