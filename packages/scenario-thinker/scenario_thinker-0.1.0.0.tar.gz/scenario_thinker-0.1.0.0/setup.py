import setuptools
from setuptools import find_packages, setup


with open("README.md", "r") as fh:
   long_description = fh.read()


setuptools.setup(
   name='scenario_thinker',
   scripts=['bin/st_prepare',
             'bin/extra_modules.py'],
   version='0.1.0.0',
   author="Me3eh",
   author_email="matt30002000@gmail.com",
   description="BDD and AI library",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/me3eh/scenario_thinker",
   install_requires=[
        'python-dotenv >= 1.0.1',
        'behave >= 1.2.5',
        'selenium >= 4.26.1',
        'openai >= 0.27.8',
        'flask >= 3.0.3',
        'Flask-Cors >= 5.0.0',
    ],
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   include_package_data=True
)
