add_executable(tst_CosseratRod tst_CosseratRod.cpp)
target_link_libraries(
  tst_CosseratRod
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_CosseratRod COMMAND tst_CosseratRod)
