from setuptools import setup, find_packages

 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='QPutils',
  version='0.0.3',
  description='Data visualization tool',
  long_description='Long Description',
  long_description_content_type='text/x-rst', 
  author='Appannagari Kaushik',
  author_email='appannagarikaushik.123@gmail.com', 
  classifiers=classifiers, 
  packages=find_packages(),
  install_requires=['pandas','matplotlib.pyplot ','numpy','seaborn'],
  python_requires='>=3.6'

)