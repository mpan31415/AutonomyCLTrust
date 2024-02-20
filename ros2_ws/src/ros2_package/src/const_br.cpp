//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
// FILE SUMMARY:
//
// - Broadcasts a constant transformation between the
//   "camera_base" link of Kinect v2 camera and the robot
//   base link "panda_link0"
//
// - Used to then obtain the transformation from /tf
//   of the point cloud in the robot's frame
//
// - Used for rendering the task scene in RViz
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////

#include <memory>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/static_transform_broadcaster.h"

#include "angles/angles.h"



#define DEPTH_CAMERA_OFFSET_MM_X 0.0f
#define DEPTH_CAMERA_OFFSET_MM_Y 0.0f
#define DEPTH_CAMERA_OFFSET_MM_Z 1.8f  // The depth camera is shifted 1.8mm up in the depth window


class ConstBr : public rclcpp::Node
{
public:

  std::string panda_base_frame = "panda_link0";
  std::string camera_base_frame = "camera_base";
  std::string depth_camera_frame = "depth_camera_link";

  // define transformation values
  // note: TF does translation before rotation
  double dx = 1.22;
  double dy = 0.6;
  double dz = 1.15;
  double rx = deg2rad(183);
  double ry = deg2rad(30);
  double rz = deg2rad(212);

  ConstBr()
  : Node("const_br")
  {
    tf_static_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    // Publish static transforms once upon initialization
    this->publishBaseToPandaTf();
    this->publishDepthToBaseTf();
  }


private:

  void publishBaseToPandaTf()
  { 
    // generate message
    geometry_msgs::msg::TransformStamped t;
    t.header.stamp = this->get_clock()->now();
    t.header.frame_id = panda_base_frame;
    t.child_frame_id = camera_base_frame;

    // translations
    t.transform.translation.x = dx;
    t.transform.translation.y = dy;
    t.transform.translation.z = dz;

    // rotations
    tf2::Quaternion q;
    q.setRPY(rx, ry, rz);
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    tf_static_broadcaster_->sendTransform(t);
  }

  void publishDepthToBaseTf()
  {
    // This is a purely cosmetic transform to make the base model of the URDF look good.
    geometry_msgs::msg::TransformStamped static_transform;

    static_transform.header.stamp = this->get_clock()->now();
    static_transform.header.frame_id = camera_base_frame;
    static_transform.child_frame_id = depth_camera_frame;

    tf2::Vector3 depth_translation = getDepthToBaseTranslationCorrection();
    static_transform.transform.translation.x = depth_translation.x();
    static_transform.transform.translation.y = depth_translation.y();
    static_transform.transform.translation.z = depth_translation.z();

    tf2::Quaternion depth_rotation = getDepthToBaseRotationCorrection();
    static_transform.transform.rotation.x = depth_rotation.x();
    static_transform.transform.rotation.y = depth_rotation.y();
    static_transform.transform.rotation.z = depth_rotation.z();
    static_transform.transform.rotation.w = depth_rotation.w();

    tf_static_broadcaster_->sendTransform(static_transform);
  }

  tf2::Vector3 getDepthToBaseTranslationCorrection()
  {
    // These are purely cosmetic tranformations for the URDF drawing!!
    return tf2::Vector3(DEPTH_CAMERA_OFFSET_MM_X / 1000.0f, DEPTH_CAMERA_OFFSET_MM_Y / 1000.0f,
                        DEPTH_CAMERA_OFFSET_MM_Z / 1000.0f);
  }

  tf2::Quaternion getDepthToBaseRotationCorrection()
  {
    // These are purely cosmetic tranformations for the URDF drawing!!
    tf2::Quaternion ros_camera_rotation;  // ROS camera co-ordinate system requires rotating the entire camera relative to
                                          // camera_base
    tf2::Quaternion depth_rotation;       // K4A has one physical camera that is about 6 degrees downward facing.

    depth_rotation.setEuler(0, angles::from_degrees(-6.0), 0);
    ros_camera_rotation.setEuler(M_PI / -2.0f, M_PI, (M_PI / 2.0f));

    return ros_camera_rotation * depth_rotation;
  }

  double deg2rad(double deg) {
    return (deg / 180) * M_PI;
  }

  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_static_broadcaster_;

};



int main(int argc, char * argv[])
{ 
  // initialize node and spin it
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ConstBr>());
  rclcpp::shutdown();
  return 0;
}