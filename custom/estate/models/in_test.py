from odoo import models, fields, api
import datetime
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class MyTest(models.Model):
    _name = 'my.test'
    _description = 'Inheritance test class'

    name = fields.Char()
    address = fields.Text()
    email = fields.Char()
    pincode = fields.Integer()


class M1(models.Model):
    _inherit = 'my.test'

    fullname = fields.Char()
    delivery_address = fields.Text()

class M2(models.Model):
    _name = "m2.test"
    _inherit = 'my.test'

    pancard = fields.Char()
    aadhaar = fields.Integer()
