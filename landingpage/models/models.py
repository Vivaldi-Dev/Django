# -*- coding: utf-8 -*-

from odoo import models, fields, api


class landingpage(models.Model):
    _name = 'landingpage.landingpage'
    _description = 'landingpage.landingpage'


class empresa(models.Model):
    _name = 'empresa.empresa'
    _description = 'empresa.empresa'

    nome_empresa = fields.Char(string='nome da empresa')
    email = fields.Char(string='email da empresa')
    numero = fields.Char(string='numero da empresa')
    nuit = fields.Char(string='nuit da empresa')


class candidato(models.Model):
    _name = 'candidato.candidato'
    _description = 'candidato.candidato'

    nome = fields.Char(string='Nome')
    apelido = fields.Char(string='Apelido')
    profissao = fields.Char(string="Profissão")
    email = fields.Char(string='E-mail')
    telefone = fields.Char(string='Telefone')


class formWeb(models.Model):
    _name = 'formweb.formweb'
    _description = 'formweb.formweb'

    nome = fields.Char(string='Nome')
    apelido = fields.Char(string='Apelido')
    email = fields.Char(string='E-mail')
    numero_celular = fields.Char(string='Telefone')
    mensagem = fields.Text(string='Mensagem')


class recrutamento(models.Model):
    _name = 'recrutamento.recrutamento'
    _description = 'recrutamento.recrutamento'

    job_id = fields.Many2one('hr.job', string='Job Position', help='Job Position', ondelete='restrict')

    job_name = fields.Char(string='Job Name', )
    job_description = fields.Html(string='Job Description')


class CustomBlog(models.Model):
    _name = 'customblog.customblog'
    _description = 'customblog.customblog'

    title = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    published_date = fields.Date(string='Published Date')
    category = fields.Char(string='Category')
    tags = fields.Char(string='Tags')
    post_title = fields.Char(string='Post Title')
    content = fields.Text(string='Content')
    comments = fields.Text(string='Comments')
    featured_image = fields.Image(string='Upload Image' , max_width=100,
                                  max_height=100,verify_resolution=False , help="This is a blog image")
