from odoo import models, fields, api, exceptions, _


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'
    _order = 'ddt_number desc'

    ddt_date_start = fields.Datetime(
        string='DDT date start',
        copy=False)
    date = fields.Date(
        string='Document Date',
        default=fields.Date.today,
        states={
            'done': [('readonly', True)],
            'in_pack': [('readonly', True)],
            'cancel': [('readonly', True)]
        }, copy=False)
    ddt_type_id = fields.Many2one(required=True)

    @api.multi
    def set_done(self):
        # put date in context to get correct next id sequence
        for package in self:
            if not package.ddt_number:
                package.ddt_number = package.ddt_type_id.sequence_id.\
                    with_context({'ir_sequence_date': package.date}
                                 ).next_by_id()
        return super(StockPickingPackagePreparation, self).set_done()

    @api.multi
    def action_put_in_pack(self):
        # put date in context to get correct next id sequence and check if
        # the date of ddt is possible, if not change it to last date available
        for package in self:
            # ----- Assign ddt number if ddt type is set
            if package.ddt_type_id and not package.ddt_number:
                package.ddt_number = package.ddt_type_id.sequence_id.\
                    with_context({'ir_sequence_date': package.date}
                                 ).next_by_id()
                # check date progression
                ddt_type_ids = self.env['stock.ddt.type'].search([
                    ('sequence_id', '=', package.ddt_type_id.sequence_id.id)
                ])
                last_ddt = self.search([
                    ('date', '>', package.date),
                    ('ddt_number', '<', package.ddt_number),
                    ('ddt_type_id', 'in', ddt_type_ids.ids),
                    ],
                    order='date desc', limit=1,
                )
                # last_ddt has a date > current ddt
                if last_ddt:
                    # today can be used
                    if fields.Date.today() > last_ddt.date:
                        package.date = fields.Date.today()
                    # last date is in the future, so use it
                    else:
                        package.date = last_ddt.date
        return super(StockPickingPackagePreparation, self).action_put_in_pack()
