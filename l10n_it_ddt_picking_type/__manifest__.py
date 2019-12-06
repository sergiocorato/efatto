# -*- coding: utf-8 -*-
#    Copyright (C) 2017-2019 Sergio Corato
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
{
    'name': 'Add pycking type to DDT',
    'version': '10.0.1.0.1',
    'category': 'other',
    'author': 'Sergio Corato',
    'website': 'https://efatto.it',
    'license': 'AGPL-3',
    'description': '''This module add possibility to add picking type
    to ddt type, so ddt can be created directly using
    a different route.''',
    'depends': [
        'l10n_it_ddt',
    ],
    'data': [
        'data/stock_picking_type.xml',
        'views/stock.xml',
    ],
    'installable': True,
}