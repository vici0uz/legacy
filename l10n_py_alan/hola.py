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
from clint.textui import colored


class zarpado_crap(osv.osv):
    _inherit = "account.invoice"

    def mierda(self, cr, uid, ids, context=None):
        account_config_settings = self.pool.get('account.config.settings')
        print colored.cyan(account_config_settings)
        def_tax = account_config_settings.browse(cr, uid).default_purchase_tax
        print colored.magenta(def_tax)
