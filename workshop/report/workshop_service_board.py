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


class workshop_service(osv.osv):
    _name = 'workshop.service.report'
    _description = "Workshop Service Statistics"
    _auto = False
    _rec_name = ''

    _columns = {
        'insurer_id': fields.many2one('res.partner', readonly=True),
        'date_approved': fields.date('Approved Date', readonly=True),
        'date_ending': fields.date('Ending Date', readonly=True),
        't_insurance': fields.boolean('Insured', readonly=True)
    }

    def _select(self):
        select_str = """
            SELECT min(s.id) as id,
                s.insurer_id as insurer_id,
                s.date_approved as date_approved,
                s.date_ending as date_ending,
                s.t_insurance as t_insurance
        """
        return select_str

    def _from(self):
        from_str = """
            workshop_service s
                join res_partner rp on (s.insurer_id = rp.id)

        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY s.insurer_id,
                     s.date_approved,
                     s.date_ending,
                     s.t_insurance
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as(
            %s
            FROM ( %s )
            %s)""" % (self._table, self._select(), self._from(), self._group_by()))
