include_guard()

if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
  )
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_DEBUG_POSTFIX D)
set(CMAKE_SKIP_INSTALL_RULES ON)

option(OPTION_ENABLE_UNITY "Enable Unity builds of project" OFF)
option(OPTION_ENABLE_CLANG_TIDY "Enable clang-tdiy as prebuild step" OFF)
option(BUILD_SHARED_LIBS "Global flag to cause add_library() to create shared libraries if on." OFF)

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  if(APPLE)
    set(OPTION_ENABLED_SANITIZER
        "ENABLE_SANITIZER_ADDRESS; ENABLE_SANITIZER_UNDEFINED_BEHAVIOR"
        CACHE STRING "Enabled sanitizer for debug build"
    )
  else()
    set(OPTION_ENABLED_SANITIZER
        "ENABLE_SANITIZER_MEMORY"
        CACHE STRING "Enabled sanitizer for debug build"
    )
  endif()
endif()

option(OPTION_ENABLE_COVERAGE "Enable test coverage of projects" OFF)
if(OPTION_ENABLE_COVERAGE)
  set(ENABLE_COVERAGE "ENABLE_COVERAGE")
endif()

if(OPTION_ENABLE_UNITY)
  set(ENABLE_UNITY "ENABLE_UNITY")
endif()

if(CMAKE_EXPORT_COMPILE_COMMANDS)
  set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES})
endif()

include(${CMAKE_CURRENT_LIST_DIR}/CPM.cmake)

cpmaddpackage("gh:aminya/project_options@0.29.0")
list(APPEND CMAKE_MODULE_PATH ${project_options_SOURCE_DIR}/src)

# Disable clang-tidy for target
macro(target_disable_clang_tidy TARGET)
  find_program(CLANGTIDY clang-tidy)
  if(CLANGTIDY)
    set_target_properties(${TARGET} PROPERTIES C_CLANG_TIDY "")
    set_target_properties(${TARGET} PROPERTIES CXX_CLANG_TIDY "")
  endif()
endmacro()

macro(check_system_property DIRECTORY)
  get_property(
    _value
    DIRECTORY ${DIRECTORY}
    PROPERTY SYSTEM
    SET
  )
  if(NOT _value)
    message(SEND_ERROR "SYSTEM property is NOT defined for ${DIRECTORY}")
  endif()
endmacro()

macro(set_system_property DIRECTORY)
  message(TRACE "${DIRECTORY}")
  set_property(DIRECTORY ${DIRECTORY} PROPERTY SYSTEM ON)
  check_system_property(${DIRECTORY})
endmacro()

macro(add_tests FILES)
  foreach(source IN LISTS ${FILES})
    string(REGEX REPLACE "\.cpp$" "" program ${source})
    add_executable(${program} ${program}.cpp)
    set_target_properties(${program} PROPERTIES CXX_STANDARD ${CMAKE_CXX_STANDARD})
    if(CMAKE_SKIP_INSTALL_RULES OR CMAKE_BUILD_TYPE STREQUAL "Debug")
      target_link_libraries(${program} PRIVATE $<BUILD_INTERFACE:project_warnings project_options>)
    endif()
    add_test(NAME ${program} COMMAND ${program})
  endforeach()
endmacro()
