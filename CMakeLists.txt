cmake_minimum_required(VERSION 3.26)

#---------------------------------------------------------------------------------------
# Compiler config
#---------------------------------------------------------------------------------------
if(NOT DEFINED CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 20)
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

#=============================
project(samples LANGUAGES CXX)
#=============================

include(cmake/options.cmake)

# ---- Setup default project_options ----

# cmake-format: off
project_options(
  # PREFIX ${PROJECT_NAME}
  ENABLE_CACHE
  #NO! ENABLE_CLANG_TIDY
  ${ENABLE_COVERAGE}
  ${OPTION_ENABLED_SANITIZER}
  #XXX ENABLE_SANITIZER_ADDRESS
  #XXX ENABLE_SANITIZER_UNDEFINED_BEHAVIOR
  #XXX ENABLE_SANITIZER_THREAD
  #XXX ENABLE_SANITIZER_MEMORY
  WARNINGS_AS_ERRORS
)
# cmake-format: on

target_compile_features(project_options INTERFACE cxx_std_${CMAKE_CXX_STANDARD})

enable_testing()

# ---- Setup experimental cmake C++20 module support ----

# see https://releases.llvm.org/15.0.0/projects/libcxx/docs/ReleaseNotes.html
#XXX add_compile_options(-fexperimental-library)
#XXX add_link_options(-lc++experimental)

set(CMAKE_EXPERIMENTAL_CXX_MODULE_CMAKE_API 2182bf5c-ef0d-489a-91da-49dbc3090d2a)
set(CMake_TEST_CXXModules_UUID "a246741c-d067-4019-a8fb-3d16b0c9d1d3")

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
  # string(CONCAT CMAKE_EXPERIMENTAL_CXX_SCANDEP_SOURCE
  #               "<CMAKE_CXX_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E -x c++ <SOURCE>"
  #               " -MT <DYNDEP_FILE> -MD -MF <DEP_FILE>"
  #               " -fmodules-ts -fdep-file=<DYNDEP_FILE> -fdep-output=<OBJECT> -fdep-format=trtbd"
  #               " -o <PREPROCESSED_SOURCE>"
  # )
  # set(CMAKE_EXPERIMENTAL_CXX_MODULE_MAP_FORMAT "gcc")
  # set(CMAKE_EXPERIMENTAL_CXX_MODULE_MAP_FLAG "-fmodules-ts -fmodule-mapper=<MODULE_MAP_FILE> -fdep-format=trtbd -x c++")

elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_DYNDEP 1)
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_MAP_FORMAT "clang")
  set(CMAKE_EXE_LINKER_FLAGS -lstdc++)
  # Workaround for C++Modules: Missing module map flags in exported compile commands
  # see https://gitlab.kitware.com/cmake/cmake/-/issues/24618
  set(CMAKE_CXX_COMPILE_OBJECT "${CMAKE_CXX_COMPILE_OBJECT} @<OBJECT>.modmap")

elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(CMAKE_EXPERIMENTAL_CXX_MODULE_DYNDEP 1)

endif()

add_subdirectory(testsimple)
add_subdirectory(testall)

