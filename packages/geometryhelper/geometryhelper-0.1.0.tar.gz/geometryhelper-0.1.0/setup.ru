from setuptools import setup, find_packages

setup(
    name="geometryhelper",
    version="0.1.0",
    author="Заур Гадаборшев",
    author_email="orlov.tigr@bk.ru",
    description="Библиотека для работы с геометрическими фигурами и кв уравнением",
    long_description=open("Заур__Илья/README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "Заур__Илья"},
    packages=find_packages(where="Заур__Илья"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)