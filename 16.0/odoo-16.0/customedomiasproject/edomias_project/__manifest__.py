{
    'name': 'Edomias Project Management',
    'version': '1.0',
    'summary': 'Manage Edomias projects with client information, locations, and rates',
    'description': """
        This module helps manage Edomias projects, track employment rates, Edomias rates, and location-specific data.
    """,
    'author': 'Your Name',
    'depends': ['base', 'project', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/edomias_menu.xml',
        'views/edomias_project_views.xml',
        'views/edomias_location_views.xml',
        'views/hr_employee_views.xml',

    ],
    'installable': True,
    'application': True,
}
