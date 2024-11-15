{
    'name': 'CRM Lost Reason Extension',
    'version': '1.0',
    'depends': ['crm'],
    'author': 'Alexandre Santos Oddocast',
    'category': 'Sales',
    'summary': 'Bloqueia a movimentação para Perdido sem definir motivo da perda.',
    'description': """
        Extensão para o módulo CRM que impede a movimentação de leads para o estágio "Perdido" 
        sem um motivo de perda definido.
    """,
    'data': [
        # 'views/crm_lead_kanban_view.xml',
    ],
    'installable': True,
    'application': False,
}
