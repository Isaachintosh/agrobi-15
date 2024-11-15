# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    pos_nfce_sync_emission = fields.Boolean(
        string="Habilitar Emissão Fiscal no POS"
    )
    
    default_nfce_fiscal_position_id = fields.Many2one(
        "account.fiscal.position",
        string="Posição Fiscal Padrão p/ NFC-e",
    )
