include ../Makefile.h
	
all:: lang

###########################################
#
###########################################

#IFCDIRFLAGS=/ifcOutput bin/ /ifcSearchDir bin/ 
.SUFFIXES: .cppm .obj .ixx
.cppm.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /TP /c /interface $*.cppm $(IFCDIRFLAGS)
	rm $*.cppm
	@echo "=== $*.obj done"
	@echo ""
.cppp.obj:
	@echo ""
	cl $(CXXFLAGSWINL) /TP /c /internalPartition $*.cppp $(IFCDIRFLAGS)
	rm $*.cppp
	@echo "=== $*.obj done"
	@echo ""
.cpp.obj:
	@echo ""
	sed -f $(TTT2CPP) < $*.cxx > $*.cpp
	cl $(CXXFLAGSWINL) /c $*.cpp $(IFCDIRFLAGS)
	rm $*.cpp
	@echo "=== $*.obj done"
	@echo ""

modsimple.win: modsimple_if.cppm modsimple_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	../clmod.py $(CXXFLAGSWINL) modsimple_if.cppm modsimple_test.cpp $(LDFLAGSWIN) /Femodsimple.exe
	rm -f *.obj *.ifc
	@echo "- OK:  modsimple.exe done"

modsimple.gcc: modsimple_if.cppm modsimple_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	$(CXX20) $(CXXFLAGS20) -xc++ modsimple_if.cppm modsimple_test.cpp $(LDFLAGS20) -o modsimple.exe
	rm -rf *.o gcm.cache
	@echo "- OK:  modsimple.exe done"

