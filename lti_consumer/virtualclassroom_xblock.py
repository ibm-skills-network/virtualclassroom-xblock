import logging
from .utils import _
from django.conf import settings

from xblock.core import Scope, String
from xblock.fields import Boolean

from .lti_xblock import DOCS_ANCHOR_TAG_OPEN
from .lti_xblock import LtiConsumerXBlock

log = logging.getLogger(__name__)

class VirtualClassroomXBlock(LtiConsumerXBlock):
    """
    This XBlock extends the LtiConsumerXBlock to provide a default configuration suitable for
    Skills Network Virtual Classroom.
    """

    display_name = String(
        display_name=_("Display Name"),
        help=_(
            "Enter the name that students see for this component. "
            "Analytics reports may also use the display name to identify this component."
        ),
        scope=Scope.settings,
        default=_("Virtual Classroom"),
    )
    lti_id = String(
        display_name=_("LTI ID"),
        help=_(
            "Enter the LTI ID for the external LTI provider. "
            "This value must be the same LTI ID that you entered in the "
            "LTI Passports setting on the Advanced Settings page."
            "<br />See the {docs_anchor_open}edX LTI documentation{anchor_close} for more details on this setting."
        ).format(
            docs_anchor_open=DOCS_ANCHOR_TAG_OPEN,
            anchor_close="</a>"
        ),
        default='virtualclassroom',
        scope=Scope.settings
    )
    launch_url = String(
        display_name=_("LTI URL"),
        help=_(
            "Enter the URL of the external tool that this component launches. "
            "This setting is only used when Hide External Tool is set to False."
            "<br />See the {docs_anchor_open}edX LTI documentation{anchor_close} for more details on this setting."
        ).format(
            docs_anchor_open=DOCS_ANCHOR_TAG_OPEN,
            anchor_close="</a>"
        ),
        default='http://localhost:4000/tool',
        scope=Scope.settings
    )
    ask_to_send_username = Boolean(
        display_name=_("Request user's username"),
        # Translators: This is used to request the user's username for a third party service.
        help=_("Select True to request the user's username."),
        default=True,
        scope=Scope.settings
    )
    ask_to_send_email = Boolean(
        display_name=_("Request user's email"),
        # Translators: This is used to request the user's email for a third party service.
        help=_("Select True to request the user's email address."),
        default=True,
        scope=Scope.settings
    )
    enable_processors = Boolean(
        display_name=_("Send extra parameters"),
        help=_("Select True to send the extra parameters, which might contain Personally Identifiable Information. "
               "The processors are site-wide, please consult the site administrator if you have any questions."),
        default=True,
        scope=Scope.settings
    )
    @property
    def lti_provider_key_secret(self):
        """
        Obtains client_key and client_secret credentials from current course.
        """
        if 'id' in settings.LTI_CREDENTIALS:
            return settings.LTI_CREDENTIALS['id'], settings.LTI_CREDENTIALS['secret']

        log.info("LTI_CREDENTIALS is not set! Using passports from advanced settings instead.")

        return super().lti_provider_key_secret
