from django.db import models
from django.utils.translation import gettext_lazy as _
from terminusgps.wialon import flags


class WialonCommandName(models.TextChoices):
    SUB_BASIC = "Basic", _("Basic Subscription")
    SUB_STANDARD = "Standard", _("Standard Subscription")
    SUB_PREMIUM = "Premium", _("Premium Subscription")
    STARTER_DISABLED = "Starter Disable On", _("Disable Starter")
    STARTER_ENABLED = "Starter Disable Off", _("Enable Starter")
    ENABLE = "On", _("Enable")
    DISABLE = "Off", _("Disable")


class WialonCommandType(models.TextChoices):
    ENGINE_BLOCK = "block_engine", _("Block Engine")
    ENGINE_UNBLOCK = "unblock_engine", _("Unblock Engine")
    CUSTOM_MSG = "custom_msg", _("Custom Message")
    DRIVER_MSG = "driver_msg", _("Message to Driver")
    DOWNLOAD_MSG = "download_msgs", _("Download messages")
    QUERY_POS = "query_pos", _("Query Position")
    QUERY_PHOTO = "query_photo", _("Query Snapshot")
    OUTPUT_ON = "output_on", _("Activate Output")
    OUTPUT_OFF = "output_off", _("Deactive Output")
    SEND_POS = "send_position", _("Send Coordinates")
    SET_REPORT_INT = "set_report_interval", _("Set Data Transfer Interval")
    UPLOAD_CFG = "upload_cfg", _("Upload Configuration")
    UPLOAD_SW = "upload_sw", _("Upload Firmware")


class WialonCommandLink(models.TextChoices):
    AUTO = "", _("Auto")
    TCP = "tcp", _("TCP")
    UDP = "udp", _("UDP")
    VRT = "vrt", _("Virtual")
    GSM = "gsm", _("SMS")


ACCESSMASK_UNIT_BASIC: int = sum(
    [
        flags.ACCESSFLAG_VIEW_ITEM_BASIC,
        flags.ACCESSFLAG_VIEW_ITEM_DETAILED,
        flags.ACCESSFLAG_RENAME_ITEM,
        flags.ACCESSFLAG_VIEW_CUSTOM_FIELDS,
        flags.ACCESSFLAG_MANAGE_CUSTOM_FIELDS,
        flags.ACCESSFLAG_MANAGE_ICON,
        flags.ACCESSFLAG_QUERY_REPORTS,
        flags.ACCESSFLAG_VIEW_ATTACHED_FILES,
        flags.ACCESSFLAG_UNIT_EXECUTE_COMMANDS,
        flags.ACCESSFLAG_UNIT_VIEW_SERVICE_INTERVALS,
        flags.ACCESSFLAG_UNIT_REGISTER_EVENTS,
        flags.ACCESSFLAG_UNIT_IMPORT_MESSAGES,
        flags.ACCESSFLAG_UNIT_EXPORT_MESSAGES,
    ]
)

ACCESSMASK_UNIT_SUPER: int = sum(
    [
        flags.ACCESSFLAG_VIEW_ITEM_BASIC,
        flags.ACCESSFLAG_VIEW_ITEM_DETAILED,
        flags.ACCESSFLAG_RENAME_ITEM,
        flags.ACCESSFLAG_VIEW_CUSTOM_FIELDS,
        flags.ACCESSFLAG_MANAGE_CUSTOM_FIELDS,
        flags.ACCESSFLAG_MANAGE_ICON,
        flags.ACCESSFLAG_QUERY_REPORTS,
        flags.ACCESSFLAG_VIEW_ATTACHED_FILES,
        flags.ACCESSFLAG_UNIT_EXECUTE_COMMANDS,
        flags.ACCESSFLAG_UNIT_VIEW_SERVICE_INTERVALS,
        flags.ACCESSFLAG_UNIT_REGISTER_EVENTS,
        flags.ACCESSFLAG_UNIT_IMPORT_MESSAGES,
        flags.ACCESSFLAG_UNIT_EXPORT_MESSAGES,
    ]
)

ACCESSMASK_UNIT_FULL: int = sum([flags.ACCESSFLAG_FULL_ACCESS])
