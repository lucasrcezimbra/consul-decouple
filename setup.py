import os

from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.rst')


if __name__ == "__main__":
    setup(
        name='consul-decouple',
        description='An extension for python-decouple to read Consul using python-consul2.',
        version='0.0.2',
        long_description=open(README).read(),
        author="Lucas Rangel Cezimbra",
        author_email="lucas@cezimbra.tec.br",
        license="LGPLv2",
        url='https://github.com/lucasrcezimbra/consul-decouple',
        keywords=['consul', 'decouple', 'python-decouple', 'python-consul', 'python-consul2'],
        install_requires=[
            'python-consul2',
            'python-decouple',
        ],
        py_modules=['consul_decouple'],
        zip_safe=False,
        include_package_data=True,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Libraries',
        ],
    )
