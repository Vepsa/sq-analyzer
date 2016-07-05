import sys
import subprocess

def shutDown():
   print("Program shutting down")
   exit()

def openFile(fileName):
   try:
      return open(fileName, "r")
   except FileNotFoundError:
      return False

def legalArguments(arguments):
   if len(arguments) != 3:
      return False
   if len(arguments[0]) != 7: # Length of the commit checksum short version
      return False
   if legalDate(arguments[2]) == False:
      return False

   return True

def legalDate(date):
   date = date.split("-")
   if len(date) != 3:
      return False
   if len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
      return False

   return True

def checkout(commit):
   process = subprocess.run(["git", "checkout", commit], stderr=subprocess.PIPE,
                            universal_newlines=True)
   print((" ").join(process.args)) # Prints executed command
   print(process.stderr)

   if "error:" in process.stderr:
      shutDown()

def runSQanalysis(version, date):
   pass

def skipLine(arguments):
   print("There is a problem with commit info file at line " + str(arguments))
   print("Skipping line.")

#-------------------------------------------------------------------------------
# Main program starts
#-------------------------------------------------------------------------------

print("sq-analyzer v0.1\n")

# Check the parameters given to program are legal
if len(sys.argv) != 2:
   print("Please specify the commit info file as a parameter for program.")
   shutDown()

f = openFile(sys.argv[1])
if f == False:
   print("File '" + sys.argv[1] + "' was not found.")
   shutDown()

for line in f:
   arguments = line.split()
   if legalArguments(arguments):
      commit = arguments[0]
      version = arguments[1]
      date = arguments[2]

      checkout(commit)
      runSQanalysis(version, date)
   else:
      skipLine(arguments)

f.close()
