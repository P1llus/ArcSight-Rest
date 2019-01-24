from distutils.core import setup

setup(
    name='loggersdk',
    version='1.0',
    description='Python library to connect to the HP Arcsight Logger REST API',
    author='Marius Iversen',
    license='MIT',
    author_email='marius@chasenet.org',
    url='https://github.com/arcsight-unofficial/arcsight-logger-api-sdk',
    download_url='https://github.com/arcsight-unofficial/arcsight-logger-api-sdk/tarball/2.0',
    keywords=['arcsight', 'logger', 'rest', 'sdk'],
    py_modules=['loggersdk'],
    install_requires=['requests'],
)
