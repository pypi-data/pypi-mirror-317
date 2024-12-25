from setuptools import setup, find_packages

setup(
    name='console-python-progress-bar',  # Уникальное имя пакета
    version='0.1.0',  # Версия пакета
    author='Evgeny Kublin',
    author_email='egenkub@gmail.com',
    description='A lightweight, customizable progress bar for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/igeni/python-progress-bar',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[],  # Добавьте зависимости, если есть
)