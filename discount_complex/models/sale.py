# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    complex_discount = fields.Char(
        'Complex Discount', size=32,
        help='E.g.: 15.5+5, or 50+10+3.5')

    @api.onchange('complex_discount', 'discount')
    def onchange_sconti(self):
        res = {}
        net = 0.0
        if self.complex_discount:
            complex_discount = self.complex_discount.replace(
                '%', '').replace(',', '.').replace('-', '+').replace(' ', '+')
            for disc in complex_discount.split('+'):
                try:
                    net = 100 - ((100.00 - net) * (100.00 - float(disc)) / 100)
                except:
                    UserError(_('Bad discount format'))
        else:
            net = self.discount
        res['discount'] = net
        return {'value': res}
