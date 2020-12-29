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
    "name": "Workshop Documentacion",
    "version": "3.0",
    "author": "Alan David Martinez",
    "category": 'custom',
    "website": 'http://rikodou.blogspot.com',
    'depends': [
        'workshop'
        ],
    "description": """
        Modulo que mejora el sistema de documentacion para imagenes y adjuntos.
        """,
    "data": [
        'static/src/xml/views/workshop_service_view.xml',
        'static/src/xml/views/workshop_multimages_template.xml',
        'static/src/xml/views/autopart_receiving.xml'
        # 'views/workshop_service_view.xml',
    ],

    'qweb': [
        'static/src/xml/qweb/image_multi.xml'
        ],
    'installable': True,
    'auto_install': False,
}
