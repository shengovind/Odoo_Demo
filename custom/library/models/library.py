from odoo import models, fields, api

class Books(models.Model):
    _name = 'library.books'
    _description = 'Library Books Model'
    _sql_constraints = [('UniqueISBN','unique(isbn)','ISBN to be unique')]

    name = fields.Char(compute='_full_book_name',store=True)
    bookname = fields.Char(required=True, string='Book Name')
    isbn = fields.Char(required=True, string='ISBN')
    edition = fields.Char(required=True, string='Book Edition')
    copies_id = fields.One2many('library.books.copies','books_id')

    @api.onchange('bookname','isbn','edition')
    def _full_book_name(self):
        for record in self:
            if record.bookname == False or record.isbn == False or record.edition == False:
                record.name = ""
            else:    
                record.name = str(record.bookname) + " - (" + str(record.isbn) + ") - " + str(record.edition)


class BooksCopies(models.Model):
    _name = 'library.books.copies'
    _description = 'Library Books Copies Model'
    _sql_constraints = [('UniqueReference','unique(name)','Reference to be unique')]

    name = fields.Integer('Unique Reference',required=True, copy=False)
    books_id = fields.Many2one('library.books')
    state = fields.Selection([
        ('instore','In Store'),
        ('issued','Issued'),
        ('lost','Lost')
    ], default='instore', required=True)


class Issuances(models.Model):
    _name = 'library.books.copies.issue'
    _description = 'Library Books Copies Issuances'

    name = fields.Char(string="Issuance Number", readonly=True, required=True, copy=False, default='New')
    user = fields.Many2one('res.partner',domain=[('library_user','=','True')])
    copies_id = fields.Many2one('library.books.copies',domain=[('state','=','instore')])
    date_of_issue = fields.Date('Issuance Date', default = lambda self: fields.Datetime.now(), copy=False)
    issue_period = fields.Integer("Days for which book is given")
    state = fields.Selection([
        ('issued','Issued'),
        ('delayed','Delayed'),
        ('returned','Returned'),
        ('lost','Lost')
    ], default='issued', required=True, readonly = True)

    @api.depends('state')
    def change_book_state(self):
        for record in self:
            if record.state == 'issued' or record.state == 'delayed':
                record.copies_id.state = 'issued'
            elif record.state == 'lost':
                record.copies_id.state = 'lost'
            else:
                record.copies_id.state = 'instore'

##Copied online - need to understand this from ashish
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'books.issuance.number') or 'New'
            result = super(Issuances,self).create(vals)
        return result

# class LibraryBookSettings(models.Model):
#     _name = 'library.books.settings'
#     _description = 'Library Books Settings'


class InheritedUser(models.Model):
    _inherit = 'res.partner'

    library_user = fields.Boolean()