import logging
import setuptools
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from setuptools.command.build_ext import build_ext
    
__package__ = 'deepnpg'

def get_version(fname):
    with open(fname) as f:
        for line in f:
            if line.startswith("__version__ = '"):
                return line.split("'")[1]
    raise RuntimeError('Error in parsing version string.')


logging.basicConfig()
log = logging.getLogger(__file__)

__version__ = get_version('deepnpg/__init__.py')


ext_errors = (CCompilerError, ModuleNotFoundError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

with open("README.md", 'r') as f:
    long_description = f.read()

def requirements():
    # The dependencies are the same as the contents of requirements.txt
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip()]
    
class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""

    def run(self):
        import numpy
        self.include_dirs.append(numpy.get_include())
        build_ext.run(self)
        
        
setup_args = {'name':__package__,
        'packages':[__package__],
        'version':__version__,
        'install_requires':["numpy>=1.17.3",
                             "scipy>=1.7.0",
                             "matplotlib>=3.5", 
                             "torch","torch_geometric", 
                             "requests"], 

        'cmdclass': {'build_ext': CustomBuildExtCommand},
        'classifiers':["Intended Audience :: Science/Research",
                "Intended Audience :: Developers",
                "Programming Language :: C",
                "Programming Language :: Python",
                "Topic :: Software Development",
                "Topic :: Scientific/Engineering",
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                "Programming Language :: Python :: 3",
                ],
        'long_description':long_description,
        'author':"Xinye Chen",
        'author_email':"xinyechenai@gmail.com",
        'description':"Python library for building preconditiioner with Graph Neural Network",
        'long_description_content_type':'text/x-rst',
        'url':"https://github.com/inEXASCALE/deepnpc.git",
        'license':'MIT License'
}

try:
    setuptools.setup(
        setup_requires=["numpy>=1.17.3"],
        **setup_args
    )


except ext_errors as ext:
    log.warning(ext)
    log.warning("Installation fails.")
