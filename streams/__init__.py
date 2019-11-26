u"""
Modules:
    exergy: exergy calculations.
"""

__version__ = '0.0.1'

import pkg_resources
from streams import exergy

REF_FILE       = pkg_resources.resource_filename('streams', 'data/ReferenceTables.xlsx')
GATEX_EXE_FILE = pkg_resources.resource_filename('streams', 'gatex_pc_if97_mj.exe')

# Load reference substance values
refs = exergy.load_reference(REF_FILE)
