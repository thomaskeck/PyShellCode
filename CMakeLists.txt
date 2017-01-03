cmake_minimum_required (VERSION 2.8.12)

set(CMAKE_C_COMPILER gcc)

project (PyShellCode C ASM_NASM)
set (PyShellCode_VERSION_MAJOR 1)
set (PyShellCode_VERSION_MINOR 0)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake")

# -O3 causes segmentation faults ...
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O0 -Wall -Wextra -g -e _main -ggdb3")
SET(CMAKE_ASM_FLAGS "${CMAKE_C_FLAGS} -x assembler-with-cpp" )

set(INTERPRETER_DESCRIPTION "Requesting program interpreter:")
 
execute_process(COMMAND readelf -l /bin/ls
    RESULT_VARIABLE return_value
    OUTPUT_VARIABLE result
)
 
if(return_value)
    message(STATUS "Cannot find a valid ELF interpreter")
else()
    string(REGEX REPLACE
        ".*[[]${INTERPRETER_DESCRIPTION} ([/][^ ].+)[]].*" "\\1"
        ELF_INTERPRETER_PATH "${result}"
    )
    message(STATUS "ELF interpreter is ${ELF_INTERPRETER_PATH}")
endif()

configure_file (
    "${PROJECT_SOURCE_DIR}/include/PyShellCode.h.in"
    "${PROJECT_BINARY_DIR}/include/PyShellCode.h"
)

configure_file (
    "${PROJECT_SOURCE_DIR}/src/PyShellCode.c.in"
    "${PROJECT_BINARY_DIR}/src/PyShellCode.c"
)

include_directories("${PROJECT_SOURCE_DIR}/include/" "${PROJECT_BINARY_DIR}/include/")

set(PyShellCode_SOURCES
    "${PROJECT_BINARY_DIR}/src/PyShellCode.c"
    "${PROJECT_SOURCE_DIR}/src/CommandLineArgumentGlue.asm"
)

set(PyShellCode_HEADERS
    "${PROJECT_BINARY_DIR}/include/PyShellCode.h"
)


add_library(PyShellCode SHARED ${PyShellCode_SOURCES} ${PyShellCode_HEADERS})
target_link_libraries(PyShellCode)

install(TARGETS PyShellCode
     LIBRARY DESTINATION lib
      ARCHIVE DESTINATION lib
      RUNTIME DESTINATION bin   
   )

install(FILES ${PyShellCode_HEADERS} DESTINATION include)

find_program(PYTHON "python3")

if (PYTHON)
    configure_file(
        "${PROJECT_SOURCE_DIR}/setup.py.in"
        "${PROJECT_SOURCE_DIR}/setup.py"
    )

    add_custom_command(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp"
                       COMMAND ${PYTHON} "${CMAKE_CURRENT_BINARY_DIR}/setup.py" build
                       COMMAND ${CMAKE_COMMAND} -E touch "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp"
                       DEPENDS ${DEPS})

    add_custom_target(target ALL DEPENDS ${OUTPUT})

    install(CODE "execute_process(COMMAND ${PYTHON} ${PROJECT_SOURCE_DIR}/setup.py install --prefix=${CMAKE_INSTALL_PREFIX})")
endif()

set(CPACK_PACKAGE_VERSION "${PyShellCode_VERSION_MAJOR}.${PyShellCode_VERSION_MINOR}")
set(CPACK_GENERATOR "RPM;DEB;TGZ")
set(CPACK_PACKAGE_NAME "PyShellCode")
set(CPACK_PACKAGE_RELEASE 1)
set(CPACK_PACKAGE_CONTACT "thomas.keck2@kit.edu")
set(CPACK_PACKAGE_VENDOR "Private")
set(CPACK_PACKAGING_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.${CMAKE_SYSTEM_PROCESSOR}")

SET(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
SET(CPACK_DEBIAN_PACKAGE_SECTION "libs")
SET(CPACK_DEBIAN_ARCHITECTURE ${CMAKE_SYSTEM_PROCESSOR})

include(CPack)
