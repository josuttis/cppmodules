C++20 introduced modules.
Unfortunately it is still not possible to write C++ programs using modules that are portable
without significant effort.
The reason is that the different compiler vendors could not agree on a common way to treat module files.
While gcc/g++ does not require any special suffix, other compiler do it (with different recommended suffixes).

In fact, Visual C++ does
- require special suffixes for specific module files and
  special /options to be set when compiling some module files
- not allow to request a compilation of different module files with ONE command
- does neither document the requested file suffixes nor the necessary command-line options

here is what Visual C++ needs:
- Interface files (module interface or interface partition)
  need suffix .ixx or the option /interface
- Internal partitions need the option /internalPartition
  (the suffix doesn't matter; they recommend the usual suffix such as .cpp).
- Module implementation units need no specific module treatment
  (use the usual suffix with no special option)
- Options /interface and /internalPartition may not be used together

This is a significant restriction because other compilers do neither need
special suffixes nor special options but also do not know what to do with the
.ixx suffix Microsoft recommends.

To circumvent this restriction and briong the idea of portable moudle files
into life, I have implemented a pything script that gives Visual C++ the flexibility it should have.
The attached script
 clmod.py
is a python script that allows to
 - use arbitrary file name suffixes for module files
 - allows to pass all files with one command line

This does not mean that different file suffixes may not make sense to deal
with C++ module files. But it helps until we see an established portable
policy for this.

For example,
given for a module Mod 3, we have:
 mod3if.cppm     : The module interface unit
 mod3impl.cpp    : An implementation unit
 mod3test.cpp    : A traditionaal translation unit
 mod3ifpart.cppm : An interface partition unit
and to test this we have:
 mod3part.cppm   : An internal partition

Calling:
 clm.py /std:c++latest mod3part.cppm mod3ifpart.cppm mod3if.cppm mod3impl.cpp mod3test.cpp /Femod3.exe

will automatically do the right thing:
 cl /std:c++latest /Femod3.exe /TP /c /internalPartition mod3part.cppm
 cl /std:c++latest /Femod3.exe /TP /c /interface mod3ifpart.cppm
 cl /std:c++latest /Femod3.exe /TP /c /interface mod3if.cppm
 cl /std:c++latest /Femod3.exe /TP /c mod3impl.cpp
 cl /std:c++latest /Femod3.exe /TP /c mod3test.cpp
 cl /std:c++latest /Femod3.exe mod3part.obj mod3ifpart.obj mod3if.obj mod3impl.obj mod3test.obj

Note tat the order of the files matters because files that import modules need
the pre-compiled module code (which is compiler-specific).
Yes, circular imports are not possible.

Passing /Femod3.exe to the compile command is not necessary but also doesn't
hurt.
In general, the script passes all options to both the compile and the link command.
Except a "/c" (compile only), which is handled by the script.

Probably not all options work correctly, but for a first test it works fine.
I would expect that this script being integrated in Visual C++ they do things right.

For more details see the book
 C++20 - The Complete Guide by Nicolai M. Josuttis
The code is licensed under a Creative Commons Attribution 4.0 International License.

