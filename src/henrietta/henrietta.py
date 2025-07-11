import socket


class Henrietta:
    def __init__(self, ip_address: str = "127.0.0.1", port: int = 52801):
        self.ip_address = ip_address
        self.port = port
        self.socket = None
        self._connected = False
        self.wheels = ["grism", "diffuser", "filter", "slit", "slide", "moving"]

    def open(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.port))
        self._connected = True

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
        self._connected = False

    def get_status(self):
        if not self._connected:
            raise ConnectionError("Henrietta is not connected.")
        # Send a request to get the status of the instrument
        self.socket.sendall(b"status\n")
        response = self.socket.recv(1024)
        return response.decode().strip().split(" ")

    # Wheel control methods
    @property
    def is_moving(self):
        return self.get_status()[1] == "1"

    def get_wheels(self, parse_str: str | None = None):
        if not self._connected:
            raise ConnectionError("Henrietta is not connected.")
        if parse_str is None:
            # Send a request to get wheel information
            self.socket.sendall(b"get_wheels\n")
            response = self.socket.recv(1024)
            response = response.decode().strip().split(",")
        else:
            # Parse the provided string
            response = parse_str.strip().split(",")
        ret = dict(zip(self.wheels, response))
        ret["moving"] = ret["moving"] == "1"  # Convert moving to boolean
        return ret

    def move_wheel(self, wheel: str, position: int):
        if not self._connected:
            raise ConnectionError("Henrietta is not connected.")
        if wheel not in self.wheels:
            raise ValueError(f"Invalid wheel: {wheel}. Valid wheels are: {self.wheels}")
        # Send a command to set the wheel position
        command = f"move_{wheel} {position}\n".encode()
        self.socket.sendall(command)
        response = self.socket.recv(1024)
        return self.get_wheels(parse_str=response.decode())

    def move_grism(self, position: int):
        return self.move_wheel("grism", position)

    def move_diffuser(self, position: int):
        return self.move_wheel("diffuser", position)

    def move_filter(self, position: int):
        return self.move_wheel("filter", position)

    def move_slit(self, position: int):
        return self.move_wheel("slit", position)

    def move_slide(self, position: int):
        return self.move_wheel("slide", position)

    # Exposure control methods
    @property
    def is_exposing(self) -> bool:
        return self.get_status()[0] == "1"

    def exposure_time(self, seconds: float | None = None) -> float:
        if not self._connected:
            raise ConnectionError("Henrietta is not connected.")
        # Send a command to set the exposure time
        if seconds is None:
            command = b"exptime\n"
        else:
            command = f"exptime {seconds}\n".encode()
        self.socket.sendall(command)
        response = self.socket.recv(1024)
        return float(response.decode().strip())

    def start_exposure(self) -> bool:
        if not self._connected:
            raise ConnectionError("Henrietta is not connected.")
        # Send a command to start the exposure
        self.socket.sendall(b"start\n")
        response = self.socket.recv(1024)
        return response.decode().strip() == "ok"

    def expose(self, seconds: float | None = None) -> bool:
        self.exposure_time(seconds)
        return self.start_exposure()
