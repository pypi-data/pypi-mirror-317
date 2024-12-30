from setuptools import find_packages,setup

with open('requirements.txt','r',encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="expreport",
    version="1.0.4",
    author="Aymen Jemi",
    author_email="jemiaymen@gmail.com",
    description="export data from csv to documents word,excel",
    licence="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['docxtpl==0.18.0', 'pandas==2.2.2', 'xlsxwriter==3.2.0'],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "expreport=expreport:cli"
        ]
    },
)
