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


from openerp import fields, models, api
from clint.textui import colored
from openerp.osv import osv
from openerp.tools.translate import _


class workshop_service(models.Model):
    _inherit = 'workshop.service'
    alarm = fields.Boolean('Alarm', compute='detect_alarm', store=True)
    alarm_ids = fields.One2many(comodel_name='workshop.service.alarm', inverse_name='service_id', string="Alarms")

    @api.one
    def action_set_approved(self):
        alarms = self.env['workshop.service.alarm'].search([('service_id', '=', self.id)])
        lista = []
        for alarm in alarms:
            lista.append(alarm.case)
        # if ((not self.multi_images) and (not self.multi_images_received)):
        #     if 'case_1' not in lista:
        #         self.alarm_ids.create({'service_id': self.id, 'active': 'True', 'case': 'case_1'})
        if (not self.attach_ids_delivery):
            if 'case_2' not in lista:
                self.alarm_ids.create({'service_id': self.id, 'active': 'True', 'case': 'case_2'})

        for service in self.env['workshop.service'].browse(self.id):
            if (len(self.alarm_ids) > 0):
                service.write({'alarm': True})
        self.write({'alarm': True})
        return super(workshop_service, self).action_set_approved()

    @api.one
    def detect_alarm(self):
        len_alarm = len(self.alarm_ids.search([('active', '=', True),('service_id','=', self.id)]))
        return len_alarm

    @api.one
    def vehicle_in(self):
        lista = []
        alarms = self.alarm_ids.search([('case', '=', 'case_3'), ('service_id', '=', self.id)])
        for alarm in alarms:
            lista.append(alarm.case)
        for vehicle in self.vehicle_ids:
            if vehicle.state == 'vehicle_out':
                if self.multi_images_received == [] or self.multi_images_received is False:
                    if 'case_3' not in lista:
                        self.alarm_ids.create({'service_id': self.id, 'active': 'True', 'case': 'case_3'})
                vehicle.write({'state': 'vehicle_in'})

    # @api.model
    # def create(self, vals, context=None):
    #     new_id = super(workshop_service, self).create(vals)
    #     new_service = self.env['workshop.service'].browse(new_id.id)
    #     if new_service.t_insurance:
    #         if not ('multi_images' or 'multi_images_received') in vals or not (vals['multi_images'] or vals['multi_images_received']):
    #             new_service.write({'alarm_ids': [(0, 0, {'service_id': new_id, 'case': 'case_1', 'active': True})]})
    #     if (colored.red(new_service.vehicle_ids[0].state) == 'vehicle_out'):
    #         print colored.red("Vehiculo Dentro")
    #     else:
    #         print colored.red("Vehiculo Dentro")
    #     # return new_id

    @api.multi
    def write(self, values):
        alarms = self.env['workshop.service.alarm']
        if len(self.alarm_ids) > 0:
            if ((self.multi_images) or (self.multi_images_received)):
                case_1 = alarms.search([('service_id', '=', self.id), ('active', '=', True), ('case', '=', 'case_1')])
                case_1.write({'active': False})
            if 'attach_ids_delivery' in values or self.attach_ids_delivery:
                case_2 = alarms.search([('service_id', '=', self.id), ('active', '=', True), ('case', '=', 'case_2')])
                case_2.write({'active': False})
            if (self.vehicle_ids):
                if ((self.vehicle_ids[0].state == 'vehicle_in') and('multi_images_received' in values or self.multi_images_received)):
                    case_3 = alarms.search([('service_id', '=', self.id), ('active', '=', True), ('case', '=', 'case_3')])
                    case_3.write({'active': False})
        if (self.detect_alarm()[0] > 0):
            values.update({'alarm': True})
        else:
            values.update({'alarm': False})
        return super(workshop_service, self).write(values)


class workshop_service_alarm(models.Model):
    _name = 'workshop.service.alarm'

    service_id = fields.Many2one(comodel_name='workshop.service')
    active = fields.Boolean('Active')
    case = fields.Selection([('case_1', 'No Images'), ('case_2', 'No approval order'), ('case_3', 'No received vehicle images')], string="Alarm")