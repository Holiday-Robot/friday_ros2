# Robot part names are RobotSpec joint-group names (e.g. "left_arm", "right_hand",
# "waist", "head"). part_a <= part_b lexicographically; self pairs are allowed.
string<=64 part_a
string<=64 part_b
# True when every collision-avoidance body pair behind this part pair is enabled.
bool enabled
# Number of controller collision-avoidance body pairs behind this part pair (>= 1).
uint16 pair_count
