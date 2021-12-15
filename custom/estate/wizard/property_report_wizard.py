from odoo import api,fields,models

class ReportPropertyWizard(models.TransientModel):
    _name = 'wizard.property.report'
    _description = 'Property Report Wizard'

    price = fields.Float("Price")
    
    def wizard_print_button(self):
        # allids = self.env['estate.property'].id
        # print(allids)

        #SELF ref is used to pull xml id
        allids = self.env['estate.property'].search([('expected_price','>=',self.price)]).ids
        return self.env.ref('estate.estate_property_report').report_action(allids)
