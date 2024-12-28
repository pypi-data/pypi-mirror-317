add_executable(tst_Simulation tst_Simulation.cpp)
target_link_libraries(
  tst_Simulation
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_Simulation COMMAND tst_Simulation)
