import time

class TelephonyTestCommon(object):
    def __init__(self):
        self.active_call = None
        self.marionette.execute_async_script("""        
        SpecialPowers.setBoolPref("dom.sms.enabled", true);
        SpecialPowers.addPermission("sms", true, document);
        marionetteScriptFinished(1);
        """, special_powers=True)

    def user_guided_incoming_call(self):
        # setup listener for incoming call
        self.marionette.execute_async_script("""        
        window.wrappedJSObject.receivedCall = false;
        window.navigator.mozTelephony.onincoming = function onincoming(event) {
            console.log("Received 'onreceived' mozTelephonyMessage event");
            window.wrappedJSObject.receivedCall = true;
            window.wrappedJSObject.active_call = event.message;
        };
        marionetteScriptFinished(1);
        """, special_powers=True)

        self.instruct("From a different phone, call the Firefox OS device, and answer the call")

        # verify call was received
        received = self.marionette.execute_script("return window.wrappedJSObject.receivedCall")
        self.assertTrue(received, "Call not received (mozTelephony.onincoming event not found)")

        # verify call type
        self.active_call = self.marionette.execute_script("return window.wrappedJSObject.active_call")
        # wip: verify call details

        # wip: also verify telephonyCall.state and telephonyCall.onincoming/alerting/connected events

        # don't need listener
        self.marionette.execute_script("window.navigator.mozTelephony.onincoming = null")

    def hangup_active_call(self):
        # hangup the active call via the webapi and verify
        self.marionette.execute_async_script("""        
        window.wrappedJSObject.receivedEvent = false;
        window.navigator.mozTelephony.onincoming = function oncallschanged(event) {
            console.log("Received 'oncallschanged' mozTelephonyMessage event");
            window.wrappedJSObject.receivedEvent = true;
            window.wrappedJSObject.event = event.message;
        };

        // hangup the call
        // WIP

        marionetteScriptFinished(1);
        """, special_powers=True)

        # verify call was ended
        received = self.marionette.execute_script("return window.wrappedJSObject.receivedEvent")
        self.assertTrue(received, "Call not ended (mozTelephony.oncallschanged event not found)")

        self.active_call = self.marionette.execute_script("return window.wrappedJSObject.active_call")
        # wip: verify call details

        # wip: need to verify telehonyCall.state and telephonyCall.ondisconnected

        # don't need listener
        self.marionette.execute_script("window.navigator.mozTelephony.onincoming = null")
