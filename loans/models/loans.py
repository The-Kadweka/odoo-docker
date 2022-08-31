from dataclasses import field
from email.policy import default
from datetime import datetime
import http
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from sqlite3 import apilevel
import string
from sys import api_version
from odoo import models, fields,api
import logging
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
class LoanAccount(models.Model):
    _name = "loan.account"

    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.installment_lines:
                if line.state == 'paid':
                    total_paid += line.amount
            bal_amount = loan.a_amnt - total_paid
            loan.total_amount = loan.r_amnt
            loan.bal_amount = bal_amount
            loan.paid_amount = total_paid

    name = fields.Char(string="Loan Number", default="/", readonly=True, help="Loan Number")
    partner_id= fields.Many2one('res.partner',string='Customer')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Pending Approval'),
        ('approved', 'Approved'),
        ('cancel', 'Rejected'),
        ('disbused', 'Disbursed'),
        ('closed', 'Closed')
        ],string="State", default='draft', track_visibility='onchange', copy=False)
    r_amnt=fields.Integer(string="Requested Amount",required=True)
    a_amnt=fields.Integer(string="Approved Amount",required=True)
    duration=fields.Integer(string="Installment(MONTHS)",required=True)
    manager_id=fields.Many2one('res.users',string="Loan Manager")
    purpose=fields.Char(string='Purpose',required=True)
    app_date=fields.Date(string="Apply Date",default=fields.Date.today())
    dis_date=fields.Date(string="Apply Date",default=fields.Date.today())
    bal_amount = fields.Float(string="Balance Amount", store=True, compute='_compute_loan_amount', help="Balance amount")
    installment_lines = fields.One2many('loan.account.line', 'loan_id', string="Loan Lines", index=True)
    paid_amount = fields.Float(string="Total Paid Amount", store=True, compute='_compute_loan_amount',help="Total paid amount")
    total_amount = fields.Float(string="Total Amount", store=True, readonly=True, compute='_compute_loan_amount',help="Total loan amount")
    loan_product_id=fields.Many2one('loan.product',string="Loan Product",required=True)
    int_rate=fields.Integer(string='Rate (%)',related="loan_product_id.rate")
    currency_id = fields.Many2one('res.currency', string='Currency',related="loan_product_id.currency_id")
    
    @api.model
    def create(self, values):
        loan_count = self.env['loan.account'].search_count(
            [('partner_id', '=', values['partner_id']), ('state', '=', 'disbused'),
             ('bal_amount', '!=', 0)])
        if loan_count:
            raise ValidationError(_("The Customer has an already a pending Loan"))
        else:
            values['name'] = self.env['ir.sequence'].get('loan.account.seq') or ' '
            res = super(LoanAccount, self).create(values)
            return res
            
    def unlink(self):
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a loan which is not in draft or cancelled state')
        return super(LoanAccount, self).unlink()

    def compute_installment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        for loan in self:
            loan.installment_lines.unlink()
            date_start = datetime.strptime(str(loan.dis_date), '%Y-%m-%d')
            amount = loan.a_amnt / loan.duration
            for i in range(1, loan.duration + 1):
                self.env['loan.account.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
            loan._compute_loan_amount()
        return True
    
 
    def action_cancel(self):
        for res in self:
            if res.state != 'draft':
                res.state='draft'
        return True

    # @api.multi
    def open_disbursement_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('loans.disbursement_wizard_view'),
            # 'name': 'disbursement_wizard_view',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'loan.disburse.wizard', 
            # 'context': {'loan_id': self.id},
            'target': 'new',
            }


class InstallmentLine(models.Model):
    _name = "loan.account.line"
    _description = "Installment Lines"
    
    loan_id = fields.Many2one('loan.account', string="Loan Ref.", help="Loan")
    date = fields.Date(string="Payment Date", required=True, help="Date of the payment")
    amount = fields.Float(string="Principle", required=True, help="Principle to be paid")
    interest = fields.Float(string="Interest", required=True, help="Interest to be paid")
    instalemt = fields.Float(string="Installment", required=True, help="Install to be paid")
    paid = fields.Float(string="Paid", required=True, help="Amount That Has Been Paid")
    state = fields.Selection([
        ('open', 'open'),
        ('paid', 'paid')
        ],string="State", default='open', track_visibility='onchange', copy=False)
