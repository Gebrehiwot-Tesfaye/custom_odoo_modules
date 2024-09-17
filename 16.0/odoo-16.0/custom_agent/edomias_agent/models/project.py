import logging

from odoo.exceptions import ValidationError
from odoo import models, fields, api

from datetime import timedelta, date

_logger = logging.getLogger(__name__)
class EdomiasProject(models.Model):
    _name = 'agent.project'
    _description = 'Edomias Project'
    _order = 'create_date desc'

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Project Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    create_date = fields.Datetime(string="Created Date", readonly=True, default=fields.Datetime.now)

    # Fields to select multiple locations and positions
    location_ids = fields.Many2many('agent.location', string='Locations', required=True)
    position_ids = fields.Many2many('edomias.position', string='Positions', required=True)

    # One2many relation to hold Edomias agents
    agent_ids = fields.One2many('edomias.agent', 'project_id', string='Agents', copy=False)

    @api.constrains('name', 'start_date', 'end_date')
    def _check_unique_name_and_dates(self):
        today = date.today()

        for record in self:
            # Check for unique project name
            project_with_same_name = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if project_with_same_name:
                raise ValidationError('The project name must be unique. Please choose a different name.')

            # Check if the start date is in the past
            if record.start_date and record.start_date < today:
                raise ValidationError("The start date cannot be in the past. Please select a valid date.")

            # Check if the end date is in the past
            if record.end_date and record.end_date < today:
                raise ValidationError("The end date cannot be in the past. Please select a valid end date.")

            # Check if the end date is before the start date
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise ValidationError(
                    "The end date cannot be earlier than the start date. Please select a valid end date.")

    @api.onchange('location_ids', 'position_ids')
    def _onchange_location_position(self):
        """ Automatically add agents when locations or positions are selected """
        # Clear the current agents list to avoid duplication
        agents = []

        # For every combination of location and position, create a new agent entry
        for location in self.location_ids:
            for position in self.position_ids:
                # Check if the agent already exists in the list
                if not any(agent.location_id == location and agent.position_id == position for agent in self.agent_ids):
                    agents.append((0, 0, {
                        'location_id': location.id,
                        'position_id': position.id,
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