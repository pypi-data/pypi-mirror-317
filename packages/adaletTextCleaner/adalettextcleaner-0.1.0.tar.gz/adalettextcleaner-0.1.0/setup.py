from setuptools import setup, find_packages

setup(

    name="adaletTextCleaner",
    version= "0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'adaletTextCleaner': ['resources/*.txt','resources/*.json','resources/*.xml'],
    },
    install_requires=[],
    description="Veri temizleme işlemleri içeren kütüphane",
    author="Murat Tekdemir",
    python_requires='>=3.6',  
)

