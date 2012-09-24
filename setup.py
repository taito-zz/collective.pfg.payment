from setuptools import find_packages
from setuptools import setup

import os


long_description = (
    open("README.txt").read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read() + "\n" +
    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
    open(os.path.join("docs", "CREDITS.txt")).read())


setup(
    name='collective.pfg.payment',
    version='0.3.2',
    description="Extends PloneFormGen to payment form.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/taito/collective.pfg.payment',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.pfg'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PloneFormGen',
        'setuptools',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,)
