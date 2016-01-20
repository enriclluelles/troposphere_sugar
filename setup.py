from setuptools import setup

setup(
    name='troposphere_sugar',
    version='0.0.1',
    description='Common utilities on top of troposphere and boto for ease of clouformation template creation',
    author='Enric Lluelles',
    author_email='enric@lluel.es',
    url="https://github.com/enriclluelles/troposphere_sugar",
    packages=['troposphere_sugar', 'troposphere_sugar.decorators'],
    install_requires=['troposphere>=1.2.0']
)
