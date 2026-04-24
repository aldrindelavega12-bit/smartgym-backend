import serial
import struct
import time


class AS608:
    HEADER = b'\xEF\x01'
    ADDRESS = b'\xFF\xFF\xFF\xFF'

    def __init__(self, port, baudrate=57600):
        self.ser = serial.Serial(port, baudrate, timeout=2)

    def _send_packet(self, packet_type, payload):
        length = len(payload) + 2
        packet = (
            self.HEADER +
            self.ADDRESS +
            bytes([packet_type]) +
            struct.pack('>H', length) +
            payload
        )

        checksum = sum(packet[6:])  # from packet_type onward
        packet += struct.pack('>H', checksum)
        self.ser.write(packet)

    def _read_response(self):
        data = self.ser.read(12)
        if len(data) < 12:
            return None
        return data

    def verify_fingerprint(self):
        # Capture Image
        self._send_packet(0x01, b'\x01')
        time.sleep(0.5)
        self._read_response()

        # Convert to template (buffer 1)
        self._send_packet(0x01, b'\x02\x01')
        time.sleep(0.5)
        self._read_response()

        # Search
        payload = b'\x04\x01\x00\x00\x00\xA3'
        self._send_packet(0x01, payload)
        time.sleep(0.5)

        response = self.ser.read(16)
        if len(response) < 16:
            return None

        confirmation_code = response[9]

        if confirmation_code != 0x00:
            return None

        page_id = struct.unpack('>H', response[10:12])[0]
        return page_id

    def enroll_fingerprint(self, location_id):
        print("Place finger...")
        self._send_packet(0x01, b'\x01')
        time.sleep(1)
        self._read_response()

        self._send_packet(0x01, b'\x02\x01')
        time.sleep(1)
        self._read_response()

        print("Remove finger...")
        time.sleep(2)

        print("Place same finger again...")
        self._send_packet(0x01, b'\x01')
        time.sleep(1)
        self._read_response()

        self._send_packet(0x01, b'\x02\x02')
        time.sleep(1)
        self._read_response()

        self._send_packet(0x01, b'\x05')
        time.sleep(1)
        self._read_response()

        payload = b'\x06' + struct.pack('>H', location_id)
        self._send_packet(0x01, payload)
        time.sleep(1)
        self._read_response()

        print(f"Fingerprint enrolled at ID {location_id}")
        return location_id
    
    
    def get_template_count(self):
        # Command 0x1D = Template count
        self._send_packet(0x01, b'\x1D')
        time.sleep(0.5)
        response = self.ser.read(14)

        if len(response) < 14:
            return 0

        count = struct.unpack('>H', response[10:12])[0]
        return count

    def close(self):
        self.ser.close()