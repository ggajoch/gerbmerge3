#!/usr/bin/env python
import sys
import glob
import os

from distutils.core import setup
import distutils.sysconfig

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerbmerge"))
from gerbmerge.gerbmerge import VERSION_MAJOR, VERSION_MINOR

if sys.version_info < (3,2,0):
  print("*"*73)
  print("GerbMerge version %d.%d requires Python 3.2 or higher" % (VERSION_MAJOR, VERSION_MINOR))
  print("*"*73)
  sys.exit(1)

SampleFiles = glob.glob('testdata/*')
DocFiles = glob.glob('doc/*')
AuxFiles = ['COPYING']

if sys.platform == 'win32' or ('bdist_wininst' in sys.argv):
  DestLib = '.'
  DestDir = os.path.join(DestLib, 'gerbmerge')
  BinFiles = ['misc/gerbmerge.bat']
  BinDir = '.'
else:
  DestLib = distutils.sysconfig.get_config_var('LIBPYTHON')
  DestDir = os.path.join(DestLib, 'gerbmerge')
  BinFiles = ['misc/gerbmerge']
  BinDir = distutils.sysconfig.get_config_var('BINDIR')  

  # Create top-level invocation program
  fid = file('misc/gerbmerge', 'wt')
  fid.write( \
  r"""#!/bin/sh
python %s/site-packages/gerbmerge/gerbmerge.py $*
  """ % DestLib)
  fid.close()

dist=setup (name = "gerbmerge",
       license = "GPL",
       version = "%d.%d" % (VERSION_MAJOR, VERSION_MINOR),
      long_description=\
r"""GerbMerge is a program that combines several Gerber
(i.e., RS274-X) and Excellon files into a single set
of files. This program is useful for combining multiple
printed circuit board layout files into a single job.

To run the program, invoke the Python interpreter on the
gerbmerge.py file. On Windows, if you installed GerbMerge in
C:\Python32, for example, open a command window (DOS box)
and type:
    C:\Python32\gerbmerge.bat

For more details on installation or running GerbMerge, see the
URL below.
""",
       description = "Merge multiple Gerber/Excellon files",
       author = "Rugged Circuits LLC",
       author_email = "support@ruggedcircuits.com",
       url = "http://ruggedcircuits.com/gerbmerge",
       packages = ['gerbmerge'],
       platforms = ['all'],
       data_files = [ (DestDir, AuxFiles), 
                      (os.path.join(DestDir,'testdata'), SampleFiles),
                      (os.path.join(DestDir,'doc'), DocFiles),
                      (BinDir, BinFiles) ]
)

do_fix_perms = 0
if sys.platform != 'win32':
  for cmd in dist.commands:
   if cmd[:7]=='install':
    do_fix_perms = 1
    break

if do_fix_perms:
  # Ensure package files and misc/help files are world readable-searchable.
  # Shouldn't Distutils do this for us?
  print("Setting permissions on installed files...")
  try:
    CHMOD_755 = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    CHMOD_644 = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    def fixperms(arg, dirname, names):
      os.chmod(dirname, CHMOD_755)
      for name in names:
        fullname = os.path.join(dirname, name)
        if os.access(fullname, os.X_OK):
          os.chmod(fullname, CHMOD_755)
        else:
          os.chmod(fullname, CHMOD_644)

    os.path.walk(DestDir, fixperms, 1)
    os.path.walk(os.path.join(DestLib, 'site-packages/gerbmerge'), fixperms, 1)

    os.chmod(os.path.join(BinDir, 'gerbmerge'), CHMOD_755)
    print("done")
  except:
    print("FAILED")
    print()
    print("*** Please verify that the installed files have correct permissions. On")
    print("*** systems without permission flags, you don't need to")
    print("*** worry about it.")

for cmd in dist.commands:
  if cmd[:7]=='install':
    print()
    print("******** Installation Complete ******** ")
    print()
    print("Sample files and documentation have been installed in:")
    print("   ", DestDir)
    print()
    print("A shortcut to starting the program has been installed as:")
    print("   ", os.path.join(BinDir, 'gerbmerge'))
    print()
