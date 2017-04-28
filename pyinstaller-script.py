#!"D:\portable\Portable Python 2.7.3.1\App\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==2.1','console_scripts','pyinstaller'
__requires__ = 'PyInstaller==2.1'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('PyInstaller==2.1', 'console_scripts', 'pyinstaller')()
)
