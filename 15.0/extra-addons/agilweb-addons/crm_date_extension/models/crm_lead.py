from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campo personalizado para armazenar a data e hora da criação
    x_create_timestamp = fields.Datetime(
        string="Data e Hora da Criação", 
        readonly=True, 
        default=fields.Datetime.now  # Define o valor padrão como a data e hora atuais
    )
