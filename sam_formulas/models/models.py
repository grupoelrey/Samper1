# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ListaMateriales(models.Model):
    _inherit = 'mrp.bom.line'

    x_porcentaje = fields.Float(string="%", digits=(3, 4))
    x_porcentaje_il = fields.Float(string="% IL", digits=(3, 4))
    x_cantidad_il = fields.Float(string="Cantidad Limitante",  digits=(12,4))


class ListaMaterialesHeader(models.Model):
    _inherit = 'mrp.bom'

    product_qty = fields.Float(string="Cantidad", digits=(12, 4))
    x_cantidad_il = fields.Float(string="Cantidad Limitante", digits=(12, 4))
    x_ingrediente_limitante = fields.Many2one(comodel_name="mrp.bom.line",
                                              string="Ingrediente Limitante",
                                              domain="[('bom_id', '=', bom_id)]")
    

class ReporteInventario(models.Model):
    _inherit = 'stock.quant'
    inventory_quantity = fields.Float(string="Cantidad disponible",  digits=(12,4))


# class sam_formulas(models.Model):
#     _name = 'sam_formulas.sam_formulas'
#     _description = 'sam_formulas.sam_formulas'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
