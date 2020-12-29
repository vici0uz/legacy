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
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
from openerp import netsvc
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from prettytable import PrettyTable
from clint.textui import colored
from openerp import models, api
from openerp import fields as Fields


def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)


class res_users(osv.Model):
    _inherit = "res.users"
    _columns = {
        'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse'),
    }
res_users()


class workshop_service_tag(osv.Model):
    _name = "workshop.service.tag"
    _columns = {
        'name': fields.char('Name', required=True, translate=True),
    }


class workshop_service(osv.Model):
    _name = 'workshop.service'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'date_rec desc'
    _description = 'Vehicle Services'

    def _service_name_get_function(
            self, cr, uid, ids, prop, unknow_none, t_insurance, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
                if record.t_insurance:
                    res[record.id] = record.partner_id.name + '/ ' + record.n_incident
                else:
                    res[record.id] = record.partner_id.name + '/ ' + record.job_no
        return res

    def _default_stock_location(self, cr, uid, context=None):
        user_obj = self.pool.get('res.users')
        stock_location = self.pool.get('ir.model.data').get_object(cr, uid, 'stock', 'stock_location_stock')
        warehouse = user_obj.browse(cr, uid, uid, context=context).warehouse_id
        if warehouse:
            stock_location = warehouse.lot_stock_id
        return stock_location.id

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancelled'})

    def action_draft(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft', 'color': '1'})

    def action_set_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        date_today = fields.date.today()
        self.write(cr, uid, ids, {'state': 'done', 'date_ending': date_today})

    def action_set_approved(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        date_today = fields.date.today()
        self.write(cr, uid, ids, {'state': 'approved', 'color': '5', 'date_approved': date_today, 'has_approved': True})

    def action_set_partially_approved(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'papproved', 'color': '4'})

    def action_set_pending(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.action_vehicle_out(cr, uid, ids, context=None)
        self.write(cr, uid, ids, {'state': 'pending', 'color': '1'})

    def on_change_vehicle(self, cr, uid, ids, vehicle_id, context=None):
        if not vehicle_id:
            return {}
        res = {}
        vehicle = self.pool.get('workshop.vehicle').browse(cr, uid, vehicle_id, context=context)
        return res

    def _get_default_author(self, cr, uid, context=None):
        return self.pool.get('res.users').read(cr, uid, uid, ['partner_id'], context=context)['partner_id'][0]

    def _autoparts_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))

        try:
            for service in self.browse(cr, uid, ids, context):
                res[service.id] = len(service.autopart_ids)
        except:
            pass
        return res

    def action_vehicle_out(self, cr, uid, ids, context=None):
        service = self.pool.get('workshop.service').browse(cr, uid, ids, context)
        for case in service:
            vehicle = case.vehicle_ids.id
            vehicle_id = self.pool.get('workshop.vehicle').write(cr, uid, vehicle,{'state': 'vehicle_out'})

    def _additional_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))
        try:
            for service in self.browse(cr, uid, ids, context):
                res[service.id] = len(service.additional)
        except:
            pass
        return res

    def copy(self, cr, uid, record_id, default=None, context=None):
        if default is None:
            default = {}

        default.update({'additional': []})
        return super(workshop_service, self).copy(cr, uid, record_id, default, context)

    def action_prueba(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'alarm': 'True'}, context=context)

    _columns = {
        'autopart_count': fields.function(_autoparts_order_count, string='# of Vehicles', type='integer'),
        'date_rec': fields.date(
            'Date', required=True, readonly=True, select=True),
        'job_no': fields.char(
            'Job Number', size=64, select=True),
        'image': fields.related(
            'insurer_id',
            'image',
            type="binary", string="Image"),
        'name': fields.function(
            _service_name_get_function,
            type="char", string="Name", store=True, select=True),
        'vehicle_ids': fields.many2many(
            'workshop.vehicle',
            'service_rel',
            'service_id',
            'vehicle_id',
            'Vehicles', readonly=True, states={'draft': [('readonly', False)]}),
        'partner_id': fields.many2one(
            'res.partner',
            'Partner',
            required=True,
            readonly=True,
            states={'draft': [('readonly', False)]}),
        'partner_id_phone': fields.related(
            'partner_id',
            'phone',
            type="char", string="Phone"
            ),
        'partner_id_mobile': fields.related(
            'partner_id',
            'mobile',
            type="char",
            string="Mobile"
            ),
        't_insurance': fields.boolean(
            'Insurance Company Check',
            readonly=True,
            states={'draft': [('readonly', False)]},
            help="Check if the vehicle is repaired trought Insurance Company"),
        'insurer_id': fields.many2one(
            'res.partner',
            'Insurance Company',
            readonly=True,
            states={'draft': [('readonly', False)]}),
        'n_incident': fields.char(
            'Incident Number',
            size=64,
            readonly=True,
            states={'draft': [('readonly', False)]}, select=True),
        'budget': fields.one2many('sale.order', 'service', 'Budget'),
        'tag_ids': fields.many2many(
            'workshop.service.tag',
            'workshop_service_tag_rel',
            'service_tag_id',
            'tag_id',
            'Tags'),
        'notes': fields.text(
            'Job Remarks',
            help="Write here all suplementary informations relative to this service"),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('papproved', 'Partially Approved'),
            ('approved', 'Approved'),
            ('cancelled', 'Cancelled'),
            ('pending', 'Pending'),
            ('done', 'Finalized')],
            "Status", readonly=True, select=True, track_visibility='onchange'),
        'progress_rate': fields.float('Progreso'),
        'expected_date': fields.date(
            'Tentative Date of Repair',
            readonly=True, states={'draft': [('readonly', False)]}),
        'service_works': fields.one2many(
            'workshop.service.work',
            'service_id', 'Works (Deprecated)', readonly=True),
        'service_works_2': fields.one2many(
            'workshop.service.work_2',
            'service_id_2',
            'Works',
            readonly=True, states={'draft': [('readonly', False)]}),
        'author': fields.many2one('res.partner', 'Author', select=1),
        'color': fields.integer('Color Index'),
        'priority': fields.selection([
            ('4', 'Very Low'),
            ('3', 'Low'),
            ('2', 'Medium'),
            ('1', 'Important'),
            ('0', 'Very important')],
            'Priority', select=True),
        'kanban_state': fields.selection([
            ('normal', 'Normal'),
            ('blocked', 'Blocked'),
            ('done', 'Ready for next stage')], 'Kanban State',
            track_visibility='onchange',
            help="A task's kanban state indicates special situations affecting it:\n"
            " * Normal is the default situation\n"
            " * Blocked indicates something is preventing the progress of this task\n"
            " * Ready for next stage indicates the task is ready to be pulled to the next stage",
            readonly=True, required=False),
        'autopart_ids': fields.one2many('workshop.autopart.receiving', 'service_id', 'Autoparts'),
        'w_state': fields.selection([
            ('state1', 'State 1'),
            ('state2', 'State 2')], 'Autoparts Alert', required=False, readonly=True
            ),
        'additional': fields.one2many('workshop.service.additional', 'parent_service_id', 'Additional'),
        'additional_count': fields.function(_additional_count, string='# of Additionals', type='integer'),
        'date_approved': fields.date('Approved Date', readonly=True),
        'date_ending': fields.date('Ending Date', readonly=True),
        'has_approved': fields.boolean('Has been approved', readonly=True),
        'vehicle_ids_color': fields.related('vehicle_ids', 'color', type="one2many", relation="workshop.vehicle.color", string="Color"),
        'km': fields.char(string='Mileage')
        # 'alarm': fields.boolean('Alarm')
    }
    _defaults = {
        'color': 0,
        # 'job_no': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'job.numberx'),
        'date_rec': fields.date.context_today,
        't_insurance': True,
        'state': 'draft',
        'progress_rate': 15,
        'priority': '2',
        'kanban_state': 'normal',
        'w_state': 'state1',
        'author': lambda self, cr, uid, ctx={}: self._get_default_author(cr, uid, ctx),
        'has_approved': False,
        'alarm': False
    }
    _sql_constraints = [
        ('name_uniq', 'unique (n_incident)', 'Incident Number must be unique!')
        ]

    def service_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancelled'}, context=context)

    def service_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def set_kanban_state_blocked(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'kanban_state': 'blocked'}, context=context)

    def set_w_state_state3(self, cr, uid, ids, context=None):
        pass

    def set_kanban_state_normal(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'kanban_state': 'normal'}, context=context)

    def set_kanban_state_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'kanban_state': 'done'}, context=context)
        return False

    def set_high_priority(self, cr, uid, ids, *args):
        """Set task priority to high
        """
        return self.write(cr, uid, ids, {'priority': '0'})

    def set_normal_priority(self, cr, uid, ids, *args):
        """Set task priority to normal
        """
        return self.write(cr, uid, ids, {'priority': '2'})

    def write(self, cr, uid, ids, vals, context=None):
        for service in self.browse(cr, uid, ids, context):
            changes = []
            work_obj = self.pool.get('workshop.service.work_2')
            x = PrettyTable(["Autoparte", "Trabajo"])
            if 'partner_id' in vals and service.partner_id.id != vals['partner_id']:
                value = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'], context=context).name
                oldpartner = (service.partner_id.name) or _('None')
                changes.append(_("Partner: from '%s' to '%s'") % (oldpartner, value))
            if 'n_incident' in vals and service.n_incident != vals['n_incident']:
                old_n_incident = service.n_incident or _('None')
                changes.append(_("Incident Number: from '%s' to '%s'") % (old_n_incident, vals['n_incident']))
            if 'job_no' in vals and service.job_no !=['job_no']:
                old_job_no = service.job_no or _('None')
                changes.append(_("Job Number: from '%s' to '%s'") % (old_job_no, vals['job_no']))
            # Custom
            if 'service_works_2' in vals and service.service_works_2 != vals['service_works_2']:
                if len(service.service_works_2) <= 0:
                    changes.append(_("I added work table"))
                else:
                    work = service.service_works_2.ids
                    for w in work:
                        part_name = (work_obj.browse(cr, uid, w).fault_part_ids_2.name)
                        work_str = (work_obj.browse(cr, uid, w).work_2)
                        if work_str == "sup":
                            work_str = "Sustituir"
                        elif work_str == "repandpaint":
                            work_str = "Reparar y Pintar"
                        elif work_str == "adjust":
                            work_str = "Ajustar"
                        elif work_str == "mount_umount":
                            work_str = "Montar/Desmontar"
                        elif work_str == "polish":
                            work_str = "Pulir"
                        elif work_str == 'paint':
                            work_str = "Pintar"
                        elif work_str == "touch_up":
                            work_str = "Retocar"
                        elif work_str == "supandpaint":
                            work_str = "Sustituir y Pintar"
                        elif work_str == "rep":
                            work_str = "Reparar"
                        elif work_str == "frame":
                            work_str = "Encuadrar"
                        x.add_row([part_name, work_str])
                    y = x.get_html_string(format=True)
                    changes.append(_("I modified the job table, Here is the old table<br/>%s")%(y))
            if len(changes) > 0:
                self.message_post(cr, uid, [service.id], body=", ".join(changes), context=context)

        service_id = super(workshop_service, self).write(cr, uid, ids, vals, context)
        return True


class workshop_service_work_2(models.Model):
    _name = 'workshop.service.work_2'


    @api.one
    def set_autopart_state(self):
        self.write({'state': 'received', 'received': True})

    service_id_2 = Fields.Many2one(comodel_name='workshop.service', string='Service', required=True, ondelete='cascade')
    work_2 = Fields.Selection([
        ('rep', 'Repair'),
        ('repandpaint', 'Repair and Paint'),
        ('sup', 'Supply'),
        ('supandpaint', 'Supply and Paint'),
        ('adjust', 'Adjust'),
        ('mount_umount', 'Mount/Unmount'),
        ('polish', 'Polish'),
        ('paint', 'Paint'),
        ('touch_up', 'Touch up'),
        ('frame', 'Frame')
        ],
        'Work',
        select=True,
        )
    fault_part_ids_2 = Fields.Many2one(comodel_name='workshop.autopart.type', string='Autopart', required=True)
    notes_2 = Fields.Text(
            'Job Remarks',
            help="Write here all suplementary informations relative to this service")
    t_insurance_additional = Fields.Boolean('Repair by Insurance')
    n_incident_additional = Fields.Char('Incident Number')
    damage_level = Fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Damage Level')
    state = Fields.Selection([('received', 'Received'), ('out', 'Absent')], string="State")
    received = Fields.Boolean('Received')
    defaults = {
        't_insurance': True,
        'state': 'received',
        'received': False

    }


# # Legacy ######################
class workshop_service_work(osv.Model):
    _name = 'workshop.service.work'
    """Legacy"""
    _columns = {
        'service_id': fields.many2one('workshop.service', 'Service', required=True, ondelete='cascade'),
        'work': fields.selection([
            ('rep', 'Repair'),
            ('repandpaint', 'Repair and Paint'),
            ('sup', 'Supply'),
            ('supandpaint', 'Supply and Paint'),
            ('adjust', 'Adjust'),
            ('mount_umount', 'Mount/Unmount')
            ],
            'Work',
            select=True,
            ),
        'fault_part_ids': fields.many2many(
            'workshop.autopart.type',
            'workshop_autopart_type_rel',
            'fault_part_id',
            'autopart_type',
            'Autopart'),
        'notes': fields.text(
            'Job Remarks',
            help="Write here all suplementary informations relative to this service")
    }
