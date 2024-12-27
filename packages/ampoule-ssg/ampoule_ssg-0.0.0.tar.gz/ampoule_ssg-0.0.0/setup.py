from setuptools import setup, find_packages

setup(
    name="ampoule-ssg",
    version="0.0.0",
    author="Roundabout developers",
    author_email="root@roundabout-host.com",
    description="A simple yet flexible static site generator based on Jinja2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://roundabout-host.com/roundabout/ampoule",
    packages=find_packages(),
    install_requires=["Jinja2", "ruamel.yaml", "beautifulsoup4", "colorama"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
