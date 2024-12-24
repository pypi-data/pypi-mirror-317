import os
from datetime import datetime
from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_desc = file.read()

MAIN_VERSION = 3.0

setup(
    name='bs_drm_adapter',
    version=os.getenv('PACKAGE_VERSION', f'{MAIN_VERSION}a{round(datetime.now().timestamp())}'),
    description='Beenius DRM Adapter',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://git.beenius.tv/devops/tools/bs-drm-adapter',
    author='Jernej Kladnik',
    author_email='jernej.kladnik@beenius.tv',
    license='Other/Proprietary License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='drm adapter content streaming integration',
    project_urls={
        'Source': 'https://git.beenius.tv/devops/tools/bs-drm-adapter',
        'Tracker': 'https://git.beenius.tv/devops/tools/bs-drm-adapter/issues'
    },
    packages=find_packages(exclude=['test_data']),
    install_requires=[
        'Flask>=1.1.2',
        'Flask-RESTful>=0.3.8,<2.0.0',
        'PyYAML>=5.3.1',
        'zeep>=4.0.0',
        'pytz>=2020.4',
        'uWSGI>=2.0.0'
    ],
    python_requires='>=3.6, <4',
)
