from setuptools import setup, find_packages

setup(
    name="djangocms-seo",
    version="0.1.1",
    description="A Django CMS app for managing SEO.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yessine Ben Rhouma",
    author_email="ben.rhouma.yessine0610@gmail.com",
    url="https://github.com/YessineBR/djangocms_seo",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django CMS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=5.1",
        "django-cms>=4.1",
    ],
    python_requires=">=3.10",
)
