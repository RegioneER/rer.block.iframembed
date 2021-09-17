from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from rer.block.iframembed.interfaces.settings import IRerBlockIframembedSettings  # noqa
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import os


class HTMLBlockDeserializerBase:
    order = 100
    block_type = "html"
    disabled = os.environ.get("disable_transform_html", False)

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self, block):

        portal_transforms = api.portal.get_tool(name="portal_transforms")
        url_to_embed = block.get("html", "")

        valid_domains = api.portal.get_registry_record(
            'available_domains',
            interface=IRerBlockIframembedSettings)

        authorized = False
        for domain in valid_domains:
            if url_to_embed.find(domain) != -1:
                authorized = True
                break

        if not authorized:
            msg = "L'url indicato non e' valido per i domini ammessi"
            raise BadRequest(msg)

        data = portal_transforms.convertTo(
            "text/x-html-safe", url_to_embed, mimetype="text/html"
        )

        html = data.getData()
        block["html"] = html

        return block


@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldDeserializationTransformer)
class HTMLBlockDeserializer(HTMLBlockDeserializerBase):
    """Deserializer for content-types that implements IBlocks behavior"""
