import random
import sys
from typing import Optional
import argparse

from item_data import Items
from location_data import pullCSV
import logicCasual
import logicExpert
import logicExpertArea
import fillSpeedrun
import fillMedium
import fillMajorMinor
import areaRando
from romWriter import RomWriter


def commandLineArgs(sys_args) :
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--casual', action="store_true", help='Casual logic, easy setting matching the vanilla Subversion experience, Default')
    parser.add_argument('-e', '--expert', action="store_true", help='Expert logic, hard setting comparable to Varia.run Expert difficulty')
    parser.add_argument('-s', '--speedrun', action="store_true", help='Speedrun fill, fast setting comparable to Varia.run Speedrun fill algorithm, Default')
    parser.add_argument('-m', '--medium', action="store_true", help='Medium fill, medium speed setting that places low-power items first for increased exploration')
    parser.add_argument('-mm', '--majorminor',  action="store_true", help='Major-Minor fill, using unique majors and locations')
    parser.add_argument('-a', '--area',  action="store_true", help='Area rando shuffles major areas of the game, expert logic only')
    args = parser.parse_args(sys_args)
    # print(args)
    return args


def plmidFromHiddenness(itemArray, hiddenness):
    if hiddenness == "open":
        plmid = itemArray[1]
    elif hiddenness == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    return plmid

def itemPlace(romWriter, location, itemArray) :
    #provide a locRow as in and the item array such as Missile, Super, etc
    # write all rom locations associated with the item location
    plmid = plmidFromHiddenness(itemArray, location['hiddenness'])
    for address in location['locids']:
        romWriter.writeItem(address, plmid, itemArray[4])
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(itemArray, location['alternateroomdifferenthiddenness'])
        romWriter.writeItem(address, plmid_altroom, itemArray[4])


# main program
def Main(argv, romWriter: Optional[RomWriter] = None) -> None:
    workingArgs=commandLineArgs(argv[1:])
    if workingArgs.expert :
        logicChoice = "E"
    elif workingArgs.area :
        logicChoice = "AR" #EXPERT area rando
    else :
        logicChoice = "C"  # Default to casual logic
    if workingArgs.medium :
        fillChoice = "M"
    elif workingArgs.majorminor :
        fillChoice = "MM"
    elif workingArgs.area :
        fillChoice = "EA" #EXPERT area rando 
    else :
        fillChoice = "S"
    # hudFlicker=""
    # while hudFlicker != "Y" and hudFlicker != "N" :
    #     hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #     hudFlicker = hudFlicker.title()
    seeeed = random.randint(1000000,9999999)
    random.seed(seeeed)
    rom1_path = "roms/Sub"+logicChoice+fillChoice+str(seeeed)+".sfc"
    rom_clean_path = "roms/Subversion12.sfc"
    #you must include Subversion 1.2 in your roms folder with this name^
    spoiler_file = open("spoilers/Sub"+logicChoice+fillChoice+str(seeeed)+".sfc.spoiler.txt", "w")

    csvdict = pullCSV()
    locArray = [csvdict[key] for key in csvdict]
    # Item = Name, Visible, Chozo, Hidden, AmmoQty

    if romWriter is None:
        romWriter = RomWriter.fromFilePaths(origRomPath=rom_clean_path, newRomPath=rom1_path)
    else:
        romWriter.setBaseFilename(rom1_path[:-4].split("/")[-1]) # remove .sfc extension and dirs
    spacePortLocs=["Ready Room",
               "Torpedo Bay",
               "Extract Storage",
               "Gantry",
               "Docking Port 4",
               "Docking Port 3",
               "Weapon Locker",
               "Aft Battery",
               "Forward Battery"]
    
    seedComplete = False
    randomizeAttempts = 0
    while seedComplete == False:
        if fillChoice == "EA" : #area rando no logic
            Connections=areaRando.RandomizeAreas(romWriter) 
            #print(Connections) #test    
        randomizeAttempts += 1
        if randomizeAttempts > 1000 :
            print("Giving up after 1000 attempts. Help?")
            break
        print("Starting randomization attempt:",randomizeAttempts)
        spoilerSave = ""
        spoilerSave += "Starting randomization attempt:"+str(randomizeAttempts)+"\n"
        #now start randomizing
        unusedLocations=[]
        unusedLocations.extend(locArray)
        availableLocations=[]
        visitedLocations=[]
        loadout=[]
        #use appropriate fill algorithm for initializing item lists
        if fillChoice == "M" :
            itemLists=fillMedium.initItemLists()
        elif fillChoice == "MM" :
            itemLists=fillMajorMinor.initItemLists()
        elif fillChoice == "EA" : #area rando uses medium fill
            itemLists=fillMedium.initItemLists()
        else :
            itemLists=fillSpeedrun.initItemLists()
        while len(unusedLocations) != 0 or len(availableLocations) != 0:
            # print("loadout contains:")
            # print(loadout)
            # for a in loadout:
            #     print("-",a[0])

            # update logic by updating unusedLocations
            # using helper function, modular for more logic options later
            # unusedLocations[i]['inlogic'] holds the True or False for logic
            if logicChoice == "E":
                logicExpert.updateLogic(unusedLocations, locArray, loadout)
            elif logicChoice == "AR":
                loadout = areaRando.updateAreaLogic(availableLocations, locArray, loadout, Connections)
                logicExpertArea.updateLogic(unusedLocations, locArray, loadout)
            else:
                logicCasual.updateLogic(unusedLocations, locArray, loadout)

            # update unusedLocations and availableLocations
            for i in reversed(range(len(unusedLocations))):  # iterate in reverse so we can remove freely
                if unusedLocations[i]['inlogic'] is True:
                    # print("Found available location at",unusedLocations[i]['fullitemname'])
                    availableLocations.append(unusedLocations[i])
                    unusedLocations.pop(i)
            # print("Available locations sits at:",len(availableLocations))
            # for al in availableLocations :
            #     print(al[0])
            # print("Unused locations sits at size:",len(unusedLocations))
            # print("unusedLocations:")
            # for u in unusedLocations :
            #     print(u['fullitemname'])

            if availableLocations == [] and unusedLocations != [] :
                print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
                spoilerSave+=f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
                break

            # split here for different fill algorithms
            if fillChoice == "M":
                placePair=fillMedium.placementAlg(availableLocations, locArray, loadout, itemLists)
            elif fillChoice == "MM":
                placePair=fillMajorMinor.placementAlg(availableLocations, locArray, loadout, itemLists)
            elif fillChoice == "EA":  # area rando
                placePair=fillMedium.placementAlg(availableLocations, locArray, loadout, itemLists)
            else :
                placePair=fillSpeedrun.placementAlg(availableLocations, locArray, loadout, itemLists)
            # it returns your location and item, which are handled here
            placeLocation=placePair[0]
            placeItem=placePair[1]
            if (placeLocation in unusedLocations) :
                unusedLocations.remove(placeLocation)
            if placeLocation == "Fail" :
                print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
                spoilerSave+=f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
                break
            itemPlace(romWriter, placeLocation, placeItem)
            availableLocations.remove(placeLocation)
            for itemPowerGrouping in itemLists :
                if placeItem in itemPowerGrouping :
                    itemPowerGrouping.remove(placeItem)
                    break
            loadout.append(placeItem)
            if ((placeLocation['fullitemname'] in spacePortLocs) == False) and ((Items.spaceDrop in loadout) == False):
                loadout.append(Items.spaceDrop)
            spoilerSave+=placeLocation['fullitemname']+" - - - "+placeItem[0]+"\n"
            #print(placeLocation['fullitemname']+placeItem[0])

            if availableLocations == [] and unusedLocations == [] :
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
                seedComplete = True
                break
            
    #add area transitions to spoiler
    if fillChoice == "EA" :
        for item in Connections :
            spoilerSave+=item[0][2]+" "+item[0][3]+" << >> "+item[1][2]+" "+item[1][3]+"\n"

    # Suit animation skip patch
    romWriter.writeBytes(0x20717, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    #if hudFlicker == "Y" :
        #writeBytes(0x547a, b"\x02")
        #writeBytes(0x547f, b"\x00")
        #uu=0
    # Morph Ball PLM patch (chozo, hidden)
    romWriter.writeBytes(0x268ce, b"\x04")
    romWriter.writeBytes(0x26e02, b"\x04")
    # skip intro (asm edits) TODO turn this into asm and a proper hook
    romWriter.writeBytes(0x16eda, b"\x1f") # initial game state set by $82:eeda
    romWriter.writeBytes(0x16ee0, b"\x06\x00") # initial game area = 6 (ceres)
    romWriter.writeBytes(0x16ee3, b"\x9f\x07") # $079f Area index
    romWriter.writeBytes(0x16ee5, b"\xa9\x05\x00\x8f\x14\xd9\x7e\xea\xea") # $7e:d914 = 05 Main
    romWriter.writeBytes(0x16eee, b"\xad\x52\x09\x22\x00\x80\x81") # jsl save game (param in A: save slot)
    romWriter.writeBytes(0x16ed0, b"\x24") # adjust earlier branch to go +6 bytes later to rts
    romWriter.writeBytes(0x16ed8, b"\x1c") # adjust earlier branch to go +6 bytes later to rts
    # disable demos (asm opcode edit). because the demos show items
    romWriter.writeBytes(0x59f29, b"\xad")
    # make always flashing doors out of vanilla gray 'animals saved' doors:
    #   edit in function $84:BE30 'gray door pre: go to link instruction if critters escaped', which is vanilla and probably not used anyway
    #   use by writing 0x18 to the high byte of a gray door plm param, OR'ed with the low bit of the 9-low-bits id part
    romWriter.writeBytes(0x23e33, b"\x38\x38\x38\x38") # set the carry bit (a lot)
    romWriter.finalizeRom()
    print("Done!")
    print("Filename is "+"Sub"+logicChoice+fillChoice+str(seeeed)+".sfc")
    spoiler_file.write("RNG Seed: {}\n".format(str(seeeed))+"\n")
    spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
    spoiler_file.write(spoilerSave)    
    print("Spoiler file is "+"Sub"+logicChoice+fillChoice+str(seeeed)+".sfc.spoiler.txt")


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")

