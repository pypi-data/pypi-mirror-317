from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='status_codes',
    version='1.3.0',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
    ],
    description="HTTP status code responses with predefined or custom messages for easy integration into web applications and APIs.",
    long_description=description,
    long_description_content_type="text/markdown",
)