"""
_encoding_fix.py -- UTF-8 stdout/stderr fix for Windows cp1250 consoles.

Usage (at the top of main()):
    from _encoding_fix import fix_stdout
    fix_stdout()

Background: Windows PowerShell and cmd default to cp1250/cp1252 which cannot
encode Hungarian accented characters (e.g. \xb2, ő). MCP Bash/PS tools
also capture stdout in the system encoding. This fix forces UTF-8 with
'replace' error handling so scripts never crash on console output.
"""

import io
import sys


def fix_stdout():
    """Wrap sys.stdout and sys.stderr in UTF-8 with 'replace' error handling."""
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
