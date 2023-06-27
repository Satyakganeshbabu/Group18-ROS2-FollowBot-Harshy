cmake_minimum_required(VERSION 3.5)

project(harshy_follow)

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)

install(PROGRAMS
  src/harshy_follow.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
