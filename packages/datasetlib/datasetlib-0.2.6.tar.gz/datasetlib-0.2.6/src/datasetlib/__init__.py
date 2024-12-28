# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : datasetlib
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  datasetlib provides quick and easy access to datasets in different fields 
#  of interest
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from basefunctions.config_handler import ConfigHandler
from datasetlib.datasets import get_dataset, get_datasets

# load default config
ConfigHandler().load_default_config("datasetlib")