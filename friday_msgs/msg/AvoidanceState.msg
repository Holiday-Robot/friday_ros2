std_msgs/Header header

# Joint limit avoidance is enabled (SetAvoidanceEnabled LIMIT_AVOIDANCE).
bool limit_avoidance_enabled
# Derived from collision_pairs: true when at least one part pair is enabled. The pair
# list is the collision avoidance state; there is no separate master switch.
# COLLISION_AVOIDANCE sets every pair at once.
bool collision_avoidance_enabled
# Rollover avoidance is enabled (ROLLOVER_AVOIDANCE).
bool rollover_avoidance_enabled
# Per part-pair collision avoidance state, one entry per part pair the controller spec
# defines (sorted by part_a, part_b). Part pairs missing here have no collision
# avoidance tasks.
CollisionPairState[<=64] collision_pairs
uint8 ROLLOVER_MODE_UNKNOWN=0
uint8 ROLLOVER_MODE_STATIC=1
uint8 ROLLOVER_MODE_DYNAMIC=2
uint8 ROLLOVER_MODE_DYNAMIC_WITH_BASE=3
# The rollover mode the controller is configured for: STATIC (phase-space envelope),
# DYNAMIC (CoP acceleration bound through the arm) or DYNAMIC_WITH_BASE (through the
# arm and the base). While rollover_avoidance_enabled is false it is the mode enabling
# resumes. UNKNOWN: the configuration matches none of the three modes.
uint8 rollover_avoidance_mode
