# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime


class AccountLoanPaymentWizard(models.TransientModel):
    _name = 'account.loan.payment.wizard'

    def _get_default_loan(self):
        return self.env['loan.account'].browse(self.env.context.get('active_ids'))

    loan_id = fields.Many2one('loan.account', string='Loan', default=_get_default_loan)
    journal_id = fields.Many2one('account.journal', string='Payment Journal')
    amount=fields.Integer(string='Payment Amount')
    payment_date=fields.Date(string='Date',default=fields.Date.today())