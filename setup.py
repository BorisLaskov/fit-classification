from setuptools import setup


# with open('README.rst') as f:
#     long_description = ''.join(f.readlines())

setup(
    name='fit_classification',
    version='0.1',
    description='todo',
    long_description='todo',
    author='Boris Laskov',
    author_email='laskobor@fit.cvut.cz',
    keywords='todo',
    license='todo',
    url='todo',
    packages=['classification'],
    # package_data={...},
    zip_safe=False,
    install_requires=['requests>=2.18.4', 'requests-oauthlib>=0.8.0',
                      'appdirs>=1.4.3', 'dataclasses>=0.4'],
    setup_requires=['pytest-runner>=3.0'],
    tests_require=['pytest>=3.4.0', 'flexmock>=0.10.2'],
    # classifiers=[
    #     ...
    #     ]
)
