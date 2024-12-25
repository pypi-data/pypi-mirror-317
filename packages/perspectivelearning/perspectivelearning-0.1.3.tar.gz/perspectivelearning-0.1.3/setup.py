from setuptools import setup, find_packages

setup(
    name="perspectivelearning",
    version="0.1.3",
    author="Sai Pavan Velidandla",
    author_email="connectwithpavan@gmail.com",
    description="A dynamic framework for hypothesis-driven iterative machine learning.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
    ],
)
