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

from openerp import models, api, fields
import openerp.addons.decimal_precision as dp
from clint.textui import colored


class InvoiceMod(models.Model):
    """Invoice Mod"""

    _inherit = "account.invoice"
    _order = "date_invoice desc"

    def _onchange_invoice_condition(self, cr, uid, ids, invoice_condition, context=None):
        if invoice_condition == 'counted':
            return {
                'value': {
                    'payment_term': 1
                }
            }
        else:
            return {
                'value': {
                    'payment_term': 3
                }
            }


    @api.one
    def prueba(self, data):
        account_config_settings = self.pool.get('account.config.settings')
        def_tax = account_config_settings.browse(self.env.cr, self.env.uid).default_purchase_tax.id
        print (colored.blue(account_config_settings))
        print (colored.cyan(def_tax))

    @api.depends('amount_tax')
    @api.one
    def get_exentas(self):
        for line in self.invoice_line:
            if len(line.invoice_line_tax_id) <= 0:
                self.exenta += line.price_subtotal

    @api.depends('amount_tax')
    @api.one
    def get_iva_5_compra(self):
        for tax in self.tax_line:
            if tax.name == "IVA 5% Compra" or tax.name == "IVA 5% Venta":
                self.iva_5 = tax.tax_amount

    @api.depends('amount_tax')
    @api.one
    def get_iva_10_compra(self):
        for tax in self.tax_line:
            if tax.name == "IVA 10% Compra" or tax.name == "IVA 10% Venta":
                self.iva_10 = tax.tax_amount

    # @api.depends('amount_tax')
    # @api.one
    # def get_iva_5_venta(self):
    #     for tax in self.tax_line:
    #         if tax.name == "IVA 5% Venta":
    #             self.iva_5_venta = tax.tax_amount

    # @api.depends('amount_tax')
    # @api.one
    # def get_iva_10_venta(self):
    #     for tax in self.tax_line:
    #         if tax.name == "IVA 10% Venta":
    #             self.iva_10_venta = tax.tax_amount

    invoice_condition = fields.Selection([
        ('credit', 'Credit'),
        ('counted', 'Counted')],
        string='Invoice Condition')

    iva_10 = fields.Float(compute='get_iva_10_compra', string="IVA 10%", store=True, default=0.0, digits=dp.get_precision('Account'))
    iva_5 = fields.Float(compute='get_iva_5_compra', string="IVA 5%", store=True, digits=dp.get_precision('Account'))
    exenta = fields.Float(compute='get_exentas', string="Exentas", store="True", digits=dp.get_precision('Account'))

    _sql_constraints = [('supplier_invoice_number_uniq', 'unique(supplier_invoice_number)', 'Invoice Number must be unique')]


class account_invoice_tax(models.Model):
    _inherit = "account.invoice.tax"

    def compute(self, invoice):
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),
                }
                if invoice.type in ('out_invoice','in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_collected_id']
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_paid_id']
                # key = (val['tax_code_id'], val['base_code_id'], val['account_id'], val['account_analytic_id'])
                key = (val['name'], val['tax_code_id'], val['base_code_id'], val['account_id'], val['account_analytic_id'])

                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])
        return tax_grouped
