import urequests as requests
import ujson as json
from umqtt.robust import MQTTClient
import time

class OM2MClient:
    """
    A client for interacting with an OM2M CSE using HTTP or MQTT 
    with basic error handling and response validation.
    """

    def __init__(self, cse_ip, device_name, container_name, cse_port=8282, 
                 cse_type="mn", cred="admin:admin", protocol='HTTP'):
        """
        Initialize the OM2MClient.

        :param cse_ip: IP address of the OM2M CSE (e.g., "10.83.2.249")
        :param device_name: Name of the device/Application Entity (AE)
        :param container_name: Name of the container
        :param cse_port: Port for the CSE (default: 8282)
        :param cse_type: Type of CSE ("mn" or "in")
        :param cred: Authorization credentials
        :param protocol: Protocol to use ("HTTP" or "MQTT")
        """
        self.cse_ip = cse_ip
        self.cse_port = cse_port
        self.device_name = device_name
        self.container_name = container_name
        self.cred = cred
        self.protocol = protocol.upper()
        self.cse = f"{cse_type}-cse"
        self.cse_url = f"http://{self.cse_ip}:{self.cse_port}/~/{self.cse}"

        # Protocol-specific setup
        if self.protocol == 'MQTT':
            try:
                self.mqtt_client = MQTTClient(
                    client_id=device_name,
                    server=cse_ip,
                    user=cred.split(":")[0],
                    password=cred.split(":")[1]
                )
                self.mqtt_client.connect()
                print("MQTT connection established.")
            except Exception as e:
                print("MQTT connection error:", e)

    def _is_2xx(self, status_code):
        """Helper to check if HTTP status code is 2xx."""
        return 200 <= status_code < 300

    def register_ae(self):
        """
        Register the Application Entity (AE) with the OM2M CSE.
        """
        payload = {
            "m2m:ae": {
                "rn": self.device_name,
                "api": f"{self.device_name}_api",
                "rr": True,
                "lbl": [self.device_name]
            }
        }

        if self.protocol == 'HTTP':
            headers = {
                'X-M2M-Origin': self.cred,
                'Content-Type': 'application/json;ty=2'
            }
            try:
                response = requests.post(self.cse_url, headers=headers, json=payload)
                if self._is_2xx(response.status_code):
                    print(f"AE registered successfully: {response.text}")
                else:
                    print(f"Error registering AE (HTTP {response.status_code}): {response.text}")
            except OSError as e:
                print("Network error while registering AE:", e)
            except Exception as e:
                print("Unexpected error while registering AE:", e)

        elif self.protocol == 'MQTT':
            topic = f"/oneM2M/req/{self.device_name}/{self.cse}"
            try:
                self.mqtt_client.publish(topic, json.dumps(payload))
                print("MQTT AE registration message sent.")
            except Exception as e:
                print("MQTT publish error (AE registration):", e)

    def create_container(self):
        """
        Create a container under the AE.
        """
        payload = {
            "m2m:cnt": {
                "rn": self.container_name
            }
        }
        if self.protocol == 'HTTP':
            headers = {
                'X-M2M-Origin': self.cred,
                'Content-Type': 'application/json;ty=3'
            }
            url = f"{self.cse_url}/{self.device_name}"
            try:
                response = requests.post(url, headers=headers, json=payload)
                if self._is_2xx(response.status_code):
                    print(f"Container created successfully: {response.text}")
                else:
                    print(f"Error creating container (HTTP {response.status_code}): {response.text}")
            except OSError as e:
                print("Network error while creating container:", e)
            except Exception as e:
                print("Unexpected error while creating container:", e)

        elif self.protocol == 'MQTT':
            topic = f"/oneM2M/req/{self.device_name}/{self.cse}/{self.container_name}/create"
            try:
                self.mqtt_client.publish(topic, json.dumps(payload))
                print("MQTT container creation message sent.")
            except Exception as e:
                print("MQTT publish error (container creation):", e)

    def send_data(self, data):
        """
        Send data to the OM2M CSE.

        :param data: Dictionary of sensor data
        """
        payload = {
            "m2m:cin": {
                "cnf": "application/json",
                "con": json.dumps(data)
            }
        }
        if self.protocol == 'HTTP':
            headers = {
                'X-M2M-Origin': self.cred,
                'Content-Type': 'application/json;ty=4'
            }
            url = f"{self.cse_url}/{self.device_name}/{self.container_name}"
            try:
                response = requests.post(url, headers=headers, json=payload)
                if self._is_2xx(response.status_code):
                    print(f"Data sent successfully: {response.text}")
                else:
                    print(f"Error sending data (HTTP {response.status_code}): {response.text}")
            except OSError as e:
                print("Network error while sending data:", e)
            except Exception as e:
                print("Unexpected error while sending data:", e)

        elif self.protocol == 'MQTT':
            topic = f"/oneM2M/req/{self.device_name}/{self.cse}/{self.container_name}/data"
            try:
                self.mqtt_client.publish(topic, json.dumps(payload))
                print("MQTT data message sent.")
            except Exception as e:
                print("MQTT publish error (data):", e)

    def stop(self):
        """
        Gracefully stop the client based on the protocol.
        """
        if self.protocol == 'MQTT':
            try:
                self.mqtt_client.disconnect()
                print("MQTT client disconnected.")
            except Exception as e:
                print("Error while disconnecting MQTT client:", e)

        print("Client stopped.")
