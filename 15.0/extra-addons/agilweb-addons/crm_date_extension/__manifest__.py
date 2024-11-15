{
    'name': 'Custom CRM date Extension',
    'version': '1.0',
    'summary': 'Extensão do CRM para exibir a data de criação no Kanban',
    'description': 'Adiciona a data de criação nos cartões da visualização Kanban do CRM.',
    'category': 'Sales',
    'author': 'Alexandre',
    'depends': ['crm'],
    "data": [
        "views/crm_lead_kanban_view.xml",
        # "views/crm_lead_views.xml",
        # "security/ir.model.access.csv"
    ],
    'installable': True,
    'application': False,
}
