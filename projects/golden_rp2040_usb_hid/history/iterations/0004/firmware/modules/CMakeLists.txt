# Generated firmware modules
target_sources(app PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/usb_hid_stack.c
  ${CMAKE_CURRENT_LIST_DIR}/usb_cdc_stack.c
  ${CMAKE_CURRENT_LIST_DIR}/flash_xip.c
  ${CMAKE_CURRENT_LIST_DIR}/pio_ws2812.c
)
target_include_directories(app PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/../generated
)
