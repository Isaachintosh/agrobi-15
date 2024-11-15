# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends("qty_available")
    @api.onchange("qty_available")
    def auto_replenish_product(self):
        for record in self:
            record.env['stock.warehouse.orderpoint'].search([
                ('product_id','=',record.id)
            ])