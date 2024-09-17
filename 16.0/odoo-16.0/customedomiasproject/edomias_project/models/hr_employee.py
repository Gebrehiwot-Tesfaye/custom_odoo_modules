from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    edomias_project_id = fields.Many2one('edomias.project', string='Edomias Project')
    location_id = fields.Many2one('edomias.location', string='Edomias Location')
