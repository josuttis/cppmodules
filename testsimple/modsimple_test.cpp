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

import ModSquare;  // import module ModSquare

int main()
{
  Square x = toSquare(42);
  std::cout << x.getValue() << '\n';
}

