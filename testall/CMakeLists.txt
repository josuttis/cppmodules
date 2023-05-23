if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wno-unused-command-line-argument)
endif()

#
# module with partitions
#
add_library(testall)
target_sources(
  testall
  PRIVATE modall_impl.cpp
  PUBLIC FILE_SET
         cxx_modules
         TYPE
         CXX_MODULES
         FILES
            modall_if.cppm
            modall_ifpart.cppm  # interface partition
            modall_part.cppm    # internal partition
)
set_target_properties(testall PROPERTIES CXX_STANDARD ${CMAKE_CXX_STANDARD})
if(CMAKE_SKIP_INSTALL_RULES AND CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_link_libraries(testall PUBLIC $<BUILD_INTERFACE:project_warnings project_options>)
endif()
add_executable(modall_test modall_test.cpp)
target_link_libraries(modall_test testall)
add_test(NAME modall_test COMMAND modall_test)
