from setuptools import setup

package_name = 'py02_rosbag'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zzw',
    maintainer_email='zzw@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'demo01_writer_py = py02_rosbag.demo01_writer_py:main',
            'demo02_reader_py = py02_rosbag.demo02_reader_py:main'
        ],
    },
)
