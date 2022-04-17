//********************************************************
// The following C++ code example uses all module artefacts.
// To understand it see
//  C++20 - The Complete Guide
//  by Nicolai M. Josuttis (www.josuttis.com)
//  http://www.cppstd20.com
//
// The code is licensed under a
//  Creative Commons Attribution 4.0 International License
//  http://creativecommons.org/licenses/by/4.0/
//********************************************************

module;                // start module unit with global module fragment

#include <iostream>

// module implementation unit:
module ModAll;

import :Name;          // import internal partition to have type Name

namespace ModAll {

  std::ostream& operator<< (std::ostream& strm, const Person& p)
  {
    return strm << '[' << p.name << ": " << p.value << ']';
  }
}

