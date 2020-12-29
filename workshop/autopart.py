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
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from clint.textui import colored


def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)


class workshop_autopart_type_tag(osv.Model):
    _name = "workshop.autopart.type.tag"

    _columns = {
        'name': fields.char('Name', required=True, translate=True)
    }


class workshop_autopart_type(osv.Model):
    _name = 'workshop.autopart.type'
    _order = 'name asc'

    def _get_default_author(self, cr, uid, context=None):
        return self.pool.get('res.users').read(cr, uid, uid, ['partner_id'], context=context)['partner_id'][0]

    def create_autopart_cat(self, cr, uid, ids, context=None):
        # # Obtener instancias
        autopart_obj = self.pool.get('workshop.autopart.type')
        print colored.red(autopart_obj.browse(cr, uid, ids).name)
        # product_category_obj = self.pool.get('product.category')
        # # Traer todos los repuestos
        # all_records = autopart_obj.search(cr, uid, [(1, '=', 1)], order='id')
        # # Obtener Raiz
        # stock_autopart_root = self.pool.get('res.company').get_root_tree(cr, uid, context=context)
        # autopart_name = autopart_obj.browse(cr, uid, ids, context=context).name
        # autopart_id = autopart_obj.browse(cr, uid, ids, context=context).id
        # search_product_category = product_category_obj.search(cr, uid, [('name', '=', autopart_name)], order='id')
        # if(len(search_product_category) <= 0):
        #     product_category_vals = {
        #         'name': autopart_obj.browse(cr, uid, ids, context).name,
        #         'parent_id': stock_autopart_root.id,
        #         'autopart_type': autopart_id,
        #         'type': 'view'
        #     }
        #     product_category_create = product_category_obj.create(cr, uid, product_category_vals, context=({'defer_parent_store_computation': True}))

    # def create_all_autopart_cats(self, cr, uid, ids, context=None):
    #     # Obtener instancias
    #     autopart_obj = self.pool.get('workshop.autopart.type')
    #     product_category_obj = self.pool.get('product.category')
    #     # Traer todos los repuestos
    #     all_autopart_types = autopart_obj.search(cr, uid, [(1, '=', 1)], order='id')
    #     # Obtener Raiz
    #     stock_autopart_root = self.pool.get('res.company').get_root_tree(cr, uid, context=context)
    #     # Obtener todas las categorias de autorepuestos
    #     root_id = stock_autopart_root.id
    #     all_auto_cats = product_category_obj.search(cr, uid, [('parent_id', '=', root_id)])
    #     # Cruzar nombres de repuestos y categorias
    #     # search = self.search_autopart_category(cr, uid, autopart_name)
    #     for autopart in all_autopart_types:
    #         autopart_name = autopart_obj.browse(cr, uid, autopart).name
    #         search = self.search_autopart_category(cr, uid, autopart_name)
    #         if(len(search) <=0):
    #             category_vals = {
    #                 'name': autopart_name,
    #                 'parent_id': root_id,
    #                 'autopart_type': autopart,
    #                 # 'type': 'view'
    #             }
    #             print autopart_name
    #             product_category_obj.create(cr, uid, category_vals, context=({'defer_parent_store_computation': True}))
    #         else:
    #             print "Ya esta"

    def search_autopart_category(self, cr, uid, autopart_name, context=None):
        autopart_obj = self.pool.get('workshop.autopart.type')
        product_category_obj = self.pool.get('product.category')
        # all_autopart_types = autopart_obj.search(cr, uid, [(1, '=', 1)], order='id')
        root_id = self.pool.get('res.company').get_root_tree(cr, uid, context=context).id
        search = product_category_obj.search(cr, uid, ['&', ('parent_id', '=', root_id), ('name', '=', autopart_name)])
        return search

    # def create(self, cr, uid, vals, context=None):
    #     if context is None:
    #         context = {}
    #     new_id = super(workshop_autopart_type, self).create(cr, uid, vals, context=None)
    #     # self.create_autopart_cat(cr, uid, new_id)
    #     return new_id

    _columns = {
        'name': fields.char('Type', required=True, translate=True),
        'tag_ids': fields.many2many('workshop.autopart.type.tag', 'autopart_type_rel', 'autopart_tag_id', 'tag_id', 'Tags'),
        'author': fields.many2one('res.partner', 'Author', select=1),
        'autopart_receiving_lot_id': fields.one2many('workshop.autopart.receiving.lot', 'autopart_type_id', string="Lot Ids")
    }
    _defaults = {
        'author': lambda self, cr, uid, ctx={}: self._get_default_author(cr, uid, ctx),
    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'Autopart Type must be unique!')]


class workshop_autopart_receiving(osv.Model):
    _name = 'workshop.autopart.receiving'
    _order = 'date_order desc'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    def _get_insurer_name(self, cr, uid, ids, field_name, unknow, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.service_id.insurer_id.name
        return res

    def make_read_only(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'done'})

    def cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancelled'})

    def notify_state(self, cr, uid, ids, context={}):
        record = self.browse(cr, uid, ids, context=None).service_id
        self.pool.get('workshop.service').write(cr, uid, [record.id], {'w_state': 'state2'})

    _columns = {
        'name': fields.char('Order Reference', required=True, copy=False,
                            readonly=True, select=True),
        'date_order': fields.datetime('Date', required=True, readonly=True, select=True, copy=False),
        'responsible_id': fields.many2one('workshop.autopart.receiving.responsible', 'Dealer', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'service_id': fields.many2one('workshop.service', 'Service'),
        'insurer_name': fields.function(_get_insurer_name, store=True, type="char", string="Insurance Company"),
        'autopart_receiving_lot_ids': fields.one2many('workshop.autopart.receiving.lot', 'workshop_autopart_receiving_id', copy=True, string='Lot'),
        'observation': fields.text('Observations'),
        'n_incident_rel': fields.related('service_id', 'n_incident', type="char", string='Sinister Number', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Supplier'),
        'insurer_id_phone_number': fields.related('partner_id', 'phone', type="char", string='Phone Number', readonly=True),
        'date_rec': fields.date('Date', required=True, readonly=True, select=True),
        'vehicle_id': fields.many2one('workshop.vehicle', 'Vehicle', required=True),
        'user_id': fields.many2one('res.users', 'Responsible', select=True, track_visibility='onchange'),
        'state': fields.selection([('draft', 'Draft'), ('done', 'Received'), ('cancelled', 'Canceled')], 'State', required=True),
        }
    _defaults = {
        'date_order': fields.datetime.now,
        'name': lambda obj, cr, uid, context: '/',
        'date_rec': fields.date.context_today,
        'user_id': lambda obj, cr, uid, context: uid,
        'state': 'draft'
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'order_no.number') or '/'
            ctx = dict(context or {}, mail_create_nolog=True)
        new_id = super(workshop_autopart_receiving, self).create(cr, uid, vals, context=ctx)
        self.message_post(cr, uid, [new_id], body=_("Receiving Autopart"), context=ctx)
        self.notify_state(cr, uid, [new_id], context=None)
        self.make_read_only(cr, uid, [new_id], context=None)
        return new_id


class workshop_autopart_receiving_lot(osv.Model):
    _name = 'workshop.autopart.receiving.lot'
    # _order = 'name asc'
    _columns = {
        'autopart_type_id': fields.many2one('workshop.autopart.type', 'Autopart', required=True),
        'qty': fields.float('Quantity', required=True),
        'workshop_autopart_receiving_id': fields.many2one('workshop.autopart.receiving', 'Workshop Autopart Receiving ID'),
    }
    _defaults = {
        'qty': 1
    }


class workshop_autopart_receiving_responsible(osv.Model):
    _name = 'workshop.autopart.receiving.responsible'
    _order = 'name asc'
    _columns = {
        'name': fields.char('Responsible', required=True),
    }
