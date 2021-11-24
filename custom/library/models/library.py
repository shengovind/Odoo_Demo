from odoo import models, fields, api
import datetime
from datetime import timedelta as td
from odoo.exceptions import UserError, ValidationError

class Books(models.Model):
    _name = 'library.books'
    _description = 'Library Books Model'
    _sql_constraints = [('UniqueISBN','unique(isbn)','ISBN to be unique')]

    name = fields.Char(compute='_full_book_name',store=True)
    bookname = fields.Char(required=True, string='Book Name')
    isbn = fields.Char(required=True, string='ISBN')
    edition = fields.Char(required=True, string='Book Edition')
    author_id = fields.Many2many('res.partner', domain=[('library_author','=','True')])
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
    ], default='instore', required=True, readonly=True)
    loser = fields.Many2one('res.partner', readonly=True)
    issuance_id = fields.One2many('library.books.copies.issue','copies_id')

    @api.depends('name','books_id.bookname')
    def _copy_name(self):
        for record in self:
            if record.name == False or record.books_id.bookname == False:
                record.display_name = ""
            else:
                record.display_name = str(record.name) + ' - ' + str(record.books_id.bookname)

    # @api.depends('issuance_id.state')
    # def _change_copy_state(self):
    #     for rec in self:
    #         for issue in rec.issuance_id:
    #             if issue.state == 'issued':
    #                 rec.state = 'issued'
    #Clashes with buttons.. WHat to do?!!

class Issuances(models.Model):
    _name = 'library.books.copies.issue'
    _description = 'Library Books Copies Issuances'

    name = fields.Char(string="Issuance Number", readonly=True, required=True, copy=False, default='New')
    books_id = fields.Many2one('library.books', required =True)
    #rel_book_copy_domain = fields.One2many(related='books_id.copies_id') #THIS WAS TO TRY DYNAMIC FILTER
    user = fields.Many2one('res.partner', required = True, domain=[('library_user','=','True')])
    copies_id = fields.Many2one('library.books.copies')
    date_of_issue = fields.Date(string='Issuance Date', default = lambda self: fields.Date.today(), readonly=True, copy=False)
    issue_period = fields.Integer(string="Fixed Issue Duration", default=7)
    due_date = fields.Date(string="Due Date", readonly=True, compute='_due_date')
    returned_date=fields.Date(string='Returned Date')
    delayed_bool = fields.Boolean(string='Delayed?', readonly=True, compute='_delay_check')
    state = fields.Selection([
        ('issued','Issued'),
        ('lost','Lost'),
        ('returned','Returned')
    ], default='issued', required=True, readonly=True)
    charges = fields.Integer(string='Charges', compute='_charges_assign')
    
    @api.depends('due_date','returned_date')
    def _charges_assign(self):
        print("\n\n charge assign called \n\n")
        for record in self:
            if record.returned_date:
                diff = record.returned_date - record.due_date
                count = diff.days
                if count <= 0:
                    record.charges = 0
                elif count <=10:
                    record.charges = count * 10
                else:
                    record.charges = count * 100
            else:
                record.charges = 0
            
    @api.depends('due_date')
    def _delay_check(self):
        print("\n\n delay call \n\n")
        for record in self:
            today = datetime.date.today()
            if today > record.due_date:
                record.delayed_bool = True
            else:
                record.delayed_bool = False

## Note!!! Depends must always assign. So ensure Else condition is always there to close the requirement

    def return_action(self):
        for record in self:
            if record.state == 'lost':
                raise UserError('Book marked as lost - cannot be returned')
            record.state = 'returned'
            record.returned_date = datetime.date.today()
            record.copies_id.state='instore'

    def lost_action(self):
        for record in self:
            if record.state == 'returned':
                raise UserError('Book is already returned!')
            record.state = 'lost'
            record.copies_id.state='lost'

    @api.onchange('copies_id')
    def _book_on_copy(self):
        for record in self:
            if record.copies_id:
                record.books_id = record.copies_id.books_id

    @api.depends('date_of_issue','issue_period')
    def _due_date(self):
        for record in self:
            record.due_date = record.date_of_issue + datetime.timedelta(days=record.issue_period)

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
    library_author = fields.Boolean()

    @api.constrains('library_user','library_author')
    def _check_author_user(self):
        for record in self:
            if record.library_user == True and record.library_author ==True:
                raise ValidationError('Author and User cannot be same person')