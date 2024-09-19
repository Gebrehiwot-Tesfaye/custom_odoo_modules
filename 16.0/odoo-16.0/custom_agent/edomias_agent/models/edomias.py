from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EdomiasAgent(models.Model):
    _name = 'edomias.agent'
    _description = 'Edomias Agent'
    _rec_name = "location_id"


    @api.model
    def some_method(self):
        # Correct usage of self.env
        template_id = self.env.ref('edomias_agent.email_template_project_created').id

    create_date = fields.Datetime(string="Created Date", readonly=True, default=fields.Datetime.now)
    project_id = fields.Many2one('agent.project', ondelete='cascade', string='Project', required=True)
    location_id = fields.Many2one('agent.location', ondelete='cascade', string='Location', required=True)
    job_id = fields.Many2one('hr.job', ondelete='cascade', string='Job Position', required=True)

    edomias_rate = fields.Float(string='Edomias Rate', required=True)
    employee_rate = fields.Float(string='Employee Rate', required=True)
    Number_of_Man_Power = fields.Integer(string='Number of Man Power', default=1)

    total_edomias_rate = fields.Float(compute='_compute_total_rates', string='Total Edomias Rate')
    total_employee_rate = fields.Float(compute='_compute_total_rates', string='Total Employee Rate')

    # New allowance fields
    hra = fields.Float(string='HRA', default=0.0)
    da = fields.Float(string='DA', default=0.0)
    travel_allowance = fields.Float(string='Travel Allowance', default=0.0)
    meal_allowance = fields.Float(string='Meal Allowance', default=0.0)
    medical_allowance = fields.Float(string='Medical Allowance', default=0.0)
    other_allowance = fields.Float(string='Other Allowance', default=0.0)

    @api.depends('edomias_rate', 'employee_rate', 'Number_of_Man_Power')
    def _compute_total_rates(self):
        for record in self:
            record.total_edomias_rate = record.edomias_rate * record.Number_of_Man_Power
            record.total_employee_rate = record.employee_rate * record.Number_of_Man_Power

    @api.constrains('edomias_rate', 'employee_rate', 'Number_of_Man_Power')
    def _check_positive_values(self):
        for record in self:
            if record.edomias_rate < 0:
                raise ValidationError('The Edomias Rate must be positive.')
            if record.employee_rate < 0:
                raise ValidationError('The Employee Rate must be positive.')
            if record.Number_of_Man_Power <= 0:
                raise ValidationError('The Number of Man Power must be greater than or equal to 1.')