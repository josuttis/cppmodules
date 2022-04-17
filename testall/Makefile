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

mod3.win: mod3part.cppm mod3ifpart.cppm mod3if.cppm mod3impl.cpp mod3test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	clm.py $(CXXFLAGSWINL) mod3part.cppm mod3ifpart.cppm mod3if.cppm mod3impl.cpp mod3test.cpp $(LDFLAGSWIN) /Femod3.exe
	#rm -f mod3*obj mod3*ifc mod3*cpp*
	@echo "- OK:  $*.exe done"

mod3.gcc: mod3part.cppm mod3ifpart.cppm mod3if.cppm mod3impl.cpp mod3test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	$(CXX20) clm.py $(CXXFLAGS20) -xc++ mod3part.cppm -xc++ mod3ifpart.cppm -xc++ mod3if.cppm mod3impl.cpp mod3test.cpp $(LDFLAGS20) -o mod3.exe
	#rm -f mod3*obj mod3*ifc mod3*cpp*
	@echo "- OK:  $*.exe done"

