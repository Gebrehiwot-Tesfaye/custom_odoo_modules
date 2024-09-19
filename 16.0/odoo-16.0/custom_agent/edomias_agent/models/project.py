import logging

from odoo.exceptions import ValidationError
from odoo import models, fields, api

from datetime import timedelta, date

_logger = logging.getLogger(__name__)
from odoo import models, fields, api

class EdomiasProject(models.Model):
    _name = 'agent.project'
    _description = 'Edomias Project'
    _order = 'create_date desc'

    name = fields.Char(string='Project Name', required=True)

    description = fields.Text(string='Project Description')
    client = fields.Char(string='Client')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    # New Fields

    modality = fields.Selection([
        ('piece_rate', 'Piece Rate'),
        ('whole', 'Whole'),
        ('defined_manpower', 'Defined Man Power'),
        # Add more modalities as needed
    ], string='Modality')
    renewal_date = fields.Date(string='Renewal Date')
    admin_cost = fields.Float(string='Administration Cost', required=False)
    agreement = fields.Binary(string='Agreement', attachment=True)
    is_cost_plus = fields.Boolean(string='Is Cost Plus')
    profit_margin_percentage = fields.Float(string='Profit Margin Percentage', required=False)



    create_date = fields.Datetime(string="Created Date", readonly=True, default=fields.Datetime.now)

    # Fields to select multiple locations and positions
    location_ids = fields.Many2many('agent.location', string='Locations', required=True)
    job_ids = fields.Many2one('hr.job', ondelete='cascade', string='Job Position', required=True)

    # position_ids = fields.Many2many('edomias.position', string='Positions', required=True)

    # One2many relation to hold Edomias agents
    agent_ids = fields.One2many('edomias.agent', 'project_id', string='Agents', copy=False)
    renewal_ids = fields.One2many('agent.project.renewal', 'project_id', string='Renewals')

    # Renewal smart button count
    # Add a computed field for the number of renewals
    renewal_count = fields.Integer(
        string='Number of Renewals',
        compute='_compute_renewal_count',
        store=True
    )

    @api.depends('renewal_ids')
    def _compute_renewal_count(self):
        for project in self:
            project.renewal_count = len(project.renewal_ids)

    # Add a One2many field to link renewals
    renewal_ids = fields.One2many(
        'agent.project.renewal',
        'project_id',
        string='Renewals'
    )
    @api.constrains('name', 'start_date', 'end_date')
    def _check_unique_name_and_dates(self):
        today = date.today()

        for record in self:
            # Check for unique project name
            project_with_same_name = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if project_with_same_name:
                raise ValidationError('The project name must be unique. Please choose a different name.')

            # Check if the start date is in the past
            # if record.start_date and record.start_date < today:
            #     raise ValidationError("The start date cannot be in the past. Please select a valid date.")

            # Check if the end date is in the past
            if record.end_date and record.end_date < today:
                raise ValidationError("The end date cannot be in the past. Please select a valid end date.")

            # Check if the end date is before the start date
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise ValidationError(
                    "The end date cannot be earlier than the start date. Please select a valid end date.")

    @api.onchange('location_ids', 'job_ids')
    def _onchange_location_position(self):
        """ Automatically add agents when locations or positions are selected """
        agents = []

        for location in self.location_ids:
            # job_ids is a Many2one field, so you can't loop through it; just reference its id
            if self.job_ids:
                # Check if the agent already exists in the list
                if not any(agent.location_id == location and agent.job_id == self.job_ids for agent in self.agent_ids):
                    agents.append((0, 0, {
                        'location_id': location.id,
                        'job_id': self.job_ids.id,
                    }))

        # Assign the new agents list to the agent_ids field
        self.agent_ids = agents

    ### ADD THIS CODE BELOW FOR EMAIL NOTIFICATIONS ###

    @api.model
    def create(self, vals):
        # Call the original create method to save the project
        project = super(EdomiasProject, self).create(vals)

        # Call method to send notification email when a project is created
        self.send_project_creation_email(project)

        return project

    def send_project_creation_email(self, project):
        """Send notification email when a project is created."""
        try:
            # Reference the correct email template
            template = self.env.ref('edomias_agent.email_template_project_created')
            _logger.info('Sending email for project: %s', project.name)

            # Send email using the template
            template.send_mail(project.id, force_send=True)

            # Log the email sending action
            _logger.info('Email successfully sent for project: %s', project.name)

        except Exception as e:
            _logger.error('Error sending email: %s', e)

    @api.model
    def check_project_end_dates(self):
        """Check for projects nearing their end date and send notifications."""
        today = fields.Date.today()
        upcoming_projects = self.search([('end_date', '<=', today + timedelta(days=30))])

        for project in upcoming_projects:
            self.send_end_date_notification(project)

    def send_end_date_notification(self, project):
        """Send email to notify about project nearing its end date."""
        try:
            template = self.env.ref('edomias_agent.email_template_contract_ending')
            template.send_mail(project.id, force_send=True)
            _logger.info('End date notification sent for project: %s', project.name)
        except Exception as e:
            _logger.error('Error sending end date email: %s', e)

    @api.model
    def toggle_column_options(self):
        # Logic to handle the toggling of column options in the view
        # This is a placeholder; implement the logic based on your needs
        pass