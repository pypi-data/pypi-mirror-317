# This file is imported from __init__.py and exec'd from setup.py

MAJOR = 2
MINOR = 3
MICRO = 1
RELEASE = False

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE:
    # if it's a rcx release, it's not proceeded by a period. If it is a
    # devx release, it must start with a period
    __version__ += 'rc1'


_kivy_git_hash = 'db2ce376f5378d0733178646a04e6ec541746e1a'
_kivy_build_date = '20241226'
