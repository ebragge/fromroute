from setuptools import setup

setup(name='fromroute',
      version='0.3',
      description='Find closest location on a predefined route from a specific point.',
      url='https://github.com/ebragge/fromroute',
      author='Eero Bragge',
      author_email='ebragge@live.com',
      license='MIT',
      packages=['fromroute'],
      install_requires=[
          'geopy', 'pandas',
      ],
      zip_safe=False)