# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_id = fields.Many2one(
        string='Sale Order',
        related='move_id.sale_line_id.order_id',
        store=True,
        index=True,
    )
    sale_partner_id = fields.Many2one(
        string='Sale Partner',
        related='sale_id.partner_id',
        store=True,
        index=True,
    )
    purchase_id = fields.Many2one(
        string='Purchase Order',
        related='move_id.purchase_line_id.order_id',
        store=True,
        index=True,
    )