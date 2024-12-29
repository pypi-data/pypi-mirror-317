import unittest

from heinanalyticalcontrol.devices import HPLCController
from heinanalyticalcontrol.devices.Agilent.hplc_param_types import HPLCAvailStatus

CHEMSTATION_MACRO_PATH = "C:\\Program Files (x86)\\Agilent Technologies\\ChemStation\\CORE"
# TODO find this automatically
pba = "C:\\Users\\Public\\Documents\\ChemStation\\2\\Data\\hplcOpt 2024-11-18 15-31-52\\001-2-phenylboronic acid.D"

# Ensure path exists
# Otherwise change the path in the macro file and restart the macro in chemstation
default_command_path = "C:\\Users\\User\\Desktop\\Lucy\\hplc-method-optimization\\tests"
default_method_name = "GENERAL-POROSHELL"
default_method_dir = "C:\\ChemStation\\1\\Methods\\"
data_dir_old = "C:\\Users\\User\\Desktop\\Lucy\\hplc-method-optimization\\hplc_data"
READ_NEW_METHOD_PARAMS = "TODO"
data_dir = "C:\\Users\\Public\\Documents\\ChemStation\\2\\Data"


class TestChemStationIntegration(unittest.TestCase):

    def test_chemstation_response(self):
        hplc = HPLCController(comm_dir=default_command_path)
        # Check the status
        self.assertTrue("NORESPONSE" not in hplc.status() and "MALFORMED" not in hplc.status())

    def test_load_existing_method(self):
        hplc = HPLCController(comm_dir=default_command_path)

        # Switch the method
        # ".M" is appended to the method name by default
        hplc.switch_method(method_name=default_method_name)

        # Check the status
        self.assertTrue("NORESPONSE" not in hplc.status() and "MALFORMED" not in hplc.status())

    def test_update_method(self):
        # need to update method
        hplc = HPLCController(comm_dir=default_command_path)
        try:
            hplc.update_method()
        except Exception as e:
            self.fail(f"hplc update method raised an {e} unexpectedly!")

    def test_hplc_status_enum(self):
        self.assertFalse(HPLCAvailStatus.has_member_key('INJECTING'))
        self.assertTrue(HPLCAvailStatus.has_member_key('STANDBY'))

if __name__ == '__main__':
    unittest.main()
