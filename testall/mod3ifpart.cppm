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

// Moule interface partition:
export module Mod3:Person;

import :Name;          // import internal partition to have type Name

// export a string and a generic function:
export namespace Mod3 {

  class Person {
   private:
    Name name;
    int value = 0;
   public:
    Person(std::string n, int v = 0)
     : name{std::move(n)}, value{v} {
    }
    friend std::ostream& operator<< (std::ostream&, const Person&);
  };
}
