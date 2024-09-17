from odoo import models, fields, api

class EdomiasProject(models.Model):
    _name = 'edomias.project'
    _description = 'Edomias Project'

    name = fields.Char(string='Project Name', required=True)
    client_name = fields.Many2one('res.partner', string='Client Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    location_ids = fields.One2many('edomias.location', 'project_id', string='Locations')
