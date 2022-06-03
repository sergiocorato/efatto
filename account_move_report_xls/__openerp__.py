# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2016 Sergio Corato - SimplERP srl (<http://www.simplerp.it>)
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
    'name': 'Account move report xls',
    'version': '8.0.0.1.0',
    'category': 'other',
    'author': 'Sergio Corato - SimplERP SRL',
    'description': 'Account move report xls',
    'website': 'http://www.simplerp.it',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'report_xls',
    ],
    'data': [
        'views/move_list_xls_view.xml',
    ],
    'installable': True
}
