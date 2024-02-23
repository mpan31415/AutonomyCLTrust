# AutonomyCLTrust

This is a research project conducted by Jiahe Pan at the University of Melbourne, Australia, under supervision of Jonathan Eden, Denny Oetomo and Wafa Johal. It utilizes a shared control teleoperated trajectory tracking setup to investigate the relationship between robot autonomy and the human operator's cognitive load and trust. It uses the [Franka Emika robot arm](https://franka.de/research) and the [Novint Falcon haptic device](https://www.forcedimension.com/company/about) for the primary trajectory tracking task and [Tobii eye trackers](https://www.tobii.com/solutions/scientific-research) for one of the cognitive load measures. Experiments were conducted with 24 participants. 


## Project Links
- Demo video: https://youtu.be/wm3UqmnWGJs
- Project site: https://sites.google.com/view/auto-cl-trust/home


## Contents

- [ROS2 Workspace](#1)
- [Eye-Tracking](#2)
- [Dual Task](#3)
- [Data](#4)
- [Data Analysis](#5)
- [Paper and Citation Info](#6)

<br>

<a id='1'></a>

# ROS2 Workspace

Ubuntu 22.04 and ROS2 (Humble) installations are required. The `ros2_ws` workspace contains the following two ROS packages:
- `ros2_package`
- `tutorial_interfaces`

### ros2_package
This package contains the code files for the primary task, including receiving information from and sending control commands to the robot, data logging scripts, and rendering the task scene in RViz. Specifically, it contains the following sub-folders:

| Folder | Description |
| ------ | ------ |
| `data_logging/csv_logs` | Contains the raw data (csv format) collected from all participants, including a header file for each participant with the calculated task performances for each trial condition. |
| `launch` | Contains ROS launch files to run the nodes defined in the `src` folder, including launching the controller with both the [Gazebo](https://docs.ros.org/en/foxy/Tutorials/Advanced/Simulators/Ignition/Ignition.html) simulator and the real robot, and to start the RViz rendering of the task. |
| `ros2_package` | Contains package files including useful functions to generate the trajectories, parameters to run experiments, and the definition of the `DataLogger` Python class. |
| `scripts` | Contains the definition of the `TrajRecorder` Python class, used for receiving control commands and robot poses into temporary data structures, before logging the data to csv files using a `DataLogger` instance. |
| `src` | Contains C++ source code for the ROS nodes used, including class definitions of the `GazeboController` and `RealController` for controlling the robot in simulation and real world respectively, the `PositionTalker` for reading the position of the Falcon joystick, and the `MarkerPublisher` for publishing visualization markers into the RViz rendering.  |
| `urdf` | Contains a auto-generated URDF file of the Franka Emika robot arm.  |

### tutorial_interfaces
This packcage contains custom ROS message and service definitions. Specifically, there are two custom `msg` interfaces defined for communication and data logging:
| Msg | Description |
| ------ | ------ |
| `Falconpos.msg` | A simple definition of a 3D coordinate in Euclidean space. Attributes: `x, y, z` |
| `PosInfo.msg` | A definition of the state vector of the system for a given timestamp. Attributes: `ref_position[], human_position[], robot_position[], tcp_position[], time_from_start` |


<br>
<a id='2'></a>

# Eye-Tracking


<br>
<a id='3'></a>

# Dual-Task


<br>
<a id='4'></a>

# Data


<br>
<a id='5'></a>

# Data Analysis


<br>
<a id='6'></a>

# Paper and Citation Info