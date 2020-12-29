# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#    Author Alan David Martínez. Copyright Alan David Martínez -             #
#                       alan.david507@gmail.com                              #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#                                                                            #
##############################################################################


{
    'name': 'Workshop Automobile Registry',
    'version': '1.8',
    'author': "Alan David Martinez",
    'license': "GPL-3",
    'category': 'Custom Modules',
    'description': """Vehicle info, data, images""",
    'website': 'http://vici0uz.wordpress.com/',
    'depends': [
        'base',
        'mail',
        'board',
        'crm',
        'sale',
        'purchase',
        'project',
        'hr',
        'account',
        # 'account_accountant',
        'taller_777',
    ],
    'data': [
        # Security
        'security/workshop_security.xml',
        'security/ir.model.access.csv',
        # Datos
        'static/src/xml/data/job_sequence.xml',
        'static/src/xml/data/workshop_cars.xml',
        'static/src/xml/data/workshop_data.xml',
        'static/src/xml/views/workshop_view.xml',

        # Asistentes
        # Vistas
        'static/src/xml/views/autopart_view.xml',
        'static/src/xml/views/partner_vehicle_view.xml',
        'static/src/xml/views/sale_service.xml',
        'static/src/xml/views/service_additional.xml',
        'static/src/xml/views/workshop_service.xml',
        # Informes
        'report/workshop_vehicle_board_report.xml',
        'report/workshop_service_board_report.xml',
        'report/workshop_insurer_autopart_board.xml',

        # security
        'security/workshop_security.xml',
        'security/ir.model.access.csv',
        # Reportes
        'static/src/xml/data/workshop_autopart_receiving.xml',
        'static/src/xml/data/agreement.xml',
        'static/src/xml/data/report_job_order.xml',
        'static/src/xml/report/autopart_receiving.xml',
        'static/src/xml/report/vehicle_agreement.xml',
        'static/src/xml/report/job_order.xml',
        # Templates
        'static/src/xml/views/workshop_templates.xml',
        # Mods
        # 'static/src/xml/views/product_mod.xml',
        'static/src/xml/views/company_view.xml'
    ],
    'demo': [
        'static/src/xml/data/workshop_demo.xml'
    ],

    'application': True,
    'installable': True,

    'active': False,
}
