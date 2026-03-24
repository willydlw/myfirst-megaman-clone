# added __inti__.py file to mark the directory as a package 

# File is excecuted once, the first time any module from this package
# is imported. Printing message to illustrate
print('Initializing src package')


# define modules visible using import *
__all__ = ['game']

# Import these modules into the package's namespace
from .game import Game 
