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

        # wip: verify the other call fields

        # hang-up the call via the webapi and verify
        self.hangup_active_call()
