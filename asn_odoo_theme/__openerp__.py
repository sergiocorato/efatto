{
    'name': 'Odoo 9 Backend-Theme',
    'version': '8.0.1.0.0',
    'author': 'Ajeng Shilvie N',
    'description': '''
        A custom module to change menu bar like Odoo Enterprise
    ''',
    'category': 'Themes/ASN',
    'depends': [
        'web',
    ],
    'data': [
        'views/custom_view.xml',
    ],
    'css': ['static/src/css/styles.css'],
    'auto_install': False,
    'installable': True,
}
