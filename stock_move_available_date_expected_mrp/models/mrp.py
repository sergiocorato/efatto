# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def open_view_stock_reserved(self):
        product = self.product_id
        domain = [
            ("product_id", "=", product.id),
            ("state", "!=", "cancel"),
            ("date", ">=", product.product_tmpl_id.date_oldest_open_move),
        ]
        view = self.env.ref(
            "stock_move_available_date_expected.view_stock_reserved_tree"
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Reserved Stock: %s") % product.name,
            "domain": domain,
            "views": [(view.id, "tree"), (False, "pivot")],
            "res_model": "stock.move",
            "context": {},
        }
