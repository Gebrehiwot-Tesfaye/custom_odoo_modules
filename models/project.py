import logging

from odoo import models, fields, api

from datetime import timedelta

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
        """Send notification email to Managing Director, HR Manager, Finance Manager, etc."""
        # Logic to select email recipients based on user roles or groups
        managing_director = self.env.ref('base.user_admin')  # Example reference for admin user
        hr_manager_group = self.env.ref('hr.group_hr_manager')
        hr_managers = self.env['res.users'].search([('groups_id', 'in', hr_manager_group.id)])

        # Find all email recipients
        recipients = managing_director | hr_managers  # Combine with other user groups as needed

        # Send email
        template_id = self.env.ref('custom_module.email_template_project_created').id  # Reference the email template
        template = self.env['mail.template'].browse(template_id)
        for recipient in recipients:
            template.email_to = recipient.email
            template.send_mail(project.id, force_send=True)

    @api.model
    def check_project_end_dates(self):
        """Check for projects whose end dates are approaching and send notifications."""
        today = fields.Date.today()
        upcoming_projects = self.search([('end_date', '<=', today + timedelta(days=30))])

        for project in upcoming_projects:
            self.send_end_date_notification(project)

    def send_end_date_notification(self, project):
        """Send email to notify about project approaching its end date."""
        # Logic to send emails to relevant users
        operation_head = self.env['res.users'].search([('role', '=', 'operation_head')])  # Example
        managing_director = self.env.ref('base.user_admin')  # Example for admin user

        # Combine all recipients and send the email
        recipients = operation_head | managing_director  # Add others like HR, Finance if needed
        template_id = self.env.ref('custom_module.email_template_contract_ending').id  # End date email template
        template = self.env['mail.template'].browse(template_id)
        for recipient in recipients:
            template.email_to = recipient.email
            template.send_mail(project.id, force_send=True)

    @api.model
    def send_project_creation_email(self, project):
        try:
            template = self.env.ref('edomias_agent.email_template_project_created')
            _logger.info('Sending email for project: %s', project.name)
            _logger.info('Email template subject: %s', template.subject)
            # Send email using the template
            template.send_mail(project.id, force_send=True)
        except Exception as e:
            _logger.error('Error sending email: %s', e)

    @api.model
    def send_project_creation_email(self, project):
        template = self.env.ref('edomias_agent.email_template_project_created')
        template.send_mail(project.id, force_send=True)