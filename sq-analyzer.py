import sys
import subprocess

def openFile(fileName):
   try:
      return open(fileName, "r")
   except FileNotFoundError:
      return False

def legalArguments(arguments):
   return len(arguments) == 3

def checkout(commit):
   process = subprocess.run(["git", "checkout", commit], stderr=subprocess.PIPE)
   gitOutput = str(process.stderr).split()
   print(gitOutput)
   if "b\"error:" in gitOutput:
      print("oli error")
   #if process.stderr != None:
      #print("Error while trying to checkout a commit: " + commit)
      #exit()

def runSQanalysis(version, date):
   pass

#-------------------------------------------------------------------------------
# Main program starts
#-------------------------------------------------------------------------------

print("sq-analyzer v0.1")

# Check the parameters given to program are legal
if len(sys.argv) != 2:
   print("Invalid parameters!")
   exit()

f = openFile(sys.argv[1])
if f == False:
   print("File '" + sys.argv[1] + "' was not found.")
   exit()

for line in f:
   arguments = line.split()
   if legalArguments(arguments):
      commit = arguments[0]
      version = arguments[1]
      date = arguments[2]

      checkout(commit)
      runSQanalysis(version, date)

f.close()
