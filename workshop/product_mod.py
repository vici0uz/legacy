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
from openerp.osv.orm import Model


class Product_Template(Model):
    """Product Template Mod"""

    _inherit = "product.template"

    _columns = {
        'autopart_type': fields.many2one('workshop.autopart.type', 'Autopart Type'),
        'model_id': fields.many2one('workshop.vehicle.model', 'Model'),
        'template_type': fields.selection([('autopart', 'Autopart'), ('paint', 'Paint')], string="Type"),
    }
    _defaults = {
        'company_id': None,
    }


class Product_Category(osv.osv):
    _inherit = "product.category"
    _order = "complete_name asc"

    _columns = {
        'autopart_type': fields.many2one('workshop.autopart.type', 'Autopart Type'),
        'brand_id': fields.many2one('workshop.vehicle.model.brand'),
        'model_id': fields.many2one('workshop.vehicle.model'),
    }
