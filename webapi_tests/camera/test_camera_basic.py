# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from semiauto import TestCase
from camera import CameraTestCommon


class TestCameraBasic(TestCase, CameraTestCommon):
    def tearDown(self):
        # ensure camera has been released
        self.release_camera()
        TestCase.tearDown(self)

    def test_get_list_of_cameras(self):
        # expect 1 or 2 cameras
        camera_list = self.get_list_of_cameras()
        self.assertTrue(0 < len(camera_list) < 3, "getListOfCameras should return 1 or 2 cameras")

    def test_get_camera(self):
        # get camera instance
        camera_list = self.get_list_of_cameras()
        if camera_list[0] is not None:
            camera_control = self.get_camera(camera_list[0])
            # camera control is hardware specific so cannot check for specific
            # properties or values; just verify the capabilities array exists
            self.assertNotEqual(camera_control['capabilities'], None, \
                                "CameraControl.capabilities must exist")
            # done with camera
            self.release_camera()
        else:
            self.fail("No camera available")

    def test_capture_single_photo(self):
        # get camera instance
        camera_list = self.get_list_of_cameras()
        if camera_list[0] is not None:
            self.get_camera(camera_list[0])
            # ask user to hold up phone
            self.instruct("Please hold up the Firefox OS phone, with the screen facing you and the camera lens exposed")
            # take a photo via webapi
            self.capture_single_photo()
            # ask user to verify photo is in gallery
            self.confirm("A photo has just been taken. Please go into the phone's gallery app and verify. \
            Is there a new photo in the picture gallery?")
            # done with camera
            self.release_camera()
        else:
            self.fail("No camera available")

    def test_release_camera(self):
        # get camera
        camera_list = self.get_list_of_cameras()
        if camera_list[0] is not None:
            camera_control = self.get_camera(camera_list[0])
        else:
            self.fail("No camera available")
        # release camera
        self.release_camera()
        # get again, to verify it was released
        camera_control = self.get_camera(camera_list[0])
        # release
        self.release_camera()
