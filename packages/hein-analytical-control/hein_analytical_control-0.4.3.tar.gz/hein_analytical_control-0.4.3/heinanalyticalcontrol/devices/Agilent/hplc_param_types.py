from dataclasses import dataclass
from enum import Enum
from typing import Union

# Commands sent to the Chemstation Macro
# See https://www.agilent.com/cs/library/usermanuals/Public/MACROS.PDF
class Command(Enum):
    def __str__(self):
        return '%s' % self.value
    
    RESET_COUNTER_CMD = "last_cmd_no = 0"
    GET_STATUS_CMD = "response$ = AcqStatus$"
    SLEEP_CMD = "Sleep {seconds}"
    STANDBY_CMD = "Standby"
    STOP_MACRO_CMD = "Stop"
    PREPRUN_CMD = "PrepRun"
    LAMP_ON_CMD = "LampAll ON"
    LAMP_OFF_CMD = "LampAll OFF"
    PUMP_ON_CMD = "PumpAll ON"
    PUMP_OFF_CMD = "PumpAll OFF"
    GET_METHOD_CMD = "response$ = _MethFile$"
    SWITCH_METHOD_CMD = 'LoadMethod "{method_dir}", "{method_name}.M"'
    START_METHOD_CMD = "StartMethod"
    RUN_METHOD_CMD = 'RunMethod "{data_dir}",, "{experiment_name}_{timestamp}"'
    STOP_METHOD_CMD = "StopMethod"
    UPDATE_METHOD_CMD = 'UpdateMethod'
    

class RegisterFlag(Enum):
    def __str__(self):
        return '%s' % self.value

    SOLVENT_A_COMPOSITION = "PumpChannel_CompositionPercentage"
    SOLVENT_B_COMPOSITION = "PumpChannel2_CompositionPercentage"
    SOLVENT_C_COMPOSITION = "PumpChannel3_CompositionPercentage"
    SOLVENT_D_COMPOSITION = "PumpChannel4_CompositionPercentage"
    FLOW = "Flow"
    MAX_TIME = "StopTime_Time"
    COLUMN_OVEN_TEMP1 = "TemperatureControl_Temperature"
    COLUMN_OVEN_TEMP2 = "TemperatureControl2_Temperature"


@dataclass
class Param:
    val: any
    chemstation_key: Union[RegisterFlag, list[RegisterFlag]]


@dataclass
class SolventRatio:
    solvent: str
    percent: float


@dataclass
class HPLCMethodParams:
    mobile_phase: Param
    organic_phase: Param
    flow: Param
    maximum_run_time: Param
    gradient_time: Param
    isocratic_hold_time: Param
    # temperature: Param


class HPLCRunningStatus(Enum):
    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    INJECTING = "INJECTING"
    PREPARING = "PREPARING"
    RUN = "RUN"
    NOTREADY = "NOTREADY"
    POSTRUN = "POSTRUN"
    RAWDATA = "RAWDATA"
    INITIALIZING = "INITIALIZING"
    NOMODULE = "NOMODULE"


class HPLCAvailStatus(Enum):
    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    PRERUN = "PRERUN"
    OFFLINE = "OFFLINE"
    STANDBY = "STANDBY"


class HPLCErrorStatus(Enum):

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    ERROR = "ERROR"
    BREAK = "BREAK"
    NORESPONSE = "NORESPONSE"
    MALFORMED = "MALFORMED"


class Optimizer(Enum):
    BAYBE = 0
    AX = 1


HPLC_WATCH_FILE = """Name MonitorFile
    Parameter infile$, outfile$
    Local in$, cmd_no, cmd$, response$, sep_position, cmd_len, last_cmd_no
    Print "infile: ", infile$, "outfile: ", outfile$

    ! Overwrite files
    Open infile$ for output as #3
    Print #3, "0 Sleep 1"
    Close #3
    Open outfile$ for output as #4
    Close #4

    last_cmd_no = 0

    Repeat
        errorflag = 0
        Sleep 0.5
        result$ = ""
        Open infile$ for input as #3
        Input #3, in$
        Close #3
        sep_position = InStr (in$, " ")
        cmd_len = Len (in$)
        cmd_no = Val (in$[1:sep_position])
        cmd$ = in$[(sep_position+1):cmd_len]

        If cmd_no > last_cmd_no Then
            last_cmd_no = cmd_no

            Print "Executing: ", in$

            ! Acknowledge reading command
            Open outfile$ for output as #4
            Print #4, cmd_no, "ACK"
            Close #4

            If cmd$ = "Exit" Then
                ! do nothing
            Else
                Evaluate cmd$
                On Error HandleError cmd_no, cmd$, outfile$
            EndIf

            If errorflag = 0 Then
                ! Write output
                Open outfile$ for append as #4
                Print #4, cmd_no, response$
                Close #4
            EndIf

            ! Confirm command execution
            Open outfile$ for append as #4
            Print #4, cmd_no, "DONE"
            Close #4
        EndIf
    Until cmd$ = "Exit"
    Print "Idle"
EndMacro

Name HandleError
    Parameter cmd_no, cmd$, outfile$
    errorflag = 1
    Open outfile$ for append as #4
    Print #4, "ERROR:", cmd_no, cmd$, "caused Error #", _Error
    Close #4
EndMacro

Name HPLCTalk_Loop
    MonitorFile "{file_name}\cmd.txt", "{file_name}\reply.txt""
EndMacro

Name HPLCTalk_Run
    If CPExists(HPLCTalk_Cp) = 0 Then
        CpStart HPLCTalk_Cp
    EndIf
    CpRequest HPLCTalk_Cp, HPLCTalk_Loop
EndMacro

Name HPLCTalk_Stop
    CpTerminate HPLCTalk_Cp
EndMacro"""
READ_WRITE_EXCEL_FILE = """! Macro code written by Thomas Dixon and edited by Lucy Hao.
! This macro reads the excel file that contains method conditions set by Python, and
! sets the conditions ready for the method to be executed.
Name UpdateMethod
  ! Pre-defines the variables that are used to set the method conditions.
{variable_definition}

  ! Creates a 'dynamic data exchange' with an open excel file so that the method data
  ! can be read.
  Chan = DDEInitiate("EXCEL", "{excel_file_path}")

  !!! Set the initial conditions for the pump based on the values in the excel sheet.
  ! Extract the different variables given the row and column number.
{read_in_excel_values}

  ! Initially change pump settings to the initial starting conditions. The table that
  ! stores the method data is deleted and then recreated using the correct headings.
  ! used before. Creating table from scratch helped to prevent several issues.
  ! Note the table is stored in the "RCPMP1Method[1]" register as "Timetable".
  DelTab RCPMP1Method[1], "Timetable"	! Deletes the table.

{update_hplc_method}

  sleep 0.2
  DownloadRCMethod PMP1
  Print("Method Updated")
  DDETerminate Chan
  Return
EndMacro"""
