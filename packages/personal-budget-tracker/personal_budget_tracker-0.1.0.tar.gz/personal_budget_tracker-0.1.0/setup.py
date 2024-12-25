from setuptools import setup, find_packages

setup(
    name='personal_budget_tracker',                # Название библиотеки
    version='0.1.0',                               # Версия
    packages=find_packages(),                      # Указываем, какие пакеты включить
    install_requires=[                             # Зависимости
        'matplotlib'
    ],
    description='Python library for tracking and analyzing personal expenses',
    author='Lamery',                       
    author_email='chigladze.maya@mail.ru',
    url='https://github.com/LaMeru/python_bibl.git',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)
