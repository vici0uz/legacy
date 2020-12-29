# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier, Bessi Nicolas, Vincent Renaville
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import osv, orm, fields
from clint.textui import colored


class product_template(osv.osv):
    """TMP fix of bug 1111430"""
    _inherit = 'product.template'
    # _rec_name = 'code_uni'
    def capitalizar(self, cr, uid, ids, name):
        if name:
            result = {
                'value': {
                    'name': str(name).upper()
                }
            }
            return result

    _columns = {
        'purchase_ok': fields.boolean('Can be Purchased',
                                      help=("Specify if the product can be selected"
                                            " in a purchase order line."))
        }
    # _sql_constraints = [
    #     ('code_uni_uniq', 'unique(code_uni)', 'The Code Number of the partner must be unique')
    #     ]


# class product_product(osv.osv):
#     inherit = "product.product"
#     # _rec_name = 'product_tmpl_id_code_uni'
#     _columns = {
#         'product_tmpl_id_code_uni': fields.related('product_tmpl_id', 'code_uni', type="char", string="Code")
#     }

#     def name_get(self, cr, user, ids, context=None):
#         print colored.red("HOlassssss")
#     # def name_get(self, cr, user, ids, context=None):
#     #     print colored.cyan('llegue perras')
#     #     if context is None:
#     #         context = {}
#     #     if isinstance(ids, (int, long)):
#     #         ids = [ids]
#     #     if not len(ids):
#     #         return []
#     #     def _name_get(d):
#     #         name = d.get('name','')
#     #         code = d.get('default_code',False)
#     #         # Vivek
#     #         part_number = d.get('part_number',False)
#     #         if part_number:
#     #             name = '%s-%s' % (name,part_number)
#     #         #End
#     #         elif code:
#     #             name = '[%s] %s' % (code,name)
#     #         elif d.get('variants'):
#     #             name = name + ' - %s' % (d['variants'],)
#     #         return (d['id'], name)

#     #     partner_id = context.get('partner_id', False)

#     #     result = []
#     #     for product in self.browse(cr, user, ids, context=context):
#     #         sellers = filter(lambda x: x.name.id == partner_id, product.seller_ids)
#     #         # Vivek
#     #         prd_temp = self.pool.get('product.template').browse(cr, user, product.id, context=context)
#     #         # End
#     #         if sellers:
#     #             for s in sellers:
#     #                 mydict = {
#     #                           'id': product.id,
#     #                           'name': s.product_name or product.name,
#     #                           #vivek
#     #                           'part_number': prd_temp.part_number,
#     #                           #End
#     #                           'default_code': s.product_code or product.default_code,
#     #                           'variants': product.variants
#     #                           }
#     #                 result.append(_name_get(mydict))
#     #         else:
#     #             mydict = {
#     #                       'id': product.id,
#     #                       'name': product.name,
#     #                       #vivek
#     #                       'part_number': prd_temp.part_number,
#     #                       #End
#     #                       'default_code': product.default_code,
#     #                       'variants': product.variants
#     #                       }
#     #             result.append(_name_get(mydict))
#     #     return result

#     # def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
#     #     print colored.red('Laydies')
#     #     if not args:
#     #         args = []
#     #     if name:
#     #         ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
#     #         if not ids:
#     #             ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
#     #         if not ids:
#     #             # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
#     #             # on a database with thousands of matching products, due to the huge merge+unique needed for the
#     #             # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
#     #             # Performing a quick memory merge of ids in Python will give much better performance
#     #             ids = set()
#     #             ids.update(self.search(cr, user, args + [('default_code',operator,name)], limit=limit, context=context))
#     #             if not limit or len(ids) < limit:
#     #                 # we may underrun the limit because of dupes in the results, that's fine
#     #                 ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
#     #                 # vivek
#     #                 # Purpose  : To filter the product by using part_number
#     #                 ids.update(self.search(cr, user, args + [('part_number',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
#     #                 #End
#     #             ids = list(ids)
#     #         if not ids:
#     #             ptrn = re.compile('(\[(.*?)\])')
#     #             res = ptrn.search(name)
#     #             if res:
#     #                 ids = self.search(cr, user, [('default_code','=', res.group(2))] + args, limit=limit, context=context)
#     #     else:
#     #         ids = self.search(cr, user, args, limit=limit, context=context)
#     #     result = self.name_get(cr, user, ids, context=context)
#     #     return result
#     # # def name_get(self, cr, user, ids, context=None):
#     #     print colored.cyan('putillas')
#     #     if context is None:
#     #         context = {}
#     #     if isinstance(ids, (int, long)):
#     #         ids = [ids]
#     #     if not len(ids):
#     #         return []

#     #     def _name_get(d):
#     #         name = d.get('name','')
#     #         code = context.get('display_product_tmpl_id_code_uni', True) and d.get('product_tmpl_id_code_uni',False) or False
#     #         if code:
#     #             name = '[%s] %s' % (code,name)
#     #         return (d['id'], name)

#     #     partner_id = context.get('partner_id', False)
#     #     if partner_id:
#     #         partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
#     #     else:
#     #         partner_ids = []

#     #     # all user don't have access to seller and partner
#     #     # check access and use superuser
#     #     self.check_access_rights(cr, user, "read")
#     #     self.check_access_rule(cr, user, ids, "read", context=context)

#     #     result = []
#     #     for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
#     #         variant = ", ".join([v.name for v in product.attribute_value_ids])
#     #         name = variant and "%s (%s)" % (product.name, variant) or product.name
#     #         sellers = []
#     #         if partner_ids:
#     #             sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
#     #         if sellers:
#     #             for s in sellers:
#     #                 seller_variant = s.product_name and (
#     #                     variant and "%s (%s)" % (s.product_name, variant) or s.product_name
#     #                     ) or False
#     #                 mydict = {
#     #                           'id': product.id,
#     #                           'name': seller_variant or name,
#     #                           'product_tmpl_id_code_uni': s.product_code or product.product_tmpl_id_code_uni,
#     #                           }
#     #                 result.append(_name_get(mydict))
#     #         else:
#     #             mydict = {
#     #                       'id': product.id,
#     #                       'name': name,
#     #                       'product_tmpl_id_code_uni': product.product_tmpl_id_code_uni,
#     #                       }
#     #             result.append(_name_get(mydict))
#     #     return result
# product_product()
