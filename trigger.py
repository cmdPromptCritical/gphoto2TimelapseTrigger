from time import sleep
from datetime import datetime
from sh import gphoto2 as gp    # uses gphoto2 program as a module
import signal, os, subprocess

sleep(15)
# kill gphoto2 process that starts whenever we connect the camera
def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the line that has what we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            print("Die!")
            # die!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)


shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "PIDSLR"
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files", "--force-overwrite", "--skip-existing"]
clearCommand = ["--folder=/store_00010001/DCIM/100NCD80", \
                "-R", "--delete-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Pictures/autotrigger"

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory. It may already exist.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    print("Bang!")
    sleep(33) # sleeps to allow for the image to be saved to memory
    # note that this sleep thing should be a function of shutter speed.
    # using sample sutter speeds and save times this section of the program
    # could be greatly optimized.
    #gp(downloadCommand)
    #sleep(4)
    #gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 14:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
            elif filename.endswith(".NEF"):
                os.rename(filename, (shot_time + ID + ".NEF"))
                print("Renamed a .NEF file")

killgphoto2Process()
#createSaveFolder()
while True:
    captureImages()
#renameFiles(picID)
