cmake_minimum_required(VERSION 3.4)

project(pybind_tof)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")

if (SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()

# Define CMAKE_INSTALL_xxx: LIBDIR, INCLUDEDIR
include(GNUInstallDirs)
include(FetchContent)

if(${WITH_OLD_PYBIND11})
  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.5.0
  )
  message(STATUS "Using old pybind11 (v2.5.0)")
else()
  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.11.1
  )
  message(STATUS "Using new pybind11 (v2.11.1)")
endif()
FetchContent_MakeAvailable(pybind11)

set(VERSION_INFO "" CACHE STRING "Version info")

set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../src)
get_filename_component(SOURCE_DIR ${SOURCE_DIR} ABSOLUTE)
message(STATUS "SOURCE_DIR: ${SOURCE_DIR}")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${SOURCE_DIR}/cmake")
message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

include(source_var)
include(load_package)


pybind11_add_module(ArducamDepthCamera
  ${PYEXPORT_SRC}
  ${SRC_FILES}
)

target_include_directories(ArducamDepthCamera
  PRIVATE
  ${INC_DIR}
)

target_link_libraries(ArducamDepthCamera
  PRIVATE
  ${LIBS}
)

target_compile_definitions(ArducamDepthCamera
  PRIVATE
  ${MACRO}
)

install(TARGETS ArducamDepthCamera DESTINATION .)
# install(FILES ${SiSDKLib} DESTINATION .)
