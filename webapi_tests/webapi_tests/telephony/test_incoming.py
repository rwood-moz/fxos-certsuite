from webapi_tests import MinimalTestCase
from webapi_tests import TelephonyTestCommon

class TestIncomingCall(MinimalTestCase, TelephonyTestCommon):
    def tearDown(self):
        self.marionette.execute_script("""
            SpecialPowers.removePermission("sms", document);
            SpecialPowers.setBoolPref("dom.sms.enabled", false);
        """)
        MinimalTestCase.tearDown(self)

    def test_incoming_call(self):
        self.user_guided_incoming_call()

        # work in progress: verify the other message fields
