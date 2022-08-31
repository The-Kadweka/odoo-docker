# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime


class LoanDisbursementWizard(models.TransientModel):
    _name = 'loan.disburse.wizard'

    # def _get_default_loan(self):
    #     return self.env['loan.account'].browse(self.env.context.get('active_ids'))

    loan_id = fields.Many2one('loan.account', string='Loan')
    journal_id = fields.Many2one('account.journal', string='Disbursement Journal')
    amount=fields.Integer(string='Disbursement Amount')
    dis_date=fields.Date(string='Date',default=fields.Date.today())

    def disburse_loan(self):
        print('TESTING THE PRINT FUNCTIONALITY')