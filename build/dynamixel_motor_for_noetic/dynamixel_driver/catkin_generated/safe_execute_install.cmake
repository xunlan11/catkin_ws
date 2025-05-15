execute_process(COMMAND "/home/robot/catkin_ws/build/dynamixel_motor_for_noetic/dynamixel_driver/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/robot/catkin_ws/build/dynamixel_motor_for_noetic/dynamixel_driver/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
