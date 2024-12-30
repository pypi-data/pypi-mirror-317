from setuptools import setup, find_packages

setup(
    name='valschoolsdk',
    version='0.1.0',
    description='A well-structured Python SDK template for school',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='ChideraVal',
    author_email='chideraval@example.com',
    license='MIT',
    install_requires=[],
    packages=find_packages(where='SchoolSDK')
)
