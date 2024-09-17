from odoo import models, fields

class Location(models.Model):
    _name = 'project.location'
    _description = 'Project Location'

    name = fields.Char(string='Location Name', required=True)
