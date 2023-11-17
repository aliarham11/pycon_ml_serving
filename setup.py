import setuptools

setuptools.setup(
    name="pycon_ml_serving",
    version="1.0.0",
    author="Yoga Aliarham",
    author_email="aliarham.skom@gmail.com",
    description="A package that use for serving inference machine learning models",
    long_description="A short description should suffice",
    long_description_content_type="text/markdown",
    url="https://github.com/aliarham11/pycon_ml_sercing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/serving"],
    install_requires=[
        "falcon==3.1.1",
        "gunicorn==20.1.0",
        "PyYAML==5.4.1"
    ],
    python_requires=">=3.7",
)