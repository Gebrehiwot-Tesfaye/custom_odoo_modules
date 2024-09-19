from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    project_id = fields.Many2one('agent.project', string='Project', required=True)
    location_id = fields.Many2one('agent.location', string='Location')

    # Wage and Allowance Fields
    wage = fields.Float(string='Wage')
    hra = fields.Float(string='HRA', default=0.0)
    da = fields.Float(string='DA', default=0.0)
    travel_allowance = fields.Float(string='Travel Allowance', default=0.0)
    meal_allowance = fields.Float(string='Meal Allowance', default=0.0)
    medical_allowance = fields.Float(string='Medical Allowance', default=0.0)
    other_allowance = fields.Float(string='Other Allowance', default=0.0)

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id and self.project_id and self.location_id:
            agent = self.env['edomias.agent'].search([
                ('job_id', '=', self.job_id.id),
                ('project_id', '=', self.project_id.id),
                ('location_id', '=', self.location_id.id)  # Ensure it's valid for the selected location
            ], limit=1)

            if agent:
                # Automatically fill wage and allowances based on the agent
                self.wage = agent.employee_rate
                self.hra = agent.hra
                self.da = agent.da
                self.travel_allowance = agent.travel_allowance
                self.meal_allowance = agent.meal_allowance
                self.medical_allowance = agent.medical_allowance
                self.other_allowance = agent.other_allowance
            else:
                # If no matching agent is found, reset fields
                self.wage = 0.0
                self.hra = 0.0
                self.da = 0.0
                self.travel_allowance = 0.0
                self.meal_allowance = 0.0
                self.medical_allowance = 0.0
                self.other_allowance = 0.0

    @api.onchange('location_id')
    def _onchange_location_id(self):
        if self.location_id and self.project_id:
            # Check if the current job position is valid for the selected location
            valid_agents = self.env['edomias.agent'].search([
                ('project_id', '=', self.project_id.id),
                ('location_id', '=', self.location_id.id),
                ('job_id', '=', self.job_id.id)
            ])

            if not valid_agents:
                # Reset job_id, wage, and allowances if no valid agent is found for the new location
                self.job_id = False
                self.wage = 0.0
                self.hra = 0.0
                self.da = 0.0
                self.travel_allowance = 0.0
                self.meal_allowance = 0.0
                self.medical_allowance = 0.0
                self.other_allowance = 0.0

            # Additional filtering for job positions based on location
            available_jobs = self.env['edomias.agent'].search([
                ('project_id', '=', self.project_id.id),
                ('location_id', '=', self.location_id.id)
            ]).mapped('job_id')

            return {
                'domain': {
                    'job_id': [('id', 'in', available_jobs.ids)]
                }
            }
        else:
            # Clear the job position, wage, and allowances if no location is selected
            self.job_id = False
            self.wage = 0.0
            self.hra = 0.0
            self.da = 0.0
            self.travel_allowance = 0.0
            self.meal_allowance = 0.0
            self.medical_allowance = 0.0
            self.other_allowance = 0.0

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            # Filter locations and job positions based on the selected project
            return {
                'domain': {
                    'location_id': [('id', 'in', self.project_id.agent_ids.location_id.ids)],
                    'job_id': [('id', 'in', self.project_id.agent_ids.job_id.ids)]
                }
            }
        else:
            # Clear domain when no project is selected
            return {
                'domain': {
                    'location_id': [],
                    'job_id': []
                }
            }
