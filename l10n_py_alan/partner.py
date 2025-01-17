# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#    Copyright (C) 2013  Alan David Martínez - alan.david507@gmail.com        #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU Affero General Public License as           #
#    published by the Free Software Foundation, either version 3 of the       #
#    License, or (at your option) any later version.                          #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU Affero General Public License for more details.                      #
#                                                                             #
#    You should have received a copy of the GNU Affero General Public License #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
###############################################################################


from openerp.osv import fields, osv


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def check_cid(cr, uid, ids, context=None):
        print "hola"

    _columns = {
        'cid': fields.char('Certificate Number', size=32, translate=True),
    }

    _sql_constraints = [
        ('cid', 'unique(cid)', 'The Certification Number of the partner must be unique')
        ]

res_partner()
