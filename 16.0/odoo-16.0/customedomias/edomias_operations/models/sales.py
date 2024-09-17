from odoo import models, fields, api

class SalesOrder(models.Model):
    _name = 'my_module.sales_order'
    _description = 'Sales Order Information'

    client_id = fields.Many2one('my_module.client', string="Client", required=True)
    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    location = fields.Char(string="Location")
    contract_info = fields.Text(string="Contract Information")
    service_ids = fields.One2many('my_module.sales_service', 'sales_order_id', string="Services")

class SalesService(models.Model):
    _name = 'my_module.sales_service'
    _description = 'Sales Service Information'

    sales_order_id = fields.Many2one('my_module.sales_order', string="Sales Order", required=True)
    service_name = fields.Char(string="Service Name", required=True)
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    admin_cost = fields.Float(string="Administration Cost")
    fixed_rate_costs = fields.Float(string="Fixed Rate Costs")
    vat = fields.Float(string="VAT")
    total_cost = fields.Float(string="Total Cost", compute='_compute_total_cost')

    @api.depends('quantity', 'unit_price', 'admin_cost', 'fixed_rate_costs', 'vat')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = (
                record.quantity * record.unit_price +
                record.admin_cost + record.fixed_rate_costs +
                record.vat
            )
