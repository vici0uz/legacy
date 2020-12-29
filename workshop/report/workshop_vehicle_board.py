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


from openerp import tools
from openerp.osv import fields, osv


class workshop_vehicle_report(osv.osv):
    _name = 'workshop.vehicle.report'
    _description = "Workshop Vehicle Statistics"
    _auto = False
    _rec_name = 'date_rec'

    _columns = {
        'date_rec': fields.date('Creation Date', readonly=True),
        'date_in': fields.date('Incoming Date', readonly=True),
        'model_id': fields.many2one('workshop.vehicle.model', 'Model', readonly=True),
        'brand_id_rel': fields.char('Brand', readonly=True),
        'has_entered': fields.boolean('Has entered', readonly=True),
        'year': fields.many2one('workshop.vehicle.year', 'Year', readonly=True)
        }
    _order = 'date_rec desc'

    def _select(self):
        select_str = """
            SELECT min(v.id) as id,
                v.model_id as model_id,
                v.date_rec as date_rec,
                v.date_in as date_in,
                v.brand_id_rel as brand_id_rel,
                v.has_entered as has_entered,
                v.year as year
        """
        return select_str

    def _from(self):
        from_str = """
            workshop_vehicle v
                join workshop_vehicle_model vm on (v.model_id = vm.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY v.model_id,
                     v.date_rec,
                     v.date_in,
                     v.brand_id_rel,
                     v.has_entered,
                     v.year
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
