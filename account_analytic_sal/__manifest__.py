# Copyright 2019-2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account analytic SAL',
    'version': '12.0.1.0.1',
    'category': 'Sale Management',
    'description':
        'Account analytic SAL',
    'author': 'Sergio Corato',
    'website': 'https://github.com/sergiocorato/efatto',
    'license': 'AGPL-3',
    'depends': [
        'contract',
        'analytic_show_sale',
        'hr_timesheet',
        'sale_delivered_percent',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sal_data.xml',
        'views/account.xml',
    ],
    'installable': True,
}
