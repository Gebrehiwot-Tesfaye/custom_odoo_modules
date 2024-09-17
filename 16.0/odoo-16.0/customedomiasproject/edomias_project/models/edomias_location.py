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

    position = fields.Selection([
        ('manager', 'Manager'),
        ('security', 'Security'),
        ('engineer', 'Engineer'),
        ('technician', 'Technician'),
        ('accountant', 'Accountant'),
        ('driver', 'Driver'),
        ('cleaner', 'Cleaner'),
        ('supervisor', 'Supervisor'),
        ('clerk', 'Clerk'),
        ('admin_assistant', 'Admin Assistant'),
    ], string='Position', required=True)

    employment_rate = fields.Float(string='Employment Rate')
    edomias_rate = fields.Float(string='Edomias Rate')
    total_rate = fields.Float(string='Total Rate', compute='_compute_total_rate', store=True)

    project_id = fields.Many2one('edomias.project', string='Project', required=True)

    # Base rates for positions
    base_position_rates = {
        'manager': (2000, 1000),
        'security': (1500, 800),
        'engineer': (2500, 1200),
        'technician': (1800, 1000),
        'accountant': (2200, 1100),
        'driver': (1600, 900),
        'cleaner': (1200, 600),
        'supervisor': (1900, 1000),
        'clerk': (1500, 800),
        'admin_assistant': (1700, 900),
    }

    # Location rate multipliers
    location_rate_multipliers = {
        'addis_ababa': 1.2,
        'bahirdar': 1.3,
        'adama': 1.1,
        'hawasa': 1.25,
        'jima': 1.15,
    }

    @api.onchange('name', 'position')
    def _onchange_location_and_position(self):
        if self.position and self.name:
            # Get base rates for the selected position
            base_employment_rate, base_edomias_rate = self.base_position_rates.get(self.position, (0, 0))

            # Adjust rates based on location
            location_multiplier = self.location_rate_multipliers.get(self.name, 1)

            self.employment_rate = base_employment_rate * location_multiplier
            self.edomias_rate = base_edomias_rate * location_multiplier

    @api.depends('employment_rate', 'edomias_rate')
    def _compute_total_rate(self):
        for record in self:
            record.total_rate = record.employment_rate + record.edomias_rate
