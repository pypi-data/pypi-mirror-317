from sys import version_info

from .driver import debugger, get_webdriver, upload_by_drop

if not all([version_info.major == 3, version_info.minor >= 9]):
    msg = """
    webdriver_helper: Python version should >=3.9，
    If you need to be compatible with special scenarios,
    please contact the developer for paid customization. """
    raise TypeError(msg)
