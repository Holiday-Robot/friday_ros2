# Command one joint for a single manipulation control step.

# Joint name from the robot description.
string target_joint

# Desired joint position in radians. NaN means hold the current position.
float32 target_position

# Reference velocity in rad/s. Zero disables velocity feedforward.
float32 target_velocity 0.0

# Reference acceleration in rad/s^2. Zero disables acceleration feedforward.
float32 target_acceleration 0.0
