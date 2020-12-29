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


from openerp.osv import osv, fields
from openerp.osv import orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class sale_order_lines(osv.osv):
    _inherit = 'sale.order.line'

    def _calcule_amount_final(self, cr, uid, ids, prop, unknow_none, context={}):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id]= (line.price_unit * line.product_uom_qty)
        return res
    def _calcule_discount(self, cr, uid, ids, prop, unknow_none, context={}):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id]= (line.discount_amount*100) / line.amount_final
        return res

    _columns = {
        'discount_amount': fields.float('Discount Amount', size=64, readonly=True, states={'draft': [('readonly', False)]}),
        'amount_final': fields.function(_calcule_amount_final, string='Monto Final', type="float", readonly=True, states={'draft': [('readonly', False)]}),
    }

    def generate_discount(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool.get('sale.order.line')
        for sale_order_line in self.browse(cr, uid, ids, context=context):
            qty = sale_order_line.product_uom_qty
            pu = sale_order_line.price_unit
            damo = sale_order_line.discount_amount
            disc = sale_order_line.discount
            af = sale_order_line.amount_final
            if damo != 0.00:
                disc = (damo * 100) / (pu * qty)
                res = 0
        return True

    # def onchange_discount(self, cr, uid, ids, amount_final, context={}):
    #     res={}
    #     for record in self.browse(cr, uid, ids):
    #         res ={
    #             'amount_final': (record.price_unit * record.product_uom_qty),
    #             'discount': ((record.discount_amount * 100)/ record.amount_final),
    #             }
    #     return {'value':res}

    # def onchange_discount_amount(self, cr, uid, ids, discount, amount_final, context={}):
    #     res = {}
    #     for record in self.browse(cr, uid, ids):
    #         res ={
    #
    #         }
    #     return {'value':res}
    #
