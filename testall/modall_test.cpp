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

#include <iostream>

import ModAll;

int main()
{
  std::cout << "test " << ModAll::modName() << '\n';
  ModAll::Person p1{"Kim", 42};
  std::cout << "p1: " << p1 << '\n';
}
