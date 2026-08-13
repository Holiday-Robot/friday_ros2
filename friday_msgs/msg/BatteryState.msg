uint8 SOC_SOURCE_UNKNOWN=0
uint8 SOC_SOURCE_NONE=1
uint8 SOC_SOURCE_BMS=2
uint8 SOC_SOURCE_ADC=3

uint8 POWER_STATE_UNKNOWN=0
uint8 POWER_STATE_NORMAL=1
uint8 POWER_STATE_WARNING=2
uint8 POWER_STATE_CRITICAL=3
uint8 POWER_STATE_SHUTDOWN=4

std_msgs/Header header
float32 state_of_charge
float32 voltage
bool connected
bool charging
uint8 state_of_charge_source
uint8 power_state
bool controller_connected
friday_msgs/BatteryPackState[<=2] packs
