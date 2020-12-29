{
    'name': 'Workshop Web Page',
    'category': 'Website',
    'summary': 'Workshop Web Page',
    'version': '1.0',
    'description': """
Workshop Website Information
============================

    """,
    'author': 'Alan David Martinez',
    'depends': [
        'website',
        'workshop',
        'website_partner'
        ],
    'data': [
        'data/website_workshop_data.xml',
        # 'data/website_workshop_demo.xml',
        'views/website_templates.xml',
        'views/website_workshop.xml',
        'security/ir.model.access.csv',
        'security/website_workshop.xml',
        ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
