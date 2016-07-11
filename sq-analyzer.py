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
   if len(arguments[0]) != 7: # Commit checksum length
      return False
   if legalDate(arguments[2]) == False:
      return False

   return True

def legalDate(date):
   date = date.split("-")
   if len(date) != 3:
      return False
   for index in range(len(date)):
      if date[index].isdigit() == False:
         return False
      if index == 0 and len(date[index]) != 4:
         return False
      elif index != 0 and len(date[index]) != 2:
         return False

   return True

def checkout(commit, testRun):
   printCmd("git checkout " + commit)
   if(testRun == False):
      process = subprocess.run(["git", "checkout", commit],
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
      if "error:" in process.stderr:
         shutDown()

def runSQ(version, date, scannerPath, testRun):
   projectVersion = str("sonar.projectVersion=" + version)
   projectDate = str("sonar.projectDate=" + date)
   printCmd(scannerPath + " -D " + projectVersion + " -D " + projectDate)
   if(testRun == False):
      process = subprocess.run([scannerPath,
                               "-D",
                               projectVersion,
                               "-D",
                               projectDate],
                               universal_newlines=True)

def skipLine(arguments):
   print("There is a problem with commit info file at line " + str(arguments))
   print("Skipping line.")

def printCmd(cmd):
   print("Running subprocess command: " + cmd)

#-------------------------------------------------------------------------------
# Main program starts
#-------------------------------------------------------------------------------

print("sq-analyzer v0.1\n")

# Check the parameters given to program are legal
test = False
if len(sys.argv) == 4 and sys.argv[3] == "test":
   test = True
elif len(sys.argv) < 3 or len(sys.argv) > 4:
   print("Please specify the commit info file and sonar scanner path as a parameters for program.")
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

      checkout(commit, test)
      runSQ(version, date, sys.argv[2], test)
   else:
      skipLine(arguments)

f.close()
