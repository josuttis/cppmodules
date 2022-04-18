#! /usr/bin/env python
##############################################################################
# Python script to let Visual C++ deal with C++ source code using modules
# - supporting arbitrary file suffixes
# - without the need to use undocumented options
# - passing all files one one command line
#
# Can also be used as skeleton for other tools to handle C++ units differently.
# 
# Special handling:
#   Pass "-debug" to have verbose output 
##############################################################################

import sys
import os
import re
import subprocess

##############################################################################
# global flags
##############################################################################

debug = False  # may be turned on with -debug


##############################################################################
# getModulesType()
# - parses the give file to find out its unit type:
# - returns:
#    "tu"   for traditional translation unit
#    "ifm"  for primary module interface unit
#    "ifp"  for interface partition unit
#    "int"  for internal partition unit
#    "impl" for module im0plementation unit
##############################################################################
def getModulesType(filename):
  #print("\n=== getModulesOpt() for", filename)
  if not os.path.isfile(filename):
      print ("*** ERROR: '" + filename + "' doesn't exist")
      sys.exit(1)
  inGlobalModuleFragment = False
  with open(filename, 'r') as f:
    for rawline in f:
      line = rawline.strip()
      # ignore comment
      # TODO: deal with /* ... */
      idx = line.find("//")
      if idx >= 0:
        line = line[:idx]
      # ignore empty line:
      if line == "":
        continue
      
      if line.startswith("module;"):
        inGlobalModuleFragment = True
        continue
      # preprocessor commands in global module fragment ignored:
      if inGlobalModuleFragment and line.startswith("#"):
        continue

      if not line.startswith("module") and \
         not line.startswith("export module"):
          # traditional translation unit => no special options
        if debug:
          print(" >", rawline)
          print("  ", filename, "is no module unit")
        return "tu"  # RETURN "traditional translation unit"

      # module unit: check its type:
      m = re.search("export module ([a-zA-Z0-9]*):([a-zA-Z0-9]*)", line)
      if m:
        # interface partition:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is interface partition '" + m.group(2) + 
                                "' in module '" + m.group(1) + "'")
        return "ifp"  # RETURN "interface partition"

      m = re.search("export module ([a-zA-Z0-9]*)", line)
      if m:
        # primary module interface:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is interface of module '" + m.group(1) + "'")
        return "ifm"  # RETURN "primary module interface"

      m = re.search("module ([a-zA-Z0-9]*):([a-zA-Z0-9]*)", line)
      if m:
        # internal partition:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is internal partition '" + m.group(2) + 
                                "' in module '" + m.group(1) + "'")
        return "int"  # RETURN "internal partition"

      m = re.search("module ([a-zA-Z0-9]*)", line)
      if m:
        # implementation unit:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is implementation unit of module '" + m.group(1) + "'")
        return "impl"  # RETURN "implementation unit

  # could not decide:
  print("*** ERROR: could not categorize", filename)
  sys.exit(1)


##############################################################################
# getModulesOpt()
# - return the command line options Visual C++ need for the passed unit
##############################################################################
def getModulesOpt(filename):
  type = getModulesType(filename)
  if type == "int":
    return "/internalPartition"
  if type == "ifm":
    return "/interface"
  if type == "ifp":
    return "/interface"
  if type == "impl":
    return ""
  if type == "tu":
    return ""
  # could not decide:
  print("*** ERROR: invalid unit type: ", type, "for", filename)
  sys.exit(1)


##############################################################################
# run()
# - runs a systemn command with the passed args
##############################################################################
def run(args):
  # since Python 3.4 we can use run() but let's support older Python versions:
  # if sys.version_info[0] > 3 or \
  #    (sys.version_info[0] > 2 and sys.version_info[1] > 4):
  #        p = subprocess.run(args)
  p = subprocess.Popen(args)
  p.wait()
  return p;


##############################################################################
# MAIN
##############################################################################

# parse all command-line options
# - separationg files (having a dot inside)
# - from compiler/linker options (the rest)
files = []
flags = []
compileOnly = False
for opt in sys.argv[1:]:
  #print(opt)
  if (opt == "-debug"):
    debug = True
    continue
  if (opt == "/c"):
    compileOnly = False
    continue
  if opt.startswith("/"):
    flags.append(opt)
    continue
  if "." in opt:
    files.append(opt)
  else:
    flags.append(opt)

#print("files: ", files)
#print("flags: ", flags)

# iterate over all files
# - checking the unit type
#   - traditional non-module translation unit or
#   - one of the module unit types
# - compile each file accordingly
print("COMPILE:")
objfiles = []
for filename in files:
  print("\n*** COMPILE '" + filename + "'")
  m = re.search("^(.*)\.([^.]*)$", filename)
  if not m:
    print("*** ERROR: file", filename, "has no suffix")
    sys.exit(1)
  fileopt = getModulesOpt(filename)
  # compile code:
  print("*** cl ", " ".join(flags), "/TP", "/c", fileopt, filename)
  if not fileopt or fileopt == "":
    p = run(["cl"] + flags + ["/TP", "/c", filename])
  else:
    p = run(["cl"] + flags + ["/TP", "/c", fileopt, filename])
  if p.returncode != 0:
    print("*** ERROR: compiling", filename, "failed")
    sys.exit(1)
  objfiles.append(m.group(1) + ".obj")

# link generated object files
if not compileOnly:
  print("\n*** LINK:")
  print("*** cl ", " ".join(flags), " ".join(objfiles))
  p = run(["cl"] + flags + objfiles)
  if p.returncode != 0:
    print("*** ERROR: linking failed")
    sys.exit(1)

