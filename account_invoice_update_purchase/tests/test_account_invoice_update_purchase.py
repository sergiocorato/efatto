from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger
from odoo import fields
from odoo.tools.date_utils import relativedelta


class AccountInvoiceUpdatePurchase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.user_model = cls.env['res.users'].with_context(no_reset_password=True)
        cls.partner = cls.env.ref('base.res_partner_2')
        buy = cls.env.ref('purchase_stock.route_warehouse0_buy')
        cls.vendor = cls.env.ref('base.res_partner_3')
        cls.supplierinfo_expired = cls.env['product.supplierinfo'].create({
            'name': cls.vendor.id,
            'price': 77,
            'date_end': fields.Date.today() + relativedelta(days=-10),
        })
        cls.supplierinfo = cls.env['product.supplierinfo'].create({
            'name': cls.vendor.id,
            'price': 88,
            'date_start': fields.Date.today() + relativedelta(days=-9),
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product Test',
            'type': 'product',
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'lst_price': 77,
            'seller_ids': [(6, 0, [cls.supplierinfo_expired.id, cls.supplierinfo.id])],
            'route_ids': [(6, 0, [buy.id])],
        })
        cls.test_user = cls.env['res.users'].create({
            'name': 'John',
            'login': 'test',
        })
        cls.uom_hundred = cls.env['uom.uom'].create({
            'name': 'Hundred',
            'category_id': cls.env.ref('uom.product_uom_categ_unit').id,
            'factor_inv': 100,
            'uom_type': 'bigger',
            'rounding': 0.01,
        })

    def _create_purchase_order_line(self, order, product, qty, date_planned=False):
        vals = {
            'order_id': order.id,
            'product_id': product.id,
            'product_qty': qty,
            'product_uom': product.uom_po_id.id,
            'price_unit': product.list_price,
            'name': product.name,
        }
        if date_planned:
            vals.update({
                'date_planned': date_planned
            })
        line = self.env['purchase.order.line'].create(vals)
        line._onchange_quantity()
        line._convert_to_write(line._cache)
        return line

    @staticmethod
    def _action_pack_operation_auto_fill(picking):
        for op in picking.mapped('move_line_ids'):
            if op.product_id.type == 'product':
                op.qty_done = op.move_id.product_uom_qty

    @mute_logger(
        'odoo.models', 'odoo.models.unlink', 'odoo.addons.base.ir.ir_model'
    )
    def test_01_invoice_update_purchase_with_standard_cost_method(self):
        self.assertEqual(self.product.categ_id.property_cost_method, 'standard')
        purchase_order1 = self.env['purchase.order'].create({
            'partner_id': self.vendor.id,
        })
        purchase_planned_date1 = fields.Datetime.now() + relativedelta(days=5)
        purchase_line = self._create_purchase_order_line(
            purchase_order1, self.product, 18, purchase_planned_date1)
        purchase_order1.button_confirm()
        current_price = purchase_line.price_unit

        self.assertEqual(purchase_line.product_uom_qty, 18)
        self.assertEqual(purchase_order1.state, 'purchase')

        picking = purchase_order1.picking_ids[0]
        self._action_pack_operation_auto_fill(picking)
        picking.button_validate()
        self.assertEqual(picking.state, 'done')

        wizard = self.env["purchase.batch_invoicing"].with_context(
            active_ids=purchase_order1.ids).create(dict())
        res = wizard.action_batch_invoice()
        invoice = self.env['account.invoice'].search(res.get('domain'))
        self.assertTrue(invoice)
        invoice_line = invoice.invoice_line_ids
        self.assertEqual(invoice_line.product_id, self.product)

        self.assertEqual(purchase_line.price_unit, current_price)
        self.assertEqual(self.supplierinfo.price, current_price)
        self.assertEqual(picking.move_lines[0].price_unit, self.product.standard_price)
        self.assertEqual(self.product.standard_price, self.product.standard_price)

        new_price = invoice_line.price_unit + 66
        invoice_line.price_unit = new_price
        invoice_line.update_purchase()
        self.assertEqual(purchase_line.price_unit, new_price)
        self.assertEqual(self.supplierinfo.price, new_price)
        self.assertEqual(picking.move_lines[0].price_unit, new_price)
        self.assertEqual(self.product.standard_price, self.product.standard_price)

        # change uom of invoice and test re-computation
        invoice_line.uom_id = self.uom_hundred
        invoice_line.update_purchase()
        self.assertAlmostEqual(purchase_line.price_unit, new_price/100)
