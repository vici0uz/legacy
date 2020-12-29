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


class workshop_operative_costs_report(osv.osv):
    _name = 'workshop.operational.cost.report'
    _description = 'Workshop Service Operational Costs'
    _auto = False

    _columns = {
        'case_total': fields.float('Approved Amount', readonly=True),
        'service_gain_total': fields.Float('Total Gain', readonly=True)
    }

    def _select(self):
        select_str= """
            SELECT miv(s.id) as id,
                v.case_total as case_total,
                v.service_gain_total as service_gain_total
        """
        return select_str

    def _from(self):
        from_str = """
            workshop_service s
        """
        return from_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from()))
