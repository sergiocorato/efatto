# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def open_view_stock_reserved(self):
        product = self.product_id.id if self.product_id.type != 'service' else False
        if product:
            domain = [('product_id', '=', product),
                      ('state', 'not in', ['cancel', 'done'])]
            view = self.env.ref(
                'stock_move_available_date_expected.view_stock_reserved_tree')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Stock reserved',
                'domain': domain,
                'views': [(view.id, 'tree'), (False, 'pivot')],
                'res_model': 'stock.move',
                'context': {'search_default_date_expected_from_today': 1}
            }
