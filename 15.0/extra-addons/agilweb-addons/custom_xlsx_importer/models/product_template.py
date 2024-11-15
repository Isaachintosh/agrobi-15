# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def open_product_qty_wizard(self):
        view_id = self.env.ref('custom_xlsx_importer.view_stock_qty_import_wizard_form')
        return {
            'name': _('Product Quantity Import Wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.qty.import.wizard',
            'view_mode': 'form',
            'views': [(view_id.id, 'form')],
            'target': 'new',
        }
