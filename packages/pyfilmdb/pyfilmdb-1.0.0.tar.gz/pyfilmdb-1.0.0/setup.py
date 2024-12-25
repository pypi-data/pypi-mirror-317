from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(
  name='pyfilmdb',
  version='1.0.0',
  author='lebedev.art.2009',
  author_email='lebedev.art.2009@yandex.ru',
  description='My first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url=None,
  packages=find_packages(),
  install_requires=[
    'requests>=2.25.1',
    'deep_translator==1.11.4',
    'langid==1.1.6',
    'PyQt6==6.8.0',
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='films database db bd api client',
  python_requires='>=3.9'
)