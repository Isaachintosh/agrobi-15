{
    'name': 'Auto Reposição PDV',
    'version': '15.0',
    'description': 'Reposição automática do estoque de produtos disponíveis no PDV',
    'summary': 'Reposição automática do estoque de produtos disponíveis no PDV',
    'author': 'Isaachintosh',
    'website': 'https://www.odoocast.com.br',
    'license': 'LGPL-3',
    'category': 'tools',
    'depends': [
        'base',
        'stock',
        'product',
        'point_of_sale',
        'purchase',
        'l10n_br_point_of_sale',
        'l10n_br_eletronic_document'
    ],
    "data": [
        "views/res_company_views.xml",
        "views/stock_location_route_views.xml",
        "views/pos_order_views.xml",
        "views/eletronic_document_views.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}