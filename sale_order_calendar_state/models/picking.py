# Copyright 2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class Picking(models.Model):
    _inherit = "stock.picking"

    date_ready_to_deliver = fields.Datetime(
        compute='_compute_date_ready_to_deliver',
        store=True
    )
    is_assigned = fields.Boolean(
        string="Printed for logistic",
        copy=False
    )

    @api.depends('state')
    def _compute_date_ready_to_deliver(self):
        for pick in self:
            if pick.state in ['draft', 'waiting', 'confirmed', 'cancel']:
                pick.date_ready_to_deliver = False
            elif pick.state == 'assigned':
                pick.date_ready_to_deliver = fields.Datetime.now()

    @api.multi
    def mark_printed_for_logistic(self):
        self.write({'is_assigned': True})

    @api.multi
    def unmark_printed_for_logistic(self):
        self.write({'is_assigned': False})

    @api.multi
    def do_unreserve(self):
        res = super().do_unreserve()
        self.write({'is_assigned': False})
        return res

    @api.multi
    def action_cancel(self):
        self.write({'is_assigned': False})
        return super().action_cancel()