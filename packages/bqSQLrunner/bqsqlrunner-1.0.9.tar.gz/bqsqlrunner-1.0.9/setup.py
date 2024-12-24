from setuptools import setup, find_packages

setup(
    name="bqSQLrunner",  # Name of your framework
    version="1.0.9",  # Version of your framework
    author="Martin Birkholz / Iulian",
    author_email="iulian.glavan@metro.digital",
    description="A Python framework for running SQL steps on BigQuery, with support for variables and dependencies. Developed by Martin Birkholz and maintained by Iulian.",
    packages=find_packages(),  # Automatically finds `framework` as a package
    include_package_data=True,
    install_requires=[
        "google-cloud-bigquery>=2.0.0",
    ],
    python_requires=">=3.7",
)
 