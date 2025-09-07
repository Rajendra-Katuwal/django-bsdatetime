from setuptools import setup, find_packages
from pathlib import Path

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else "Django fields for bsdatetime"

setup(
    name="django-bsdatetime",
    version="1.0.0",
    packages=find_packages(include=["django_bsdatetime", "django_bsdatetime.*"]),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "bsdatetime>=1.1.0",
    ],
    python_requires=">=3.9",
    description="Django model fields for Bikram Sambat (Nepali) dates (bsdatetime core)",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rajendra Katuwal",
    author_email="raj.katuwal2061@gmail.com",
    url="https://github.com/Rajendra-Katuwal/django-bsdatetime",
    project_urls={
        "Documentation": "https://Rajendra-Katuwal.github.io/bsdatetime.docs/",
        "Source": "https://github.com/Rajendra-Katuwal/django-bsdatetime",
        "Issues": "https://github.com/Rajendra-Katuwal/django-bsdatetime/issues",
    },
    license="MIT",
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Internationalization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["django", "bikram sambat", "nepali", "calendar", "date", "datetime", "fields"],
)
