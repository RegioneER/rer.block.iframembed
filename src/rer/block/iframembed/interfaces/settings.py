# -*- coding: utf-8 -*-
from rer.block.iframembed import _
from plone.restapi.controlpanels.interfaces import IControlpanel
from zope.interface import Interface
from zope import schema


class IRerBlockIframembedSettings(Interface):
    """Interface for RerBlockIframembed controlpanel"""

    available_domains = schema.Tuple(
        title=_(u'Allowed domains'),
        description=_(u"One value for row"),
        missing_value=None,

        value_type=schema.TextLine()
    )


class IRerBlockIframembedSettingsControlpanel(IControlpanel):
    """ """
