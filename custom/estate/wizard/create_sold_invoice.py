from odoo import api,fields,models

class CreateSoldInvoice(models.TransientModel):
    _name = 'wizard.create.sold.invoice'
    _description = 'creates sold invoice wizard on click'

    partner_id = fields.Many2one('res.partner')

    def make_invoice(self):
        print("\n\n make invoice called from wizard\n\n")
        print(self.partner_id.name)
        print(self._context.get('active_ids',[]))
        active_id = self._context.get('active_ids',[])
        property = self.env['estate.property'].browse(active_id)
        if property:
            vals = {}
            journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
            vals['partner_id'] = self.partner_id
            vals['move_type'] = 'out_invoice'
            vals['journal_id'] = journal.id
            vals['invoice_line_ids'] = [(0,0,{'name':property.name, 'quantity' : 1 , 'price_unit' : property.selling_price}),
            (0,0,{'name':'comission', 'quantity' : 1 , 'price_unit' : property.selling_price*6/100})
            ]
            self.env['account.move'].create(vals)
