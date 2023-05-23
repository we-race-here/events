import logging
import os
import sys

log = logging.getLogger('apps')


def exception(e):
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)
        log.error(f' Error: {e}  Error Type:  {exc_type}  Module Name: {fname} Line No : {exc_tb.tb_lineno}')
    except Exception :
        log.error(e)
