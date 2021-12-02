# created using ./odoo-bin scaffold estate_account /location/as/required
# -*- coding: utf-8 -*-

from odoo import models, fields, api


#commenting this out since we are trying wizard - have put in base model

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_action(self):
        print('\n\n Button clicked from inherit\n\n')
        
        super(EstateProperty,self).sold_action()
        for record in self:
            vals = {}
            journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
            vals['partner_id'] = record.buyer_id.id
            vals['move_type'] = 'out_invoice'
            vals['journal_id'] = journal.id
            vals['invoice_line_ids'] = [(0,0,{'name':record.name, 'quantity' : 1 , 'price_unit' : record.selling_price})]
            self.env['account.move'].create(vals)


# class estate_account(models.Model):
#     _name = 'estate_account.estate_account'
#     _description = 'estate_account.estate_account'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
