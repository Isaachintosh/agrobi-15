{
    'name': 'Account Extension - Analítico e Sintético',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Extensão do módulo de contabilidade para adicionar tipos Analítico e Sintético',
    'description': """Este módulo estende o módulo account para adicionar novos tipos de conta: Analítico e Sintético.""",
    'depends': ['account'],
    'data': [
        'data/data_account_type_extension.xml',
    ],
    'installable': True,
    'application': False,
}
