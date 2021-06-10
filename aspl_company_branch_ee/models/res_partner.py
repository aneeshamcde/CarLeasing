# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user_rec = self.env['res.users'].sudo().browse(self._uid).branch_ids.ids
        new_args = []
        if user_rec:
            sql = """SELECT id FROM res_partner
                    WHERE branch_id in %s""" % (" (%s) " % ','.join(map(str, user_rec)))
            self._cr.execute(sql)
            result = self._cr.fetchall()
            rec = [each[0] for each in result]
            args += ['|', ('id', 'in', rec), ('branch_id', '=', False)]
            return super(ResPartner, self).search(args=args, offset=offset, limit=limit,
                                                  order=order, count=count)
        return super(ResPartner, self).search(args=args, offset=offset, limit=limit,
                                              order=order, count=count)

    branch_id = fields.Many2one('company.branch', string="Branch",
                                default=lambda self: self.env.user.branch_id)
