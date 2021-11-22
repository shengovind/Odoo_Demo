from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Books(models.Model):
    _name = 'library.books'
    _description = 'Library Books Model'
    _sql_constraints = [('UniqueISBN','unique(isbn)','ISBN to be unique')]

    name = fields.Char(compute='_full_book_name',store=True)
    bookname = fields.Char(required=True, string='Book Name')
    isbn = fields.Char(required=True, string='ISBN')
    edition = fields.Char(required=True, string='Book Edition')
    copies_id = fields.One2many('library.books.copies','books_id')
    copies_count = fields.Integer(compute='_count_copies')
    # Check if this gets called when bulk upload

    @api.depends('copies_id')
    def _count_copies(self):
        for record in self:
            record.copies_count = len(record.copies_id)

    @api.depends('bookname','isbn','edition')
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
    _rec_name = 'display_name'

    name = fields.Char(string='Unique Reference',required=True, copy=False)
    display_name = fields.Char(compute='_copy_name')
    books_id = fields.Many2one('library.books')
    state = fields.Selection([
        ('instore','In Store'),
        ('issued','Issued'),
        ('lost','Lost')
    ], default='instore', required=True)
    issuance_id = fields.One2many('library.books.copies.issue','copies_id')

    @api.depends('name','books_id.bookname')
    def _copy_name(self):
        for record in self:
            if record.name == False or record.books_id.bookname == False:
                record.display_name = ""
            else:
                record.display_name = str(record.name) + ' - ' + str(record.books_id.bookname)

class Issuances(models.Model):
    _name = 'library.books.copies.issue'
    _description = 'Library Books Copies Issuances'

    name = fields.Char(string="Issuance Number", readonly=True, required=True, copy=False, default='New')
    books_id = fields.Many2one('library.books')
    user = fields.Many2one('res.partner', required = True, domain=[('library_user','=','True')])
    copies_id = fields.Many2one('library.books.copies')
    date_of_issue = fields.Date(string='Issuance Date', default = lambda self: fields.Datetime.now(), readonly=True, copy=False)
    issue_period = fields.Integer(string="Issue Duration")
    state = fields.Selection([
        ('issued','Issued'),
        ('delayed','Delayed'),
        ('returned','Returned'),
        ('lost','Lost')
    ], default='issued', required=True, readonly = True)
    
    @api.onchange('copies_id')
    def _book_on_copy(self):
        for record in self:
            if record.copies_id:
                record.books_id = record.copies_id.books_id

    @api.constrains('books_id','copies_id.books_id')
    def _check_book_copy_relation(self):
        for record in self:
            if record.books_id != record.copies_id.books_id:
                raise UserError("Select related book and copy")

##Copied online - need to understand this from ashish
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'books.issuance.number') or 'New'
            result = super(Issuances,self).create(vals)
        return result

class InheritedUser(models.Model):
    _inherit = 'res.partner'

    library_user = fields.Boolean()