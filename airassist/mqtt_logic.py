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
        self.server = server # "192.168.0.38"
        self.port = port # 1883  # Standard
        self.mqtt_user = user
        self.mqtt_pwd = pwd
        self.subject_publish_on = subject_on  # "cmnd/gosund4/POWER1"
        self.subject_publish_off = subject_off # "cmnd/gosund4/POWER1"
        self.subject_subscribe = subject_subscribe # "stat/gosund4/POWER1"
        self.msg_on = payload_on
        self.msg_off = payload_off
        print("MQTT-Connect")
        self.client = mqtt.Client("meerk40t")
        if self.mqtt_user is not None:
            self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
        self.client.connect(self.server, self.port)
        if self.subject_subscribe is not None:
            self.client.subscribe(self.subject_subscribe)
            self.client.on_message = self.on_subscribe
        self.client.loop_start()

    def on_subscribe(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def cmd_on(self):
        print("MQTT-turnon")
        if not self.client is None:
            print(f"Will publish {self.subject_publish_on}; {self.msg_on}")
            for i in range(5):
                result = self.client.publish(self.subject_publish_on, self.msg_on)
                if result[0] == 0:
                    continue
                else:
                    print("Failed, another attempt %d" % i)
                    self.client.loop()
                    time.sleep(0.1)

    def cmd_off(self):
        print("MQTT-turnoff")
        if not self.client is None:
            print(f"Will publish {self.subject_publish_off}; {self.msg_off}")
            for i in range(5):
                result = self.client.publish(self.subject_publish_off, self.msg_off)
                if result[0] == 0:
                    continue
                else:
                    print("Failed, another attempt %d" % i)
                    self.client.loop()
                    time.sleep(0.1)

    def __del__(self):
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

