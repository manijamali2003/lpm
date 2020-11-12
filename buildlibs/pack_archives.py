#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import shutil, os, sys,glob, platform,py_compile, subprocess
from buildlibs import control

def compile (src,dest):
    subprocess.call ([sys.executable,'-m','nuitka','--remove-output',src,'-o',dest])
    subprocess.call (['chmod','-x',dest])

## Build ##
def build(name):
    if not ("packs/"+name + "/code") and ("packs/"+name + "/data") and (
            "packs/"+name + "/control") and ("packs/"+name + "/control/manifest"):
        exit(0)

    shutil.make_archive("var/cache/lpm/archives/build/data", "zip",    "packs/"+name + "/data")
    shutil.make_archive("var/cache/lpm/archives/build/code", "zip",    "packs/"+name + "/code")
    shutil.make_archive("var/cache/lpm/archives/build/control", "zip", "packs/"+ name + "/control")

    shutil.make_archive(name, "zip", "var/cache/lpm/archives/build")
    os.rename (name+".zip","build-packs/"+name+".la")
    clean()

## Clean the cache ##
def clean():
    shutil.rmtree("var/cache/lpm")
    os.mkdir("var/cache/lpm")
    os.mkdir("var/cache/lpm/gets")
    os.mkdir("var/cache/lpm/archives")
    os.mkdir("var/cache/lpm/archives/code")
    os.mkdir("var/cache/lpm/archives/control")
    os.mkdir("var/cache/lpm/archives/data")
    os.mkdir("var/cache/lpm/archives/build")

## Unpack .la archives ##

def unpack (name):
    shutil.unpack_archive("build-packs/"+name+".la","var/cache/lpm/archives/build","zip")
    shutil.unpack_archive("var/cache/lpm/archives/build/data.zip","var/cache/lpm/archives/data","zip")
    shutil.unpack_archive("var/cache/lpm/archives/build/code.zip","var/cache/lpm/archives/code", "zip")
    shutil.unpack_archive("var/cache/lpm/archives/build/control.zip","var/cache/lpm/archives/control", "zip")

    ## Unpack database only ##

    name = control.read_record ("name","var/cache/lpm/archives/control/manifest")
    unpack = control.read_record ("unpack","var/cache/lpm/archives/control/manifest")

    ## Setting up ##

    if os.path.isfile ("var/cache/lpm/archives/control/manifest"): shutil.copyfile("var/cache/lpm/archives/control/manifest","stor/etc/lpm/packages/"+name+".manifest")
    if os.path.isfile("var/cache/lpm/archives/control/list"): shutil.copyfile("var/cache/lpm/archives/control/list","stor/etc/lpm/packages/" + name + ".list")
    if os.path.isfile("var/cache/lpm/archives/control/compile"): shutil.copyfile("var/cache/lpm/archives/control/compile","stor/etc/lpm/packages/" + name + ".compile")

    ## Compile codes ##
    if os.path.isfile ("var/cache/lpm/archives/control/compile"):
        listcodes = control.read_list("var/cache/lpm/archives/control/compile")
        for i in listcodes:
            i = i.split(":")

            compile('var/cache/lpm/archives/code/'+i[0], 'var/cache/lpm/archives/data/'+i[1])


    ## Archive data again ##
    shutil.make_archive("var/cache/lpm/archives/build/data","zip","var/cache/lpm/archives/data")

    ## Unpack data again ##
    shutil.unpack_archive("var/cache/lpm/archives/build/data.zip","stor/"+unpack,"zip")

    ## Save source code ##
    shutil.unpack_archive('var/cache/lpm/archives/build/code.zip','stor/usr/src/'+name,'zip')
    clean()

def install ():
    list = os.listdir('packs')
    for i in list:
        if os.path.isdir('packs/'+i):
            build(i)
            unpack(i)

def inst (pack):
    build(pack)
    unpack(pack)

def learniaa_env ():
    os.makedirs('stor/etc/lpm/packages')
    os.makedirs('stor/etc/lpm/mirrors')
    os.makedirs('stor/var/cache/archives/build')
    os.makedirs('stor/var/cache/archives/data')
    os.makedirs('stor/var/cache/archives/code')
    os.makedirs('stor/var/cache/archives/control')
    os.makedirs('stor/var/cache/gets')
    os.makedirs('stor/var/cache/backups')
