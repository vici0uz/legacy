# -*- encoding: utf-8 -*-
##############################################################################
#
#    Aquasys G.K.
#    Copyright (C) 2013-2014
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
    'name': 'Disable decimal points',
    'version': '1.0',
    'category': 'General',
    'description': """
This module is used for Wonder AOI to remove decimal points.
==================================
""",
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "www.acespritech.com",
    'depends': ['base', 'web', 'decimal_precision'],
    "data": [
        'static/src/xml/templates/disable_decimal.xml',
        'base/res_lang_view.xml',
        ],

    # 'data': [],
    # 'js': ['static/src/js/disable_decimal.js'],
    'installable': True,
    'auto_install': False,
}
