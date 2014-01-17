from distutils.core import setup

setup(
    name='XeroAPI',
    version='0.0.6',
    author='Beesdom',
    author_email='team@beesdom.com',
    packages=['xeroapi', 'xeroapi.tests'],
    url='https://github.com/beesdom/XeroAPI',
    license='LICENSE.txt',
    description='Python client API for private XERO applications.',
    long_description=open('README.rest').read(),
    install_requires=[
        "M2Crypto",
        "oauth2",
    ],
)
