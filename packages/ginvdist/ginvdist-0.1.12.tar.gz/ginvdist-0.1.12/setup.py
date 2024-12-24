from setuptools import find_packages, setup


def get_long_description():
    return 'https://github.com/TheMumblingMammoth/GInvDist/blob/main/README.md'

def get_requirements():
    return ['numpy', 'sympy', 'graphviz']

setup(
    name="ginvdist",
    version="0.1.12",
    description="проект GInvDist - система для распределённого вычисления базисов Грёбнера(и инволютивных базисов) с использованием инволютивного деления.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Мамонов А.А. Салпагаров С.И. Блинков Ю.А.",
    author_email="anton.mamonov.golohvastogo@mail.ru",
    url="https://github.com/TheMumblingMammoth/GInvDist",
    project_urls={
        "GitHub Project": "https://github.com/TheMumblingMammoth/GInvDist",
        "Issue Tracker": "https://github.com/TheMumblingMammoth/GInvDist/blob/main/Meta/issues",
    },
    packages=['ginv'],
    install_requires=get_requirements(),
    python_requires=">=3.1",

    keywords=[
        "distributed calculation",
    ],
    license="GNU LGPL",
)



