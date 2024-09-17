from odoo import models, fields, api

class Payroll(models.Model):
    _name = 'my_module.payroll'
    _description = 'Payroll Information'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    earning = fields.Float(string="Earning")
    deduction = fields.Float(string="Deduction")
    total_pay = fields.Float(string="Total Pay", compute='_compute_total_pay')

    @api.depends('earning', 'deduction')
    def _compute_total_pay(self):
        for record in self:
            record.total_pay = record.earning - record.deduction
