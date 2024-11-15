# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    default_purchase_route = fields.Boolean(
        string="Rota Padrão para Reposições",
        help="Habilite essa opção para o sistema prioriza-la na reposição de estoques",
        default=False
    )