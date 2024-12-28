add_executable(tst_StableNeoHookean tst_StableNeoHookean.cpp)
target_link_libraries(
  tst_StableNeoHookean
  PUBLIC Mandos::Core
         TinyAD
         Catch2::Catch2WithMain
         spdlog::spdlog
         fmt::fmt
)

add_test(NAME tst_StableNeoHookean COMMAND tst_StableNeoHookean)
