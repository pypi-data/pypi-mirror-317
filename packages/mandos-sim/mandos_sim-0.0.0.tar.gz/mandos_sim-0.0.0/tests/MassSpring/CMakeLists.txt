add_executable(tst_MassSpring tst_MassSpring.cpp)
target_link_libraries(
  tst_MassSpring
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_MassSpring COMMAND tst_MassSpring)
