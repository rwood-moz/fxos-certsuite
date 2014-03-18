import time

class TelephonyTestCommon(object):
    def __init__(self):
        self.in_call = None
        self.marionette.execute_async_script("""        
        SpecialPowers.setBoolPref("dom.sms.enabled", true);
        SpecialPowers.addPermission("sms", true, document);
        marionetteScriptFinished(1);
        """, special_powers=True)

    def user_guided_incoming_call(self):
        # setup listener for incoming call
        self.marionette.execute_async_script("""        
        window.wrappedJSObject.receivedCall = false;
        window.navigator.mozTelephony.onreceived = function onreceived(event) {
            console.log("Received 'onreceived' mozTelephonyMessage event");
            window.wrappedJSObject.receivedCall = true;
            window.wrappedJSObject.in_call = event.message;
        };
        marionetteScriptFinished(1);
        """, special_powers=True)

        self.instruct("From a different phone, phone the Firefox OS device, and answer the call")

        # verify call was received
        received = self.marionette.execute_script("return window.wrappedJSObject.receivedCall")
        self.assertTrue(received, "Call not received (mozTelephony.onreceived event not found)")

        # verify call event
        self.in_call = self.marionette.execute_script("return window.wrappedJSObject.in_call")
        print "Received call (id: %s)" %self.in_call['id']
        self.assertTrue(len(self.in_call['body']) > 0, "Received SMS has no message body (was text included in the sent SMS message?)")
        self.confirm("Received call with text '%s'; does this text match what was sent to the Firefox OS phone?" %self.in_sms['body'])

        # don't need listener
        self.marionette.execute_script("window.navigator.mozTelephony.onreceived = null")
