from setuptools import setup, find_packages

setup(
    name='com-chery-user-util',
    version='0.0.4',
    packages=[
        'com_chery',
        'com_chery.chery_user_util',
    ],
    include_package_data=True,
    install_requires=[
        'requests',
        'python-dotenv',
    ],
    description='temp package, will be deleted later 2024-12-24',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # author='Your Name',
    # author_email='your.email@example.com',
    # url='https://example.com/com_example_root',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)