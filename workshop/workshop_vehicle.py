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


import string
from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from openerp import models, api, _
from openerp import fields as Fields
from clint.textui import colored


def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

# Asignaciones Comunes


class workshop_vehicle_tag(osv.Model):
    _name = 'workshop.vehicle.tag'

    _columns = {
        'name': fields.char('Name', required=True, translate=True),
    }


class workshop_vehicle_model(osv.Model):
    _name = 'workshop.vehicle.model'
    _description = 'model of vehicle'
    _order = 'name asc'

    def _model_name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            name = record.modelname
            if record.brand_id.name:
                name = record.brand_id.name + ' / ' + name
            res[record.id] = name
        return res

    def on_change_brand(self, cr, uid, ids, model_id, context=None):
        if not model_id:
            return {'value': {'image_medium': False}}
        brand = self.pool.get('workshop.vehicle.model.brand').browse(cr, uid, model_id, context=context)
        return {
            'value': {
                'image_medium': brand.image,
            }
        }

    # # Obtener la Raiz - OK
    # def _get_root(self, cr, uid, ids, context=None):
    #     stock_autopart_root = self.pool.get('res.company').get_root_tree(cr, uid, context=context)
    #     root_id = stock_autopart_root.id
    #     return root_id
    # # Crear todas las categorias de marcas

    # # Obtener Marca
    # def _check_brand(self, cr, uid, ids, context=None):
    #     model_brand_obj = self.pool.get('workshop.vehicle.model.brand')
    #     model_obj = self.pool.get('workshop.vehicle.model')
    #     model = model_obj.browse(cr, uid, ids).name
    #     brand = model_obj.browse(cr, uid, ids).brand_id.id
    #     model_brand_obj.create_brand_tree(cr, uid, brand, context=None)

    # # Obtener todas las Categorias de la Marca -OK
    # def _get_all_brand_cat(self, cr, uid, ids, context=None):
    #     root_id = self._get_root(cr, uid, ids)
    #     product_category_obj = self.pool.get('product.category')
    #     model_obj = self.pool.get('workshop.vehicle.model')
    #     brand_obj = self.pool.get('workshop.vehicle.model.brand')
    #     brand_id = model_obj.browse(cr, uid, ids).brand_id.id
    #     all_auto_cat = product_category_obj.search(cr, uid, [('brand_id', '=', brand_id)])
    #     return all_auto_cat

    # # Chequear Modelos
    # def _check_model(self, cr, uid, all_auto_cat, ids, context=None):
    #     product_category_obj = self.pool.get('product.category')
    #     model_name = self.pool.get('workshop.vehicle.model').browse(cr, uid, ids).modelname
    #     model_id = self.pool.get('workshop.vehicle.model').browse(cr, uid, ids).id
    #     for auto_cat in all_auto_cat:
    #         if (len(product_category_obj.search(cr, uid, ['&', ('parent_id', '=', auto_cat), ('model_id', 'in', ids)])) == 0):
    #             product_category_vals = {
    #                 'name': model_name,
    #                 'model_id': model_id,
    #                 'parent_id': auto_cat
    #             }
    #             print product_category_vals
    #             product_category_obj.create(cr, uid, product_category_vals, context=({'defer_parent_store_computation': True}))
    #         else:
    #             print "Ya ta"

    # def create_model_tree(self, cr, uid, ids, context=None):
    #     root_id = self._get_root(cr, uid, ids)
    #     # check_brand = self._check_brand(cr, uid, ids)
    #     all_auto_cat = self._get_all_brand_cat(cr, uid, ids)
    #     self._check_model(cr, uid, all_auto_cat, ids)

    _columns = {
        'name': fields.function(
            _model_name_get_fnc,
            type="char",
            string='Name',
            store=True),
        'modelname': fields.char("Model name", size=32, required=True),
        'brand_id': fields.many2one(
            'workshop.vehicle.model.brand',
            'Model Brand',
            required=True,
            help='Brand of the vehicle.'),
        'image': fields.related(
            'brand_id',
            'image',
            type="binary",
            string="Logo"),
        'image_medium': fields.related(
            'brand_id',
            'image_medium',
            type="binary",
            string="Logo"),
        'image_small': fields.related(
            'brand_id',
            'image_small',
            type="binary",
            string="Logo"),
    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'Name must be unique!')]


class workshop_vehicle_model_brand(osv.Model):
    _name = 'workshop.vehicle.model.brand'
    _description = 'Brand of the Vehicle'
    _order = 'name asc'

    # def create_brand_tree(self, cr, uid, ids, context=None):
    #     stock_autopart_root = self.pool.get('res.company').get_root_tree(cr, uid, context=context)
    #     model_brand_obj = self.pool.get('workshop.vehicle.model.brand')
    #     product_category_obj = self.pool.get('product.category')
    #     print "Comienza Busqueda todas las caregorias"
    #     all_auto_cat = product_category_obj.search(cr, uid, [('parent_id', '=', stock_autopart_root.id)], order='id')
    #     print "Finaliza Busqueda todas las categorias"
    #     brand_name = model_brand_obj.browse(cr, uid, ids).name
    #     brand_id = model_brand_obj.browse(cr, uid, ids).id
    #     print brand_id
    #     for auto_cat in all_auto_cat:
    #         print "Comienza Busqueda"
    #         search = product_category_obj.search(cr, uid, ['&', ('parent_id', '=', auto_cat), ('name', '=', brand_name)])
    #         print search
    #         print "Fin Busqueda"
    #         if (len(search) <= 0):
    #             category_id = product_category_obj.browse(cr, uid, auto_cat).id
    #             category_vals = {
    #                 'name': brand_name,
    #                 'parent_id': category_id,
    #                 'brand_id': brand_id
    #             }
    #             print "Comienza Creacion"
    #             print category_vals
    #             product_category_obj.create(cr, uid, category_vals, context=({'defer_parent_store_computation': True}))
    #             print "Finaliza Creacion"
    #         else:
    #             print "Ya esta"

    # def create_all_category_brands(self, cr, uid, ids, context=None):
    #     model_brand_obj = self.pool.get('workshop.vehicle.model.brand')
    #     all_brands = model_brand_obj.search(cr, uid, [(1, '=', 1)], order= 'id')
    #     for brand in all_brands:
    #         self.create_brand_tree(cr, uid, brand, context=None)

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
        'name': fields.char('Brand Name', size=64, required=True),
        'image': fields.binary(
            "Logo",
            help="""This field hold the image use as logo for the brand,"
            limited to 1024x1024px."""),
        'image_medium': fields.function(
            _get_image,
            fnct_inv=_set_image,
            string="Medium-sized photo",
            type="binary",
            multi="_get_image",
            store={
                'workshop.vehicle.model.brand': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                },
            help="""Medium-sized logo of the brand. It is automatically
                resized as a 128x128px image, with aspect ratio preserved.
                Use this field in form views or some kanban views."""),

        'image_small': fields.function(
            _get_image,
            fnct_inv=_set_image,
            string="Small-sized photo",
            type="binary",
            multi="_get_image",
            store={
                'workshop.vehicle.model.brand': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                },
            help="Small-sized photo of the brand. It is automatically "
                 "resized as a 64x64px image, with aspect ratio preserved. "
                 "Use this field aniwhere a small image is required."),
    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'Name must be unique!')]

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        new_id = super(workshop_vehicle_model_brand, self).create(cr, uid, vals)
        # self.create_brand_tree(cr, uid, [new_id], context=None)
        return new_id


class workshop_vehicle(osv.Model):

    _inherit = 'mail.thread'
    _name = 'workshop.vehicle'
    _description = 'Information on a vehicle'
    _order = 'date_rec desc'

    def _vehicle_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.reg_type:
                res[record.id] = record.autopart_type.name + '/ ' + record.model_id.brand_id.name + '/' + record.model_id.modelname + '/ ' + record.partner_id.name
            else:
                res[record.id] = record.model_id.brand_id.name + '/' + record.model_id.modelname + ' / ' + record.vin_sn
        return res

    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This open the xml view specified in xml_id for the current
        vehicle """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'workshop', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_vehicle_id': ids[0]})
            res['domain'] = [('vehicle_ids', '=', ids[0])]
            return res
        return False

    def capitalizar(self, cr, uid, ids, vin_sn=''):
        if vin_sn:
            result = {
                'value': {
                    'vin_sn': str(vin_sn).upper()
                }
            }
            return result

    def upper_case(self, cr, uid, ids, license_plate=''):
        if license_plate:
            result = {
                'value': {
                    'license_plate': str(license_plate).upper()
                }
            }
            return result

    def receiving_vehicle(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        date_today = fields.date.today()
        self.write(cr, uid, ids, {'state': 'vehicle_in', 'has_entered': True, 'now_in': True, 'date_in': date_today})

    def vehicle_outgoing(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        date_today = fields.date.today()
        self.write(cr, uid, ids, {'state': 'vehicle_out', 'now_in': False, 'date_out': date_today})

    def _get_brand_name(self, cr, uid, ids, field_name, unknow, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.model_id.brand_id.name
        return res

    _columns = {
        'name': fields.function(
            _vehicle_name_get_fnc,
            type="char",
            string="Name",
            store=True,
            select=True),
        'date_rec': fields.date(
            string="Creation Date",
            required=True,
            readonly=True,
            select=True,
            translate=True),
        'license_plate': fields.char(
            'License Plate',
            size=32,
            help='License plate number of the vehicle(ie: plate number for a car)',
            select=True),
        'vin_sn': fields.char(
            'Chassis Number',
            size=32,
            help='Unique number written on the vehicle motor (VIN/SN number)',
            select=True),
        'image': fields.related(
            'model_id',
            'image',
            type="binary",
            string="Logo"),
        'image_small': fields.related(
            'model_id',
            'image_small',
            type="binary",
            string="Logo"),
        'image_medium': fields.related(
            'model_id',
            'image_medium',
            type="binary",
            string="Logo"),
        'model_id': fields.many2one('workshop.vehicle.model', 'Model'),
        'type': fields.many2one(
            'workshop.vehicle.type',
            'Type of Vehicle',
            help='Type of Vehicle'),
        'partner_id': fields.many2one('res.partner', "Owner", required=True),
        'color': fields.many2one(
            'workshop.vehicle.color',
            'Color', help='Color of the vehicle'),
        'state': fields.selection([
            ('vehicle_in', 'Vehicle in Repair'),
            ('vehicle_in_observation', 'Vehicle in Observation'),
            ('vehicle_out', 'Not in Workshop')],
            'Status',
            select=True,
            readonly=True,
            track_visibility='onchange',
            help='Current state of the vehicle'),
        'counter': fields.float(size=8, string="Counter", required=True),
        'doors': fields.integer(
            'Doors Number',
            help='Number of doors of the vehicle'),
        'seats': fields.integer(
            'Seats Number',
            help='Number of seats of the vehicle'),
        'tag_ids': fields.many2many(
            'workshop.vehicle.tag',
            'workshop_vehicle_tag_rel',
            'vehicle_tag_id',
            'tag_id',
            'Tags'),
        'transmission': fields.selection([
            ('manual', 'Manual'),
            ('automatic', 'Automatic')],
            'Transmission',
            help='Transmission Used by the vehicle'),
        'fuel_type': fields.selection([
            ('gasoline', 'Gasoline'),
            ('diesel', 'Diesel'),
            ('electric', 'Electric'),
            ('hybrid', 'Hybrid')],
            'Fuel Type', help='Fuel Used by the vehicle'),
        'year': fields.many2one('workshop.vehicle.year', 'Year'),
        'service_ids': fields.many2many(
            'workshop.service',
            'service_rel',
            'vehicle_id',
            'service_id',
            'Services'),
        'reg_type': fields.boolean('Autopart?'),
        'autopart_type': fields.many2one(
            'workshop.autopart.type', string="Autopart type"),
        'has_entered': fields.boolean('Has entered to workshop'),
        'workshop_log': fields.one2many('workshop.vehicle.log', 'vehicle_id', 'Logs'),
        'date_in': fields.date('Vehicle Incoming', readonly=True),
        'date_out': fields.date('Vehicle Outgoing', readonly=True),
        'now_in': fields.boolean('In Workshop Actually', readonly=True),
        'brand_id_rel': fields.function(_get_brand_name, type="char", string="Brand", readonly=True, store=True),
    }

    _defaults = {
        'date_rec': fields.date.context_today,
        'doors': 5,
        'counter': 1,
        'reg_type': False,
        'state': 'vehicle_out',
        'has_entered': False
    }

    _sql_constraints = [(
        'name_uniq',
        'unique(vin_sn)',
        'Chassis Number must be unique!')]

    def on_change_model(self, cr, uid, ids, model_id, context=None):
        if not model_id:
            return {}
        model = self.pool.get('workshop.vehicle.model').browse(cr, uid, model_id, context=context)
        return {
            'value': {
                'image_medium': model.image,
            }
        }

    def create(self, cr, uid, data, context=None):
        vehicle_id = super(workshop_vehicle, self).create(cr, uid, data, context=context)
        try:
            (model, mail_group_id) = self.pool.get('ir.model.data').get_object_references(cr, uid, 'mail', 'group_all_employees')
            vehicle = self.browse(cr, uid, vehicle_id, context=context)
            self.pool.get('mail.group').message_post(
                cr, uid, [mail_group_id], body=_('Service %s has been created! Please Check.') % (vehicle.name),
                subtype='mail.mt_comment', context=context)
        except:
            pass
        return vehicle_id

    def write(self, cr, uid, ids, vals, context=None):
        for vehicle in self.browse(cr, uid, ids, context):
            changes = []
            if 'model_id' in vals and vehicle.model_id.id != vals['model_id']:
                value = self.pool.get('workshop.vehicle.model').browse(cr, uid, vals['model_id'], context=context).name
                oldmodel = vehicle.model_id.name or _('None')
                changes.append(_("Model: from '%s' to '%s'") % (oldmodel, value))
            if 'partner_id' in vals and vehicle.partner_id.id != vals['partner_id']:
                value = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'], context=context).name
                oldpartner = vehicle.partner_id.name or _('None')
                changes.append(_("Owner: from '%s' to '%s'") % (oldpartner, value))
            if 'license_plate' in vals and vehicle.license_plate != vals['license_plate']:
                old_license_plate = vehicle.license_plate or _('None')
                changes.append(_("License Plate: from '%s' to '%s'") % (old_license_plate, vals['license_plate']))
            if 'vin_sn' in vals and vehicle.vin_sn != vals['vin_sn']:
                old_vin_sn = vehicle.vin_sn or _('None')
                changes.append(_("Chassis Number: from '%s' to '%s'") % (old_vin_sn, vals['vin_sn']))
            if len(changes) > 0:
                self.message_post(cr, uid, [vehicle.id], body=", ".join(changes), context=context)
        vehicle_id = super(workshop_vehicle, self).write(cr, uid, ids, vals, context)
        return True


# class workshop_vehicle_year(osv.Model):
#     _name = 'workshop.vehicle.year'
#     _order = 'name desc'

#     _columns = {
#         'name': fields.char('Year', size=4, required=True),
#     }

#     _sql_constraints = [('name_uniq', 'unique(name)', 'Year must be unique!')]
class workshop_vehicle_year(models.Model):
    _name = 'workshop.vehicle.year'
    _order = "name desc"

    name = Fields.Char(string="Year", size=4, required=True)


class workshop_vehicle_type(models.Model):
    _name = 'workshop.vehicle.type'
    _order = 'name asc'

    name = Fields.Char(string='Type', required=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Type must be unique!')]


class workshop_vehicle_color(models.Model):
    _name = 'workshop.vehicle.color'
    _order = 'name asc'

    name = Fields.Char(string='Color', size=32, required=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Color must be unique!')]


class workshop_vehicle_autopart(osv.Model):
    _name = 'workshop.vehicle.autopart'
    _order = 'name asc',
    _columns = {
        'name': fields.char('Name', size=64, required=True),
    }
workshop_vehicle_autopart()


class workshop_vehicle_log(osv.Model):
    _name = 'workshop.vehicle.log'
    _order = 'date_in asc',
    _columns = {
        'vehicle_id': fields.many2one('workshop.vehicle', 'Vehicle'),
        'date_in': fields.date('Date Incoming'),
        'date_out': fields.date('Date Outgoing'),
        'in_workshop': fields.boolean('In the workshop')
    }
    _defaults = {
        'in_workshop': False,
        'date_in': fields.date.context_today
    }
