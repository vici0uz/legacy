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

from openerp import http
from openerp.http import request


class website_workshop(http.Controller):

    @http.route(['/insurers'], type='http', auth="public", website=True)
    def insurers(self, **post):
        res_partner_obj = request.registry['res.partner']
        partner_ids = res_partner_obj.search(request.cr, request.uid, [('website_published', '=', True)],
                                           context=request.context)
        values = {
            'partner_ids': res_partner_obj.browse(request.cr, request.uid, partner_ids, request.context)
        }
        return request.website.render("website_workshop.index", values)
