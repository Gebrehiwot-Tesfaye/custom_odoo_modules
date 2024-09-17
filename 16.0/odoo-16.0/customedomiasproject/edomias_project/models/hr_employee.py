from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    contract_date = fields.Date(string='Contract Date')
    allowance_rate = fields.Float(string='Allowance Rate')
    edomias_project_id = fields.Many2one('edomias.project', string='Edomias Project')
    location_id = fields.Many2one('edomias.location', string='Edomias Location')
