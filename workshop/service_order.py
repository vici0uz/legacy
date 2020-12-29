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


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc


class sale_order(osv.osv):
    _name= "sale.order"
    _inherit= "sale.order"

    def on_change_service(self, cr, uid, ids, service_id, context=None):
        if not service_id:
            return {}
        service = self.pool.get('workshop.service').browse(cr, uid, service_id, context=context)
        return {
            'value': {
                'images': service.multi_images,
            }
        }

    _columns = {
        'service': fields.many2one('workshop.service', 'Service', readonly=True, states={'draft': [('readonly', False)]}),
        'images': fields.related('service', 'multi_images',type="text", string="Images to Budget", readonly=True),
        # 'vehicles': fields.related('service', 'vehicle_ids', relation="workshop.service", type="many2many", string="Vehicles", readonly=True),
        # 'autoparts': fields.related('service', 'autopart_ids', relation="workshop.service", type="many2many", string="Autoparts", readonly=True),
    }

sale_order()
