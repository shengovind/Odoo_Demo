from odoo import models, fields

class EstateBooks(models.Model):
	_name = 'estate.books'
	_description = 'Estate Books'
	
	name = fields.Char(string="Book Name", default = "",required=True)
	description = fields.Text()
	isbn = fields.Char(copy=False)
	date_published = fields.Date()
