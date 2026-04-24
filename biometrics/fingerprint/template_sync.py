from pyfingerprint.pyfingerprint import PyFingerprint


class TemplateSync:

    def __init__(self, in_sensor, out_sensor):
        self.in_sensor = in_sensor
        self.out_sensor = out_sensor

    def sync_template(self, positionNumber):

        try:
            print("Syncing template ID:", positionNumber)

            # Load template from IN sensor
            self.in_sensor.loadTemplate(positionNumber, 0x01)

            # Download characteristics
            characteristics = self.in_sensor.downloadCharacteristics(0x01)

            # Upload to OUT sensor
            self.out_sensor.uploadCharacteristics(0x01, characteristics)

            # Store in OUT sensor
            self.out_sensor.storeTemplate(positionNumber)

            print("Template synced successfully.")

        except Exception as e:
            print("Template sync error:", e)