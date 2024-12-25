from setuptools import setup
VERSION = '0.0.3'


setup(
    name='valar',
    version=VERSION,
    packages=['valar'],
    url='https://gitee.com/GRIFFIN120/valar',
    license='MIT License',
    author='刘寅鹏',
    author_email='liuyinpeng@buaa.edu.cn',
    description='Valar Margulis'
)

print(f'twine upload dist/valar-{VERSION}.tar.gz ')