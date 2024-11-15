# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64

_logger = logging.getLogger(__name__)


class StockQtyImportWizard(models.TransientModel):
    _name = 'stock.qty.import.wizard'
    _description = _('StockQtyImportWizard')

    xlsx_file = fields.Binary(string='XLSX File', required=True)
    xlsx_file_name = fields.Char(string='XLSX File Name')

    def import_xlsx(self):
        """ Abre o xlsx_file, pesquisa por 2 colunas, a de referencia interna e quantidade, pesquisa pelo produto e atualiza a quantidade em mãos """
        try:
            import xlrd
            from xlrd import open_workbook
        except ImportError:
            raise UserError(_('Please install xlrd module'))

        if self.xlsx_file:
            decoded_data = base64.b64decode(self.xlsx_file)
            wb = open_workbook(file_contents=bytes(decoded_data))
            for sheet in wb.sheets():
                ref_column = None
                qty_column = None
                for column in range(1, sheet.ncols):
                    if 'Referência Interna' in sheet.cell(0, column).value:
                        ref_column = column
                    if 'Quantidade' in sheet.cell(0, column).value:
                        qty_column = column
                index = 0
                for row in range(1, sheet.nrows):
                    ref = None
                    qty = None
                    if sheet.cell(row, ref_column).value:
                        ref = sheet.cell(row, ref_column).value
                    if sheet.cell(row, qty_column).value:
                        qty = sheet.cell(row, qty_column).value
                    if ref and qty:
                        product = self.env['product.product'].search([('default_code', '=', ref)], limit=1)
                        if product:
                            template_id = product.action_update_quantity_on_hand()
                            if product.qty_available < 0:
                                qty = abs(product.qty_available + qty)
                            if qty < 0:
                                qty = abs(qty)
                            try:
                                wizard_id = self.env['stock.change.product.qty'].create({
                                    'product_id': product.id,
                                    'product_tmpl_id': product.product_tmpl_id.id,
                                    'new_quantity': qty,
                                })
                                wizard_id.change_product_qty()
                            except Exception as e:
                                _logger.error(f'Erro ao atualizar a quantidade do produto {product.name}: {e}')
                                wizard_id.new_quantity = abs(qty)
                    index += 1
                    _logger.info(f'Atualização de Quantidades de Produtos: {index}/{sheet.nrows}')