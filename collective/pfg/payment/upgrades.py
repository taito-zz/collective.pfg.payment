from Products.CMFCore.utils import getToolByName

import logging


PROFILE_ID = 'profile-collective.pfg.payment:default'


def upgrade_1000_to_1001(context, logger=None):
    """Reimport actions.xml"""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting actions.')
    setup.runImportStepFromProfile(
        PROFILE_ID, 'actions', run_dependencies=False, purge_old=False)
    logger.info('Reimported actions.')
