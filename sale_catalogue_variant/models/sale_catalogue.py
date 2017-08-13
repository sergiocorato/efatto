# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
import re


class SaleCatalogue(models.Model):
    _name = "sale.catalogue"

    def _get_partner_default(self):
        res = False
        if self._context['params'].get('action', False):
            if self._context['params'].get('action') == \
                    self.env['ir.model.data'].get_object_reference(
                        'sale_catalogue_variant',
                        'action_sale_catalogue_variant_form')[1]:
                res = self.env.user.company_id.\
                    sale_mobile_catalogue_partner_default
        return res

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        default=_get_partner_default)
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        related='partner_id.property_product_pricelist',
    )
    product_template_id = fields.Many2one('product.template')
    product_template_name = fields.Char(
        related='product_template_id.name')
    product_template_name_bis = fields.Char(
        related='product_template_id.name')
    product_template_image = fields.Binary(
        related='product_template_id.image_medium')
    product_template_image_bis = fields.Binary(
        related='product_template_id.image_medium')
    product_attribute_line_id = fields.Many2one(
        'product.attribute.line',
        domain="[('product_tmpl_id','=',product_template_id)]",)
    product_attribute_name = fields.Char(
        related='product_attribute_value_id.attribute_id.name')
    product_attribute_value_name = fields.Char(
        related='product_attribute_value_id.name')
    product_attribute_name_bis = fields.Char(
        related='product_attribute_value_id.attribute_id.name')
    product_attribute_value_name_bis = fields.Char(
        related='product_attribute_value_id.name')
    product_attribute_name1 = fields.Char(
        related='product_attribute_value1_id.attribute_id.name')
    product_attribute_value_name1 = fields.Char(
        related='product_attribute_value1_id.name')
    product_attribute_line1_id = fields.Many2one(
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
    product_attribute_value1_ids = fields.Many2many(
        string='Values',
        related='product_attribute_line1_id.value_ids',
        readonly=True)
    product_attribute_value1_id = fields.Many2one(
        'product.attribute.value',
        domain="[('id', 'in', product_attribute_value1_ids[0][2])]"
    )
    product_attribute_image = fields.Binary(
        related='product_attribute_value_id.image')
    product_attribute_image_bis = fields.Binary(
        related='product_attribute_value_id.image')
    product_attribute_image1 = fields.Binary(
        related='product_attribute_value1_id.image')
    price_unit = fields.Float(string='Price unit',
                              digits_compute=dp.get_precision('Product Price'))
    product = fields.Char()
    scan = fields.Char('Scan QR Code')
    discount = fields.Float()
    net_price = fields.Float()
    is_combination = fields.Boolean(
        related='product_template_id.is_combination'
    )

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.discount = self.partner_id.default_sale_discount

    @api.onchange('product_template_id')
    def onchange_product_template(self):
        if self.product_template_id:
            self.product_attribute_line_id = self.product_template_id.\
                attribute_line_ids.filtered(
                    lambda x: x.attribute_id.name == 'CAT. A'
                )

    @api.onchange('product_attribute_line_id')
    def onchange_product_attribute_line(self):
        #if manually changed, get price (and remove material color and name?)
        if self.product_template_id:
            self.price_unit = self._get_price_unit()

    @api.onchange('discount', 'price_unit')
    def onchange_discount(self):
        if self.discount:
            self.net_price = round(
                self.price_unit * (100.0 - self.discount) / 100.0 + 0.5, 0)

    @api.onchange('scan')
    def _scan(self):
        if self.scan:
            # FIRST check if it is a product template (x letter-number)
            product_template = self.env['product.template'].search(
                [('prefix_code', '=', self.scan.upper())])
            if product_template:
                self._set_product_template(product_template)
                return
            # TWO check if it is a material-color (1 letter 2 number)
            if re.match('[A-Z][0-9][0-9]', self.scan.upper()):
                material = self.scan[0].upper()
                color = self.scan[1:3]
                self._set_material_color(material, color)
                return

            # FOUR1 check simple material (& + 1 letter + [1 letter + 2 number] + '+' + [1 letter + 2 number])
            if re.match('[&][A-Z][A-Z][0-9]{2}[+][A-Z][0-9]{2}', self.scan.upper()):
                material = self.scan[:2].upper()
                color = self.scan[2:].upper()
                self._set_material_color(material, color)
                return

            # FOUR check simple material (2 number + 1 or 2 letter + 2 number)
            if re.match('[0-9]{2}[A-Z]{1,2}[0-9]{2}', self.scan.upper()):
                material = self.scan[:2].upper()
                color = self.scan[2:].upper()
                self._set_material_color(material, color)
                return

            # NO MATCHES FOUND: clean all fields
            self.product_attribute_line_id = \
                self.product_attribute_line1_id = \
                self.product_attribute_child_id = \
                self.product_attribute_value_id = \
                self.product_attribute_value1_id = \
                self.product_template_id = False

    @api.multi
    def _set_product_template(self, product_template):
        self.product_template_id = product_template
        self.product = product_template.prefix_code
        self.price_unit = 0.0
        self.scan = ''
        # clean all children fields
        self.product_attribute_line_id = \
            self.product_attribute_line1_id = \
            self.product_attribute_child_id = \
            self.product_attribute_value_id = \
            self.product_attribute_value1_id = \
            False

    @api.multi
    def _set_material_color(self, material, color):
        attribute = self.env['product.attribute'].search(
            [('code', '=', material)])
        # first search if material has parent
        if attribute and attribute.parent_id and not self.is_combination:
            # it's a child attribute: set in one passage the attribute line
            # from parent of attribute, and the product_attribute_child_id
            for attribute_line in self.product_template_id. \
                    attribute_line_ids:
                product_attribute_child = \
                    attribute_line.attribute_id.child_ids.filtered(
                        lambda x: x.code == material)
                if product_attribute_child:
                    self.product_attribute_child_id = \
                        product_attribute_child
                    self.product_attribute_line_id = self. \
                        product_template_id.attribute_line_ids.filtered(
                        lambda x: x.attribute_id ==
                                  product_attribute_child.parent_id)
                    self.product = self.product_template_id.prefix_code + \
                                   product_attribute_child.code
                    self._get_color(color, self.product_attribute_line_id)
                    self.scan = ''
                    return
        if attribute and attribute.parent_id and self.is_combination:
            if self.product_attribute_line_id:
                # is already chosen first material, so add the second
                product_attribute_line1 = self.product_template_id. \
                    attribute_line_ids.filtered(
                    lambda x: x.attribute_id.code == material)
                if not self.product_attribute_value_id:
                    self.product = self.scan = ''
                if product_attribute_line1:
                    self.product_attribute_line1_id = product_attribute_line1
                    self._get_color(color, self.product_attribute_line1_id)
                    self.scan = ''
                    return
        if attribute and not attribute.parent_id or attribute and self.is_combination:
            # is the first material, work as usual
            product_attribute_line = self.product_template_id. \
                attribute_line_ids.filtered(
                    lambda x: x.attribute_id.code == material)
            if product_attribute_line:
                self.product_attribute_line_id = product_attribute_line
                self._get_color(color, self.product_attribute_line_id)
                self.scan = ''
                return

    def _get_color(self, color, product_attribute_line_id):
        if self.product_attribute_child_id:
            product_attribute_value = self.product_attribute_child_id. \
                value_ids.filtered(lambda x: x.code == color)
        else:
            product_attribute_value = product_attribute_line_id.\
                value_ids.filtered(lambda x: x.code == color)
        if product_attribute_value:
            if self.product_attribute_value_id:
                self.product_attribute_value1_id = product_attribute_value
            else:
                self.product_attribute_value_id = product_attribute_value
            product = False
            # we can search here for product only if not with child variant
            if not self.product_attribute_child_id.parent_id and not self.is_combination:
                product = self.env['product.product'].search([
                    ('product_tmpl_id', '=', self.product_template_id.id),
                    ('attribute_value_ids', '=',
                     self.product_attribute_value_id.id)
                ])
            if product:
                self.product = product.default_code
            else:
                if self.product_attribute_child_id:
                    self.product = self.product_template_id.prefix_code + \
                        self.product_attribute_child_id.code + \
                        product_attribute_value.code
                else:
                    if self.product_attribute_line1_id:
                        self.product = self.product_template_id.prefix_code + \
                            self.product_attribute_line_id.attribute_id.code +\
                            self.product_attribute_value_id.code + \
                            self.product_attribute_line1_id.attribute_id.code+\
                            product_attribute_value.code
                    else:
                        self.product = self.product_template_id.prefix_code + \
                            self.product_attribute_line_id.attribute_id.code + \
                            product_attribute_value.code
            self.price_unit = self._get_price_unit()
        else:
            self.product_attribute_value_id = False

    @api.multi
    def _get_price_unit(self):
        self.ensure_one()
        if self.product_template_id:
            price_extra = 0.0
            attribute_id = False
            for attr_line in self.product_attribute_line_id:
                price_extra += attr_line.price_extra
                # if attr_line.value_id:
                #     attribute_id = attr_line.attribute_id
            for attr_line1 in self.product_attribute_line1_id:
                price_extra += attr_line1.price_extra
            for attribute_line in self.product_attribute_value_id:
                # if attribute_line.attribute_id == attribute_id:
                price_extra += attribute_line.price_extra
            return self.pricelist_id.with_context({
                'uom': self.product_template_id.uom_id.id,
                'date': fields.Date.today(),
                'price_extra': price_extra,
            }).template_price_get(
                self.product_template_id.id, 1.0,
                self.partner_id.id)[self.pricelist_id.id]
