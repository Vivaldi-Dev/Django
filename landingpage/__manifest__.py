

# -*- coding: utf-8 -*-
{
    'name': "landingpage",
    'description': 'Default website theme',
    'category': 'Theme',
    'sequence': 50,
    'version': '1.0',
    'depends': ['base','hr','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/templates/home.xml',
        'views/templates/empresa.xml',
        'views/website_form.xml',
        'views/templates/candidato.xml',
        'views/templates/website.xml',
        'views/templates/menuRecrutamento.xml',
        'views/templates/quemsomos.xml',
        'views/templates/formweb.xml',
        'views/templates/viewformweb.xml',
        'views/templates/blogview.xml',
        'views/templates/blogtemplate.xml',
        'views/templates/bloginfo.xml',
        'views/templates/templateid.xml',
        'views/assets.xml',
    ],
    'qweb': [
    ],
    'assets': {
        'web.assets_frontend': [
            '/landingpage/static/src/js/blog.js',
            '/landingpage/static/src/js/recrutament.js',
        ],
    },

    'images': [

    ],
    'snippet_lists': {
    },
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
