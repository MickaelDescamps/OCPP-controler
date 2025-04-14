import time
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import enums as ocpp_enums
from ocpp.v16 import call_result

from ocpp_controler.logger import get_logger


class ChargePoint(cp):

    def __init__(self, id, websocket):
        super().__init__(id, websocket)

        self.class_logger = get_logger("ocpp_controler", "INFO")
        self.logger = self.class_logger.getChild(self.id)

    @on(Action.boot_notification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        """Method called when charge point connects to central system"""

        self.logger.info(f"Charge point {self.id} connected")
        self.logger.debug(f"Charge point {self.id} (manufacturer - {charge_point_vendor} model - {charge_point_model}) boot notification: {kwargs}")

        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.heartbeat)
    async def on_heartbeat(self):
        self.logger.info(f"Heartbeat from charge point {self.id}")
        return call_result.Heartbeat(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.authorize)
    async def on_authorize(self, id_tag):
        self.logger.info(f"Authorize request from charge point {self.id} with id_tag {id_tag}")

        authorization_result = True

        if authorization_result:
            self.logger.info(f"Authorize request from charge point {self.id} with id_tag {id_tag} accepted")
            result_status = ocpp_enums.AuthorizationStatus.accepted
        else:
            self.logger.info(f"Authorize request from charge point {self.id} with id_tag {id_tag} rejected")
            result_status = ocpp_enums.AuthorizationStatus.blocked

        return call_result.AuthorizePayload(
            id_tag_info={
                'status': result_status
            }
        )

    @on(Action.start_transaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp):
        self.logger.info(f"Start transaction request from charge point {self.id} with id_tag {id_tag}")
        return call_result.StartTransactionPayload(
            transaction_id=int(time.time() * 1000),
            id_tag_info={
                'status': ocpp_enums.AuthorizationStatus.accepted
            }
        )

    @on(Action.stop_transaction)
    async def on_stop_transaction(self, id_tag, timestamp, transaction_id):
        self.logger.info(f"Stop transaction request from charge point {self.id} with id_tag {id_tag}")
        return call_result.StopTransactionPayload(
            id_tag_info={
                'status': ocpp_enums.AuthorizationStatus.accepted
            }
        )

