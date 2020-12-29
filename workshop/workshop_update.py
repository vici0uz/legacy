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

from openerp import fields, models, api, _
from clint.textui import colored


class workshop_service(models.Model):
    _inherit = 'workshop.service'

    @api.multi
    def write(self, values):
        seq = self.env['ir.sequence'].get('job.numberx')
        if 'state' in values:
            if values['state'] == 'approved':
                if not self.job_no:
                    seq = self.env['ir.sequence'].get('job.numberx')
                    values.update({'job_no': seq})

        if 't_insurance' in values:
            if values['t_insurance'] is False:
                values.update({'n_incident': None, 'insurer_id': None})

        return super(workshop_service, self).write(values)
