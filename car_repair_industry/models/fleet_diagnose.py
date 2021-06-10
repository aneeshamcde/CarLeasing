# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError, ValidationError


class fleet_diagnose(models.Model):
	_name = 'fleet.diagnose'
	_inherit = ['mail.thread']
	_description = "Fleet diagnose"
	
	name =  fields.Char(string='Subject', required=True)
	service_rec_no = fields.Char(string='Receipt No', readonly=True, copy=False)
	client_id = fields.Many2one('res.partner', string='Client', required=True)
	client_phone = fields.Char(string='Phone')
	client_mobile = fields.Char(string='Mobile')
	client_email = fields.Char(string='Email')
	receipt_date = fields.Date(string='Date of Receipt')
	contact_name = fields.Char(string='Contact Name')
	phone = fields.Char(string='Contact Number')
	fleet_id = fields.Many2one('fleet.vehicle','Car')
	license_plate = fields.Char('License Plate', help='License plate number of the vehicle (ie: plate number for a car)')
	vin_sn = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)')
	model_id = fields.Many2one('fleet.vehicle.model', 'Model', help='Model of the vehicle')
	fuel_type = fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle')
	service_type = fields.Many2one('service.type', string='Nature of Service')
	user_id = fields.Many2one('res.users', string='Technician')
	priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
	description = fields.Text(string='Fault Description')
	spare_part_ids = fields.One2many('spare.part.line', 'diagnose_id', string='Spare Parts Needed')
	est_ser_hour = fields.Float(string='Estimated Sevice Hours')
	service_product_id = fields.Many2one('product.product', string='Service Product')
	service_product_price = fields.Integer('Service Product Price')
	fleet_repair_id = fields.Many2one('fleet.repair', string='Source', copy=False)
	sale_order_id = fields.Many2one('sale.order', string='Sales Order', copy=False)
	state = fields.Selection([
			('draft', 'Draft'),
			('in_progress', 'In Progress'),
			('done', 'Complete'),
			], 'Status', default="draft", readonly=True, copy=False, help="Gives the status of the fleet Diagnosis.", index=True)
	fleet_repair_line = fields.One2many('fleet.repair.line', 'diagnose_id', string="fleet Lines")
	fleet_repair_count = fields.Integer(string='Repair Orders', compute='_compute_repair_id')
	workorder_count = fields.Integer(string='Work Orders', compute='_compute_workorder_id')
	is_workorder_created = fields.Boolean(string="Workorder Created")
	confirm_sale_order = fields.Boolean(string="confirm sale order")
	is_invoiced = fields.Boolean(string="invoice Created", default=False)
	quotation_count = fields.Integer(string="Quotations", compute='_compute_quotation_id')
	saleorder_count = fields.Integer(string="Sale Order", compute='_compute_saleorder_id')
	inv_count = fields.Integer(string="Invoice")
	
	_order = 'id desc'

	@api.depends('fleet_repair_id')
	def _compute_repair_id(self):
		for diagnose in self:
			repair_order_ids = self.env['fleet.repair'].search([('diagnose_id', '=', diagnose.id)])            
			diagnose.fleet_repair_count = len(repair_order_ids)

	
	@api.depends('is_workorder_created')
	def _compute_workorder_id(self):
		for diagnose in self:
			work_order_ids = self.env['fleet.workorder'].search([('diagnose_id', '=', diagnose.id)])            
			diagnose.workorder_count = len(work_order_ids)

	
	@api.depends('sale_order_id')
	def _compute_quotation_id(self):
		for diagnose in self:
			quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'), ('diagnose_id.id', '=', diagnose.id)])            
			diagnose.quotation_count = len(quo_order_ids)
	
	
	@api.depends('confirm_sale_order')
	def _compute_saleorder_id(self):
		for diagnose in self:
			diagnose.quotation_count = 0
			so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'), ('diagnose_id.id', '=', diagnose.id)])            
			diagnose.saleorder_count = len(so_order_ids)

	
	@api.depends('is_invoiced')
	def _compute_invoice_id(self):
		count = 0 
		for diagnose in self:
			so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'), ('diagnose_id.id', '=', diagnose.id)])
			for order in so_order_ids:
				inv_order_ids = self.env['account.move'].search([('origin', '=', diagnose.name)])            
				if inv_order_ids:
					self.inv_count = len(inv_order_ids)         
 
 
	
	def button_view_repair(self):
		list = []
		context = dict(self._context or {})
		repair_order_ids = self.env['fleet.repair'].search([('diagnose_id', '=', self.id)])         
		for order in repair_order_ids:
			list.append(order.id)
		return {
			'name': _('Car Repair'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.repair',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}


	
	def button_view_workorder(self):
		list = []
		context = dict(self._context or {})
		work_order_ids = self.env['fleet.workorder'].search([('diagnose_id', '=', self.id)])           
		for order in work_order_ids:
			list.append(order.id)
		return {
			'name': _('Car Work Order'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.workorder',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}

	
	def button_view_quotation(self):
		list = []
		context = dict(self._context or {})
		quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'),('diagnose_id', '=', self.id)])           
		for order in quo_order_ids:
			list.append(order.id)
		return {
			'name': _('Sale'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'sale.order',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}
  
	
	def button_view_saleorder(self):
		list = []
		context = dict(self._context or {})
		quo_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('diagnose_id', '=', self.id)])           
		for order in quo_order_ids:
			list.append(order.id)
		return {
			'name': _('Sale'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'sale.order',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}
 
	
	def button_view_invoice(self):
		list = []
		inv_list  = []
		so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('diagnose_id', '=', self.id)])
		for order in so_order_ids:
			inv_order_ids = self.env['account.move'].search([('origin', '=',order.name )])            
			if inv_order_ids:
				for order_id in inv_order_ids:
					if order_id.id not in list:
						list.append(order_id.id)
							

		context = dict(self._context or {})
		return {
			'name': _('Invoice '),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'account.move',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}

	
	def button_in_progress(self):
		self.write({'state': 'in_progress'})

	
	def button_done(self):
		self.write({'state':'done'})

	
	def button_cancel(self):
		self.write({'state':'cancel'})

	
	def button_draft(self):
		self.write({'state':'draft'})

	@api.onchange('client_id')
	def onchange_partner_id(self):
		addr = {}
		if self.client_id:
			addr = self.pool.get('res.partner').address_get([self.client_id.id], ['contact'])
		return {'value': addr}

	
	def action_create_quotation(self):
		repair_obj = self.env['fleet.repair']
		mod_obj = self.env['ir.model.data']
		product_obj = self.env['product.product']
		act_obj = self.env['ir.actions.act_window']
		service_hour = 0.0
		counter = 0
		for fleet_line in self.fleet_repair_line:
			if fleet_line.spare_part_ids:
				counter += 1
		quote_vals = {
			'partner_id': self.client_id.id or False,
			'state': 'draft',
			'client_order_ref': self.name,
			'diagnose_id': self.id,
			'fleet_repair_id': self.fleet_repair_id.id,
		}
		order_id = self.env['sale.order'].create(quote_vals)
		if self.fleet_repair_id:
			id = self.fleet_repair_id.id
			self.fleet_repair_id.write({'state': 'diagnosis_complete', 'sale_order_id': order_id.id})
		for fleet_line in self.fleet_repair_line:
			if fleet_line.guarantee == 'no' or fleet_line.guarantee == 'yes':
				service_hour += fleet_line.est_ser_hour
				if service_hour != 0.0:
					service_line_vals = {
						'product_id': fleet_line.service_product_id.id,
						'name': fleet_line.service_product_id.name,
						'product_uom_qty': service_hour,
						'product_uom': fleet_line.service_product_id.uom_id.id,
						'price_unit' : fleet_line.service_product_price,
						'order_id': order_id.id,
						'car_model' : fleet_line.model_id.name,
						'license_plate' : fleet_line.license_plate,
					}
					self.env['sale.order.line'].create(service_line_vals)
		for fleet_line in self.fleet_repair_line:
			if fleet_line.guarantee == 'yes':
				for part_line in fleet_line.spare_part_ids:
					line_vals = {
						'product_id': part_line.product_id.id,
						'name': part_line.product_id.name,
						'product_uom_qty': part_line.quantity,
						'product_uom': part_line.product_id.uom_id.id,
						'price_unit' : part_line.price_unit,
						'order_id': order_id.id,
						'car_model' : fleet_line.model_id.name,
						'license_plate' : fleet_line.license_plate,
					}
					self.env['sale.order.line'].create(line_vals)
			elif fleet_line.guarantee == 'no':
				for part_line in fleet_line.spare_part_ids:
					line_vals = {
						'product_id': part_line.product_id.id,
						'name': part_line.product_id.name,
						'product_uom_qty': part_line.quantity,
						'product_uom': part_line.product_id.uom_id.id,
						'price_unit' : part_line.price_unit,
						'order_id': order_id.id,
						'car_model' : fleet_line.model_id.name,
						'license_plate' : fleet_line.license_plate,
					}
					self.env['sale.order.line'].create(line_vals)
		result = mod_obj.get_object_reference('sale', 'action_orders')
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj.get_object_reference('sale', 'view_order_form')
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = order_id.id or False
		self.write({'sale_order_id': order_id.id, 'state': 'done'})
		return result
		
	
	def action_view_sale_order(self):
		mod_obj = self.env['ir.model.data']
		act_obj = self.env['ir.actions.act_window']
		order_id = self.sale_order_id.id
		result = mod_obj.get_object_reference('sale', 'action_orders')
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj.get_object_reference('sale', 'view_order_form')
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = order_id or False
		return result
		

	
	def action_view_fleet_repair(self):
		mod_obj = self.env['ir.model.data']
		act_obj = self.env['ir.actions.act_window']
		repair_id = self.fleet_repair_id.id
		result = mod_obj.get_object_reference('car_repair_industry', 'action_fleet_repair_tree_view')
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj.get_object_reference('car_repair_industry', 'view_fleet_repair_form')
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = repair_id or False
		return result

		
class spare_part_line(models.Model):
	_name = 'spare.part.line'
	_description = "Fleet diagnose"

	product_id = fields.Many2one('product.product', string='Product', required=True)
	name = fields.Char(string='Description')
	default_code = fields.Char(string='Product Code')
	uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
	quantity = fields.Float(string='Quantity', required=True)
	price_unit = fields.Float(string='Unit Price')
	diagnose_id = fields.Many2one('fleet.diagnose', string='fleet Diagnose')
	workorder_id = fields.Many2one('fleet.workorder', string='fleet Workorder')
	fleet_id = fields.Many2one('fleet.repair.line', string='Fleet')
		
	
	@api.onchange('product_id')
	def onchange_product_id(self):
		res = {}
		product_obj = self.env['product.product']
		if self.product_id:
			res = {'default_code': self.product_id.default_code,'price_unit': self.product_id.lst_price}
		return {'value': res}

