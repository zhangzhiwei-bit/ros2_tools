from setuptools import setup
from glob import glob
package_name = 'py05_exercise'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob("launch/*.launch.xml")),
        ('share/' + package_name, glob("launch/*.launch.py")),
        ('share/' + package_name, glob("launch/*.launch.yaml")),
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
            'exer01_spawn_py = py05_exercise.exer01_spawn_py:main',
            'exer02_tf_broadcaster_py = py05_exercise.exer02_tf_broadcaster_py:main',
            'exer03_tf_listener_py = py05_exercise.exer03_tf_listener_py:main',
        ],
    },
)
