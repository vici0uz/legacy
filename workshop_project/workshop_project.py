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
import openerp.addons.decimal_precision as dp


class workshop_service(models.Model):
    _inherit = 'workshop.service'

    # @api.one
    # @api.depends('supply_line.cost_price', 'supply_line.invoiced_amount', 'labor_line.labor_cost')
    # def _compute_supplies_costs(self):
    #     self.service_supply_cost = sum(line.cost_price for line in self.supply_line)
    #     self.service_invoiced_amount = sum(line.invoiced_amount for line in self.supply_line)
    #     self.service_labor_cost = sum(line.labor_cost for line in self.labor_line)
    #     self.service_supply_gain = (self.service_invoiced_amount - self.service_supply_cost)

    @api.one
    @api.depends('supply_line.cost_price', 'supply_line.invoiced_amount', 'supply_line_2.cost_price', 'supply_line_2.invoiced_amount', 'labor_line.labor_cost')
    def _compute_supplies_costs(self):
        # print colored.red("Computado")
        # # self.service_supply_cost = sum(line.cost_price for line in self.supply_line)
        if self.supply_line:
            # print colored.red("HAY")
            self.service_supply_cost = sum(line.cost_price for line in self.supply_line)
            self.service_invoiced_amount = sum(line.invoiced_amount for line in self.supply_line)
            # for line in self.supply_line:
            #     print colored.red(line.cost_price)

        elif self.supply_line_2:
            # print colored.blue("HAY NUEVO")
            self.service_supply_cost = sum(line.cost_price for line in self.supply_line_2)
            self.service_invoiced_amount = sum(line.invoiced_amount for line in self.supply_line_2)
        else:
            # print colored.cyan("paso")
            pass
        self.service_labor_cost = sum(line.labor_cost for line in self.labor_line)
        self.service_supply_gain = (self.service_invoiced_amount - self.service_supply_cost)

    @api.one
    @api.depends('case_ids.approved_amount')
    def _compute_total_amount(self):
        self.case_total = sum(line.approved_amount for line in self.case_ids)

    @api.one
    @api.depends('case_total', 'service_labor_cost', 'service_supply_cost')
    def _compute_total_gain(self):
        self.service_gain_total = self.case_total - (self.service_labor_cost + self.service_supply_cost)

    project_id = fields.Many2one(comodel_name='project.project')
    project_id_progress = fields.Float('Progress')

    labor_line = fields.One2many(comodel_name='workshop.service.labor', inverse_name='service_id', string="Labor Cost")


    service_invoiced_amount = fields.Float('Invoiced Amount', compute='_compute_supplies_costs', store=True, digits=dp.get_precision('Product Price'))
    service_labor_cost = fields.Float(string="Labor Cost", compute='_compute_supplies_costs', store=True, digits=dp.get_precision('Product Price'))
    case_ids = fields.One2many(comodel_name='workshop.service.case', inverse_name='service_id')
    case_total = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True, digits=dp.get_precision('Product Price'))
    service_gain_total = fields.Float(string="Total Gain", compute='_compute_total_gain', store=True, digits=dp.get_precision('Product Price'))
    # INSUMOS
    service_supply_cost = fields.Float(string='Supplies Cost', compute='_compute_supplies_costs', digits=dp.get_precision('Product Price'), store=True)
    service_supply_gain = fields.Float(string='Gain', compute='_compute_supplies_costs', digits=dp.get_precision('Product Price'), store=True)

    # NEW
    # NUEVA LINEA DE INSUMOS
    supply_line_2 = fields.One2many(comodel_name='workshop.service.supply_line',inverse_name='service_id')
    # LEGACY
    # VIEJA LINEA DE INSUMOS
    supply_line = fields.One2many(comodel_name='workshop.service.supply', inverse_name='service_id', string="Operational Costs")

    _defaults = {
        'project_id_progress': 0
    }


class project_project(models.Model):
    _inherit = 'project.project'

    workshop_service_id = fields.Many2one(comodel_name='workshop.service', string="Case")
    service_job_no = fields.Char(string='Job Number', related='workshop_service_id.job_no')


# #############################LEGACY##########################################
#                                                                             #
#                                                                             #
class workshop_service_supply(models.Model):
    _name = 'workshop.service.supply'

    @api.one
    def get_author(self):
        self.author = self.create_uid.name

    @api.one
    @api.depends('cost_price', 'invoiced_amount')
    def _compute_gain(self):
        self.subtotal_gain = self.invoiced_amount - self.cost_price

    cost_type = fields.Selection([('supply', 'Supply'), ('autopart', 'Autopart')], 'Type')
    service_id = fields.Many2one(comodel_name='workshop.service')
    product_id = fields.Many2one(comodel_name='product.product')
    autopart_id = fields.Many2one(comodel_name='workshop.autopart.type')
    cost_price = fields.Float(string='Cost Price', digits=dp.get_precision('Product Price'))
    invoiced_amount = fields.Float(string='Invoiced Amount', digits=dp.get_precision('Product Price'))
    subtotal_gain = fields.Float(string='Subtotal Gain', compute='_compute_gain', digits= dp.get_precision('Product Price'))
    author = fields.Char(compute='get_author')
# #############################################################################


class workshop_service_cost(models.Model):
    _name = 'workshop.service.labor'

    labor_type = fields.Selection([('regular', 'Regular'), ('outsourced', 'Outsourced')], 'Labor Condition')
    service_id = fields.Many2one(comodel_name='workshop.service', string='Case')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    partner_id = fields.Many2one(comodel_name='res.partner')
    labor_cost = fields.Float(string='Labor Cost', digits=0)
    notes = fields.Text(string='Observations')

    _defaults = {
        'labor_type': 'regular'
    }


class workshop_service_case(models.Model):
    _name = 'workshop.service.case'

    service_id = fields.Many2one(comodel_name='workshop.service')
    case_n_incident = fields.Char('Incident Number')
    case_t_insurance = fields.Boolean('Repair by Insurance')
    approved_amount = fields.Float(string='Approved Amount', digits=dp.get_precision('Product Price'))
    motive = fields.Selection([('labor_cost', 'Labor Cost'), ('replacement', 'Replacemente'), ('both', 'Both'), ('franchise', 'Franchise'), ('discount', 'Discount')], string="Cost Motif")


class res_partner(models.Model):
    _inherit = 'res.partner'

    outsourced = fields.Boolean('Outsourced')

    _defaults = {
        'outsourced': False
    }


class workshop_service_supply_line(models.Model):
    _name = 'workshop.service.supply_line'

    @api.one
    @api.depends('cost_price', 'qty', 'invoiced_amount')
    def _compute_gain(self):
        context = self._context
        self.cost_price = self.qty * self.cost_price
        self.invoiced_amount = self.qty * self.invoiced_amount
        self.sub_gain = self.invoiced_amount - self.cost_price

    @api.model
    def get_default_cost_price(self):
        return self.product_id.standard_price

    @api.multi
    def product_id_change(self, product, qty=0, cost_price=False, invoiced_amount=False):
        context = self._context
        values = {}
        if not product:
            return {'value': {}, 'domain': {}}
        product = self.env['product.product'].browse(product)
        values['cost_price'] = cost_price * qty or product.standard_price * qty
        values['invoiced_amount'] = invoiced_amount * qty or product.lst_price * qty
        return {'value': values, 'context': context}

    @api.one
    def get_author(self):
        self.author = self.create_uid.name

    service_id = fields.Many2one(comodel_name='workshop.service')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    author = fields.Char(compute='get_author')
    qty = fields.Float(default=1, string="Quantity", digits=dp.get_precision('Product Price'))
    cost_price = fields.Float(string='Price', digits=dp.get_precision('Product Price'), default=get_default_cost_price)
    invoiced_amount = fields.Float(string='Invoiced', digits=dp.get_precision('Product Price'))
    sub_gain = fields.Float(digits=dp.get_precision('Product Price'), compute='_compute_gain')