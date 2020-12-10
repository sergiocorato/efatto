# Copyright 2015 Angel Moya <angel.moya@domatix.com>
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Analytic Show Invoice',
    'summary': 'Button in analityc to show their invoices',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Domatix,'
              'Tecnativa,'
              'Sergio Corato,'
              'Odoo Community Association (OCA)',
    'website': 'https://efatto.it',
    'depends': ['account', 'analytic'],
    'category': 'Sales Management',
    'data': [
        'views/analytic_view.xml',
    ],
    'installable': True,
}
