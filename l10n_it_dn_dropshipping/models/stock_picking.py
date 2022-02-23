# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'shipping.information.updater.mixin']

    @api.multi
    @api.returns('res.partner')
    def get_partners(self):
        partner_id = self.mapped('partner_id')

        if len(partner_id) != 1 and self.location_dest_id.usage == 'customer':
            raise ValueError(
                "You have just called this method on an heterogeneous set "
                "of pickings.\n"
                "All pickings should have the same 'partner_id' field value.")

        src_location_id = self.mapped('location_id')

        if len(src_location_id) != 1:
            raise ValueError(
                "You have just called this method on an heterogeneous set "
                "of pickings.\n"
                "All pickings should have the same 'location_id' field value.")

        dest_location_id = self.mapped('location_dest_id')

        if len(dest_location_id) != 1:
            raise ValueError(
                "You have just called this method on an heterogeneous "
                "set of pickings.\n"
                "All pickings should have the same 'location_dest_id' "
                "field value.")

        src_warehouse_id = src_location_id.get_warehouse()
        dest_warehouse_id = dest_location_id.get_warehouse()

        src_partner_id = src_warehouse_id.partner_id
        dest_partner_id = dest_warehouse_id.partner_id

        if not src_partner_id:
            src_partner_id = partner_id
            if not dest_partner_id:
                dest_partner_id = self.mapped('move_ids_without_package.partner_id')

            if not dest_partner_id:
                raise ValueError(
                    "Fields 'src_partner_id' and 'dest_partner_id' "
                    "cannot be both unset.")

        elif not dest_partner_id:
            dest_partner_id = partner_id

        return (src_partner_id, dest_partner_id)