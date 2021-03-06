# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from webapi_tests.semiauto import TestCase
from webapi_tests.telephony import TelephonyTestCommon


class TestTelephonyOutgoing(TestCase, TelephonyTestCommon):
    """
    This is a test for the `WebTelephony API`_ which will:

    - Disable the default gaia dialer, so that the test app can handle calls
    - Ask the test user to specify a destination phone number for the test call
    - Setup mozTelephonyCall event listeners for the outgoing call
    - Use the API to initiate the outgoing call
    - Ask the test user to answer the call on the destination phone
    - Keep the call active for 5 seconds, then hang up the call via the API
    - Verify that the corresponding mozTelephonyCall events were triggered
    - Re-enable the default gaia dialer

    .. _`WebTelephony API`: https://developer.mozilla.org/en-US/docs/Web/Guide/API/Telephony
    """

    def setUp(self):
        self.addCleanup(self.clean_up)
        super(TestTelephonyOutgoing, self).setUp()
        self.wait_for_obj("window.navigator.mozTelephony")
        # disable the default dialer manager so it doesn't grab our calls
        self.disable_dialer()

    def test_telephony_outgoing(self):
        # use the webapi to make an outgoing call to user-specified number
        self.user_guided_outgoing_call()

        # have user answer the call on target
        self.answer_call(incoming=False)

        # keep call active for awhile
        time.sleep(5)

        # disconnect the active call
        self.hangup_call()

    def clean_up(self):
        # re-enable the default dialer manager
        self.enable_dialer()
