from setuptools import setup, find_packages

setup(
    name='toneo',  
    version='0.1.0',  
    packages=find_packages(), 
    install_requires=[
        'requests',  
    ],
    description='connest smart contract', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Указываем формат Markdown
    url='https://t.me/pozozal',  # URL репозитория
    author='pozozal',  # Ваше имя
    author_email='12@mail4.uk',  # Ваш email
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',
)
