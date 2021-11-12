from odoo import models, fields, api
import datetime
from datetime import timedelta

class EstatePropertyType(models.Model):
	_name = 'estate.property.type'
	_description = 'Estate Property Type'
	
	name = fields.Char(required=True)

class EstatePropertyTag(models.Model):
	_name = 'estate.property.tag'
	_description = 'Estate Property Tag'
	
	name = fields.Char(required=True)
	display = fields.Boolean()

class EstatePropertyOffers(models.Model):
	_name = 'estate.property.offers'
	_description = 'Estate Property Offers'
	
	name = fields.Text()
	offer_person = fields.Many2one('res.partner')
	price = fields.Float()
	offer_date = fields.Date(default = lambda self: fields.Datetime.now(), copy=False)
	offer_status = fields.Selection([('accept','Accepted'),('reject','Rejected')])
	property_id = fields.Many2one('estate.property')
	valid_days = fields.Integer(default = 7)
	valid_till = fields.Date(compute = "_valid_till_date", inverse =  "_inverse_valid_days")

	@api.depends("offer_date","valid_days")
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
	offers_ids = fields.One2many('estate.property.offers','property_id')
	total_area = fields.Integer(compute = "_compute_area")
	best_price = fields.Integer(compute = "_compute_bestprice")
	#store = True can be used as another argument to force store area

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
	
#--
