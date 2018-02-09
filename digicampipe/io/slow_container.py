from numpy import ndarray, uint8, int64, int32, float32, float64

from astropy import units as u
from ctapipe.core import Container
try:
    from ctapipe.core import Field
except ImportError:
    from ctapipe.core import Item as Field


__all__ = [
    "DriveSystemContainer",
    "fill_DriveSystem",
    "MasterSST1MContainer",
    "fill_MasterSST1M",
    "DigicamSlowControlContainer",
    "fill_DigicamSlowControl",
    "SafetyPLCContainer",
    "fill_SafetyPLC",
    "PDPSlowControlContainer",
    "fill_PDPSlowControl",
    "SlowDataContainer",
    "fill_slow",
]


class DriveSystemContainer(Container):
    capacity_exceeded_error_crit_time = Field(int64, "capacity_exceeded_error_crit_time")
    capacity_exceeded_error_ec = Field(int64, "capacity_exceeded_error_ec")
    capacity_exceeded_error_rev = Field(int64, "capacity_exceeded_error_rev")
    current_cache_size = Field(int64, "current_cache_size")
    current_max_velocity_az = Field(float32, "current_max_velocity_az")
    current_max_velocity_el = Field(float32, "current_max_velocity_el")
    current_nominal_position_az = Field(float32, "current_nominal_position_az")
    current_nominal_position_el = Field(float32, "current_nominal_position_el")
    current_position_az = Field(float32, "current_position_az")
    current_position_el = Field(float32, "current_position_el")
    current_time = Field(int64, "current_time")
    current_track_step_pos_az = Field(float32, "current_track_step_pos_az")
    current_track_step_pos_el = Field(float32, "current_track_step_pos_el")
    current_track_step_t = Field(int64, "current_track_step_t")
    current_velocity_az = Field(float32, "current_velocity_az")
    current_velocity_el = Field(float32, "current_velocity_el")
    has_cache_capacity = Field(int64, "has_cache_capacity")
    has_local_mode_requested = Field(uint8, "has_local_mode_requested")
    has_remote_mode_requested = Field(uint8, "has_remote_mode_requested")
    in__position_az = Field(float32, "in__position_az")
    in__position_el = Field(float32, "in__position_el")
    in__t_after = Field(int64, "in__t_after")
    in__track_step_pos_az = Field(float32, "in__track_step_pos_az")
    in__track_step_pos_el = Field(float32, "in__track_step_pos_el")
    in__track_step_t = Field(int64, "in__track_step_t")
    in__v_rel = Field(float32, "in__v_rel")
    invalid_argument_error_crit_time = Field(int64, "invalid_argument_error_crit_time")
    invalid_argument_error_ec = Field(int64, "invalid_argument_error_ec")
    invalid_argument_error_rev = Field(int64, "invalid_argument_error_rev")
    invalid_operation_error_crit_time = Field(int64, "invalid_operation_error_crit_time")
    invalid_operation_error_ec = Field(int64, "invalid_operation_error_ec")
    invalid_operation_error_rev = Field(int64, "invalid_operation_error_rev")
    is_in_park_position = Field(uint8, "is_in_park_position")
    is_in_parking_zone = Field(uint8, "is_in_parking_zone")
    is_in_start_position = Field(uint8, "is_in_start_position")
    is_moving = Field(uint8, "is_moving")
    is_off = Field(uint8, "is_off")
    is_on_source = Field(uint8, "is_on_source")
    is_tracking = Field(uint8, "is_tracking")
    no_permission_error_crit_time = Field(int64, "no_permission_error_crit_time")
    no_permission_error_ec = Field(int64, "no_permission_error_ec")
    no_permission_error_rev = Field(int64, "no_permission_error_rev")
    operation_aborted_error_crit_time = Field(int64, "operation_aborted_error_crit_time")
    operation_aborted_error_ec = Field(int64, "operation_aborted_error_ec")
    operation_aborted_error_rev = Field(int64, "operation_aborted_error_rev")
    operation_stopped_error_crit_time = Field(int64, "operation_stopped_error_crit_time")
    operation_stopped_error_ec = Field(int64, "operation_stopped_error_ec")
    operation_stopped_error_rev = Field(int64, "operation_stopped_error_rev")
    recent_error_rev = Field(int64, "recent_error_rev")
    system_is_busy_error_crit_time = Field(int64, "system_is_busy_error_crit_time")
    system_is_busy_error_ec = Field(int64, "system_is_busy_error_ec")
    system_is_busy_error_rev = Field(int64, "system_is_busy_error_rev")
    time = Field(float64, "TIME")
    timestamp = Field(int64, "TIMESTAMP")


def fill_DriveSystem(event, hdu, slow_event):
    event.slow_data.drivesystem.time = hdu.data["TIME"][slow_event]
    event.slow_data.drivesystem.timestamp = hdu.data["TIMESTAMP"][slow_event]
    event.slow_data.drivesystem.capacity_exceeded_error_crit_time = hdu.data["capacity_exceeded_error_crit_time"][slow_event]
    event.slow_data.drivesystem.capacity_exceeded_error_ec = hdu.data["capacity_exceeded_error_ec"][slow_event]
    event.slow_data.drivesystem.capacity_exceeded_error_rev = hdu.data["capacity_exceeded_error_rev"][slow_event]
    event.slow_data.drivesystem.current_cache_size = hdu.data["current_cache_size"][slow_event]
    event.slow_data.drivesystem.current_max_velocity_az = hdu.data["current_max_velocity_az"][slow_event]
    event.slow_data.drivesystem.current_max_velocity_el = hdu.data["current_max_velocity_el"][slow_event]
    event.slow_data.drivesystem.current_nominal_position_az = hdu.data["current_nominal_position_az"][slow_event]
    event.slow_data.drivesystem.current_nominal_position_el = hdu.data["current_nominal_position_el"][slow_event]
    event.slow_data.drivesystem.current_position_az = hdu.data["current_position_az"][slow_event]
    event.slow_data.drivesystem.current_position_el = hdu.data["current_position_el"][slow_event]
    event.slow_data.drivesystem.current_time = hdu.data["current_time"][slow_event]
    event.slow_data.drivesystem.current_track_step_pos_az = hdu.data["current_track_step_pos_az"][slow_event]
    event.slow_data.drivesystem.current_track_step_pos_el = hdu.data["current_track_step_pos_el"][slow_event]
    event.slow_data.drivesystem.current_track_step_t = hdu.data["current_track_step_t"][slow_event]
    event.slow_data.drivesystem.current_velocity_az = hdu.data["current_velocity_az"][slow_event]
    event.slow_data.drivesystem.current_velocity_el = hdu.data["current_velocity_el"][slow_event]
    event.slow_data.drivesystem.has_cache_capacity = hdu.data["has_cache_capacity"][slow_event]
    event.slow_data.drivesystem.has_local_mode_requested = hdu.data["has_local_mode_requested"][slow_event]
    event.slow_data.drivesystem.has_remote_mode_requested = hdu.data["has_remote_mode_requested"][slow_event]
    event.slow_data.drivesystem.in__position_az = hdu.data["in__position_az"][slow_event]
    event.slow_data.drivesystem.in__position_el = hdu.data["in__position_el"][slow_event]
    event.slow_data.drivesystem.in__t_after = hdu.data["in__t_after"][slow_event]
    event.slow_data.drivesystem.in__track_step_pos_az = hdu.data["in__track_step_pos_az"][slow_event]
    event.slow_data.drivesystem.in__track_step_pos_el = hdu.data["in__track_step_pos_el"][slow_event]
    event.slow_data.drivesystem.in__track_step_t = hdu.data["in__track_step_t"][slow_event]
    event.slow_data.drivesystem.in__v_rel = hdu.data["in__v_rel"][slow_event]
    event.slow_data.drivesystem.invalid_argument_error_crit_time = hdu.data["invalid_argument_error_crit_time"][slow_event]
    event.slow_data.drivesystem.invalid_argument_error_ec = hdu.data["invalid_argument_error_ec"][slow_event]
    event.slow_data.drivesystem.invalid_argument_error_rev = hdu.data["invalid_argument_error_rev"][slow_event]
    event.slow_data.drivesystem.invalid_operation_error_crit_time = hdu.data["invalid_operation_error_crit_time"][slow_event]
    event.slow_data.drivesystem.invalid_operation_error_ec = hdu.data["invalid_operation_error_ec"][slow_event]
    event.slow_data.drivesystem.invalid_operation_error_rev = hdu.data["invalid_operation_error_rev"][slow_event]
    event.slow_data.drivesystem.is_in_park_position = hdu.data["is_in_park_position"][slow_event]
    event.slow_data.drivesystem.is_in_parking_zone = hdu.data["is_in_parking_zone"][slow_event]
    event.slow_data.drivesystem.is_in_start_position = hdu.data["is_in_start_position"][slow_event]
    event.slow_data.drivesystem.is_moving = hdu.data["is_moving"][slow_event]
    event.slow_data.drivesystem.is_off = hdu.data["is_off"][slow_event]
    event.slow_data.drivesystem.is_on_source = hdu.data["is_on_source"][slow_event]
    event.slow_data.drivesystem.is_tracking = hdu.data["is_tracking"][slow_event]
    event.slow_data.drivesystem.no_permission_error_crit_time = hdu.data["no_permission_error_crit_time"][slow_event]
    event.slow_data.drivesystem.no_permission_error_ec = hdu.data["no_permission_error_ec"][slow_event]
    event.slow_data.drivesystem.no_permission_error_rev = hdu.data["no_permission_error_rev"][slow_event]
    event.slow_data.drivesystem.operation_aborted_error_crit_time = hdu.data["operation_aborted_error_crit_time"][slow_event]
    event.slow_data.drivesystem.operation_aborted_error_ec = hdu.data["operation_aborted_error_ec"][slow_event]
    event.slow_data.drivesystem.operation_aborted_error_rev = hdu.data["operation_aborted_error_rev"][slow_event]
    event.slow_data.drivesystem.operation_stopped_error_crit_time = hdu.data["operation_stopped_error_crit_time"][slow_event]
    event.slow_data.drivesystem.operation_stopped_error_ec = hdu.data["operation_stopped_error_ec"][slow_event]
    event.slow_data.drivesystem.operation_stopped_error_rev = hdu.data["operation_stopped_error_rev"][slow_event]
    event.slow_data.drivesystem.recent_error_rev = hdu.data["recent_error_rev"][slow_event]
    event.slow_data.drivesystem.system_is_busy_error_crit_time = hdu.data["system_is_busy_error_crit_time"][slow_event]
    event.slow_data.drivesystem.system_is_busy_error_ec = hdu.data["system_is_busy_error_ec"][slow_event]
    event.slow_data.drivesystem.system_is_busy_error_rev = hdu.data["system_is_busy_error_rev"][slow_event]
    return event


class MasterSST1MContainer(Container):
    dplc_azel = Field(ndarray, "dplc_azel")
    dplc_energy = Field(int32, "dplc_energy")
    dplc_errors = Field(ndarray, "dplc_errors")
    dplc_state = Field(int32, "dplc_state")
    dplc_statuses = Field(ndarray, "dplc_statuses")
    dplc_time = Field(float64, "dplc_time")
    dplc_velocity = Field(ndarray, "dplc_velocity")
    events_timings = Field(ndarray, "events_timings")
    master_time = Field(float64, "master_time")
    splc_control = Field(int32, "splc_control")
    splc_errors = Field(ndarray, "splc_errors")
    splc_state = Field(int32, "splc_state")
    splc_statuses = Field(ndarray, "splc_statuses")
    splc_telemetry = Field(ndarray, "splc_telemetry")
    splc_time = Field(float64, "splc_time")
    target_radec = Field(ndarray, "target_radec")
    time = Field(float64, "TIME")
    timestamp = Field(int64, "TIMESTAMP")


def fill_MasterSST1M(event, hdu, slow_event):
    event.slow_data.mastersst1m.time = hdu.data["TIME"][slow_event]
    event.slow_data.mastersst1m.timestamp = hdu.data["TIMESTAMP"][slow_event]
    event.slow_data.mastersst1m.dplc_azel = hdu.data["dplc_azel"][slow_event]
    event.slow_data.mastersst1m.dplc_energy = hdu.data["dplc_energy"][slow_event]
    event.slow_data.mastersst1m.dplc_errors = hdu.data["dplc_errors"][slow_event]
    event.slow_data.mastersst1m.dplc_state = hdu.data["dplc_state"][slow_event]
    event.slow_data.mastersst1m.dplc_statuses = hdu.data["dplc_statuses"][slow_event]
    event.slow_data.mastersst1m.dplc_time = hdu.data["dplc_time"][slow_event]
    event.slow_data.mastersst1m.dplc_velocity = hdu.data["dplc_velocity"][slow_event]
    event.slow_data.mastersst1m.events_timings = hdu.data["events_timings"][slow_event]
    event.slow_data.mastersst1m.master_time = hdu.data["master_time"][slow_event]
    event.slow_data.mastersst1m.splc_control = hdu.data["splc_control"][slow_event]
    event.slow_data.mastersst1m.splc_errors = hdu.data["splc_errors"][slow_event]
    event.slow_data.mastersst1m.splc_state = hdu.data["splc_state"][slow_event]
    event.slow_data.mastersst1m.splc_statuses = hdu.data["splc_statuses"][slow_event]
    event.slow_data.mastersst1m.splc_telemetry = hdu.data["splc_telemetry"][slow_event]
    event.slow_data.mastersst1m.splc_time = hdu.data["splc_time"][slow_event]
    event.slow_data.mastersst1m.target_radec = hdu.data["target_radec"][slow_event]
    return event


class DigicamSlowControlContainer(Container):
    absolutetime = Field(int64, "AbsoluteTime")
    appstatus = Field(ndarray, "appStatus")
    crate1_status = Field(ndarray, "Crate1_status")
    crate1_t = Field(ndarray, "Crate1_T")
    crate1_timestamps = Field(ndarray, "Crate1_timestamps")
    crate2_status = Field(ndarray, "Crate2_status")
    crate2_t = Field(ndarray, "Crate2_T")
    crate2_timestamps = Field(ndarray, "Crate2_timestamps")
    crate3_status = Field(ndarray, "Crate3_status")
    crate3_t = Field(ndarray, "Crate3_T")
    crate3_timestamps = Field(ndarray, "Crate3_timestamps")
    crates = Field(ndarray, "Crates")
    cstparameters = Field(ndarray, "cstParameters")
    cstswitches = Field(ndarray, "cstSwitches")
    fadcoffset = Field(int32, "FadcOffset")
    fadcresync = Field(int32, "FadcResync")
    localtime = Field(int64, "LocalTime")
    opcuatime = Field(int64, "opcuaTime")
    time = Field(float64, "TIME")
    timestamp = Field(int64, "TIMESTAMP")
    trigger_status = Field(int32, "trigger_status")
    trigger_timestamp = Field(int64, "trigger_timestamp")
    triggerparameters = Field(ndarray, "triggerParameters")
    triggerstatus = Field(ndarray, "triggerStatus")
    triggerswitches = Field(ndarray, "triggerSwitches")


def fill_DigicamSlowControl(event, hdu, slow_event):
    event.slow_data.digicamslowcontrol.absolutetime = hdu.data["AbsoluteTime"][slow_event]
    event.slow_data.digicamslowcontrol.crate1_t = hdu.data["Crate1_T"][slow_event]
    event.slow_data.digicamslowcontrol.crate1_status = hdu.data["Crate1_status"][slow_event]
    event.slow_data.digicamslowcontrol.crate1_timestamps = hdu.data["Crate1_timestamps"][slow_event]
    event.slow_data.digicamslowcontrol.crate2_t = hdu.data["Crate2_T"][slow_event]
    event.slow_data.digicamslowcontrol.crate2_status = hdu.data["Crate2_status"][slow_event]
    event.slow_data.digicamslowcontrol.crate2_timestamps = hdu.data["Crate2_timestamps"][slow_event]
    event.slow_data.digicamslowcontrol.crate3_t = hdu.data["Crate3_T"][slow_event]
    event.slow_data.digicamslowcontrol.crate3_status = hdu.data["Crate3_status"][slow_event]
    event.slow_data.digicamslowcontrol.crate3_timestamps = hdu.data["Crate3_timestamps"][slow_event]
    event.slow_data.digicamslowcontrol.crates = hdu.data["Crates"][slow_event]
    event.slow_data.digicamslowcontrol.fadcoffset = hdu.data["FadcOffset"][slow_event]
    event.slow_data.digicamslowcontrol.fadcresync = hdu.data["FadcResync"][slow_event]
    event.slow_data.digicamslowcontrol.localtime = hdu.data["LocalTime"][slow_event]
    event.slow_data.digicamslowcontrol.time = hdu.data["TIME"][slow_event]
    event.slow_data.digicamslowcontrol.timestamp = hdu.data["TIMESTAMP"][slow_event]
    event.slow_data.digicamslowcontrol.appstatus = hdu.data["appStatus"][slow_event]
    event.slow_data.digicamslowcontrol.cstparameters = hdu.data["cstParameters"][slow_event]
    event.slow_data.digicamslowcontrol.cstswitches = hdu.data["cstSwitches"][slow_event]
    event.slow_data.digicamslowcontrol.opcuatime = hdu.data["opcuaTime"][slow_event]
    event.slow_data.digicamslowcontrol.triggerparameters = hdu.data["triggerParameters"][slow_event]
    event.slow_data.digicamslowcontrol.triggerstatus = hdu.data["triggerStatus"][slow_event]
    event.slow_data.digicamslowcontrol.triggerswitches = hdu.data["triggerSwitches"][slow_event]
    event.slow_data.digicamslowcontrol.trigger_status = hdu.data["trigger_status"][slow_event]
    event.slow_data.digicamslowcontrol.trigger_timestamp = hdu.data["trigger_timestamp"][slow_event]
    return event


class SafetyPLCContainer(Container):
    lc = Field(int32, "lc")
    splc_cab_other = Field(ndarray, "SPLC_CAB_Other")
    splc_cab_temperature = Field(ndarray, "SPLC_CAB_Temperature")
    splc_cam_airpressure = Field(ndarray, "SPLC_CAM_AirPressure")
    splc_cam_chiller_analogvalue = Field(ndarray, "SPLC_CAM_Chiller_AnalogValue")
    splc_cam_chiller_digitalvalue = Field(ndarray, "SPLC_CAM_Chiller_DigitalValue")
    splc_cam_chiller_manualregister = Field(int32, "SPLC_CAM_Chiller_manualRegister")
    splc_cam_chiller_register = Field(int32, "SPLC_CAM_Chiller_Register")
    splc_cam_errorlist1 = Field(int32, "SPLC_CAM_ErrorList1")
    splc_cam_errorlist2 = Field(int32, "SPLC_CAM_ErrorList2")
    splc_cam_hkb_commandstatus = Field(int32, "SPLC_CAM_HKB_CommandStatus")
    splc_cam_hkb_outparam = Field(ndarray, "SPLC_CAM_HKB_OutParam")
    splc_cam_humidity = Field(ndarray, "SPLC_CAM_Humidity")
    splc_cam_proc = Field(int32, "SPLC_CAM_Proc")
    splc_cam_procstep = Field(int32, "SPLC_CAM_ProcStep")
    splc_cam_status = Field(int32, "SPLC_CAM_Status")
    splc_cam_temperature = Field(ndarray, "SPLC_CAM_Temperature")
    splc_drv_errorlist = Field(int32, "SPLC_DRV_ErrorList")
    splc_drv_proc = Field(int32, "SPLC_DRV_Proc")
    splc_drv_procstep = Field(int32, "SPLC_DRV_ProcStep")
    splc_drv_status = Field(int32, "SPLC_DRV_Status")
    splc_drv_switch_status = Field(int32, "SPLC_DRV_Switch_Status")
    splc_opt_proc = Field(int32, "SPLC_OPT_Proc")
    splc_opt_procstep = Field(int32, "SPLC_OPT_ProcStep")
    splc_opt_status = Field(int32, "SPLC_OPT_Status")
    splc_oth_errorlist = Field(int32, "SPLC_OTH_ErrorList")
    splc_oth_time = Field(int64, "SPLC_OTH_Time")
    splc_oth_version = Field(float64, "SPLC_OTH_Version")
    splc_sta_status = Field(int32, "SPLC_STA_Status")
    splc_sta_telctrl = Field(int32, "SPLC_STA_TelCtrl")
    splc_sta_telstate = Field(int32, "SPLC_STA_TelState")
    tbf = Field(int64, "tbf")
    time = Field(float64, "TIME")
    timestamp = Field(int64, "TIMESTAMP")


def fill_SafetyPLC(event, hdu, slow_event):
    event.slow_data.safetyplc.splc_cab_other = hdu.data["SPLC_CAB_Other"][slow_event]
    event.slow_data.safetyplc.splc_cab_temperature = hdu.data["SPLC_CAB_Temperature"][slow_event]
    event.slow_data.safetyplc.splc_cam_airpressure = hdu.data["SPLC_CAM_AirPressure"][slow_event]
    event.slow_data.safetyplc.splc_cam_chiller_analogvalue = hdu.data["SPLC_CAM_Chiller_AnalogValue"][slow_event]
    event.slow_data.safetyplc.splc_cam_chiller_digitalvalue = hdu.data["SPLC_CAM_Chiller_DigitalValue"][slow_event]
    event.slow_data.safetyplc.splc_cam_chiller_register = hdu.data["SPLC_CAM_Chiller_Register"][slow_event]
    event.slow_data.safetyplc.splc_cam_chiller_manualregister = hdu.data["SPLC_CAM_Chiller_manualRegister"][slow_event]
    event.slow_data.safetyplc.splc_cam_errorlist1 = hdu.data["SPLC_CAM_ErrorList1"][slow_event]
    event.slow_data.safetyplc.splc_cam_errorlist2 = hdu.data["SPLC_CAM_ErrorList2"][slow_event]
    event.slow_data.safetyplc.splc_cam_hkb_commandstatus = hdu.data["SPLC_CAM_HKB_CommandStatus"][slow_event]
    event.slow_data.safetyplc.splc_cam_hkb_outparam = hdu.data["SPLC_CAM_HKB_OutParam"][slow_event]
    event.slow_data.safetyplc.splc_cam_humidity = hdu.data["SPLC_CAM_Humidity"][slow_event]
    event.slow_data.safetyplc.splc_cam_proc = hdu.data["SPLC_CAM_Proc"][slow_event]
    event.slow_data.safetyplc.splc_cam_procstep = hdu.data["SPLC_CAM_ProcStep"][slow_event]
    event.slow_data.safetyplc.splc_cam_status = hdu.data["SPLC_CAM_Status"][slow_event]
    event.slow_data.safetyplc.splc_cam_temperature = hdu.data["SPLC_CAM_Temperature"][slow_event]
    event.slow_data.safetyplc.splc_drv_errorlist = hdu.data["SPLC_DRV_ErrorList"][slow_event]
    event.slow_data.safetyplc.splc_drv_proc = hdu.data["SPLC_DRV_Proc"][slow_event]
    event.slow_data.safetyplc.splc_drv_procstep = hdu.data["SPLC_DRV_ProcStep"][slow_event]
    event.slow_data.safetyplc.splc_drv_status = hdu.data["SPLC_DRV_Status"][slow_event]
    event.slow_data.safetyplc.splc_drv_switch_status = hdu.data["SPLC_DRV_Switch_Status"][slow_event]
    event.slow_data.safetyplc.splc_opt_proc = hdu.data["SPLC_OPT_Proc"][slow_event]
    event.slow_data.safetyplc.splc_opt_procstep = hdu.data["SPLC_OPT_ProcStep"][slow_event]
    event.slow_data.safetyplc.splc_opt_status = hdu.data["SPLC_OPT_Status"][slow_event]
    event.slow_data.safetyplc.splc_oth_errorlist = hdu.data["SPLC_OTH_ErrorList"][slow_event]
    event.slow_data.safetyplc.splc_oth_time = hdu.data["SPLC_OTH_Time"][slow_event]
    event.slow_data.safetyplc.splc_oth_version = hdu.data["SPLC_OTH_Version"][slow_event]
    event.slow_data.safetyplc.splc_sta_status = hdu.data["SPLC_STA_Status"][slow_event]
    event.slow_data.safetyplc.splc_sta_telctrl = hdu.data["SPLC_STA_TelCtrl"][slow_event]
    event.slow_data.safetyplc.splc_sta_telstate = hdu.data["SPLC_STA_TelState"][slow_event]
    event.slow_data.safetyplc.time = hdu.data["TIME"][slow_event]
    event.slow_data.safetyplc.timestamp = hdu.data["TIMESTAMP"][slow_event]
    event.slow_data.safetyplc.lc = hdu.data["lc"][slow_event]
    event.slow_data.safetyplc.tbf = hdu.data["tbf"][slow_event]
    return event


class PDPSlowControlContainer(Container):
    opcuatime = Field(int64, "opcuaTime")
    pdpstatus = Field(int64, "PDPStatus")
    sector1_adc = Field(ndarray, "Sector1_ADC")
    sector1_clsaturation = Field(ndarray, "Sector1_CLsaturation")
    sector1_ghv = Field(ndarray, "Sector1_GHV")
    sector1_hv = Field(ndarray, "Sector1_HV")
    sector1_t = Field(ndarray, "Sector1_T")
    sector1_tsaturation = Field(ndarray, "Sector1_Tsaturation")
    sector2_adc = Field(ndarray, "Sector2_ADC")
    sector2_clsaturation = Field(ndarray, "Sector2_CLsaturation")
    sector2_ghv = Field(ndarray, "Sector2_GHV")
    sector2_hv = Field(ndarray, "Sector2_HV")
    sector2_t = Field(ndarray, "Sector2_T")
    sector2_tsaturation = Field(ndarray, "Sector2_Tsaturation")
    sector3_adc = Field(ndarray, "Sector3_ADC")
    sector3_clsaturation = Field(ndarray, "Sector3_CLsaturation")
    sector3_ghv = Field(ndarray, "Sector3_GHV")
    sector3_hv = Field(ndarray, "Sector3_HV")
    sector3_t = Field(ndarray, "Sector3_T")
    sector3_tsaturation = Field(ndarray, "Sector3_Tsaturation")
    sectors = Field(ndarray, "Sectors")
    time = Field(float64, "TIME")
    timestamp = Field(int64, "TIMESTAMP")


def fill_PDPSlowControl(event, hdu, slow_event):
    event.slow_data.pdpslowcontrol.pdpstatus = hdu.data["PDPStatus"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_adc = hdu.data["Sector1_ADC"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_clsaturation = hdu.data["Sector1_CLsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_ghv = hdu.data["Sector1_GHV"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_hv = hdu.data["Sector1_HV"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_t = hdu.data["Sector1_T"][slow_event]
    event.slow_data.pdpslowcontrol.sector1_tsaturation = hdu.data["Sector1_Tsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_adc = hdu.data["Sector2_ADC"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_clsaturation = hdu.data["Sector2_CLsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_ghv = hdu.data["Sector2_GHV"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_hv = hdu.data["Sector2_HV"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_t = hdu.data["Sector2_T"][slow_event]
    event.slow_data.pdpslowcontrol.sector2_tsaturation = hdu.data["Sector2_Tsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_adc = hdu.data["Sector3_ADC"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_clsaturation = hdu.data["Sector3_CLsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_ghv = hdu.data["Sector3_GHV"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_hv = hdu.data["Sector3_HV"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_t = hdu.data["Sector3_T"][slow_event]
    event.slow_data.pdpslowcontrol.sector3_tsaturation = hdu.data["Sector3_Tsaturation"][slow_event]
    event.slow_data.pdpslowcontrol.sectors = hdu.data["Sectors"][slow_event]
    event.slow_data.pdpslowcontrol.time = hdu.data["TIME"][slow_event]
    event.slow_data.pdpslowcontrol.timestamp = hdu.data["TIMESTAMP"][slow_event]
    event.slow_data.pdpslowcontrol.opcuatime = hdu.data["opcuaTime"][slow_event]
    return event


class SlowDataContainer(Container):
    drivesystem = Field(DriveSystemContainer(), "DriveSystem")
    mastersst1m = Field(MasterSST1MContainer(), "MasterSST1M")
    digicamslowcontrol = Field(DigicamSlowControlContainer(), "DigicamSlowControl")
    safetyplc = Field(SafetyPLCContainer(), "SafetyPLC")
    pdpslowcontrol = Field(PDPSlowControlContainer(), "PDPSlowControl")


def fill_slow(class_name, event, hdu, slow_event):
    if class_name == "DriveSystem":
        event = fill_DriveSystem(event, hdu, slow_event)
    elif class_name == "MasterSST1M":
        event = fill_MasterSST1M(event, hdu, slow_event)
    elif class_name == "DigicamSlowControl":
        event = fill_DigicamSlowControl(event, hdu, slow_event)
    elif class_name == "SafetyPLC":
        event = fill_SafetyPLC(event, hdu, slow_event)
    elif class_name == "PDPSlowControl":
        event = fill_PDPSlowControl(event, hdu, slow_event)
    else:
        print("ERROR in fill_slow(): class %s not known." %class_name)
        print("Try to regenerate slow data containers ?")
    return event


