from odoo import models, fields

class EstateBooksCategory(models.Model):
	_name = 'estate.books.category'
	_description = 'Estate Books Categories'
	
	name = fields.Char()
	books_id = fields.One2many('estate.books','category')

class EstateBooksRackLocation(models.Model):
	_name = 'estate.books.rack.location'
	_description = 'Estate Books Rack LOcation'
	
	name = fields.Char(required = True)
	racknumber = fields.Integer()
	shelfnumber = fields.Integer()
	books_id = fields.One2many('estate.books','location')

class EstateBooks(models.Model):
	_name = 'estate.books'
	_description = 'Estate Books'
	_sql_constraints = [('UniqueISBN','unique(isbn)','ISBN Needs to be unique')]
	
	name = fields.Char(string="Book Name", default = "",required=True)
	description = fields.Text()
	isbn = fields.Char(string="ISBN(Unique)",copy=False)
	date_published = fields.Date()
	author = fields.Many2many('res.partner')
	publisher = fields.Many2one('res.partner')
	category = fields.Many2one('estate.books.category')
	location = fields.Many2one('estate.books.rack.location')




