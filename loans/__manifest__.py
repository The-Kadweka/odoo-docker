{
    'name': "Loans Management",
    'summary': """ """,
    'version': '15.0.1.0.0',
    'description': """ """,
    'author': '@The-Kadweka',
    'website': 'http://mzinge.pythonanywhere.com',
    'category': 'Tools',
    'depends': ['base','contacts'],
    'license': 'AGPL-3',
    'data': [
        'views/loan_product_view.xml',
        'views/loans_view.xml',
        'views/loan_seq.xml',
        'security/ir.model.access.csv',
        'wizard/disburse_wizard.xml',
        # 'wizard/payment_wizard.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}