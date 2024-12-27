from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
def parse_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


setup(
    name="eeg_auto_tools",
    version="0.0.6",
    author="Sear",
    author_email="vasilijkrukovskij2015@gmail.com",
    description="The set of tools for working with EEG data",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
)