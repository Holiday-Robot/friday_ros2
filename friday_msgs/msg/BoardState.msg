uint8 STATE_NORMAL=0
uint8 STATE_STOPPING=1
uint8 STATE_STOPPED=2
uint8 STATE_FAULT=3
uint8 STATE_RESETTING=4

string<=64 board_name
uint8 state
uint32 error_code
bool fault
bool reset_failed
bool emergency_stop_recovering
