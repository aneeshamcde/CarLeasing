# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo import tools
from odoo.exceptions import UserError, ValidationError


class fleet_repair(models.Model):
	_name = 'fleet.repair'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "Car Repair"
	
	name = fields.Char(string='Subject', required=True)
	sequence = fields.Char(string='Sequence', readonly=True ,copy =False)
	client_id = fields.Many2one('res.partner', string='Client', required=True,track_visibility='onchange')
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
	guarantee = fields.Selection(
			  [('yes', 'Yes'), ('no', 'No')], string='Under Guarantee?')
	guarantee_type = fields.Selection(
			[('paid', 'paid'), ('free', 'Free')], string='Guarantee Type')
	service_type = fields.Many2one('service.type', string='Nature of Service')
	user_id = fields.Many2one('res.users', string='Assigned to',track_visibility='onchange')
	priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
	description = fields.Text(string='Notes')
	service_detail = fields.Text(string='Service Details')
	state = fields.Selection([
			('draft', 'Received'),
			('diagnosis', 'In Diagnosis'),
			('diagnosis_complete', 'Diagnosis Complete'),
			('quote', 'Quotation Sent'),
			('saleorder', 'Quotation Approved'),
			('workorder', 'Work in Progress'),
			('work_completed', 'Work Completed'),
			('invoiced', 'Invoiced'),
			('done', 'Done'),
			('cancel', 'Cancelled'),
			], 'Status', default = "draft",readonly=True, copy=False, help="Gives the status of the fleet repairing.", index=True,track_visibility='onchange')
	diagnose_id = fields.Many2one('fleet.diagnose', string='Car Diagnose', copy=False)
	workorder_id = fields.Many2one('fleet.workorder', string='Car Work Order', copy=False)
	sale_order_id = fields.Many2one('sale.order', string='Sales Order', copy=False)
	fleet_repair_line = fields.One2many('fleet.repair.line', 'fleet_repair_id', string="Car Lines")
	workorder_count = fields.Integer(string='Work Orders', compute='_compute_workorder_id')
	dig_count  = fields.Integer(string='Diagnosis Orders', compute='_compute_dignosis_id')
	quotation_count = fields.Integer(string ="Quotations", compute='_compute_quotation_id')
	saleorder_count = fields.Integer(string = "Sale Order", compute='_compute_saleorder_id')
	inv_count = fields.Integer(string = "Invoice")
	confirm_sale_order = fields.Boolean('is confirm')  

	
	def button_view_diagnosis(self):
		list = []
		context = dict(self._context or {})
		dig_order_ids = self.env['fleet.diagnose'].search([('fleet_repair_id', '=', self.id)])           
		for order in dig_order_ids:
			list.append(order.id)
		return {
			'name': _('Car Diagnosis'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.diagnose',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}

	
	def button_view_workorder(self):
		list = []
		context = dict(self._context or {})
		work_order_ids = self.env['fleet.workorder'].search([('fleet_repair_id', '=', self.id)])           
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
		quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'),('fleet_repair_id', '=', self.id)])           
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
		quo_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', self.id)])           
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
		imd = self.env['ir.model.data']
		action = imd.xmlid_to_object('account.action_invoice_tree1')
		list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
		form_view_id = imd.xmlid_to_res_id('account.invoice_form')
		so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', self.id)])
		for order in so_order_ids:
			inv_order_ids = self.env['account.move'].search([('origin', '=',order.name )])            
			if inv_order_ids:
				for order_id in inv_order_ids:
					if order_id.id not in list:
						list.append(order_id.id)
							
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		if len(list) > 1:
			result['domain'] = "[('id','in',%s)]" % list
		elif len(list) == 1:
			result['views'] = [(form_view_id, 'form')]
			result['res_id'] = list[0]
		else:
			result = {'type': 'ir.actions.act_window_close'}
		return result
	
	
	@api.depends('workorder_id')
	def _compute_workorder_id(self):
		for order in self:
			work_order_ids = self.env['fleet.workorder'].search([('fleet_repair_id', '=', order.id)])            
			order.workorder_count = len(work_order_ids)

	
	@api.depends('diagnose_id')
	def _compute_dignosis_id(self):
		for order in self:
			dig_order_ids = self.env['fleet.diagnose'].search([('fleet_repair_id', '=', order.id)])            
			order.dig_count = len(dig_order_ids)

	
	@api.depends('sale_order_id')
	def _compute_quotation_id(self):
		for order in self:
			quo_order_ids = self.env['sale.order'].search([('state', '=', 'draft'),('fleet_repair_id', '=', order.id)])            
			order.quotation_count = len(quo_order_ids)
	
	
	@api.depends('confirm_sale_order')
	def _compute_saleorder_id(self):
		for order in self:
			order.quotation_count = 0
			so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', order.id)])            
			order.saleorder_count = len(so_order_ids)

	
	@api.depends('state')
	def _compute_invoice_id(self):
		count  = 0 
		if self.state== 'invoiced': 
			for order in self:
				so_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('fleet_repair_id', '=', order.id)])
				for order in so_order_ids:
					inv_order_ids = self.env['account.move'].search([('origin', '=',order.name )])            
					if inv_order_ids:
						self.inv_count = len(inv_order_ids)
	
	_order = 'id desc'

	@api.model
	def default_get(self,fields):
		res = super(fleet_repair, self).default_get(fields)
		res['sequence'] = self.env['ir.sequence'].next_by_code('fleet.repair')
		res['receipt_date'] = datetime.now()
		return res

	
	def diagnosis_created(self):
		self.write({'state':'diagnosis'})

	
	def quote_created(self):
		self.write({'state':'quote'})

	
	def order_confirm(self):
		self.write({'state':'saleorder'})

	
	def fleet_confirmed(self):
		self.write({'state':'confirm'})

	
	def workorder_created(self):
		self.write({'state':'workorder'})

	@api.onchange('client_id')
	def onchange_partner_id(self):
		addr = {}
		if self.client_id:
			addr = self.client_id.address_get(['contact'])
			addr['client_phone'] = self.client_id.phone
			addr['client_mobile'] = self.client_id.mobile
			addr['client_email'] = self.client_id.email
		return {'value': addr}

	
	def action_create_fleet_diagnosis(self):
		Diagnosis_obj = self.env['fleet.diagnose']
		fleet_line_obj = self.env['fleet.repair.line']
		repair_obj = self.env['fleet.repair'].browse(self._ids[0])
		mod_obj = self.env['ir.model.data']
		act_obj = self.env['ir.actions.act_window']
		if not repair_obj.fleet_repair_line:
			raise Warning('You cannot create Car Diagnosis without Cars.')
		
		diagnose_vals = {
			'service_rec_no': repair_obj.sequence,
			'name': repair_obj.name,
			'priority': repair_obj.priority,
			'receipt_date': repair_obj.receipt_date,
			'client_id': repair_obj.client_id.id,
			'contact_name': repair_obj.contact_name,
			'phone': repair_obj.phone,
			'client_phone': repair_obj.client_phone,
			'client_mobile': repair_obj.client_mobile,
			'client_email': repair_obj.client_email,
			'fleet_repair_id': repair_obj.id,
			'state': 'draft',
		}
		diagnose_id = Diagnosis_obj.create(diagnose_vals)
		for line in repair_obj.fleet_repair_line:
			fleet_line_vals = {
				'fleet_id': line.fleet_id.id,
				'license_plate': line.license_plate,
				'vin_sn': line.vin_sn,
				'fuel_type': line.fuel_type,
				'model_id': line.model_id.id,
				'service_type': line.service_type.id,
				'guarantee': line.guarantee,
				'guarantee_type':line.guarantee_type,
				'service_detail': line.service_detail,
				'diagnose_id': diagnose_id.id,
				'state': 'diagnosis',
				'source_line_id': line.id,
			}
			fleet_line_obj.create(fleet_line_vals)
			line.write({'state': 'diagnosis'})
		
		self.write({'state': 'diagnosis', 'diagnose_id': diagnose_id.id})
		result = mod_obj.get_object_reference('car_repair_industry', 'action_fleet_diagnose_tree_view')
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj.get_object_reference('car_repair_industry', 'view_fleet_diagnose_form')
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = diagnose_id.id or False
		return result

	
	def action_print_receipt(self):
		assert len(self._ids) == 1, 'This option should only be used for a single id at a time'
		return self.env.ref('car_repair_industry.fleet_repair_receipt_id').report_action(self)

	
	def action_print_label(self):
		if not self.fleet_repair_line:
			raise UserError(_('You cannot print report without Car details'))

		assert len(self._ids) == 1, 'This option should only be used for a single id at a time'
		#return self.env['report'].get_action(self._ids[0],'car_repair_industry.machi_rep_label_temp_id')
		return self.env.ref('car_repair_industry.fleet_repair_label_id').report_action(self)

	
	def action_view_quotation(self):
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

	
	
	def action_view_work_order(self):
		mod_obj = self.env['ir.model.data']
		act_obj = self.env['ir.actions.act_window']
		work_order_id = self.workorder_id.id
		result = mod_obj.get_object_reference('car_repair_industry', 'action_fleet_workorder_tree_view')
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj.get_object_reference('car_repair_industry', 'view_fleet_workorder_form')
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = work_order_id or False
		return result


class service_type(models.Model):
	_name = 'service.type'
	_description = "Service Type"

	name = fields.Char(string='Name')


class fleet_repair_line(models.Model):
	_name = 'fleet.repair.line'
	_description = "Fleet repair line"


	fleet_id = fields.Many2one('fleet.vehicle','Car')
	license_plate = fields.Char('License Plate', help='License plate number of the vehicle (ie: plate number for a car)')
	vin_sn= fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)')
	model_id= fields.Many2one('fleet.vehicle.model', 'Model', help='Model of the vehicle')
	fuel_type= fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle')
	guarantee= fields.Selection(
			[('yes', 'Yes'), ('no', 'No')], string='Under Guarantee?')
	guarantee_type= fields.Selection(
			[('paid', 'paid'), ('free', 'Free')], string='Guarantee Type')
	service_type= fields.Many2one('service.type', string='Nature of Service')
	fleet_repair_id= fields.Many2one('fleet.repair', string='Car.', copy=False)
	service_detail= fields.Text(string='Service Details')
	diagnostic_result= fields.Text(string='Diagnostic Result')
	diagnose_id= fields.Many2one('fleet.diagnose', string='Car Diagnose', copy=False)
	workorder_id= fields.Many2one('fleet.workorder', string='Car Work Order', copy=False)
	source_line_id= fields.Many2one('fleet.repair.line', string='Source')
	est_ser_hour= fields.Float(string='Estimated Sevice Hours')
	service_product_id= fields.Many2one('product.product', string='Service Product')
	service_product_price= fields.Float('Service Product Price')
	spare_part_ids= fields.One2many('spare.part.line', 'fleet_id', string='Spare Parts Needed')
	state= fields.Selection([
			('draft', 'Draft'),
			('diagnosis', 'In Diagnosis'),
			('done', 'Done'),
			], 'Status', default="draft", readonly=True, copy=False, help="Gives the status of the fleet Diagnosis.", index=True)

	_rec_name = 'fleet_id'
	

	
	def name_get(self):
		if not self._ids:
			return []
		if isinstance(self._ids, (int, int)):
					ids = [self._ids]
		reads = self.read(['fleet_id', 'license_plate'])
		res = []
		for record in reads:
			name = record['license_plate']
			if record['fleet_id']:
				name = record['fleet_id'][1]
			res.append((record['id'], name))
		return res
		

	
	def action_add_fleet_diagnosis_result(self):
		for obj in self:
			self.write({'state': 'done'})
		return True
		
	@api.model
	def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
		res = super(fleet_repair_line,self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
		return res

	@api.onchange('fleet_id')
	def onchange_fleet_id(self):
		addr = {}
		if self.fleet_id:
			fleet = self.fleet_id
			addr['license_plate'] = fleet.license_plate
			addr['vin_sn'] = fleet.vin_sn
			addr['fuel_type'] = fleet.fuel_type
			addr['model_id'] = fleet.model_id.id
		return {'value': addr}


class fleet_repair_analysis(models.Model):
	_name = 'fleet.repair.analysis'
	_description = "Fleet repair analysis"
	_order = 'id desc'

	id = fields.Integer('fleet Id', readonly=True)
	sequence =fields.Char(string='Sequence', readonly=True)
	receipt_date = fields.Date(string='Date of Receipt', readonly=True)
	state = fields.Selection([
			('draft', 'Received'),
			('diagnosis', 'In Diagnosis'),
			('diagnosis_complete', 'Diagnosis Complete'),
			('quote', 'Quotation Sent'),
			('saleorder', 'Quotation Approved'),
			('workorder', 'Work in Progress'),
			('work_completed', 'Work Completed'),
			('invoiced', 'Invoiced'),
			('done', 'Done'),
			('cancel', 'Cancelled'),
			], 'Status', readonly=True, copy=False, help="Gives the status of the fleet repairing.", index=True)
	client_id = fields.Many2one('res.partner', string='Client', readonly=True)
		

	

