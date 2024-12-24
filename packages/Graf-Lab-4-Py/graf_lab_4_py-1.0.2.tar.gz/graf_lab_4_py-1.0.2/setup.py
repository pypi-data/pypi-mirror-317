from setuptools import setup, find_packages


def readme():
  with open('README.md', encoding='utf-8') as f:
    return f.read()


setup(
  name='Graf_Lab_4_Py',
  version='1.0.2',
  author='Sadova Diana, Zhukova Arina',
  author_email='grnshinnosha@gmail.com,arichka2005@yandex.ru',
  description='Библиотека для работы с графами и алгоритмами на них.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DianaSadova/Graf', # url - ссылка на страницу пакета.
  packages=find_packages(),
  install_requires=['requests>=2.25.1','matplotlib==3.10.0', 'numpy==2.2.1', 'networkx==3.4.2'], # список зависимостей, включая их версии
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='graf, mathematics',
  project_urls={
    'GitHub': 'https://github.com/DianaSadova/Graf'
  },
  python_requires='>=3.6'
)

'''

1. изменение кода 
2. изменяем setup.py
3. собрать код в пакет (wheel, ...)
4. загружаем пакет в репозитории (twine)
'''