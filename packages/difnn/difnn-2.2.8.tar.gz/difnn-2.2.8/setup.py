from setuptools import setup, find_packages

setup(
    name="difnn",  
    version="2.2.8",
    description="difnn",  
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",
    author="Forecaster",  
    packages=find_packages(),  
    package_data={
        "difnn": ["forecast_utility.cp312-win_amd64.pyd", "autotm_utility.cp312-win_amd64.pyd", "difnn_utility.cpython-310-x86_64-linux-gnu.so",  "forecast_utility.cpython-310-x86_64-linux-gnu.so", "autotm_utility.cpython-310-x86_64-linux-gnu.so", "difnn_utility.cpython-310-x86_64-linux-gnu.so"],  
    },
    include_package_data=True,  
    install_requires=open("requirements.txt").read().splitlines(),  
    entry_points={
        "console_scripts": [
            "difnn=difnn.main:main",  #
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  
)
