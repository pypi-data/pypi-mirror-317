add_executable(tst_FixedProjection tst_FixedProjection.cpp)
target_link_libraries(
  tst_FixedProjection
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_FixedProjection COMMAND tst_FixedProjection)
