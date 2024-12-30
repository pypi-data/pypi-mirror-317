#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "embree_avx2" for configuration "Release"
set_property(TARGET embree_avx2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(embree_avx2 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libembree_avx2.a"
  )

list(APPEND _cmake_import_check_targets embree_avx2 )
list(APPEND _cmake_import_check_files_for_embree_avx2 "${_IMPORT_PREFIX}/lib/libembree_avx2.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
