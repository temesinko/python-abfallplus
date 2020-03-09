# -*- coding: utf-8 -*-

"""A library providing a Python interface for the Abfall+ API"""

__author__ = 'Jan Temešinko'
__email__ = 'jan+github@temesinko.de'
__copyright__ = 'Copyright (c) 2020 Jan Temešinko'
__license__ = 'MIT License'
__version__ = '0.1'
__url__ = 'https://github.com/temesinko/python-abfallplus'
# __download_url__ = ''
__description__ = 'A Python wrapper for the Abfall+ API'

from .models import (
    Community,
    Street,
    WasteType,
)

from .api import Api
