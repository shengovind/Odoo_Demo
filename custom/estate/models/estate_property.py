from odoo import models, fields, api
import datetime
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [(('UniqueName','unique(name)','Name to be unique'))]
    
    name = fields.Char(required=True)
    property_id = fields.One2many('estate.property','estate_property_type_id')
    offer_ids = fields.One2many('estate.property.offers','property_type_id') #Related fieldthat is used to show how many offers each property type has - the two which are not linked
    offer_count = fields.Integer(compute ='_compute_offer_count')

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [(('UniqueName','unique(name)','Tag Name to be unique'))]
    
    name = fields.Char(required=True)
    display = fields.Boolean()
    color = fields.Integer()

class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = 'Estate Property Offers'
    _order = "price desc"
    
    name = fields.Text()
    offer_person = fields.Many2one('res.partner')
    price = fields.Float()
    offer_date = fields.Date(default = lambda self: fields.Datetime.now(), copy=False)
    offer_status = fields.Selection([('accept','Accepted'),('reject','Rejected')])
    property_id = fields.Many2one('estate.property')
    valid_days = fields.Integer(default = 7)
    valid_till = fields.Date(compute = "_valid_till_date", inverse =  "_inverse_valid_days")
    property_type_id = fields.Many2one(related="property_id.estate_property_type_id",store=True)
    #^^^^ THis is a related field that is used to show how many offers each property type has - the two which 
    # ....  do not have direct link

    #global methods that will be called using buttons
    #this shows how a many to one mapped object can change the one to many object value using mapped id
    #this also shows how one can reference other records in the same list
    def offer_status_accept_action(self):
        for record in self:
            # if record.offer_status == 'reject':
            # 	raise UserError("Rejected once cannot be accepted again")
            #Better to write the above in onchane - since this gets called only when button is clicked
            #whereas it can be changed from the base model too
            
            record.offer_status = 'accept'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.offer_person

    def offer_status_reject_action(self):
        for record in self:
            # if record.offer_status == 'accept':
            # 	raise UserError("Accepted once cannot be rejected")
            #Better to write the above in onchane - since this gets called only when button is clicked
            #whereas it can be changed from the base model too
            record.offer_status = 'reject'

    @api.depends("offer_date","valid_days")
    # _ start since it is internally called method
    def _valid_till_date(self):
        print("\n\n _valid_till_date called")
        #This print is only to check the call in command prompt. To see what happens when store=True is used"
        for record in self:
            record.valid_till = record.offer_date + datetime.timedelta(days=record.valid_days)

    @api.depends("offer_date","valid_till")
    def _inverse_valid_days(self):
        print("\n\n _inverse_valid_days called")
        #This print is only to check the call in command prompt. To see what happens when store=True is used"
        for record in self:
            days = record.valid_till - record.offer_date
            record.valid_days = days.days

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"
    
    name = fields.Char(string="Main Name", default = "",required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_oritntation = fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')])
    active = fields.Boolean(default = True)	
    estate_property_type_id = fields.Many2one('estate.property.type')
    employee_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    property_tag_id = fields.Many2many('estate.property.tag', domain="[('display','=',True)]")
    # tag_show = fields.Selection([('all','All'),('select','Only True')],default='all')
    # ^^ was me trying to show dropdown for property tag basd on dynamic domain
    offers_ids = fields.One2many('estate.property.offers','property_id')
    total_area = fields.Integer(compute = "_compute_area")
    best_price = fields.Integer(compute = "_compute_bestprice")
    #store = True can be used as another argument to force store area
    state = fields.Selection([('new','New'),('sold','Sold'),('cancel','Cancel')],default='new')

    @api.depends("living_area","garden_area")
    def _compute_area(self):
        print("\n\n Compute area called")
        #This print is only to check the call in command prompt. To see what happens when store=True is used"
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids.price")
    def _compute_bestprice(self):
        for record in self:
            maxprice = 0

            for offers in record.offers_ids:
                if offers.price > maxprice:
                    maxprice = offers.price

            record.best_price = maxprice

    @api.onchange("garden")
    def _onchange_garden(self):
        print("\n\n _onchange_garden called")
        #This print is only to check the call in command prompt. To see what happens when store=True is used"
        for record in self:
            if record.garden:
                record.garden_area = 10
            else:
                record.garden_area = 0
    
    # # This is to add a dynamic domain filter based on another field
    # @api.onchange("tag_show")
    # def _onchange_tag_show(self):
    # 	print("\n\n _onchange_tag_show called")
    
    # 	for record in self:
    # 		b = ''
    # 		if record.tag_show == 'all':
    # 			b = "[('display','=',True),'|',('display','=',False]"
    # 		else:
    # 			b = "[('display','=',True)]"
            
    # 		return b
#--

    def sold_action(self):
        print("\n\n Sold action clicked")
        #shows how exceptions can be raised
        #shows how 
        for record in self:
            if record.state == 'cancel':
                raise UserError("Cannot sell cancelled property")	
            record.state = 'sold'

    def cancel_action(self):
        print("\n\n Cancel action clicked")
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot cancel sold property")
            record.state = 'cancel'

    @api.constrains('living_area','garden_area')
    #this is how python constraints are written. Sql is performance wise better.
    def _check_garden_area(self):
        for record in self:
            if record.garden_area > record.living_area:
                raise ValidationError("Garden Area cannot be more than Living area")

