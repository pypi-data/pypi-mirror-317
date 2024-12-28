add_executable(tst_Colliders tst_Colliders.cpp)
target_link_libraries(
  tst_Colliders
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_Colliders COMMAND tst_Colliders)
