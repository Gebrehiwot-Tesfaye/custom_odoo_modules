from odoo import models, fields

class EdomiasLocation(models.Model):
    _name = 'agent.location'
    _description = 'Edomias Location'

    name = fields.Char(string='Location Name', required=True)
    description = fields.Text(string='Location Description')
    create_date = fields.Datetime(string="Created Date", readonly=True, default=fields.Datetime.now)
    # Add other common fields for location
