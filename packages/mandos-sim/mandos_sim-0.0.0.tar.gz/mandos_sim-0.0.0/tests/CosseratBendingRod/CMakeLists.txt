add_executable(tst_CosseratBendingRod tst_CosseratBendingRod.cpp)
target_link_libraries(
  tst_CosseratBendingRod
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
         spdlog::spdlog
         fmt::fmt
)

add_test(NAME tst_CosseratBendingRod COMMAND tst_CosseratBendingRod)
