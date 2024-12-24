from __future__ import annotations
from kc3zvd.iot_state.subscribers import redis
import paho.mqtt.client as mqtt
import asyncio
import json
import click
import logging
logger = logging.getLogger(__name__)
# prefix/device_type/area_name/device_name/state_class

async def handle_state_messages(channel: redis.client.PubSub):

    ctx = click.get_current_context()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(host=ctx.obj['mqtt']['host'], port=ctx.obj['mqtt']['port'])
    mqttc.loop_start()
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            logger.info("Handling state message")
            logger.debug(message)

            payload = json.loads(message['data'].decode('utf-8'))

            try:
                device = payload['data']['device']
                state = payload['data']['state']
            except KeyError:
                logger.infq:("Missing key in message")
                continue


            topic = f"{ctx.obj['mqtt']['topic_prefix']}{device['device_type']}/{device['area_name']}/{device['friendly_name']}/{state['state_class']}"
            
            message = {
                "device": device,
                "state": state
            }

            message = json.dumps(device)
            logger.info("Sending message to mqtt")
            logger.debug(f"Topic: {topic}")
            logger.debug(f"Message: {message}")
            mqttc.publish(topic=topic, payload=json.dumps(message)).wait_for_publish()
    mqttc.disconnect()
    mqttc.loop_stop()

async def handle_notification_messages(channel: redis.client.PubSub):
    pass

async def subscribe():
    ctx = click.get_current_context()
    redis_url = ctx.obj['redis_url']
    logger.debug('Creating event queue subscribers...')
    update = asyncio.create_task(redis.subscribe('device:state:update', handle_state_messages, redis_url))
    create = asyncio.create_task(redis.subscribe('device:state:create', handle_state_messages, redis_url))
    p_all = asyncio.create_task(redis.subscribe('notification:all', handle_notification_messages, redis_url))
    p_mqtt = asyncio.create_task(redis.subscribe('notification:mqtt', handle_notification_messages, redis_url))
    await update
    await create
    await p_all
    await p_mqtt

def run():
    """Begins monitoring of queue to publish events to mqtt

    Note: Events Monitored
        - `device:state:update`
        - `device:state:create`
        - `notification:all`
        - `notification:mqtt`
    
    """
    logger.info("Starting iot-state service(s)...")
    asyncio.run(subscribe())

