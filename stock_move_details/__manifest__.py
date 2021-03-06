# Copyright 2017-2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock move details in tree',
    'version': '12.0.1.0.0',
    'category': 'other',
    'description': """
    Stock product available quantity in move tree
    """,
    'author': 'Sergio Corato',
    'website': 'https://www.efatto.it',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock.xml',
    ],
    'installable': True,
}
