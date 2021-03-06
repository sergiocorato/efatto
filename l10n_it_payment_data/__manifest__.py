# Copyright 2015-2020 Sergio Corato <https://github.com/sergiocorato>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Italy common payment data',
    'version': '12.0.1.0.2',
    'category': 'other',
    'description': """
    Italy common payment data
    """,
    'author': 'Sergio Corato',
    'website': 'https://efatto.it',
    'license': 'LGPL-3',
    "depends": [
        'account_payment_term_extension',
        'l10n_it_fiscal_payment_term',
    ],
    "data": [
        'data/payment_data.xml',
    ],
    "installable": True,
}
