from setuptools import setup, find_packages
import os

version = '1.1.0'

setup(name='rvs.schooltemplate',
      version=version,
      description="A Plone site template for Rocky School sites",
      long_description=open("README.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone template',
      author='Rocky View Schools',
      author_email='info@rockyview.ab.ca',
      license='GPL',
      url='http://www.rockyview.ab.ca',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rvs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone',
          'Derma.RockySchool',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

