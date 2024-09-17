from odoo import models, fields, api

class Project(models.Model):
    _name = 'my_module.project'
    _description = 'Project Information'

    name = fields.Char(string="Project Name", required=True)
    client_id = fields.Many2one('my_module.client', string="Client", required=True)
    contract_start_date = fields.Date(string="Contract Start Date")
    contract_end_date = fields.Date(string="Contract End Date")
    modality = fields.Selection([
        ('piece_rate', 'Piece Rate'),
        ('whole_defined', 'Whole Defined Man Power'),
        # Add other modalities as needed
    ], string="Modality")
    num_manpower = fields.Integer(string="Number of Man Power")
    renewal_date = fields.Date(string="Renewal Date")
    region = fields.Char(string="Region")
    location = fields.Char(string="Location")
    admin_cost = fields.Float(string="Administration Cost")
    fixed_rate_costs = fields.Float(string="Fixed Rate Costs")
    profit_margin_percentage = fields.Float(string="Profit Margin Percentage")
    type = fields.Selection([
        ('cleaning', 'Cleaning'),
        ('security', 'Security'),
        # Add other types as needed
    ], string="Type")
    employee_rate_ids = fields.One2many('my_module.employee_rate', 'project_id', string="Employee Rates")
    edomias_rate_ids = fields.One2many('my_module.edomias_rate', 'project_id', string="Edomias Rates")
    pension_tax_center = fields.Char(string="Pension Tax Center")
    income_tax_center = fields.Char(string="Income Tax Center")
    contract_notification_date = fields.Date(string="Contract Notification Date")

    @api.model
    def create(self, vals):
        # Send email notification when a new project is created
        res = super(Project, self).create(vals)
        self.env.ref('my_module.new_project_email_template').send_mail(res.id)
        return res

    @api.model
    def check_contract_end_dates(self):
        # Logic to check contract end dates and send notifications
        projects = self.search([('contract_end_date', '<=', fields.Date.today())])
        for project in projects:
            # Send notification logic here
            pass

    @api.model
    def check_manpower_limits(self):
        # Logic to check if employee count exceeds the number of manpower
        projects = self.search([])
        for project in projects:
            if len(project.employee_rate_ids) > project.num_manpower:
                # Send notification logic here
                pass

class EmployeeRate(models.Model):
    _name = 'my_module.employee_rate'
    _description = 'Employee Rate Information'

    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    location = fields.Char(string="Location")
    position = fields.Char(string="Position")
    rate = fields.Float(string="Rate")

class EdomiasRate(models.Model):
    _name = 'my_module.edomias_rate'
    _description = 'Edomias Rate Information'

    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    location = fields.Char(string="Location")
    position = fields.Char(string="Position")
    rate = fields.Float(string="Rate")
