default: modsimple.win

include ../Makefile.h
	
###########################################
# generic rules for special module suffixes
###########################################

.SUFFIXES: .cppm .cppp .obj .ixx
.ixx.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /TP /c /interface $*.ixx $(IFCDIRFLAGS)
	@echo "=== $*.obj done"
	@echo ""
.cppm.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /TP /c /interface $*.cppm $(IFCDIRFLAGS)
	@echo "=== $*.obj done"
	@echo ""
.cppp.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /TP /c /internalPartition $*.cppp $(IFCDIRFLAGS)
	@echo "=== $*.obj done"
	@echo ""
.cpp.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /c $*.cpp $(IFCDIRFLAGS)
	@echo "=== $*.obj done"
	@echo ""

###########################################
# targets for Visual C++ and GCC
###########################################

modsimple.win: modsimple_if.cppm modsimple_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	../clmod.py $(CXXFLAGSWINL) modsimple_if.cppm modsimple_test.cpp $(LDFLAGSWIN) /Femodsimple.exe
	#rm -f *.obj *.ifc
	@echo "- OK:  modsimple.exe done"

modsimple.gcc: modsimple_if.cppm modsimple_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	$(CXX20) $(CXXFLAGS20) -xc++ modsimple_if.cppm modsimple_test.cpp $(LDFLAGS20) -o modsimple.exe
	#rm -rf *.o gcm.cache
	@echo "- OK:  modsimple.exe done"

