from common import wifi
from common import mqtt
from controls.control_panel import ControlPanel
import sys
import io


def run():
    wifi.connect()
    mqtt.publish_action('/iot/device/lifecycle','status','Booting')

    try:
        panel = ControlPanel()
        panel.loop_forever()

    except Exception as e:
        buf = io.StringIO()
        sys.print_exception(e, buf)  # Write traceback to buffer
        traceback_str = buf.getvalue()
        print(traceback_str)
        mqtt.publish_action('/iot/device/lifecycle','error',traceback_str)
