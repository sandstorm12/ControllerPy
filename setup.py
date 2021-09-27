from setuptools import setup


def read_requirements(path='./requirements.txt'):
    with open(path, encoding='utf-8', errors='ignore') as file:
        install_requires = file.readlines()

    return install_requires


setup(
    name="ControllerPy",
    version="0.2.2",
    author="Hamid Mohammadi",
    author_email="sandstormeatwo@gmail.com",
    description="Control mouse and keyboard input using a controller",
    scripts=[
        'controllerpy'
    ],
    package_data={'': ['config.yaml']},
    include_package_data=True,
    install_requires=read_requirements()
)