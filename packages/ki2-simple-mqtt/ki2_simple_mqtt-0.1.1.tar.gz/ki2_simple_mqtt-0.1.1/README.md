# SimpleMqtt

SimpleMqtt is a Python library designed to simplify MQTT client operations. It extends the Paho MQTT client to provide enhanced functionality while maintaining a clean and flexible interface. Whether you're building synchronous or asynchronous applications, SimpleMqtt has you covered.

## Features

- **Enhanced Callback Management:** Manage multiple callbacks for each event type (`on_connect`, `on_disconnect`, `on_message`) seamlessly.
- **Topic-Specific Callbacks:** Easily associate callbacks with specific topics or topic patterns, simplifying message handling.
- **Deferred Subscriptions:** Automatically handles subscriptions made before a connection is established, applying them as soon as the connection is active.
- **Dual-Mode Clients:** Provides both synchronous (`SimpleMqttSync`) and asynchronous (`SimpleMqttAsync`) clients.
- **Callback Flexibility:** Supports both synchronous and asynchronous callbacks, regardless of the client type.
- **JSON Integration:** Publish and receive JSON messages effortlessly with built-in serialization and deserialization support.

## Why SimpleMqtt?

While Paho MQTT is a robust library for working with MQTT, SimpleMqtt enhances its capabilities by:

1. Allowing multiple callbacks to be registered for each event (`on_connect`, `on_disconnect`, `on_message`).
2. Providing a straightforward mechanism to bind callbacks to specific topics or patterns (e.g., `home/+/temperature`).
3. Simplifying the callback interface by encapsulating event data in a single parameter.
4. Handling subscriptions even if they are made before a connection is established.
5. Offering synchronous and asynchronous client implementations with uniform features.
6. Adding native support for JSON serialization and deserialization.

## Installation

Install the library via pip:

```bash
pip install ki2-simple-mqtt
```

## Getting Started

Here are quick examples to get you started:

### Synchronous Example

```python
from SimpleMqtt import SimpleMqttSync, OnConnectEvent, OnDisconnectEvent, OnMessageEvent

def on_connect(event: OnConnectEvent):
    print(f"Connected (rc={event.reason_code})")

def on_disconnect(event: OnDisconnectEvent):
    print(f"Disconnected (rc={event.reason_code})")

def on_message(event: OnMessageEvent):
    print(f"Message received on {event.topic}: {event.payload}")

mqtt = SimpleMqttSync()

mqtt.on_connect(on_connect)
mqtt.on_disconnect(on_disconnect)
mqtt.on_message(on_message)

mqtt.subscribe("test/topic")  # Deferred if not connected
mqtt.connect("localhost")

mqtt.loop_forever()
```

### Asynchronous Example

```python
import asyncio
from SimpleMqtt import SimpleMqttAsync, OnMessageEvent

async def on_message(event: OnMessageEvent):
    print(f"Message received on {event.topic}: {event.payload}")

async def main():
    mqtt = SimpleMqttAsync()

    mqtt.on_message(on_message)

    await mqtt.subscribe("test/topic")  # Deferred if not connected
    await mqtt.connect("localhost")

    try:
        await mqtt.loop()
    except KeyboardInterrupt:
        print("Disconnecting...")
        await mqtt.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Features

### Multiple Callbacks per Event

SimpleMqtt allows you to register multiple callbacks for the same event. For example, you can have separate callbacks to log connection events and update a user interface:

```python
def log_connection(event):
    print(f"Logging: Connected with code {event.reason_code}")

def notify_user(event):
    print("User notified of connection")

mqtt.on_connect(log_connection)
mqtt.on_connect(notify_user)
```

### Topic-Specific Callbacks

Bind callbacks directly to topics or patterns for targeted message handling:

```python
def custom_handler(event):
    print(f"Custom handler for {event.topic}: {event.payload}")

mqtt.on_topic_message("home/+/temperature", custom_handler)
```

### Deferred Subscriptions

SimpleMqtt simplifies handling subscriptions by allowing them to be registered before the client is connected. These subscriptions are automatically applied once the connection is established:

```python
mqtt.subscribe("test/topic")  # Can be called before connecting
mqtt.connect("localhost")
```

### Synchronous and Asynchronous Callback Support

Both clients (`SimpleMqttSync` and `SimpleMqttAsync`) support synchronous and asynchronous callbacks, making it easy to integrate into a variety of application architectures.

```python
async def async_handler(event):
    await some_async_operation()
    print(f"Async handled message on {event.topic}")

mqtt.on_message(async_handler)
```

### JSON Integration

SimpleMqtt simplifies working with JSON by supporting direct serialization and deserialization. For instance:

#### Publishing JSON

```python
mqtt.publish("sensor/data", {"temperature": 22.5, "humidity": 60})
```

#### Receiving JSON

```python
def handle_json_message(event: OnMessageEvent):
    data = event.as_json  # Automatically deserializes payload into a Python dictionary
    print(f"Received JSON data: {data}")

mqtt.on_message(handle_json_message)
```

## Advanced Usage

### Managing QoS and Retained Messages

Fine-tune QoS and retained message settings for better control over message delivery:

```python
mqtt.subscribe("test/topic", qos=1)
mqtt.publish("test/topic", "Hello, MQTT!", retain=True)
```

## Limitations

While SimpleMqtt provides many enhancements over the base Paho MQTT library, there are some limitations to be aware of:

1. **Feature Scope:** SimpleMqtt prioritizes simplicity and usability, so some advanced or less commonly used Paho MQTT features might not be directly exposed.
2. **Connection-Dependent Subscriptions:** Deferred subscriptions only apply to topics registered using `subscribe` methods. Direct use of the underlying Paho client bypasses this mechanism.
3. **Incompatibility with Existing Paho Callbacks:** SimpleMqtt uses a simplified callback signature with a single parameter encapsulating all event data. This means that existing callbacks designed specifically for Paho's native interface cannot be reused directly with SimpleMqtt.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
