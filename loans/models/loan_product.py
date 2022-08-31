from dataclasses import Field, field
from email.policy import default
from datetime import datetime
import http
from locale import currency
from dateutil.relativedelta import relativedelta
from pkg_resources import require
from odoo.exceptions import ValidationError, UserError
from sqlite3 import apilevel
import string
from sys import api_version
from odoo import models, fields,api
import logging
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
class LoanProduct(models.Model):
    _name = "loan.product"

    name=fields.Char(string="Loan Product Name",required=True)
    rate=fields.Integer(string="Interest Rate (%)",required=True)
    currency_id=fields.Many2one('res.currency',string="Currency",required=True)
    allow_gr_period=fields.Boolean(string="Allow Grace Period?",required=True)
    max_gr_period=fields.Integer(string="Grace Period(MAXIMUN)",required=True)
