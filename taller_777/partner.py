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
from openerp.tools.translate import _
from clint.textui import colored


class res_partner(osv.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'insurer': fields.boolean('Insurance Company Check'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        for partner in self.browse(cr, uid, ids, context):
            changes = []
            if 'name' in vals and partner.name != vals['name']:
                old_name = partner.name or _('None')
                changes.append(_("Partner name from: '%s' to '%s'")%(old_name, vals['name']))
            if 'vat' in vals and partner.vat != vals['vat']:
                old_vat = partner.vat or _('None')
                changes.append(_("Vat from: '%s' to '%s'")%(old_vat, vals['vat']))
            if 'cid' in vals and partner.cid != vals['cid']:
                old_cid = partner.cid or _('None')
                changes.append(_("Certificate Number from: '%s' to '%s'")%(old_cid, vals['cid']))
            if 'phone' in vals and partner.phone != vals['phone']:
                old_phone = partner.phone or _('None')
                changes.append(_("Phone Number from: '%s' to '%s'")%(old_phone, vals['phone']))
            if 'mobile' in vals and partner.mobile != vals['mobile']:
                old_mobile = partner.mobile or _('None')
                changes.append(_("Mobile from: '%s' to '%s'")%(old_mobile, vals['mobile']))
            if len(changes) > 0:
                self.message_post(cr, uid, [partner.id], body=", ".join(changes), context=context)
        return super(res_partner, self).write(cr, uid, ids, vals, context)

res_partner()
