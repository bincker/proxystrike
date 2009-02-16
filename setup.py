from setuptools import setup, find_packages

setup(
    # other arguments here...
    entry_points = {
        'console_scripts': [
            'foo = my_package.some_module:main_func',
            'bar = other_module:some_func',
        ],
        'gui_scripts': [
            'baz = my_package_gui.start_func',
        ]
    }
)
