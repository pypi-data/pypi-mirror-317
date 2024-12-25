from setuptools import setup, find_packages
setup(
    name="kivy_hot_tile_package",
    version="1.1",
    author="Daniel Kříž",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_hot_tile_package = kivy_hot_tile_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_hot_tile_package/*'],
    },
)
