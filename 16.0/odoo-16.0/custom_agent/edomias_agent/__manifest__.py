{
    'name': 'Edomias Agent Module',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Employee management system for Edomias Agent',
    'depends': ['base','hr_contract','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/location_views.xml',
        'views/position_views.xml',
        'views/edomias_views.xml',
        'views/menu_views.xml',
         'views/hr_employee_contract_views.xml',
        'data/email_templates.xml',  # Include the email templates
        'data/cron_jobs.xml',
        'views/assets.xml',
    ],

'assets': {
        'web.assets_frontend': [
            'edomias_agent/static/src/css/custom_styles.css',

        ],
    'web.assets_backend': [
        'edomias_agent/static/src/css/custom_styles.css'
      'edomias_agent/static/src/js/project_date_restriction.js',


    ],
    },
    'installable': True,
    'application': True,
   'images': 'static/description/icon.png',
}
