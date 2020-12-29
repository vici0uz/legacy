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

from openerp.osv import fields, osv


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _vehicle_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))

        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(partner.vehicle)
        except:
            pass
        return res

    def _work_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))

        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(partner.service)
        except:
            pass
        return res

    def copy(self, cr, uid, record_id, default=None, context=None):
        if default is None:
            default = {}

        default.update({'vehicle': []}, {'service': []})

        return super(res_partner, self).copy(cr, uid, record_id, default, context)

    _columns = {
        'vehicle_count': fields.function(_vehicle_order_count, string='# of Vehicles', type='integer'),
        'work_count': fields.function(_work_order_count, string='# of Services', type='integer'),
        'vehicle': fields.one2many('workshop.vehicle', 'partner_id', 'Vehicles'),
        'service': fields.one2many('workshop.service', 'insurer_id', 'Services'),
    }
