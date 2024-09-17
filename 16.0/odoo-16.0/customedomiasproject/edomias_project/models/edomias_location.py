from odoo import models, fields, api

class EdomiasLocation(models.Model):
    _name = 'edomias.location'
    _description = 'Edomias Project Location'

    name = fields.Selection([
        ('addis_ababa', 'Addis Ababa'),
        ('bahirdar', 'Bahirdar'),
        ('adama', 'Adama'),
        ('hawasa', 'Hawasa'),
        ('jima', 'Jima'),
    ], string='Location', required=True)

    project_id = fields.Many2one('edomias.project', string='Project', required=True)
    position = fields.Char(string='Position')
    employment_rate = fields.Float(string='Employment Rate')
    edomias_rate = fields.Float(string='Edomias Rate')

    @api.onchange('name')
    def _onchange_location_name(self):
        # Set default rates based on location
        if self.name == 'addis_ababa':
            self.employment_rate = 2000
            self.edomias_rate = 1000
        elif self.name == 'bahirdar':
            self.employment_rate = 2500
            self.edomias_rate = 1500
        elif self.name == 'adama':
            self.employment_rate = 1800
            self.edomias_rate = 1200
        elif self.name == 'hawasa':
            self.employment_rate = 2200
            self.edomias_rate = 1300
        elif self.name == 'jima':
            self.employment_rate = 1600
            self.edomias_rate = 1100
