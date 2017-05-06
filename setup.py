from setuptools import setup, find_packages

setup(
    name = 'hcc_risk_models',
    version = '0.0.1.dev1',
    description = (
        'Hierarchical Condition Category (HCC) risk models from the '
        'Centers for Medicare and Medicaid Services (CMS) and the '
        'Department of Health and Human Services (HHS)'),

    url = 'www.example.com',
    author = 'Gabriel Altay',
    author_email = 'gabriel.altay@gmail.com',

    packages = find_packages(),
    install_requires = ['numpy', 'pandas', 'python-dateutil', 'pytz', 'six'],
    package_data = {
        '': ['*.csv', '*.txt'],
    },


)
