# ROS2 Debug Checklist

## Build problems

### Package not found
- Source the ROS2 underlay first: `source /opt/ros/<distro>/setup.bash`
- Run `rosdep install --from-paths src --ignore-src -y`
- Check `package.xml` dependency declarations

### Python package builds but executable not found
- Verify `setup.py` / `entry_points`
- Rebuild with `colcon build --symlink-install`
- Source `install/setup.bash`
- Check `ros2 pkg executables <pkg>`

### CMake package fails
- Verify `find_package(...)` lines
- Verify `ament_target_dependencies(...)`
- Ensure install rules exist

## Runtime problems

### Topic exists but subscriber receives nothing
Most likely a QoS mismatch.
- Sensor streams: usually `BEST_EFFORT`
- Commands/state: usually `RELIABLE`
- Check with `ros2 topic info /topic -v`

### Parameters fail
- Confirm the node actually declared the parameter
- Confirm ROS2, not ROS1
- Check namespace / node name

### Actions fail
- Confirm action server exists with `ros2 action list`
- Confirm correct action type and goal schema

### rosbridge issues
- Confirm `rosbridge_server` is running
- Confirm IP/port reachability
- Confirm ROS graph is alive before blaming the bridge

## Safety reminders
- For any motion example, include a stop command or neutral output path
- Separate simulation examples from real hardware examples
- Never assume `/cmd_vel` semantics; inspect message type and controller behavior first
