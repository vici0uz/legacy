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

from openerp.osv import orm, fields


class ResCompany(orm.Model):
    """Add autopart's stock root"""
    _inherit = "res.company"
    _columns = {
        'autopart_stock_root': fields.many2one('product.category', 'Category')
    }

    def get_root_tree(self, cr, uid, id=None, context=None):
        if isinstance(id, (tuple, list)):
            assert len(id) == 1, "One ID  expected"
            id = id[0]
        if id:
            return self.browse(cr, uid, id, context=context).autopart_stock_root
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return user.insurer_id.autopart_stock_root
