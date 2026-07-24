builtin_interfaces/Time stamp

string name
float64 percent
float64 voltage
int32 connected
int32 lock_state    # latch state machine: 0 IDLE/1 LOCKED/2 UNLOCKED/3 LOCKING/4 UNLOCKING/5 ERROR
uint8 threshold     # 0-100 low-battery alarm SoC
int32 latch_sensor  # latch limit-switch GPIO: 0 NONE/1 CLOSED/2 OPEN/3 BOTH
int32 is_charging   # 1 = charging
int32 cycles        # battery charge/discharge cycle count
float64 cell_temp   # cell temperature [degC]
