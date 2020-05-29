from setuptools import find_packages, setup


# with open('README.rst') as f:
#     LONG_DESC = f.read()

setup(
    name='aiven',
    version='0.0.1',
    url='http://example.com',
    description='Test exercise to produce and consume web metrics',
    # long_description=LONG_DESC,
    author='Pynchia', author_email='pyncha@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    keywords=['aiven', ],
    packages=find_packages(),
    # packages=['aiven'],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    producercli = aiven.producer.cli:cli
    consumercli = aiven.consumer.cli:cli
    """,
    install_requires=[]
)
