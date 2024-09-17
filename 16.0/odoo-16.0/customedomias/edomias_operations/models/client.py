from odoo import models, fields, api

class Client(models.Model):
    _name = 'my_module.client'
    _description = 'Client Information'

    name = fields.Char(string="Client Name", required=True)
    project_ids = fields.One2many('my_module.project', 'client_id', string="Projects")
