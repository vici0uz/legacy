# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#    Copyright (C) 2013  Alan David Martínez - alan.david507@gmail.com        #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU Affero General Public License as           #
#    published by the Free Software Foundation, either version 3 of the       #
#    License, or (at your option) any later version.                          #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU Affero General Public License for more details.                      #
#                                                                             #
#    You should have received a copy of the GNU Affero General Public License #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
###############################################################################

{
    'name': 'Taller 777 Customization',
    'version': '1.0',
    'license': "GPL-3",
    'author': 'Alan David Martinez',
    'description': """Adds Custom Invoices, Chart Accounts and Relations""",
    'website': 'http://rikodou.blogspot.com',
    'category': 'Technical Settings',
    'depends': [
        'product',
        'account',
        'sale',
        'l10n_py_alan',
        'product'
        ],
    'data': [
        'static/src/xml/invoice_taller_777_mod.xml',
        'static/src/xml/views/partner.xml',
        'views/product_mod.xml',
        # 'views/partner.xml',
        # Templates
        'static/src/xml/templates/taller_777_templates.xml'
        ],
    'installable': True,
    'active': False,
}
