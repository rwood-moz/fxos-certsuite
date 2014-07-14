# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from webapi_tests.semiauto import TestCase
from webapi_tests.device_storage import DeviceStorageTestCommon


class TestSdcardStorage(TestCase, DeviceStorageTestCommon):

    def setUp(self):
        self.file_name = "test_sdcard_certsuite"
        self.file_contents = "This is a sample text file"
        self.addCleanup(self.clean_up)
        super(TestSdcardStorage, self).setUp()
        self.marionette.execute_script("window.wrappedJSObject.sdcard = navigator.getDeviceStorage(\"sdcard\")")

    def test_sdcard_availability(self):
        ret_check_sdcard = self.is_sdcard_available()
        self.assertEqual(True, ret_check_sdcard, "SDCard is unavailable. "
                        "Please ensure there is an SD card in the device and "
                        "usb storage sharing is not enabled")

    def test_add_namedfile_sdcard(self):
        if self.is_sdcard_available():
            #add the file to sdcard
            ret_add_namedfile_sdcard = self.add_namedfile_sdcard(self.file_name,
                                                            self.file_contents)

            self.assertEqual(True, ret_add_namedfile_sdcard, "Unable "
                             "to add the file")
            #delete the file for cleanup
            if self.delete_file_sdcard(self.file_name) is False:
                self.fail("Failed to delete the file")
        else:
            self.fail("Sdcard is unavailable")

    def test_get_file_sdcard(self):
        if self.is_sdcard_available():
            if self.add_namedfile_sdcard(self.file_name, self.file_contents):
                #get the file from sdcard
                ret_file_abspath_sdcard = self.get_file_sdcard(self.file_name)
                if ret_file_abspath_sdcard is False:
                    self.fail("Not Found the file")
                #delete the file for cleanup
                if self.delete_file_sdcard(self.file_name) is False:
                    self.fail("Failed to delete the file")
            else:
                self.fail("Unable to add the file")
        else:
            self.fail("Sdcard is unavailable")

    def test_delete_file_sdcard(self):
        if self.is_sdcard_available():
            if self.add_namedfile_sdcard(self.file_name, self.file_contents):
                #delete the file
                ret_file_delete_sdcard = self.delete_file_sdcard(self.file_name)
                self.assertEqual(True, ret_file_delete_sdcard, "Unable to "
                                "delete the file")
            else:
                self.fail("Unable to add the file")
        else:
            self.fail("Sdcard is unavailable")

    def test_enumerate_files_sdcard(self):
        if self.is_sdcard_available():
            if self.add_namedfile_sdcard(self.file_name, self.file_contents):
                #enumerate the files
                filelist_sdcard_unicode = self.enumerate_files_sdcard()
                self.assertNotEqual(0, len(filelist_sdcard_unicode), "There "
                                 "should be at least one file added as part "
                                 "of this test")
                ret_file_delete_sdcard = self.delete_file_sdcard(self.file_name)
                if self.delete_file_sdcard(self.file_name) is False:
                    self.fail("Failed to delete the file")
            else:
                self.fail("Unable to add the file")
        else:
            self.fail("Sdcard is unavailable")

    def clean_up(self):
        #As each test is using the same file, get and delete the file if any test fails in between
        if self.get_file_sdcard(self.file_name) is True:
            if self.delete_file_sdcard(self.file_name) is False:
                self.fail("Failed to delete the file in clean up")
        self.file_name = None
        self.file_contents = None
        self.marionette.execute_script("window.wrappedJSObject.sdcard = null")
