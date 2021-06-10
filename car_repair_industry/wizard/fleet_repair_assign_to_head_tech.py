# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class fleet_repair_assign_to_head_tech(models.TransientModel):
	_name = 'fleet.repair.assignto.headtech'
	_description = "Fleet diagnose assignto Head Technician"
	
	user_id = fields.Many2one('res.users', string='Head Technician', required=True)

	def do_assign_ht(self):
		if self.user_id and self._context.get('active_id'):
			self.pool.get('fleet.repair').write(self._context.get('active_id'), {'user_id': self.user_id.id, 'state': 'confirm'})
		return {'type': 'ir.actions.act_window_close'}
