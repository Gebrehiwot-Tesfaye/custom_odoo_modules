from odoo import models, fields, api, exceptions


class Purchase(models.Model):
    _name = 'my_module.purchase'
    _description = 'Purchase Information'

    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    requisition = fields.Char(string="Store Requisition")
    goods_available = fields.Boolean(string="Goods Available")
    purchase_requisition_id = fields.Many2one('my_module.purchase_requisition', string="Purchase Requisition")
    comparison_report = fields.Binary(string="Comparison Report")
    purchase_order_id = fields.Many2one('my_module.purchase_order', string="Purchase Order")
    vat_returnable = fields.Boolean(string="VAT Returnable")
    non_vat_returnable = fields.Boolean(string="Non VAT Returnable")

    @api.model
    def create_purchase_order(self, vals):
        # Ensure the 'project_id' and 'goods_available' fields are in vals
        if 'project_id' not in vals or 'goods_available' not in vals:
            raise exceptions.ValidationError("Project ID and Goods Availability must be provided.")

        # Create a new record
        res = super(Purchase, self).create(vals)

        # Process based on goods availability
        if not res.goods_available:
            # Create a purchase requisition
            requisition_vals = {
                'project_id': res.project_id.id,
                'requisition': res.requisition,
                'state': 'draft'
            }
            purchase_requisition = self.env['my_module.purchase_requisition'].create(requisition_vals)
            res.purchase_requisition_id = purchase_requisition.id

            # TODO: Add logic for managing comparison report and quotations
            # Here you might handle creating quotations, managing comparison reports, and approval workflows

        else:
            # If goods are available, create a purchase order directly
            purchase_order_vals = {
                'project_id': res.project_id.id,
                'vat_returnable': res.vat_returnable,
                'non_vat_returnable': res.non_vat_returnable,
                'state': 'draft'
            }
            purchase_order = self.env['my_module.purchase_order'].create(purchase_order_vals)
            res.purchase_order_id = purchase_order.id

        return res


class PurchaseRequisition(models.Model):
    _name = 'my_module.purchase_requisition'
    _description = 'Purchase Requisition'

    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    requisition = fields.Char(string="Requisition")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
    ], default='draft', string="Status")

    @api.model
    def approve_requisition(self):
        for rec in self:
            rec.state = 'approved'


class PurchaseOrder(models.Model):
    _name = 'my_module.purchase_order'
    _description = 'Purchase Order'

    project_id = fields.Many2one('my_module.project', string="Project", required=True)
    vat_returnable = fields.Boolean(string="VAT Returnable")
    non_vat_returnable = fields.Boolean(string="Non VAT Returnable")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', string="Status")

    # Add more fields as necessary for the purchase order

    @api.model
    def confirm_order(self):
        for rec in self:
            rec.state = 'confirmed'

    @api.model
    def finalize_order(self):
        for rec in self:
            rec.state = 'done'
