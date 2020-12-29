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
    'name': 'Localization Module for Paraguay',
    'version': '1.9',
    'author': 'Alan David Martinez',
    'license': "GPL-3",
    'category': 'Localization',
    'description': """
Paraguayan accounting chart and tax localization.
==================================================
    """,
    'depends': [
        'account_chart',
        'hr'
        ],
    'data': [
        'static/src/xml/views/hr_view.xml',
        'static/src/xml/views/partner_py.xml',
        'static/src/xml/views/company_py.xml',
        'static/src/xml/views/invoice_mod.xml',
        'data/account_tax_code.xml',
        'data/l10n_py_chart.xml',
        'data/account_tax.xml',
        'data/l10n_py_wizard.xml'
        ],
    'application': False,
    'installable': True,
    'active': False,
    'images': [
        'images/config_chart_l10n_py.jpeg',
        'images/l10n_py_chart.jpeg'
        ],
}
