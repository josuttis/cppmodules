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

// THE module interface
export module ModAll;

// import and export interface partition Person:
export import :Person;

// export a string and a generic function:
export namespace ModAll {

  auto modName() {
    return "ModAll";
  }

  void printColl(auto&& coll) {
    for (const auto& elem : coll) {
      std::cout << elem << ' ';
    }
    std::cout << '\n';
  }
}
