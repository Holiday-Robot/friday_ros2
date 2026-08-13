std_msgs/Header header
# gen1 hands publish 466 points (233 per hand: thumb 38 + fingers 4x34 + palm 59);
# the bound must cover both hands in one message.
friday_msgs/TactilePointState[<=512] points
