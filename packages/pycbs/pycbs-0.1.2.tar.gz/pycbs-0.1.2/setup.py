from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    readme = file.read()


setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    # url="https://github.com/your_username/my_package",
    packages=find_packages(),
)
