from distutils.core import setup

setup(
    name='arcsightrest',
    version='1.2',
    description='Python library to connect to the HP Arcsight Logger REST API',
    author='Marius Iversen',
    license='MIT',
    author_email='marius@chasenet.org',
    url='https://github.com/P1llus/ArcSight-Rest',
    download_url='https://github.com/P1llus/ArcSight-Rest/tarball/1.2',
    keywords=['arcsight', 'logger', 'rest'],
    include_package_data=True,
    zip_safe=True,
    py_modules=['arcsightrest'],
    install_requires=[
        'untangle',
        'requests',
    ],
)
