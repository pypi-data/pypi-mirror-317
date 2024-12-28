import os
import subprocess
from setuptools import setup, find_packages
from objectDependencies import object_dependencies, base_package_name, current_yaml
from __init__ import __version__

version_file_path = "MYVERSION"


'''
def read_version():
    repo_path = os.getenv('CI_PROJECT_DIR', os.path.abspath(os.path.dirname(__file__)))
    version_file_path = os.path.join(repo_path,'MYVERSION')
    print(version_file_path)

    if not os.path.isfile(version_file_path):
        print(f"(read_version) Le fichier version ({version_file_path}) n'existe pas")
        return '0.0.0.0'
    with open(version_file_path, 'r') as version_file:
        version = version_file.read()
        print(f"(read_version) La version dans le fichier MYVERSION {version_file_path} est {version}")
    return version
'''

def read_version():
    with open('__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('\'"')
    raise RuntimeError("Unable to find version string.")


def increment_version(version):
    major, minor, patch, build = map(str, version.split('.'))
    val = int(build) + 1
    res = str(val)  # Increment the patch version
    return f"{major}.{minor}.{patch}.{res}"

def write_version(version):
    repo_path = os.getenv('CI_PROJECT_DIR', os.path.abspath(os.path.dirname(__file__)))
    version_file_path = os.path.join(repo_path,'MYVERSION')
    print(version_file_path)
    with open(version_file_path, 'w') as version_file:
        version_file.write(version)

if os.getenv('CI'):
    # Only increment the version in CI environment
    if os.getenv('CI_COMMIT_REF_NAME') == 'main':
        current_version = read_version()
        new_version = __version__
        print(new_version)
        write_version(new_version)
    else:
        new_version = read_version()
else:
    new_version = read_version()





def print_found_packages():
    # Utilisez find_packages() pour obtenir la liste des packages trouvés
    packages = find_packages(include=[base_package_name,base_package_name+'.'+current_yaml, base_package_name+'.'+ current_yaml + '.*'])
    print("Packages trouvés :")
    for package in packages:
        print(f"  {package}")

print_found_packages()

# myversion = read_version()
# new_version = increment_version(myversion)
new_version = __version__
include_pack = [
      base_package_name,
      base_package_name + '.' + current_yaml,
      base_package_name + '.' + current_yaml + '.*' 
]

print(include_pack)

setup(
    name=base_package_name+'-'+current_yaml,
    version=new_version,
    packages = find_packages(include=include_pack),
    # packages=find_packages(include=['pydataspace', 'pydataspace.jsonLDObject', 'pydataspace.jsonLDObject.*']),
    package_data={
        'mypackage': [base_package_name+'/data/*.yaml'],  # Inclut tous les fichiers .json et .txt dans le répertoire data/
    },
    include_package_data=True,
    install_requires=object_dependencies,
    author='Olivier Tirat',
    author_email='olivier.tirat@free.fr',
    description='Objet FederatedIdentifier pour pydataspace',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/dataspace2/ontologies/jsonldobject',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)



