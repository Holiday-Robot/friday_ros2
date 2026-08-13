uint8 STATUS_UNKNOWN=0
uint8 STATUS_OK=1
uint8 STATUS_DISCONNECTED=2
uint8 STATUS_ERROR=3

string<=64 sensor_id
sensor_msgs/Range measurement
uint8 status
