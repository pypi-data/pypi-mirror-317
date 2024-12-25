from setuptools import find_packages, setup

setup(
    name='netbox-task',
    version='1.0.1',
    description = 'Run AWX Task from Netbox',
    author='HuyTM',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'netbox_task': ['netbox_task/*'],
    },
    entry_points={
        'netbox_task': [
            'netbox_task = netbox_task:Plugin',
        ],
    },
)