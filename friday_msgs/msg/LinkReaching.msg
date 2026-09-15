# Command one end-effector frame for a single manipulation control step.

# Target end-effector link from the robot description.
string target_frame

# Frame for target_pos, target_quat, target_vel and target_acc. An empty string means world.
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

# Goal rates in reference_frame: linear = velocity of the target point itself
# (d/dt target_pos, m/s), angular = rate of the target frame (rad/s). This is NOT
# a spatial twist about the reference-frame origin; convert such a twist with
# linear = v_origin + angular x target_pos. Zero disables velocity feedforward.
# The goal pose is not integrated from this twist; stream target_pos and
# target_quat together with target_vel.
geometry_msgs/Twist target_vel

# Goal acceleration with the same point convention (linear = d2/dt2 target_pos,
# m/s^2; angular rad/s^2). Zero disables acceleration feedforward.
geometry_msgs/Accel target_acc
