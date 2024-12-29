"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple library to quere EODHistoricalData in a multithreaded environment
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from basefunctions.config_handler import ConfigHandler
from eod2pd.eod2pddownloadercallable import (
    EOD2PDMESSAGEIDENTIFIER,
    EOD2PDDownloaderCallable,
)
from eod2pd.eod2pddownloader import EOD2PDDownloader
from eod2pd.utils import get_dataframes_from_output_queue, create_multiindex_dataframe

__all__ = [
    "EOD2PDMESSAGEIDENTIFIER",
    "EOD2PDDownloaderCallable",
    "EOD2PDDownloader",
    "get_dataframes_from_output_queue",
    "create_multiindex_dataframe",
]

# load default config
ConfigHandler().load_default_config("eod2pd")

# get the default downloader
def get_default_downloader() -> EOD2PDDownloader:
    return default_downloader

# create a default downloader
default_downloader = EOD2PDDownloader()

