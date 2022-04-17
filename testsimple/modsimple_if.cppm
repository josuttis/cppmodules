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

// THE module interface
export module ModSquare;

int square(int i);

export class Square {
 private:
   int value;
 public:
   Square(int i) 
    : value{square(i)} {
   }
   int getValue() const {
     return value;
   }
};

export template<typename T>
Square toSquare(const T& x) {
  return Square{x};
}

int square(int i) {
  return i * i;
}

