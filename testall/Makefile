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

modall.win: modall_part.cppm modall_ifpart.cppm modall_if.cppm modall_impl.cpp modall_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	../clm.py -debug $(CXXFLAGSWINL) modall_part.cppm modall_ifpart.cppm modall_if.cppm modall_impl.cpp modall_test.cpp $(LDFLAGSWIN) /Femodall.exe
	#rm -f modall*obj modall*ifc
	@echo "- OK:  $*.exe done"

modall.gcc: modall_part.cppm modall_ifpart.cppm modall_if.cppm modall_impl.cpp modall_test.cpp
	@echo ""
	@echo "=== COMPILE & LINK:"
	$(CXX20) $(CXXFLAGS20) -xc++ modall_part.cppm -xc++ modall_ifpart.cppm -xc++ modall_if.cppm modall_impl.cpp modall_test.cpp $(LDFLAGS20) -o modall.exe
	#rm -f modall*o gcm-cache/modall*gcm
	@echo "- OK:  $*.exe done"

