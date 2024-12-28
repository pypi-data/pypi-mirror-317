from setuptools import setup, find_packages

setup(
    name="Policy_Packs",
    version="10312024",
    description="Proofpoint Policy Packs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eaobserveit/Policy-Packs/",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
