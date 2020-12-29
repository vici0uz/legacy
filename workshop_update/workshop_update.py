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

from openerp import fields, models, api, _
import openerp.addons.decimal_precision as dp
from clint.textui import colored


class workshop_service(models.Model):
    _inherit = 'workshop.service'

    @api.one
    @api.depends('state')
    def approved(self):
        print colored.red("Fue llamado papu")
    # supply_line2 = fields.One2many(comodel_name='workshop.service.supply2', inverse_name='service_id', string="Operational Costs")

    # @api.multi
    # def write(self, values):
    #     print colored.red(values)
    #     if 't_insurance' in values:
    #         print colored.blue("Solo en este caso se ejecuta")
    #         if values['t_insurance'] is False:
    #             values.update({'n_incident': None, 'insurer_id': None})

    #     return super(workshop_service, self).write(values)


class workshop_service_supply2(models.Model):
    _name = 'workshop.service.supply2'

    @api.one
    def get_author(self):
        self.author = self.create_uid.name

    @api.one
    def get_price(self):
        self.get_price = self.product_id.product_tmpl_id.standard_price

    service_id = fields.Many2one(comodel_name='workshop.service')
    product_id = fields.Many2one(comodel_name='product.product')
    author = fields.Char(compute='get_author', store=True)
    qty = fields.Float(string='Quantity')
    cost_price = fields.Float(string='Cost Price', compute='get_price', digits=dp.get_precision('Product Price'))
    subtotal_gain = fields.Float(string='Subtotal Gain', compute='_compute_gain', digits=dp.get_precision('Product Price'))