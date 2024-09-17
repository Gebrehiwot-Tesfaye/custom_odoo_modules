# edomias_operation/__manifest__.py

{
    'name': 'Edomias_Operation_Management',
    'version': '1.0',
    'summary': 'Manage clients, projects, payroll, purchases, and sales for Edomias International',
    'author': 'Your Name',
    'category': 'Operations',
    'depends': ['base', 'hr', 'purchase', 'sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/client_views.xml',
        'views/project_views.xml',
        'views/payroll_views.xml',
        'views/purchase_views.xml',
        'views/sales_views.xml',
        'views/menu_views.xml',
        # 'data/email_templates.xml',

        'data/data.xml',
    ],
    'installable': True,
    'application': False,
}
