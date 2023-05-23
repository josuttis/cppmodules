if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wno-unused-command-line-argument)
endif()

#
# module with partitions
#
add_library(testsimple)
target_sources(
  testsimple
  PUBLIC FILE_SET
         cxx_modules
         TYPE
         CXX_MODULES
         FILES
            modsimple_if.cppm
)
set_target_properties(testsimple PROPERTIES CXX_STANDARD ${CMAKE_CXX_STANDARD})
if(CMAKE_SKIP_INSTALL_RULES AND CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_link_libraries(testsimple PUBLIC $<BUILD_INTERFACE:project_warnings project_options>)
endif()
add_executable(modsimple_test modsimple_test.cpp)
target_link_libraries(modsimple_test testsimple)
add_test(NAME modsimple_test COMMAND modsimple_test)
