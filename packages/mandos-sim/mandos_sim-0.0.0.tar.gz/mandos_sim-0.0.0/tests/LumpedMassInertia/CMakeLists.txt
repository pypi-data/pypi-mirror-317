add_executable(tst_LumpedMassInertia tst_LumpedMassInertia.cpp)
target_link_libraries(
  tst_LumpedMassInertia
  PUBLIC Mandos::Core
         TinyAD
         Catch2::Catch2WithMain
)

add_test(NAME tst_LumpedMassInertia COMMAND tst_LumpedMassInertia)
