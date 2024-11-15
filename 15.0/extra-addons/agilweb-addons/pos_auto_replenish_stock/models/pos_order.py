# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    eletronic_document_id = fields.Many2one('eletronic.document', string='Documento Eletrônico')
    
    manual_creation = fields.Boolean(string='Criação Manual', default=False)

    def _process_order(self, order, draft, existing_order):
        result = super(PosOrder, self)._process_order(order, draft, existing_order)
        pos_order_id = self.env['pos.order'].browse(result)
        for line in pos_order_id.lines:
            product_id = line.product_id
            replenish_conf_id = self.env['stock.warehouse.orderpoint'].search([
                ('product_id', '=', product_id.id)
            ])
            if replenish_conf_id:
                if product_id.qty_available <= replenish_conf_id.product_min_qty:
                    # valida se ja tem, e se estiver pendente, finaliza a compra
                    purchase_order_id = self.env['purchase.order'].search([
                        ('product_id', '=', product_id.id),
                        ('state', 'in', ['draft', 'sent'])
                    ], order='id desc', limit=1)
                    replenish_quantity = product_id.qty_available + replenish_conf_id.product_max_qty
                    route_id = product_id.route_ids[0]
                    if route_id:
                        if self.env.company.create_purchase_order_id:
                            
                            replenish_id = self.env['product.replenish'].create({
                                'product_tmpl_id': product_id.product_tmpl_id.id,
                                'product_id': product_id.id,
                                'quantity': replenish_quantity,
                                'date_planned': fields.Datetime.now(),
                                'route_ids': route_id.ids,
                                'product_uom_id': product_id.uom_id.id
                            })
                            replenish_id.launch_replenishment()
                            
                            purchase_order_id = self.env['purchase.order'].search([
                                ('product_id', '=', product_id.id),
                                ('date_planned', '=', replenish_id.date_planned)
                            ], order='id desc', limit=1)
                            if purchase_order_id:
                                purchase_order_id.button_confirm()
                        
                        if self.env.company.confirm_picking_id:
                            picking_id = self.env['stock.picking'].search([
                                ('origin', '=', purchase_order_id.name)
                            ], order='id desc', limit=1)
                            if picking_id:
                                picking_id.action_set_quantities_to_reservation()
                                picking_id.button_validate()
                            
                            if self.env.company.auto_create_invoice:
                                purchase_order_id.action_create_invoice()
        return result

    def create_manual_invoice_document(self):
        for record in self:
            eletronic_document_id = record.create_eletronic_invoice(record)
            record.manual_creation = True
            record.eletronic_document_id = eletronic_document_id.id

    def _compute_nfe_number(self):
        for item in self:
            if not item.sending_nfe:
                item.sending_nfe = False
            if not item.nfe_exception:
                item.nfe_exception = False
            if not item.nfe_status:
                item.nfe_status = ""
            if not item.nfe_number:
                
                company_id = item.env.company or item.env.user.company_id
                nfe_number = company_id.l10n_br_nfe_sequence.next_by_id()
                
                nfe_id = item.env['eletronic.document'].search([('numero', '=', int(nfe_number))], limit=1)
                if not nfe_id:
                    nfe_id = item.env['eletronic.document'].search([], limit=1, order='numero desc')
                
                if nfe_id:
                    item.nfe_number = nfe_id.numero + 1
                else:
                    item.nfe_number = 0
            
            if not item.nfe_exception_number:
                item.nfe_exception_number = 0
            if item.env.company.pos_nfce_sync_emission or item.manual_creation:
                super(PosOrder, item)._compute_nfe_number()