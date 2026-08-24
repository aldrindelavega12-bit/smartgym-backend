from sync.member_handler import (
    handle_member_created,
    handle_member_deleted
)

from sync.payment_handler import (
    handle_payment_updated
)

from sync.walkin_handler import (
    handle_walkin_created,
    handle_walkin_deleted,
    handle_walkin_payment_updated,
    handle_walkin_locker_assigned
)

from sync.locker_handler import (
    handle_locker_overtime_paid
)

from sync.activation_handler import (
    handle_activation_created
)

from sync.face_handler import (
    handle_face_sync
)

from sync.fp_handler import (
    handle_fp_sync
)


HANDLERS = {

    "MEMBER_CREATED": handle_member_created,

    "MEMBER_DELETED": handle_member_deleted,

    "PAYMENT_UPDATED": handle_payment_updated,

    "WALKIN_CREATED": handle_walkin_created,

    "WALKIN_PAYMENT_UPDATED": handle_walkin_payment_updated,

    "WALKIN_LOCKER_ASSIGNED": handle_walkin_locker_assigned,

    "WALKIN_DELETED": handle_walkin_deleted,

    "LOCKER_OVERTIME_PAID": handle_locker_overtime_paid,

    "FP_SYNC": handle_fp_sync,

    "ACTIVATION_CREATED": handle_activation_created
}


def handle_event(event, fp_manager=None):

    event_type = event.get("event_type")
    payload = event.get("payload", {})

    # ==========================================
    # FILE EVENT
    # ==========================================

    if event_type == "FACE_SYNC":

        return handle_face_sync(event)

    # ==========================================
    # GET HANDLER
    # ==========================================

    handler = HANDLERS.get(event_type)

    if handler is None:

        return {
            "success": False,
            "message": f"Unknown event: {event_type}"
        }

    # ==========================================
    # EVENTS THAT NEED FINGERPRINT MANAGER
    # ==========================================

    if event_type in (
        "FP_SYNC",
        "MEMBER_DELETED"
    ):

        return handler(
            payload,
            fp_manager
        )

    # ==========================================
    # NORMAL EVENTS
    # ==========================================

    return handler(payload)