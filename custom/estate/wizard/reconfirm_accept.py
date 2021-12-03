from odoo import api,fields,models

class ReconfirmAcceptOffer(models.TransientModel):
    _name = 'wizard.reconfirm.accept.offer'
    _description = 'reconfirmation'

    acceptance = fields.Boolean(string = 'Acceptance', default=False)
    same_offers = fields.Many2one('estate.property')

    def yes_button(self):
        for record in self:
            record.acceptance = True
            print(record.acceptance)

        active_id = self._context.get('active_ids',[])
        offer = self.env['estate.property.offers'].browse(active_id)
        if offer:
            for rec in offer.property_id.offers_ids:
                rec.offer_status = 'reject'
            
            offer.offer_status = 'accept'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.offer_person
