from setuptools import setup, find_packages

setup(
    name="django-tenantflow",
    version="1.0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=5.0",
        "psycopg2-binary",
    ],
    license="MIT",
    description="A Django library to enable semi-isolated multitenancy in your project with users outside the tenant.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ConspiraciXn/django-tenantflow",
    author="Jared Soto",
    author_email="jared.sl@icloud.com",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
)
