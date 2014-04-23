# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.wait import Wait


class CameraTestCommon(object):
    def get_list_of_cameras(self):
        camera_list = self.marionette.execute_script("return window.navigator.mozCameras.getListOfCameras()")
        self.assertTrue(camera_list is not None, "getListOfCameras should return an array")
        return camera_list

    def get_camera(self, camera_to_get):
        # get camera instance
        options = {'camera': camera_to_get}

        self.marionette.execute_async_script("""
        var options = arguments[0];
        var camera_manager = window.navigator.mozCameras;
        window.wrappedJSObject.camera_control = null;
        window.wrappedJSObject.rcvd_success = false;
        window.wrappedJSObject.rcvd_error = false;

        function onSuccess(camera) {
            console.log("RW: get camera success");
            window.wrappedJSObject.camera_control = camera;
            window.wrappedJSObject.rcvd_success = true;
        };

        function onError(error) {
            window.wrappedJSObject.rcvd_error = true;
            console.log(error);
        };

        console.log("RW: about to get camera");

        camera_manager.getCamera(options, onSuccess, onError);
        marionetteScriptFinished(1);
        """, script_args=[options])

        # wait for camera instance
        wait = Wait(self.marionette, timeout=10, interval=0.5)
        try:
            wait.until(lambda x: x.execute_script("return window.wrappedJSObject.rcvd_success"))
        except:
            if (self.marionette.execute_script("return window.wrappedJSObject.rcvd_error")):
                self.fail("mozCameras.getCamera returned error")
            else:
                self.fail("Failed to get camera")

        return(self.marionette.execute_script("return window.wrappedJSObject.camera_control"))

    def capture_single_photo(self):
        # take single photo via the webapi; assumes camera instance exists
        self.marionette.execute_async_script("""
        var camera_control = window.wrappedJSObject.camera_control;
        var storage = window.navigator.getDeviceStorage('pictures');
        window.wrappedJSObject.capture_success = false;
        window.wrappedJSObject.capture_error = false;

        var options = {
            pictureSize: camera_control.capabilities.pictureSizes[0],
            fileFormat: camera_control.capabilities.fileFormats[0]           
        };

        function captureSuccess(blob) {
            storage.addNamed(blob, 'cert_' + Date.now().toString() + '.jpg');
            console.log("RW: capture success, blob just saved");
            window.wrappedJSObject.capture_success = true;
        };

        function captureError(error) {
            console.log("RW: capture error");
            window.wrappedJSObject.capture_error = true;
            console.log(error);
        };

        console.log("RW: about to take photo");
        camera_control.takePicture(options, captureSuccess, captureError);

        marionetteScriptFinished(1);
        """)

        # wait for photo capture
        wait = Wait(self.marionette, timeout=10, interval=0.5)
        try:
            wait.until(lambda x: x.execute_script("return window.wrappedJSObject.capture_success"))
        except:
            if (self.marionette.execute_script("return window.wrappedJSObject.capture_error")):
                self.fail("CameraControl.takePhoto returned error")
            else:
                self.fail("Failed to take photo")

    def release_camera(self):
        # if camera is in use, release it
        if (self.marionette.execute_script("return window.wrappedJSObject.camera_control") != None):
            # release camera instance
            self.marionette.execute_async_script("""
            var camera_control = window.wrappedJSObject.camera_control;
            window.wrappedJSObject.release_success = false;
            window.wrappedJSObject.release_error = false;

            function relSuccess(camera) {
                window.wrappedJSObject.camera_control = null;
                window.wrappedJSObject.rel_success = true;
                console.log("RW: release camera success");
            };

            function relError(error) {
                window.wrappedJSObject.rel_error = true;
                console.log(error);
            };

            if (camera_control != null) {
                console.log("RW: about to release camera");
                camera_control.release(relSuccess, relError);
            };
            marionetteScriptFinished(1);
            """)

            # wait for camera release
            wait = Wait(self.marionette, timeout=10, interval=0.5)
            try:
                wait.until(lambda x: x.execute_script("return window.wrappedJSObject.rel_success"))
            except:
                if (self.marionette.execute_script("return window.wrappedJSObject.rel_error")):
                    self.fail("CameraControl.release returned error")
                else:
                    self.fail("Failed to release camera")
