from setuptools import setup, find_packages
setup(
    name="kivy_find_recipe_package",
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
            'kivy_find_recipe_package = kivy_find_recipe_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_find_recipe_package/*'],
    },
)
