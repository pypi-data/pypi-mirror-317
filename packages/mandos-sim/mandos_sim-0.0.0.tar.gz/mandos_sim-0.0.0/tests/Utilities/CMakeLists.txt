add_executable(tst_Utilities tst_Utilities.cpp)
target_link_libraries(
  tst_Utilities
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_Utilities COMMAND tst_Utilities)
