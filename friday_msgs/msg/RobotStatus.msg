builtin_interfaces/Time stamp

bool ecat_stop
bool robot_stop
bool robot_pause
bool sensor_ready
bool motor_ready
bool joint_lock
uint8[16] joint_lock_mask  # per-joint lock bitmask, 1 bit per joint. byte k covers joints [k*8 .. k*8+7]: bit j of byte k is 1 when joint[k*8+j] caused the lock. e.g. joint[0] -> byte[0] bit 0, joint[7] -> byte[0] bit 7, joint[8] -> byte[1] bit 0. Supports up to 128 joints; unused bits are 0.
