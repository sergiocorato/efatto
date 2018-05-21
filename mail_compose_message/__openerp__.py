{
    'name': 'Abilita pulsante Scrivi Mail',
    'version': '1.0.0',
    'category': 'Social Network',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'summary': 'Abilita il pulsante "Scrivi Mail" nella casella di posta',
    'depends': ['mail'],
    'website': 'http://www.emiprotechnologies.com',
    'description':
        """
Abilitando questo modulo, l'utente potrà comporre nuove email dalla sua casella di posta.
Questo modulo è stato tradotto/testato/modificato per rispondere alle caratteristiche ed ai
requisiti di SimplERP (<http://www.simplerp.it>
        """,
    'images': ['static/description/main_screen.png'],
    'installable': False,
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'data': [
        'views/mail.xml',
    ],
}
