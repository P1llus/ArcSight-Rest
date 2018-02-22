from distutils.core import setup

setup(
    name='arcsightrest',
    version='1.2',
    description='Python library to connect to the HP Arcsight Logger REST API',
    author='Fabian Bartenschlager',
    license='MIT',
    author_email='misc0815@mailbox.org',
    url='https://github.com/gear0/ArcSight-Rest',
    download_url='https://github.com/gear0/ArcSight-Rest/tarball/1.2',
    keywords=['arcsight', 'logger', 'rest'],
    include_package_data=True,
    zip_safe=True,
    py_modules=['arcsightrest'],
    install_requires=[
        'untangle',
        'requests',
    ],
)
