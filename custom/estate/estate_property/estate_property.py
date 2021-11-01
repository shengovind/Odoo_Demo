from odoo import models, fields

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