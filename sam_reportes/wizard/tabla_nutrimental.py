# -*- coding: utf-8 -*-

# tabla_nutrimental.py
# Impresión de la tabla nutrimental de un producto.
# VBueno 1603202112:12

# En product.product (y/o product.template) están los porcentajes de proteínas,
# grasa, grasa saturada, humedad, carbohidratos, azúcares y sodio para hacer el
# cálculo en base a cantidad del producto y/o cantidad de ingrediente limitante
# que se capture en el wizard.

import logging
from odoo.tools.float_utils import float_round
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class TablaNutrimental(models.TransientModel):

    _name = 'wizard.tabla.nutrimental'
    _description = 'Tabla Nutrimental'

    producto = fields.Many2one('mrp.bom', string="Producto")
    cantidad = fields.Float(string="Cantidad")
    ing_limitante = fields.Many2one('mrp.bom.line',string="Ingrediente limitante")
    cant_limitante = fields.Float(string="Cantidad limitante")
    pct_merma = fields.Float(string='% Merma')
    consolidado = fields.Boolean(string="Fórmula consolidada", )

    # campos para consolidar
    x_secuencia = fields.Char(string="Número")
    ingr = fields.Many2one('product.product', string="Producto")
    cod_prov = fields.Char(string="Código Prov", required=False, )
    cant_tot = fields.Float(string="Cant Total", digits=(12, 4))
    unidad = fields.Char(string="Unidad")
    pct_formula = fields.Float(string="% Fórmula", digits=(6, 2))
    pct_categoria = fields.Float(string="% Grupo", digits=(6, 2))
    x_orden = fields.Integer(string="Orden", required=False, )

    # estos campos son para consolidar la fórmula
    x_componente = fields.Char(string="Componente", required=False, )
    x_cant_comp = fields.Float(string="Cantidad",  required=False, digits=(8,4) )
    x_pct_proteina = fields.Float(string="% Proteína", required=False, digits=(3, 4))
    x_pct_grasas_tot = fields.Float(string="% Grasas tot", required=False,
                                digits=(3, 2))
    x_pct_grasas_sat = fields.Float(string="% Grasas sat", required=False,
                                digits=(3, 2))
    x_pct_grasas_trans = fields.Float(string="% Grasas trans", required=False,
                                digits=(3, 2))
    x_pct_humedad = fields.Float(string="% Humedad", required=False,
                                digits=(3, 2))
    x_pct_carbs = fields.Float(string="% Carbs", required=False,
                                digits=(3, 2))
    x_pct_azucares = fields.Float(string="% Azúcares", required=False,
                                digits=(3, 2))
    x_mg_sodio = fields.Float(string="mg Sodio", required=False,
                                digits=(5, 4))
    x_proteina_kg = fields.Float(string="kg Proteína", required=False,
                                digits=(4, 4))
    x_grasa_kg = fields.Float(string="kg Grasa", required=False,
                                digits=(4, 4))
    x_grasa_sat_kg = fields.Float(string="kg Grasa sat", required=False,
                                digits=(4, 4))
    x_grasa_trans_kg = fields.Float(string="kg Grasa trans", required=False,
                                digits=(4, 4))
    x_humedad_kg = fields.Float(string="kg Humedad", required=False,
                                  digits=(4, 4))
    x_carbs_kg = fields.Float(string="kg Carbs", required=False,
                                  digits=(4, 4))
    x_azucares_kg = fields.Float(string="kg Azúcares", required=False,
                                  digits=(4, 4))
    x_sodio_mg = fields.Float(string="mg Sodio", required=False,
                                  digits=(4, 4))

    # permite seleccionar el ingrediente limitante.
    @api.onchange('producto')
    def onchange_producto(self):
        nlista = self.producto.id
        self.pct_merma = self.producto.product_tmpl_id.x_pct_merma
        for rec in self:
            return {'domain': {'ing_limitante':
                                   [('bom_id', '=', nlista)]}}


    # imprime la tabla nutrimental.
    def imprime_tabla_nutrimental(self):

        vals = []
        ingredientes1 = self.env['mrp.bom.line'].search(
            [('bom_id.id', '=', self.producto.id)])

        ingredientes = sorted(ingredientes1, key=lambda l: l.product_qty,
                              reverse=True)

        if not self.consolidado: # la fórmula no se consolida

            if not self.ing_limitante:
                for ingrediente in ingredientes:
                    vals.append({
                        'componente': ingrediente.product_id.name,
                        'cant_comp': self.cantidad * (ingrediente.x_porcentaje / 100),
                        'pct_proteina': ingrediente.product_id.x_pct_proteinas,
                        'pct_grasas_tot': ingrediente.product_id.x_pct_grasas_totales,
                        'pct_grasas_sat': ingrediente.product_id.x_pct_grasas_saturadas,
                        'pct_grasas_trans': ingrediente.product_id.x_mgkg_grasas_trans,
                        'pct_humedad': ingrediente.product_id.x_pct_humedad,
                        'pct_carbs': ingrediente.product_id.x_pct_hidratos_de_carbono,
                        'pct_azucares': ingrediente.product_id.x_pct_azucares,
                        'mg_sodio': ingrediente.product_id.x_mg_sodio,
                        'proteina_kg': (ingrediente.product_id.x_pct_proteinas / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'grasa_kg': (ingrediente.product_id.x_pct_grasas_totales / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'grasa_sat_kg': (ingrediente.product_id.x_pct_grasas_saturadas / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'grasa_trans_kg':ingrediente.product_id.x_mgkg_grasas_trans * 10 * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'humedad_kg': (ingrediente.product_id.x_pct_humedad / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'carbs_kg': (ingrediente.product_id.x_pct_hidratos_de_carbono / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'azucares_kg': (ingrediente.product_id.x_pct_azucares / 100) * (self.cantidad * (ingrediente.x_porcentaje / 100)),
                        'sodio_mg': ingrediente.product_id.x_mg_sodio * 10 * (self.cantidad * (ingrediente.x_porcentaje / 100))

                    })

            if self.ing_limitante:
                ncantidad_il = self.ing_limitante.product_qty
                for ingrediente in ingredientes:
                    vals.append({
                        'componente': ingrediente.product_id.name,
                        'cant_comp': self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'pct_proteina': ingrediente.product_id.x_pct_proteinas,
                        'pct_grasas_tot': ingrediente.product_id.x_pct_grasas_totales,
                        'pct_grasas_sat': ingrediente.product_id.x_pct_grasas_saturadas,
                        'pct_grasas_trans': ingrediente.product_id.x_mgkg_grasas_trans,
                        'pct_humedad': ingrediente.product_id.x_pct_humedad,
                        'pct_carbs': ingrediente.product_id.x_pct_hidratos_de_carbono,
                        'pct_azucares': ingrediente.product_id.x_pct_azucares,
                        'mg_sodio': ingrediente.product_id.x_mg_sodio,
                        'proteina_kg': (ingrediente.product_id.x_pct_proteinas / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'grasa_kg': (ingrediente.product_id.x_pct_grasas_totales / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'grasa_sat_kg': (ingrediente.product_id.x_pct_grasas_saturadas / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'grasa_trans_kg': ingrediente.product_id.x_mgkg_grasas_trans * 10 * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'humedad_kg': (ingrediente.product_id.x_pct_humedad / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'carbs_kg': (ingrediente.product_id.x_pct_hidratos_de_carbono / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'azucares_kg': (ingrediente.product_id.x_pct_azucares / 100) * self.cant_limitante * (ingrediente.product_qty / ncantidad_il),
                        'sodio_mg': ingrediente.product_id.x_mg_sodio * 10 * self.cant_limitante * (ingrediente.product_qty / ncantidad_il)
                    })

        if self.consolidado: # se consolida la fórmula.
            nsecuencia = self.env['ir.sequence'].next_by_code(
                'formulas.consolidadas')

            for ingrediente in ingredientes:
                # verifica que el ingrediente se fabrique.
                # las rutas pueden incluir comprar, fabricar, vender, etc.
                subf = 0
                rutas = ingrediente.product_tmpl_id.route_ids
                for ruta in rutas:
                    if ruta.id == 5: # 5 == fabricar
                        subf = 1
                        break

                if subf == 1:
                    ncant_limitante = self.cantidad * (ingrediente.x_porcentaje / 100)

                    bom_pf = self.env['mrp.bom'].search([(
                        'product_tmpl_id','=',ingrediente.product_tmpl_id.id)]).id

                    subformula = self.env['mrp.bom.line'].search([
                        ('bom_id.id', '=', bom_pf)])

                    if not subformula:
                        subf = 0

                    for componente in subformula:
                        ncomponente = self.env['wizard.formulas'].search(
                                [('ingr.id','=', componente.product_id.id),
                                 ('x_secuencia','=',nsecuencia)])

                        if not ncomponente:

                            norden = 0
                            if 'ca' in componente.product_id.default_code:
                                norden = 1
                            elif 'ad' in componente.product_id.default_code:
                                norden = 2
                            elif 'in' in componente.product_id.default_code:
                                norden = 3
                            else:
                                norden = 4

                            self.env['wizard.formulas'].create({
                                'x_secuencia':nsecuencia,
                                'ingr': componente.product_id.id,
                                'cant_tot': ncant_limitante * (componente.x_porcentaje / 100),
                                'unidad': componente.product_id.uom_id.name,
                                'pct_formula': componente.x_porcentaje,
                                'pct_categoria': componente.x_porcentaje_categoria,
                                'x_orden': norden
                            })

                        if ncomponente:
                            ncant = ncomponente.cant_tot
                            ncomponente.write({'cant_tot':(ncant_limitante * (componente.x_porcentaje / 100)) + ncant})




        data = {'ids': self.ids,
                'model':self._name,
                'vals':vals,
                'producto':self.producto.product_tmpl_id.name,
                'codigo': self.producto.product_tmpl_id.default_code,
                'cantidad':self.cantidad,
                'ing_limitante':self.ing_limitante,
                'nombre_il':self.ing_limitante.product_tmpl_id.name,
                'cant_limitante':self.cant_limitante,
                'pct_merma':self.pct_merma
                }

        return self.env.ref('sam_reportes.tabla_nutrimental_reporte').report_action(self, data=data)