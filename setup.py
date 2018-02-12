from setuptools import setup


with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='fit_classification',
    version='0.1.2',
    description='Access Classification portal API from your Python programs',
    long_description=long_description,
    author='Boris Laskov',
    author_email='laskobor@fit.cvut.cz',
    keywords='CTU FIT,Classification,coursework',
    license='MIT License',
    url='https://github.com/145k0v/fit-classification',
    packages=['classification'],
    zip_safe=False,
    install_requires=['requests>=2.18.4', 'requests-oauthlib>=0.8.0',
                      'appdirs>=1.4.3', 'dataclasses>=0.4'],
    setup_requires=['pytest-runner>=3.0'],
    tests_require=['pytest>=3.4.0', 'flexmock>=0.10.2', 'betamax>=0.8.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        ]
)
