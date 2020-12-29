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


from openerp import fields, models, api
from clint.textui import colored


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # @api.one
    # @api.depends('dimension', 'product_uos_qty')
    # def calculate(self):

    #     if self.dimension:
    #         dimensions = eval(self.dimension)
    #         self.detail = self.product_uos_qty / (dimensions)

    qty_per_unit = fields.Float(string='Qty', default=0)
    length = fields.Char(string="Length")

