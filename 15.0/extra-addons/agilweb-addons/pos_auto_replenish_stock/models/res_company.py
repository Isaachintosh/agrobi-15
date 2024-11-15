from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    
    create_purchase_order_id = fields.Boolean(
        string="Habilitar criação de Compras",
        help="Habilite esse campo para criar compras de reposição de estoque automaticamente",
        default=False
    )
    
    confirm_picking_id = fields.Boolean(
        string="Habilitar confirmação da entrada em estoque",
        help="Habilite esse campo para confirmar automaticamente o produto comprado por reposição",
        default=False,
    )
    
    auto_create_invoice = fields.Boolean(
        string="Habilitar criação da fatura da compra",
        help="Habilite esse campo para a gesação da fatura da reposição ser automática",
        default=False,
    )