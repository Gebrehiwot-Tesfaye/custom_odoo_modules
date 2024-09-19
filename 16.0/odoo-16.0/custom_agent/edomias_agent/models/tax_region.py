from odoo import models, fields

class TaxRegion(models.Model):
    _name = 'tax.region'
    _description = 'Tax Region'

    tax_region_name = fields.Char(string='Tax Region Name', required=True)
    description = fields.Text(string='Description')

    def name_get(self):
        return [(record.id, record.tax_region_name) for record in self]
