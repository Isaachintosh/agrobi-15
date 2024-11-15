# -*- coding: utf-8 -*-
{
    'name': 'Custom_xlsx_importer',
    'version': '',
    'summary': """ Custom_xlsx_importer Summary """,
    'author': '',
    'website': '',
    'category': '',
    'depends': ['base', 'stock', 'product'],
    "data": [
        "wizard/stock_qty_import_wizard.xml",
        "security/ir.model.access.csv",
        "views/product_template_views.xml"
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
