"""
Module to provide API for the remote control of the Agilent HPLC systems.

HPLCController sends commands to Chemstation software via a command file.
Answers are received via reply file. On the Chemstation side, a custom
Macro monitors the command file, executes commands and writes to the reply file.
Each command is given a number (cmd_no) to keep track of which commands have
been processed.

.. moduleauthor:: Alexander Hammer, Hessam Mehr
"""

import time
import os
import logging
import polling

from .hplc_param_types import Command, HPLCAvailStatus, HPLCRunningStatus, HPLCErrorStatus
from .chromatogram import AgilentHPLCChromatogram, TIME_FORMAT

# maximum command number
MAX_CMD_NO = 255

# Default Chemstation data directory
DEFAULT_DATA_DIR = "C:\\Users\\Public\\Documents\\ChemStation\\1\\Data"

# Default Chemstation methods directory
DEFAULT_METHOD_DIR = ""


class HPLCController:
    """
    Class to control Agilent HPLC systems via Chemstation Macros.
    """

    def __init__(
            self,
            comm_dir: str,
            data_dir: str = None,
            cmd_file: str = "cmd",
            reply_file: str = "reply",
            logger=None,
    ):
        """
        Initialize HPLC controller.
        comm_dir: Name of directory for communication.
        data_dir: path to where chemstation will save the data.
                    If None, data will be saved in default folder Chem32\\1\\Data
        cmd_file: name of command file
        reply_file: name of reply file
        The macro must be loaded in the Chemstation software.
        dir and filenames must match those specified in the Macro.
        """
        self.cmd_file = os.path.join(comm_dir, cmd_file)
        self.reply_file = os.path.join(comm_dir, reply_file)
        self.cmd_no = 0
        self._most_recent_hplc_status = None

        if data_dir is None:
            if os.path.isdir(DEFAULT_DATA_DIR):
                self.data_dir = DEFAULT_DATA_DIR
            else:
                raise FileNotFoundError(
                    f"Default data_dir {DEFAULT_DATA_DIR} not found."
                )
        else:
            self.data_dir = data_dir

        self.spectra = {
            "A": AgilentHPLCChromatogram(self.data_dir),
            "B": AgilentHPLCChromatogram(self.data_dir),
            "C": AgilentHPLCChromatogram(self.data_dir),
            "D": AgilentHPLCChromatogram(self.data_dir),
        }

        self.data_files = []

        # Create files if needed
        open(self.cmd_file, "a").close()
        open(self.reply_file, "a").close()

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("hplc_logger")
            self.logger.addHandler(logging.NullHandler())

        self.reset_cmd_counter()

        self.logger.info("HPLC Controller initialized.")

    def _set_status(self):
        """
        """
        status = self.status()[0]
        self._most_recent_hplc_status = HPLCAvailStatus[status] if HPLCAvailStatus.has_member_key(status) else HPLCRunningStatus[status] if HPLCRunningStatus.has_member_key(status) else HPLCErrorStatus[status] if HPLCErrorStatus.has_member_key(status) else ""

    def _check_data_status(self):
        old_status = self._most_recent_hplc_status
        self._set_status()
        ready_with_data = isinstance(self._most_recent_hplc_status, HPLCAvailStatus) and old_status != self._most_recent_hplc_status
        return ready_with_data

    def check_hplc_ready_with_data(self):
        """
        """
        self._set_status()

        hplc_run_done = polling.poll(
            lambda: self._check_data_status(),
            # ignore_exceptions=(IOError,),
            timeout=(10) * 60,
            step=30
        )

        return hplc_run_done

    def _send(self, cmd: str, cmd_no: int, num_attempts=5):
        """
        Low-level execution primitive. Sends a command string to HPLC.

        Args:
            cmd: Command string to be sent
            cmd_no: Command number

        Raises:
            IOError: Could not write to command file.
        """
        err = None
        for _ in range(num_attempts):
            time.sleep(1)
            try:
                with open(self.cmd_file, "w", encoding="utf8") as cmd_file:
                    cmd_file.write(f"{cmd_no} {cmd}")
            except IOError as e:
                err = e
                self.logger.warning("Failed to send command; trying again.")
                continue
            else:
                self.logger.info("Sent command #%d: %s.", cmd_no, cmd)
                return
        else:
            raise IOError(f"Failed to send command #{cmd_no}: {cmd}.") from err

    def _receive(self, cmd_no: int, num_attempts=100) -> str:
        """
        Low-level execution primitive.

        Args:
            cmd_no: Command number
            num_retries: Number of retries to open reply file

        Raises:
            IOError: Could not read reply file.
        """
        err = None
        for _ in range(num_attempts):
            time.sleep(1)

            try:
                with open(self.reply_file, "r", encoding="utf_16") as reply_file:
                    response = reply_file.read()
            except OSError as e:
                err = e
                self.logger.warning("Failed to read from reply file; trying again.")
                continue

            try:
                first_line = response.splitlines()[0]
                response_no = int(first_line.split()[0])
            except IndexError as e:
                err = e
                self.logger.warning("Malformed response %s; trying again.", response)
                continue

            # check that response corresponds to sent command
            if response_no == cmd_no:
                self.logger.info("Reply: \n%s", response)
                return response
            else:
                self.logger.warning(
                    "Response #: %d != command #: %d; trying again.",
                    response_no,
                    cmd_no,
                )
                continue
        else:
            raise IOError(f"Failed to receive reply to command #{cmd_no}.") from err

    def send(self, cmd: str):
        """
        Sends a command to Chemstation.

        Args:
            cmd: Command to be sent
        """
        if self.cmd_no == MAX_CMD_NO:
            self.reset_cmd_counter()

        self.cmd_no += 1
        self._send(cmd, self.cmd_no)

    def receive(self) -> str:
        """
        Returns messages received in reply file.
        """
        return self._receive(self.cmd_no)

    def reset_cmd_counter(self):
        """
        Resets the command counter.
        """
        self._send(Command.RESET_COUNTER_CMD, cmd_no=MAX_CMD_NO + 1)
        self._receive(cmd_no=MAX_CMD_NO + 1)
        self.cmd_no = 0

        self.logger.debug("Reset command counter")

    def sleep(self, seconds: int):
        """
        Tells the HPLC to wait for a specified number of seconds.

        Args:
            seconds: number of seconds to wait
        """
        self.send(Command.SLEEP_CMD.format(seconds=seconds))
        self.logger.debug("Sleep command sent.")

    def standby(self):
        """
        Switches all modules in standby mode.
        All lamps and pumps are switched off.
        """
        self.send(Command.STANDBY_CMD)
        self.logger.debug("Standby command sent.")

    def preprun(self):
        """
        Prepares all modules for run.
        All lamps and pumps are switched on.
        """
        self.send(Command.PREPRUN_CMD)
        self.logger.debug("PrepRun command sent.")

    def status(self):
        """
        Returns a list with the device status. It can be:
        INITIALIZING    Set during initialization
        NOMODULE        No module configured
        OFFLINE         Currently in offline mode
        STANDBY         All modules in standby mode. Lamps/pumps switched off
        PRERUN          Ready to start run
        INJECTING       Injecting
        PREPARING       Run is being prepared. For example, doing a balance
        RUN             Run is in progress
        POSTRUN         Postrun is in progress
        RAWDATA         Rawdata are still being processed following a run
        NOTREADY        Run cannot be started
        ERROR           Error occurred
        BREAK           Injection paused
        NORESPONSE
        MALFORMED
        """
        self.send(Command.GET_STATUS_CMD)
        time.sleep(1)

        try:
            parsed_response = self.receive().splitlines()[1].split()[1:]
        except IOError:
            return ["NORESPONSE"]
        except IndexError:
            return ["MALFORMED"]
        return parsed_response

    def stop_macro(self):
        """
        Stops Macro execution. Connection will be lost.
        """
        self.send(Command.STOP_MACRO_CMD)

    def update_method_param(self, param_type, param_value, register:str):
        """
        SetObjHdrVal RCPMP1Method[1], "PumpChannel2_CompositionPercentage", organic_phase
        """
        setting_command = "SetObjHdrVal" if param_type == "num" else "SetObjHdrText"

        self.send(
            f'{setting_command} RCPMP1Method[1], {register}, {param_value}'
        )
        time.sleep(2)


    def desired_method_already_loaded(self, method_name):
        """
        """
        self.send(Command.GET_METHOD_CMD)
        parsed_response = self._hplc_controller.receive().splitlines()[1].split()[1:][0]
        return method_name in parsed_response
    
    def switch_method(self, method_name: str, method_dir=DEFAULT_METHOD_DIR):
        """
        Allows the user to switch between pre-programmed methods.

        Args:
            method_name: any available method in Chemstation method directory

        Raises:
            IndexError: Response did not have expected format. Try again.
            AssertionError: The desired method is not selected. Try again.
        """
        self.send(
            Command.SWITCH_METHOD_CMD.format(method_dir=method_dir, method_name=method_name)
        )

        time.sleep(2)
        self.send(Command.GET_METHOD_CMD)
        time.sleep(2)
        # check that method switched
        for _ in range(10):
            try:
                parsed_response = self.receive().splitlines()[1].split()[1:][0]
                break
            except IndexError:
                self.logger.debug("Malformed response. Trying again.")
                continue

        assert parsed_response == f"{method_name}.M", "Switching Methods failed."

    def lamp_on(self):
        """
        Turns the UV lamp on.
        """
        self.send(Command.LAMP_ON_CMD)

    def lamp_off(self):
        """
        Turns the UV lamp off.
        """
        self.send(Command.LAMP_OFF_CMD)

    def pump_on(self):
        """
        Turns on the pump on.
        """
        self.send(Command.PUMP_ON_CMD)

    def pump_off(self):
        """
        Turns the pump off.
        """
        self.send(Command.PUMP_OFF_CMD)

    def start_method(self):
        """
        Starts and executes a method to run according to Run Time Checklist.
        Device must be ready. (status="PRERUN")
        """
        self.send(Command.START_METHOD_CMD)

    def run_method(self, data_dir: str, experiment_name: str):
        """
        This is the preferred method to trigger a run.
        Starts the currently selected method, storing data
        under the <data_dir>/<experiment_name>.D folder.
        The should <experiment_name> end with a timestamp in the '%Y-%m-%d-%H-%M' format.
        Device must be ready. (status="PRERUN")

        Args:
            data_dir: Directory where to save the data
            experiment_name: Name of the experiment
        """
        timestamp = time.strftime(TIME_FORMAT)

        self.send(
            Command.RUN_METHOD_CMD.format(
                data_dir=data_dir, experiment_name=experiment_name, timestamp=timestamp
            )
        )

        folder_name = f"{experiment_name}_{timestamp}.D"
        self.data_files.append(os.path.join(data_dir, folder_name))
        self.logger.info("Started HPLC run:  %s.", folder_name)

    def stop_method(self):
        """
        Stops the run.
        A dialog window will pop up and manual intervention may be required.
        """
        self.send(Command.STOP_METHOD_CMD)

    def get_spectrum(self):
        """
        Load last chromatogram for any channel in spectra dictionary.
        """
        # will block if spectrum is measuring
        last_file = self.data_files[-1] if len(self.data_files) > 0 else None

        if last_file is None:
            raise IndexError

        for channel, spec in self.spectra.items():
            spec.load_spectrum(data_path=last_file, channel=channel)
            self.logger.info("%s chromatogram loaded.", channel)


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.DEBUG)

    controller = HPLCController(os.path.dirname(sys.argv[-1]))

    controller.send('Print "Hi"')
