import os

try:
    from __revision__ import __revision__
except:
    __revision__ = 'develop'

metadata = {
    'name': "djopenid",
    'version': "1.0",
    'release': __revision__,
    'url': 'http://www.jollydream.com',
    'author': 'hanbox',
    'author_email': 'han.mdarien@gmail.com',
    'admin': 'han.mdarien@gmail.com',
    'dependencies': (
        'python-openid',
        'boto',
        'South',
    ),
    'description': 'Jollydream Inc',
    'license': 'Private',
}