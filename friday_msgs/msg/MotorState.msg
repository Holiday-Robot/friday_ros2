builtin_interfaces/Time stamp

string name
float64 position  # motor-side present position [rad]
float64 velocity  # motor-side present velocity [rad/s]
float64 effort    # motor torque [Nm]
# Decoded motor lifecycle status, robot-generation-agnostic. Each driver maps its
# own raw firmware status bits (fault=bit3 estop=bit4) into this single value.
# Priority: ESTOP > FAULT > RUN > ENABLE > READY > OFF.
uint8 STATUS_OFF=0
uint8 STATUS_READY=1
uint8 STATUS_ENABLE=2
uint8 STATUS_RUN=3
uint8 STATUS_FAULT=4
uint8 STATUS_ESTOP=5
uint8 status

uint8 motor_mode  # actual control mode reported by firmware (2=POSITION, 3=PID, 5=TORQUE, 0=unknown)
int8 temperature  # motor temperature [degC]; 0 if N/A
