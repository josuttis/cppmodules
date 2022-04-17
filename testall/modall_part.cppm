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
#include <cassert>

// internal partition:
module ModAll:Name;

class Name {
 private:
  std::string name;
 public:
  Name(std::string n)
   : name{std::move(n)} {
    assert(!name.empty());   // require non-empty name
  }

  friend std::ostream& operator<< (std::ostream& strm, const Name& n) {
    return strm << n.name;
  }
};

