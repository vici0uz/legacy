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
from openerp.osv import osv, fields


class workshop_autopart_insurer(osv.osv):
    _name = 'workshop.autopart.insurer'
    _description = 'Autopart Receiving Statistics'
    _auto = False
    _rec_name = 'date_order'

    _columns = {
        'date_order': fields.datetime('Date Order', readonly=True),
        'autopart_type_id': fields.many2one('workshop.autopart.type', 'Autopart type', readonly=True),
        'autopart_qty': fields.float('# of Qty', readonly=True)
    }

    _order = 'date_order desc'

    def _select(self):
        select_str = """
            SELECT min(l.id) as id,
                l.autopart_type_id as autopart_type_id,
                l.qty as autopart_qty,
                r.date_order as date_order
        """
        return select_str

    def _from(self):
        from_str = """
            workshop_autopart_receiving_lot l
                join workshop_autopart_receiving r on (l.workshop_autopart_receiving_id=r.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.autopart_type_id,
                    l.qty,
                    r.date_order
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))
