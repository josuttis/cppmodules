# clmod.py

A script to let Visual C++ deal easily with C++20 programs using modules.

## Why?

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

Here is what Visual C++ needs in detila for module files:
- **Interface files** (module interface or interface partition)
  need suffix `.ixx` or the option `/interface`
- **Internal partitions** need the option `/internalPartition`
  (the suffix doesn't matter; they recommend the usual suffix such as .cpp).
- **Module implementation units** need no specific module treatment
  (use the usual suffix with no special option)
- Options `/interface` and `/internalPartition` may not be used together

This is a significant restriction because other compilers do neither need
special suffixes nor special options but also do not know what to do with the
`.ixx` suffix Microsoft recommends.

To circumvent this restriction and bring the idea of portable module files
to life, I have implemented a pythen script that gives Visual C++ the flexibility it should have.
The attached script
 **clmod.py**
is a python script that allows to
- use arbitrary file name suffixes for module files
- allows to pass all files with one command line

This does not mean that different file suffixes may not make sense to deal
with C++ module files. But it helps until we see an established portable
policy for this.

## For example

Given for a module ModAll (see the subdirectory testall),
we have:
- **modall_if.cppm**     : The module interface unit
- **modall_ifpart.cppm** : An interface partition unit
- **modall_part.cppm**   : An internal partition
- **modall_impl.cpp**    : An implementation unit

To test this we have:
- **modall_test.cpp**    : A traditional translation unit

Calling:

    clmod.py /std:c++latest modall_part.cppm modall_ifpart.cppm modall_if.cppm modall_impl.cpp modall_test.cpp /Femodall.exe

will automatically do the right thing:

    cl /std:c++latest /Femodall.exe /TP /c /internalPartition modall_part.cppm
    cl /std:c++latest /Femodall.exe /TP /c /interface modall_ifpart.cppm
    cl /std:c++latest /Femodall.exe /TP /c /interface modall_if.cppm
    cl /std:c++latest /Femodall.exe /TP /c modall_impl.cpp
    cl /std:c++latest /Femodall.exe /TP /c modall_test.cpp
    cl /std:c++latest /Femodall.exe modall_part.obj modall_ifpart.obj modall_if.obj modall_impl.obj modall_test.obj

Note tat the order of the files matters, because files that import modules need
the pre-compiled module code (which is compiler-specific).
Yes, circular imports are not possible.

Passing `/Femodall.exe` to the compile command is not necessary but also doesn't
hurt.
In general, the script passes all options to both the compile and the link command.
Except a `/c` (compile only), which is handled by the script to not start the linker.

Probably not all options work correctly, but for a first test it works fine.
I would hope that the support this script provides is soon directly provided by Visual C++.

## Tests

I have provided the folloiwng subdirectories to test the script:
- **testsimple**: a simple module example using only a module interface 
- **testall**: a full module example using all module units with extension `.cppm`
- **testallixx**: a full module example using Visual C++ conventions (`.ixx` for interface files)
- **testallcpp**: a full module example using `.cpp`for all files (as gcc supports)

## More

For more details how to implement and deal with C++20 modules
see

>  C++20 - The Complete Guide by Nicolai M. Josuttis
>
>  http://cppstd20.com

## License

The code is licensed under a Creative Commons Attribution 4.0 International License.

http://creativecommons.org/licenses/by/4.0/


