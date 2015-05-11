from setuptools import setup, find_packages

setup(
    name='SSD1331',
    version='0.1',
    description='Basic interface to an SSD1331 controller over SPI',
    packages=find_packages(exclude=['build', 'dist', '*.egg-info']),
    install_requires=['spidev', 'PIL', 'RPi.GPIO'],
)
