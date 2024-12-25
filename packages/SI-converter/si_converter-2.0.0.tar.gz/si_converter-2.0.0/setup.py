from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r',encoding="utf8") as f:
    return f.read()

setup(
  name='SI_converter',
  version='2.0.0',
  author='Yanuskevich M.D.',
  author_email='mikhal_2005@mail.ru',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages('.'),
  install_requires=[''],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='system si converter',
  project_urls={
  },
  python_requires='>=3.7'
)