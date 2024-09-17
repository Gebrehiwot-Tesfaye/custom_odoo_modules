from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EdomiasAgent(models.Model):
    _name = 'edomias.agent'
    _description = 'Edomias Agent'

    @api.model
    def some_method(self):
        # Correct usage of self.env
        template_id = self.env.ref('edomias_agent.email_template_project_created').id

    create_date = fields.Datetime(string="Created Date", readonly=True, default=fields.Datetime.now)
    project_id = fields.Many2one('agent.project', ondelete='cascade', string='Project', required=True)
    location_id = fields.Many2one('agent.location', ondelete='cascade', string='Location', required=True)
    position_id = fields.Many2one('edomias.position', ondelete='cascade', string='Position', required=True)

    edomias_rate = fields.Float(string='Edomias Rate', required=True)
    employee_rate = fields.Float(string='Employee Rate', required=True)
    quantity = fields.Integer(string='Quantity', default=1)

    total_edomias_rate = fields.Float(compute='_compute_total_rates', string='Total Edomias Rate')
    total_employee_rate = fields.Float(compute='_compute_total_rates', string='Total Employee Rate')
    net_profit = fields.Float(compute='_compute_total_rates', string='Net Profit')

    @api.depends('edomias_rate', 'employee_rate', 'quantity')
    def _compute_total_rates(self):
        for record in self:
            record.total_edomias_rate = record.edomias_rate * record.quantity
            record.total_employee_rate = record.employee_rate * record.quantity
            record.net_profit = record.total_edomias_rate - record.total_employee_rate

    @api.constrains('edomias_rate', 'employee_rate', 'quantity')
    def _check_positive_values(self):
        for record in self:
            if record.edomias_rate < 0:
                raise ValidationError('The Edomias Rate must be positive.')
            if record.employee_rate < 0:
                raise ValidationError('The Employee Rate must be positive.')
            if record.quantity <= 0:
                raise ValidationError('The Quantity must be greater than or equal to 1.')
