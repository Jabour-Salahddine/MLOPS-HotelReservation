
from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-HotelReservation",
    version="0.1",
    author="Salahddine",
    author_email="jaboursalahddine@gmail.com",
    packages=find_packages(),
    install_requires = requirements,
)