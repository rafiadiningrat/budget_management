# -*- coding: utf-8 -*-
{
    'name': "infomedia",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','om_account_accountant','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/sequence.xml',
        'views/purchase_order_views.xml',
        # 'views/service_team_views.xml',
        # 'views/work_order_views.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/menu_items.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

