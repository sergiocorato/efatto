# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = ['sale.order', "product.configurator"]
    _name = "sale.order"

    product_template_id = fields.Many2one('product.template')
    product_template_image = fields.Binary(
        related='product_template_id.image_medium')
    product_attribute_line_id = fields.Many2one(
        'product.attribute.line',
        domain="[('product_tmpl_id','=',product_template_id)]"
        )
    product_attribute_child_ids = fields.One2many(
        string='Childs',
        related='product_attribute_line_id.attribute_id.child_ids',
        readonly=True)
    product_attribute_child_id = fields.Many2one(
        'product.attribute',
        domain="[('id', 'in', product_attribute_child_ids[0][2])]"
    )
    product_attribute_value_ids = fields.Many2many(
        string='Values',
        related='product_attribute_line_id.value_ids',
        readonly=True)
    product_attribute_value_id = fields.Many2one(
        'product.attribute.value',
        domain="[('id', 'in', product_attribute_value_ids[0][2])]"
    )
    product_attribute_image = fields.Binary(
        related='product_attribute_value_id.image')
    price_unit = fields.Float(string='Price unit',
                              digits_compute=dp.get_precision('Product Price'))
    product = fields.Char()

    scan_template = fields.Char('Scan Template')
    scan_material = fields.Char('Scan Material')
    scan_color = fields.Char('Scan Material Color')
    scan_stitching = fields.Char('Scan Stitching')
    scan_stitching_color = fields.Char('Scan Stitching Color')

    @api.onchange('scan_template')
    def _scan_template(self):
        if self.scan_template:
            product_template = self.env['product.template'].search(
                [('prefix_code', '=', self.scan_template)])
            if product_template:
                self.product_template_id = product_template
            self.scan_template = ''

    @api.onchange('scan_material')
    def _scan_material(self):
        if self.scan_material:
            # first search if material has parent
            attribute = self.env['product.attribute'].search(
                [('code', '=', self.scan_material)])
            # product_attribute_child = product_attribute_line = False
            if attribute and attribute.parent_id:
                # it's a child attribute: set in one passage the attribute line
                # from parent of attribute, and the product_attribute_child_id
                for attribute_line in self.product_template_id.\
                        attribute_line_ids:
                    product_attribute_child = \
                        attribute_line.attribute_id.child_ids.filtered(
                            lambda x: x.code == self.scan_material)
                    if product_attribute_child:
                        self.product_attribute_child_id = \
                            product_attribute_child
                        self.product_attribute_line_id = self.\
                            product_template_id.attribute_line_ids.filtered(
                                lambda x: x.attribute_id ==
                                          product_attribute_child.parent_id)
                        break
            elif attribute and not attribute.parent_id:
                product_attribute_line = self.product_template_id.\
                    attribute_line_ids.filtered(
                    lambda x: x.attribute_id.code == self.scan_material)
                if product_attribute_line:
                    self.product_attribute_line_id = product_attribute_line
        self.scan_material = ''

    @api.onchange('scan_color')
    def _scan_color(self):
        if self.scan_color:
            if self.product_attribute_child_id:
                product_attribute_value = self.product_attribute_child_id. \
                    value_ids.filtered(lambda x: x.code == self.scan_color)
            else:
                product_attribute_value = self.product_attribute_line_id.\
                    value_ids.filtered(lambda x: x.code == self.scan_color)
            if product_attribute_value:
                self.product_attribute_value_id = product_attribute_value
                #todo put in product char field the code of variant not existing too
                product = self.env['product.product'].search([
                    ('product_tmpl_id', '=', self.product_template_id.id),
                    ('attribute_value_ids', '=',
                     self.product_attribute_value_id.id)
                ])
                if len(product) == 1:
                    self.product = product.default_code
            else:
                self.product_attribute_value_id = False
                self.product = False
        self.scan_color = ''

    # #TODO scan stitching
    # @api.onchange('scan_stitching')
    # def _scan_material(self):
    #     if self.scan_material:
    #         product_attribute_line = self.product_template_id.\
    #             attribute_line_ids.filtered(lambda x: x.attribute_id.code ==
    #                                                   self.scan_material)
    #         if product_attribute_line:
    #             self.product_attribute_line_id = product_attribute_line
    #         else:
    #             self.product_attribute_line_id = False
    #     self.scan_material = ''
    #
    # #TODO scan stitching color
    # @api.onchange('scan_stitching_color')
    # def _scan_color(self):
    #     if self.scan_color:
    #         product_attribute_value = self.product_attribute_line_id.\
    #             value_ids.filtered(lambda x: x.code == self.scan_color)
    #         if product_attribute_value:
    #             self.product_attribute_value_id = product_attribute_value
    #             #todo put in product char field the code of variant not existing too
    #             product = self.env['product.product'].search([
    #                 ('product_tmpl_id', '=', self.product_template_id.id),
    #                 ('attribute_value_ids', '=',
    #                  self.product_attribute_value_id.id)
    #             ])
    #             if len(product) == 1:
    #                 self.product = product.default_code
    #         else:
    #             self.product_attribute_value_id = False
    #             self.product = False
    #     self.scan_color = ''

    @api.onchange('product_template_id')
    def onchange_product(self):
        self.product_attribute_line_id = self.product_attribute_child_id = \
            self.product_attribute_value_id = self.product = False

    @api.onchange('product_attribute_line_id')
    def onchange_product_attribute(self):
        self.product_attribute_value_id = self.product = False

    @api.onchange('product_attribute_value_id')
    def onchange_product_attribute_value(self):
        for order in self:
            product = self.env['product.product'].search([
                ('product_tmpl_id','=', order.product_template_id.id),
                ('attribute_value_ids','=', order.product_attribute_value_id.id)
            ])
            if len(product) == 1:
                order.product = product.default_code
            else:
                order.product = False

    @api.multi
    @api.onchange('product_attribute_value_id')
    @api.depends('product_template_id')
    def onchange_price_unit(self):
        self.ensure_one()
        if self.product_template_id:
            price_extra = 0.0
            attribute_id = False
            for attr_line in self.product_attribute_line_id:
                price_extra += attr_line.price_extra
                # if attr_line.value_id:
                #     attribute_id = attr_line.attribute_id
            for attribute_line in self.product_attribute_value_id:
                # if attribute_line.attribute_id == attribute_id:
                price_extra += attribute_line.price_extra
            self.price_unit = self.pricelist_id.with_context({
                'uom': self.product_template_id.uom_id.id,
                'date': self.date_order,
                'price_extra': price_extra,
            }).template_price_get(
                self.product_template_id.id, 1.0,
                self.partner_id.id)[self.pricelist_id.id]

    @api.multi
    def add_product_in_order(self):
        for order in self:
            order.scan = order.product
