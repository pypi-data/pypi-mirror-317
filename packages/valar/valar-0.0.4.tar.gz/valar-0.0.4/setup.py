from setuptools import setup
NAME = 'valar'
VERSION = '0.0.4'

setup(
    name=NAME,
    version=VERSION,
    packages=['valar_base','valar_common','valar_meta'],
    url='https://gitee.com/GRIFFIN120/valar',
    license='MIT License',
    author='刘寅鹏',
    author_email='liuyinpeng@buaa.edu.cn',
    description='Valar Margulis'
)

print(f'twine upload dist/{NAME}-{VERSION}.tar.gz ')