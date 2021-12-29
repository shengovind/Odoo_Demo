{
    'name': 'Real Estate',
    'description': 'Haha test desc',
    'category': 'Estate',
    'application':True,
    'depends':['base','account','portal','website'],
    'data': [
        'security/security_records.xml',
        'security/ir.model.access.csv',
        'wizard/property_report_wizard_view.xml',
        'wizard/reconfirm_accept_view.xml',
        'views/estate_menus.xml',
        'views/estate_portal_view.xml',
        'views/estate_index.xml',
        'wizard/create_sold_invoice_view.xml',
        'views/estate_property_views.xml',
        'report/property_detail_pdf.xml',
        'report/property_detail_pdf_lang.xml',
        'report/property_report.xml'
    ],
}
