# Command one viewing frame for a single manipulation control step.

# Viewing frame link from the robot description.
string viewing_frame

# Frame for target_pos: a robot link or joint name. An empty string means the
# robot base footprint frame. A name the controller does not know drops the command.
# The controller fixes the point in place when the command arrives.
string reference_frame

# Joints allowed to move. An empty array deactivates this command.
string[] active_joints

# Point in reference_frame that the viewing frame should face.
geometry_msgs/Point target_pos
