from setuptools import setup, find_packages

str_version = '1.1.12'

setup(name='skyctl',
      version=str_version,
      description='SkyCtl CLI Tool For Skybackend Server',
      author='XieJunWei',
      author_email='643657447@qq.com',
      license='MIT',
      packages=find_packages(),
      package_data={
          '': ['*.ini']
      },
      zip_safe=False,
      include_package_data=True,
      install_requires=['pypinyin', 'opencv-python', 'requests', 'configparser', 'Click', 'tabulate', 'kubernetes',
                        'pyyaml'],
      python_requires='>=3',
      entry_points={
          'console_scripts': [
              'skyctl = ctl.terminal:cli',
          ],
      },
      )
