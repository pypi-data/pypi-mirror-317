from setuptools import setup
setup(
    name='cnlunar',
    version='0.2.0',
    packages=['cnlunar'],
    url='https://github.com/OPN48/cnLunar',
    author='cuba3',
    author_email='cuba3@163.com',
    long_description=open('README.rst', encoding='utf-8').read(),
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
#