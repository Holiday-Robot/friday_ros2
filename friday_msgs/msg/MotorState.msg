uint8 STATE_UNKNOWN=0
uint8 STATE_OFF=1
uint8 STATE_READY=2
uint8 STATE_ENABLED=3
uint8 STATE_RUNNING=4
uint8 STATE_FAULT=5
uint8 STATE_ESTOP=6

uint8 MODE_IDLE=0
uint8 MODE_VELOCITY=1
uint8 MODE_POSITION=2
uint8 MODE_SIMPLE=3
uint8 MODE_WHEEL=4
uint8 MODE_TORQUE=5

uint8 EXTERNAL_ENCODER_NOT_PRESENT=0
uint8 EXTERNAL_ENCODER_VALID=1
uint8 EXTERNAL_ENCODER_ERROR=2

uint8 LIMIT_PERCENTAGE_UNKNOWN=255

string<=64 name
bool connected
uint8 state
uint32 error_code
uint8 present_mode
float64 position
float64 velocity
float64 torque
uint8 velocity_limit_percentage
uint8 current_limit_percentage
int8 temperature
uint8 external_encoder_status
float64 external_encoder_position
