from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    eletronic_doc_id = fields.Many2one(
        comodel_name="eletronic.document",
        string="Nota Eletrônica Relacionada"
    )