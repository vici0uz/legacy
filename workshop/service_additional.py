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


class workshop_service_additional(osv.Model):
    _name = 'workshop.service.additional'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'parent_service_id': fields.many2one('workshop.service', 'Parent Service', required=True),
        'additional_work_ids': fields.one2many('workshop.service.additional.work', 'additional_service_id', required=True, string='Additional'),
        'additional_n_incident': fields.char('Incident Number', size=64),
        'additional_t_insurer': fields.boolean('Insured?')
    }
    _defaults = {
        'additional_t_insurer': False
    }


class workshop_service_additional_work(osv.Model):
    _name = 'workshop.service.additional.work'

    _columns = {
        'additional_service_id': fields.many2one('workshop.service.additional', 'Service', required=True, ondelete='cascade'),
        'work': fields.selection([
            ('prov', 'Provision of spare parts'),
            ('rep', 'Repair'),
            ('repandpaint', 'Repair and Paint'),
            ('sup', 'Supply'),
            ('supandpaint', 'Supply and Paint'),
            ('adjust', 'Adjust'),
            ('mount_umount', 'Mount/Unmount'),
            ('polish', 'Polish'),
            ('paint', 'Paint'),
            ('touch_up', 'Touch up')],
            'Work',
            select=True, required=True
            ),
        'fault_part_ids': fields.many2one('workshop.autopart.type', 'Autopart', required=True),
        'notes': fields.text(
            'Job Remarks',
            help="Write here all suplementary informations relative to this service")
    }
