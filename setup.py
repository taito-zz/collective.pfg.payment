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
    version='0.5',
    description="Extends PloneFormGen to payment form.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/taito/collective.pfg.payment',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['collective', 'collective.pfg'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PloneFormGen',
        'hexagonit.testing',
        'setuptools'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
