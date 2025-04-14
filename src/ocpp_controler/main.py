import asyncio
import websockets
from ocpp_controler.charge_point import ChargePoint




async def on_connect(websocket, path):
    """Method called by charge point at connection"""

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']  # type: ignore
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())