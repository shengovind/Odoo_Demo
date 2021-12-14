from odoo import api,fields,models

class ReportPropertyWizard(models.TransientModel):
    _name = 'wizard.property.report'
    _description = 'Property Report Wizard'

    price = fields.Float("Price")
    
    def wizard_print_button(self):
        # allids = self.env['estate.property'].id
        # print(allids)

        #SELF ref is used to pull xml id
        allids = [i.id for i in self.env['estate.property'].search([('expected_price','>=',self.price)])]
        print(allids)
        print(self.env.context)
        return self.env.ref('estate.estate_property_report').report_action(self,allids)