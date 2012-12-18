'''
Created on Dec 9, 2012

@author: Aitor Gómez Goiri <aitor.gomez@deusto.es>

To install/reinstall/uninstall the project and its dependencies using pip:
     sudo pip install ./
     sudo pip install ./ --upgrade
     sudo pip uninstall netuse
'''
from setuptools import setup, find_packages

setup(name="otsopy",
      version="0.1",
      description="An Otsopack implementation in Python.",
      long_description = \
      """
      An Otsopack implementation in Python which uses:
      - Rdflib to manage the semantic information.
      - XXX to expose HTTP RESTfull services.
      """,
      author = "Aitor Gomez-Goiri",
      author_email = "aitor.gomez@deusto.es",
      maintainer = "Aitor Gomez-Goiri",
      maintainer_email = "aitor.gomez@deusto.es",
      url = "http://github.com/gomezgoiri/otsoPy",
      packages = ["otsopy"],
      download_url = "https://github.com/gomezgoiri/otsoPy/zipball/master",
      license = "http://www.apache.org/licenses/LICENSE-2.0",
      platforms = ["any"],
      package_dir = {
        '': 'src',
      },
      packages = find_packages('src'),  # include all packages under src
      install_requires = [
                          'simpy',
                          'rdflib<3a',
                          'fuxi',
                          'pymongo',
                          'mongoengine',
                          'mock', # http://www.voidspace.org.uk/python/mock/
                          'numpy',
                          'matplotlib',
                          ],
      #license = "Apache",
      keywords = "otsopack webOfThings wot semanticWeb distribution internetOfThings iot",
      #entry_points = {}
)