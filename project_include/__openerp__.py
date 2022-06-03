# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Sergio Corato - SimplERP SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Project include in other project',
    'version': '8.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Allows to include a project in other project',
    'description':
        'With this module you are able to include a project '
        'in other project',
    'author': 'Sergio Corato - Simplerp srl',
    'website': 'http://www.simplerp.it',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_view.xml'
    ],
    'installable': True,
}
