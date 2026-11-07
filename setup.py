from setuptools import setup, find_packages

setup(
    name="it_inventory_47_backend",
    version="1.0.0",
    description="Back-End project with Flask + Python + MySQL (Variant 47, Taras Nedoviz, IP-22)",
    author="Taras Nedoviz",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-SQLAlchemy",
        "PyMySQL",
        "cryptography",
        "PyYAML",
    ],
)
