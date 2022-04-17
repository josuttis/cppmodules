#! /usr/bin/env python
#
# Python script to let Visual C++ deal with C++ source code using mdules
# - supporting arbitrary file suffixes
# - without the need to use undocumented options
# - passing all files one one command line

import sys
import os
import re
import subprocess

debug = False

def getModulesOpt(filename):
  #print("\n=== getModulesOpt() for", filename)
  if not os.path.isfile(filename):
      print ("ERROR: '" + filename + "' doesn't exist")
      sys.exit(1)
  inGlobalModuleFragment = False
  with open(filename, encoding='latin1') as f:
    for rawline in f:
      line = rawline.strip()
      # ignore comment
      # TODO: deal with /* ... */
      idx = line.find("//")
      if idx >= 0:
        line = line[:idx]
      if line == "":
        continue
      
      if line.startswith("module;"):
        inGlobalModuleFragment = True
        continue
      if inGlobalModuleFragment and line.startswith("#"):
        continue

      if not line.startswith("module") and \
         not line.startswith("export module"):
          # traditional translation unit => no special options
        if debug:
          print(" >", rawline)
          print("  ", filename, "is no module unit")
        return ""
      
      # preprocessor in global module fragment ignored:

      # module unit: check its type:
      m = re.search("export module ([a-zA-Z0-9]*):([a-zA-Z0-9]*)", line)
      if m:
        # interface partition:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is interface partition '" + m.group(2) + 
                                "' in module '" + m.group(1) + "'")
        return "/interface"
      m = re.search("export module ([a-zA-Z0-9]*)", line)
      if m:
        # module interface:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is interface of module '" + m.group(1) + "'")
        return "/interface"
      m = re.search("module ([a-zA-Z0-9]*):([a-zA-Z0-9]*)", line)
      if m:
        # internal partition:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is internal partition '" + m.group(2) + 
                                "' in module '" + m.group(1) + "'")
        return "/internalPartition"
      m = re.search("module ([a-zA-Z0-9]*)", line)
      if m:
        # implementation unit:
        if debug:
          print(" >", rawline)
          print("  ", filename, "is implementation unit of module '" + m.group(1) + "'")
        return ""
  # could not decide:
  print("ERROR: could not categorize", filename)
  sys.exit(1)


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
for f in files:
  print("\n*** COMPILE: '" + f + "'")
  m = re.search("^(.*)\.([^.]*)$", f)
  if not m:
    print("ERROR: file", filename, "has no suffix")
    sys.exit(1)
  fileopt = getModulesOpt(f)
  # compile code:
  print("    cl ", " ".join(flags), "/TP", "/c", fileopt, f)
  if not fileopt or fileopt == "":
    p = subprocess.Popen(["cl"] + flags + ["/TP", "/c", f])
  else:
    p = subprocess.Popen(["cl"] + flags + ["/TP", "/c", fileopt, f])
  p.wait()
  objfiles.append(m.group(1) + ".obj")

# link generated object files
if not compileOnly:
  print("\n*** LINK:")
  print("    cl ", " ".join(flags), " ".join(objfiles))
  p = subprocess.Popen(["cl"] + flags + objfiles)
  p.wait()


