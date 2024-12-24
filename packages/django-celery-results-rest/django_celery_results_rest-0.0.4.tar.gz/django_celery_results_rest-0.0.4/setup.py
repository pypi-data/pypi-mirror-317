from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='django-celery-results-rest',
    version='0.0.4',
    license='MIT',
    author='zengqiu',
    author_email='zengqiu@qq.com',
    description='RESTful API for django-celery-results',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    install_requires=['django-celery-results>=2.5.1', 'djangorestframework>=3.14.0', 'django-filter>=23.5'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)