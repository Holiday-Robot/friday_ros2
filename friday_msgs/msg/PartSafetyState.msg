string part
uint32 err_code
uint8 state     # 0=NORMAL 1=STOPPING 2=STOPPED 3=FAULT 4=RESETTING
uint16 bits     # bit0=ESTOP bit1=FAULT bit2=RESET_FAILED bit5=ESTOP_RECOVERY
uint8 estop     # bit0=WIRED bit1=SW bit2=WIRELESS
bool estop_recovering  # estop active or post-release recovery window; err_code suppressed, fault_reset premature
bool reset_ready       # (STOPPED||FAULT) && !estop_recovering — fault_reset will take effect now
