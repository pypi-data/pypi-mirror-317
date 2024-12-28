add_executable(tst_RotationMatrixDerivatives tst_RotationMatrixDerivatives.cpp)
target_link_libraries(
  tst_RotationMatrixDerivatives
  PUBLIC Mandos::Core
         Catch2::Catch2WithMain
)

add_test(NAME tst_RotationMatrixDerivatives COMMAND tst_RotationMatrixDerivatives)
