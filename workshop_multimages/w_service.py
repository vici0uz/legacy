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
from openerp.tools.translate import _
import ast
import unicodedata
from clint.textui import colored


class workshop_service(osv.Model):
    _inherit = "workshop.service"

    def _img_count(self, cr, uid, ids, field_name, args, context=None):
        res = dict(map(lambda x: (x, 0), ids))
        for service in self.browse(cr, uid, ids):
            if field_name == 'counter_multimages':
                if service.multi_images:
                    bruto = service.multi_images
                    tratado = unicodedata.normalize('NFKD', bruto).encode('ascii', 'ignore')
                    lista = eval(str(tratado))
                    cont = len(lista)
                    res[service.id] = cont
            elif field_name == 'counter_multimages_rec':
                if service.multi_images_received:
                    bruto = service.multi_images_received
                    tratado = unicodedata.normalize('NFKD', bruto).encode('ascii', 'ignore')
                    lista = eval(str(tratado))
                    cont = len(lista)
                    res[service.id] = cont
            elif field_name == 'counter_multimages_del':
                if service.multi_images_delivered:
                    bruto = service.multi_images_delivered
                    tratado = unicodedata.normalize('NFKD', bruto).encode('ascii', 'ignore')
                    lista = eval(str(tratado))
                    cont = len(lista)
                    res[service.id] = cont
        return res

        def autoparts(self, cr, uid, ids, context=None):
            pass

    _columns = {
        'multi_images': fields.text("To Budgeting"),
        'multi_images_received': fields.text("Received Vehicle"),
        'multi_images_delivered': fields.text("Delivered Vehicle"),
        'attach_ids': fields.many2many(
            'ir.attachment',
            'class_ir_attachments_rel',
            'class_id',
            'attachment_id',
            'Related Documents'),
        'attach_ids_delivery': fields.many2many(
            'ir.attachment',
            'class_ir_attachments_delivery_rel',
            'class_id',
            'attachment_id',
            'Received Documents'
            ),
        'counter_multimages': fields.function(_img_count, string="Images Bugeting", type='integer'),
        'counter_multimages_rec': fields.function(_img_count, string="Images Received", type='integer'),
        'counter_multimages_del': fields.function(_img_count, string="Images Delivered", type='integer'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        for service in self.browse(cr, uid, ids, context):
            changes = []
        if 'multi_images' in vals and service.multi_images != vals['multi_images']:
            if service.multi_images:
                saneado = unicodedata.normalize('NFKD', service.multi_images).encode('ascii', 'ignore')
                nro_img1 = (len(ast.literal_eval(str(saneado))))
            else:
                nro_img1 = 0
            nro_img2 = (len(ast.literal_eval(vals.get('multi_images'))))
            ctx_final = (nro_img2 - nro_img1)
            changes.append(_("Have been uploaded %s pictures to budgeting documentation") % (ctx_final))
            if len(changes) > 0:
                self.message_post(cr, uid, [service.id], body=", ".join(changes), context=context)
        # Received
        if 'multi_images_received' in vals and service.multi_images_received != vals['multi_images_received']:
            if service.multi_images_received:
                saneado = unicodedata.normalize('NFKD', service.multi_images_received).encode('ascii', 'ignore')
                nro_img1 = (len(ast.literal_eval(str(saneado))))
            else:
                nro_img1 = 0
            nro_img2 = (len(ast.literal_eval(vals.get('multi_images_received'))))
            ctx_final = (nro_img2 - nro_img1)
            changes.append(_("Have been uploaded %s pictures to received vehicle documentation") % (ctx_final))
            if len(changes) > 0:
                self.message_post(cr, uid, [service.id], body=", ".join(changes), context=context)
        # Delivered
        if 'multi_images_delivered' in vals and service.multi_images_delivered != vals['multi_images_delivered']:
            if service.multi_images_delivered:
                saneado = unicodedata.normalize('NFKD', service.multi_images_delivered).encode('ascii', 'ignore')
                nro_img1 = (len(ast.literal_eval(str(saneado))))
            else:
                nro_img1 = 0
            nro_img2 = (len(ast.literal_eval(vals.get('multi_images_delivered'))))
            ctx_final = (nro_img2 - nro_img1)
            changes.append(_("Have been uploaded %s pictures to delivered vehicle documentation") % (ctx_final))
            if len(changes) > 0:
                self.message_post(cr, uid, [service.id], body=", ".join(changes), partner_ids=None, context=context)
        # FIN
        return super(workshop_service, self).write(cr, uid, ids, vals, context)

workshop_service()
