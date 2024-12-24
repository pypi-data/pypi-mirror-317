from setuptools import setup, find_packages
setup(
    name="kivy_weather_app_package",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'kivy_weather_app_package = kivy_weather_app_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_weather_app_package/*'],
    },
)
