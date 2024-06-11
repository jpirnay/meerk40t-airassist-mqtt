import time
import paho.mqtt.client as mqtt

# Establish the core class
class AirAssist():

    def __init__(
        self,
        context,
        server=None, port=None,
        subject_on=None, payload_on=None,
        subject_off=None, payload_off=None,
        subject_subscribe=None,
        user=None, pwd=None,
    ):
        if port is None:
            port = 1883
        if payload_on is None:
            payload_on = "ON"
        if payload_off is None:
            payload_off = "OFF"
        self.context = context
        self.channel = None
        if self.context:
            self.channel = self.context.kernel.channel("console")
        self.server = server # "192.168.0.38"
        self.port = port # 1883  # Standard
        self.mqtt_user = user
        self.mqtt_pwd = pwd
        self.state = mqtt.Disconnected
        self.m_keep_alive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = mqtt.MQTT_3_1
        self.subject_publish_on = subject_on  # "cmnd/gosund4/POWER1"
        self.subject_publish_off = subject_off # "cmnd/gosund4/POWER1"
        self.subject_subscribe = subject_subscribe # "stat/gosund4/POWER1"
        self.msg_on = payload_on
        self.msg_off = payload_off
        print("MQTT-Connect")
        self.client = mqtt.Client("meerk40t", clean_session=self.m_cleanSession, protocol=self.m_protocolVersion)
        # Establish callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        if self.mqtt_user is not None:
            self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
        self.connect_to_host()
        if self.subject_subscribe is not None:
            self.subscribe(self.subject_subscribe)

    #################################################################
    # Logging
    def log_info(self, msg):
        if self.channel is None:
            print (msg)
        else:
            self.channel(msg)

    #################################################################
    # Connection Management
    def connect_to_host(self):
        if self.server:
            try:
                self.client.connect(self.server, port=self.port, keepalive=self.m_keep_alive)
                self.state = mqtt.Connecting
                self.client.loop_start()
            except Exception as e:
                # Not working, provide feedback
                self.log_info(f"Wasn't able to connect to {self.server}:{self.port}: {e}")

    def disconnect_from_host(self):
        self.client.loop_stop()
        self.client.disconnect()

    #################################################################
    # Data exchange
    def subscribe(self, path):
        if self.state == mqtt.Connected:
            self.client.subscribe(path)
            self.log_info(f"MQTT: Subscribed to {', '.join([p[0] for p in path])}")

    def publish(self, topic, payload=None, qos=0, retain=False):
        if self.state == mqtt.Connected:
            self.client.publish(topic, payload, qos, retain)

    #################################################################
    # Callbacks
    def on_subscribe(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def on_message(self, mqttc, obj, msg):
        topic = msg.topic
        try:
            mstr = msg.payload.decode("utf8")
            retained = msg.retain
            self.messageSignal.emit(topic, mstr, retained)
        except UnicodeDecodeError as e:
            self.log_info(f"MQTT MESSAGE DECODE ERROR: {e} ({msg.topic}={msg.payload.__repr__()})")

    def on_connect(self, *args):
        rc = args[3]
        if rc == 0:
            self.state = mqtt.Connected

        else:
            self.state = mqtt.Disconnected


    def on_disconnect(self, *args):
        self.state = mqtt.Disconnected

    def cmd_on(self):
        print("MQTT-turnon")
        self.publish(self.subject_publish_on, self.msg_on)

    def cmd_off(self):
        print("MQTT-turnoff")
        self.publish(self.subject_publish_on, self.msg_off)

    def __del__(self):
        if self.state == mqtt.Connected:
            self.disconnect_from_host()

