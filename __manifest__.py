# -*- coding: utf-8 -*-
{
    'name': "Request For Approval",
    
    'sequence': 1,
    'summary': """
        Money Approval""",

    'description': """
        Vendor Payment Request 
        Petty Cash Request
    """,

    'author': "Inventions Technologies",
    'website': "http://www.it.co.tz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'mail'],

    # always loaded
    'data': [
        'security/payment_access_right.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
  'application': True,
}