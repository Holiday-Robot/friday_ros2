# Status of a single camera's video stream target.

string camera_name
bool   enable # true=on, false=off

# Below fields are only valid for `enable=true`
# --- Transport target ---
string destination_ip      # RTP: destination_ip. Setting `localhost(127.0.0.1)` will be rejected.
uint16 destination_port    # RTP: destination_port

# --- Encoder Settings --- (H264 only)
uint32 bitrate_kbps        # 0 -> yaml default
uint32 keyframe_interval   # 0 -> yaml default
