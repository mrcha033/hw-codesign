# Generated firmware modules
target_sources(app PRIVATE
  ../../../firmware/modules/usb_cdc.c
  ../../../firmware/modules/bme280_driver.c
  ../../../firmware/modules/data_streamer.c
  ../../../firmware/modules/biped_motion_state.c
  ../../../firmware/modules/lsm6dsox_driver.c
  ../../../firmware/modules/pca9685_servo_pwm.c
  ../../../firmware/modules/servo_safety_watchdog.c
)
