# Command one end-effector frame for a single manipulation control step.

# Target end-effector link from the robot description.
string target_frame

# Frame for target_pos and target_quat. An empty string means world.
string reference_frame

# Joints allowed to move. An empty array deactivates this command.
string[] active_joints

# Controller reaching mode. The default enables position and orientation.
uint8 mode 3

# Position objective weight.
float32 position_weight 5.0

# Orientation objective weight.
float32 orientation_weight 1.0

# Continuously update the goal when tracking a moving target.
bool tracking false

# Target position in reference_frame.
geometry_msgs/Point target_pos

# Target orientation in reference_frame.
geometry_msgs/Quaternion target_quat
