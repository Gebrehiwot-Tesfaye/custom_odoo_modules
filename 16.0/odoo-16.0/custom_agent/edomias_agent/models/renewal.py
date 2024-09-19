from odoo import models, fields, api

class AgentProjectRenewal(models.Model):
    _name = 'agent.project.renewal'
    _description = 'Project Renewal'

    project_id = fields.Many2one('agent.project', string='Project', required=True)
    renewal_start_date = fields.Date(string='Renewal Start Date', required=True)
    renewal_end_date = fields.Date(string='Renewal End Date', required=True)
    updated_price = fields.Float(string='Updated Price')
    renewal_number = fields.Integer(string='Renewal Number', compute='_compute_renewal_number', store=True)
