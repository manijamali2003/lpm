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

from buildlibs import pack_archives as pack
from buildlibs import control
import shutil, os, sys, hashlib,getpass,platform

import shutil, os

## pre build ##
if os.path.isdir ("stor"): shutil.rmtree("stor")

if not os.path.isdir ("var"):
	os.mkdir ("var")
	os.mkdir('var/cache')
	os.mkdir ("var/cache/lpm")
	os.mkdir ("var/cache/lpm/archives")
	os.mkdir ("var/cache/lpm/archives/data")
	os.mkdir ("var/cache/lpm/archives/control")
	os.mkdir ("var/cache/lpm/archives/code")
	os.mkdir ("var/cache/lpm/archives/build")
	os.mkdir ("var/cache/lpm/gets")

if not os.path.isdir ("stor"):
	os.mkdir ("stor")
	os.mkdir ("stor/var")
	os.makedirs ("stor/etc/lpm/packages")

if not os.path.isdir ("build-packs"): os.mkdir ("build-packs")

pack.inst('lpm')
pack.build('hi')
#pack.learniaa_env()

shutil.make_archive('stor','zip','stor')
shutil.unpack_archive('stor.zip','/','zip')
os.remove('stor.zip')