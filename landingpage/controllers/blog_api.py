from odoo import http
from odoo.http import request
import base64


class BlogController(http.Controller):

    @http.route('/get-blog/', auth='public', type="json", methods=['POST'])
    def get_blog(self):
        registros = request.env['customblog.customblog'].sudo().search([])

        dados_blog = []

        for registro in registros:


            dados_blog.append({
                'id': registro.id,
                'author': registro.author,
                'published_date': registro.published_date.strftime('%Y-%m-%d'),
                'category': registro.category,
                'tags': registro.tags,
                'post_title': registro.post_title,
                'content': registro.content,
                'comments': registro.comments,
                'featured_image_url': registro.featured_image,
            })

        return dados_blog
