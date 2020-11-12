'''
    In the name of God, the Compassionate, the Merciful
    Learniaa Educational Company All rights reserved.

    LPM Package Manager based on libabr/paye
'''

import platform, getpass, sys, os, shutil,subprocess

from termcolor import colored

def read_record (name,filename):
    file = open (filename,"r")
    strv = file.read()
    file.close()
    strv = strv.split("\n")

    for i in strv:
        if i.startswith(name):
            i = i.split(": ")
            if i[0]==(name):
                return i[1]

def read_list (filename):
    file = open (filename,"r")
    strv = file.read()
    file.close()
    strv = strv.split("\n")
    return strv

def write_record(name, value, filename):
    file = open (filename,'r')
    all = file.read()
    file.close()
    record = read_record(name, filename)
    os.remove(filename)
    if not (record == None):
        all = all.replace("\n"+name + ": " + record, "")
    file = open(filename,'w')
    file.write(all + "\n" + name + ": " + value)
    file.close()

# package #
class Package:
    ## Clean the cache ##
    def clean (self):

        if getpass.getuser()=='root':
            if os.path.isdir("/var/cache/lpm"):
                shutil.rmtree("/var/cache/lpm")
                os.mkdir("/var/cache/lpm")
                os.mkdir("/var/cache/lpm/gets")
                os.mkdir("/var/cache/lpm/archives")
                os.mkdir("/var/cache/lpm/archives/code")
                os.mkdir("/var/cache/lpm/archives/control")
                os.mkdir("/var/cache/lpm/archives/data")
                os.mkdir("/var/cache/lpm/archives/build")
        else:
            print (colored ("lpm: error: Permission denied","red"))
            

    ## Create .la archive ##

    def build(self,name):
        
        
        

        if getpass.getuser()=='root':
            if not os.path.isfile(name + "/control/manifest"):
                print (colored ("lpm: error: cannot create archive package","red"))
                self.clean()
                sys.exit(0)

            if not os.path.isdir(name + "/data"): os.mkdir(name + "/data")
            if not os.path.isdir(name + "/code"): os.mkdir(name + "/code")

            ## Remove cache archives ##
            if os.path.isdir('/var/cache/lpm/archives/control'): shutil.rmtree('/var/cache/lpm/archives/control')
            if os.path.isdir('/var/cache/lpm/archives/data'): shutil.rmtree('/var/cache/lpm/archives/data')
            if os.path.isdir('/var/cache/lpm/archives/code'): shutil.rmtree('/var/cache/lpm/archives/code')

            ## Copy dir ##
            shutil.copytree(name + '/data', '/var/cache/lpm/archives/data')
            shutil.copytree(name + '/control', '/var/cache/lpm/archives/control')
            shutil.copytree(name + '/code', '/var/cache/lpm/archives/code')

            ## Pack archives ##
            shutil.make_archive("/var/cache/lpm/archives/build/data", "zip",
                                '/var/cache/lpm/archives/data')
            shutil.make_archive("/var/cache/lpm/archives/build/control", "zip",
                                '/var/cache/lpm/archives/control')
            shutil.make_archive("/var/cache/lpm/archives/build/code", "zip",
                                '/var/cache/lpm/archives/code')
            shutil.make_archive(name, "zip", "/var/cache/lpm/archives/build")

            shutil.copyfile (name + ".zip", name + ".la")
            os.remove(name + ".zip")
            ## Unlock the cache ##
        else:
            print (colored ("lpm: error: Permission denied","red"))


    ## Unpack .la archives ##

    def unpack(self,name):
        

        if getpass.getuser()=='root':

            ## unpack package ##
            shutil.unpack_archive(name, "/var/cache/lpm/archives/build", "zip")

            shutil.unpack_archive("/var/cache/lpm/archives/build/data.zip",
                                  "/var/cache/lpm/archives/data", "zip")
            shutil.unpack_archive("/var/cache/lpm/archives/build/control.zip",
                                  "/var/cache/lpm/archives/control", "zip")
            shutil.unpack_archive("/var/cache/lpm/archives/build/code.zip",
                                  "/var/cache/lpm/archives/code", "zip")

            ## Get database of this package ##
            name = read_record("name", "/var/cache/lpm/archives/control/manifest").lower()
            unpack = read_record("unpack", "/var/cache/lpm/archives/control/manifest")
            depends = read_record("depends", "/var/cache/lpm/archives/control/manifest")

            if not (depends == None):
                depends.split(",")

            ## Search for tree dependency ##

            if not depends == None:
                for i in depends:
                    if not os.path.isfile("/etc/lpm/packages/" + i + ".manifest"):
                        os.system ('lpm in ' + name)

            ## Write dependency ##

            if not depends == None:
                for i in depends:
                    f = open ("/etc/lpm/packages/" + i + ".depends","w")
                    f.write(name + "\n")
                    f.close()

            ## Run preinstall script ##

            if os.path.isfile('/var/cache/lpm/archives/control/preinstall'):
                shutil.copyfile('/var/cache/lpm/archives/control/preinstall', '/usr/bin/preinstall')
                subprocess.call(['chmod', '-x', '/usr/bin/preinstall'])
                os.system('preinstall')  # Run it
                os.remove('/usr/bin/preinstall')

                ## Copy preinstall script ##

                shutil.copyfile('/var/cache/lpm/archives/control/preinstall', '/etc/lpm/packages/' + name + ".preinstall")

            ## Setting up ##

            if os.path.isfile("/var/cache/lpm/archives/control/list"): shutil.copyfile("/var/cache/lpm/archives/control/list","/etc/lpm/packages/" + name + ".list")
            if os.path.isfile("/var/cache/lpm/archives/control/manifest"): shutil.copyfile("/var/cache/lpm/archives/control/manifest","/etc/lpm/packages/" + name + ".manifest")
            if os.path.isfile("/var/cache/lpm/archives/control/compile"): shutil.copyfile("/var/cache/lpm/archives/control/compile","/etc/lpm/packages/" + name + ".compile")

            compilefiles = read_record('compile','/var/cache/lpm/archives/control/manifest')
            if compilefiles=='Yes':
                compiles = read_list('/var/cache/lpm/archives/control/compile')

                for i in compiles:
                    spl = i.split(":")

                    code = '/var/cache/lpm/archives/code/' + spl[0]
                    dest = "/var/cache/lpm/archives/data/" + spl[1]

                    subprocess.call([sys.executable, '-m', 'nuitka', '--remove-output', code, '-o', dest])
                    subprocess.call(['chmod', '-x', dest])

            ## Create data archive ##
            shutil.make_archive("/var/cache/lpm/archives/build/data", 'zip','/var/cache/lpm/archives/data')

            ## Unpack data again ##
            shutil.unpack_archive("/var/cache/lpm/archives/build/data.zip", (unpack), "zip")

            ## Save the source

            shutil.unpack_archive('/var/cache/lpm/archives/build/code.zip',('/usr/src/'+name),'zip')

            ## After install ##

            ## Run postinstall script ##

            if os.path.isfile('/var/cache/lpm/archives/control/postinstall'):
                shutil.copyfile('/var/cache/lpm/archives/control/postinstall', '/usr/bin/postinstall')
                subprocess.call(['chmod', '-x', '/usr/bin/postinstall'])
                os.system('postinstall')  # Run it
                os.remove('/usr/bin/postinstall')

                ## Copy preinstall script ##

                shutil.copyfile('/var/cache/lpm/archives/control/postinstall', '/etc/lpm/packages/' + name + ".postinstall")

            ## Copy other scripts ##
            if os.path.isfile('/var/cache/lpm/archives/control/preremove'):
                shutil.copyfile('/var/cache/lpm/archives/control/preremove', '/etc/lpm/packages/' + name + ".preremove")

            if os.path.isfile('/var/cache/lpm/archives/control/postremove'):
                shutil.copyfile('/var/cache/lpm/archives/control/postremove', '/etc/lpm/packages/' + name + ".postremove")


            ## Unlock the cache ##
        else:
            print (colored ("lpm: error: Permission denied","red"))

    ## Remove package ##
    def uninstall (self,name):
        
        
        
        
        name = name.lower()

        if getpass.getuser()=='root':

            location = "/etc/lpm/packages/" + name + ".manifest"

            if not os.path.isfile(location):
                print (colored (f"lpm: error: {name}: package not found","red"))
                self.clean()
                sys.exit(0)

            ## Database control ##

            list = "/etc/lpm/packages/" + name + ".list"
            compile = '/etc/lpm/packages/'+name+".compile"
            preinstall = "/etc/lpm/packages/" + name + ".preinstall"
            postinstall = "/etc/lpm/packages/" + name + ".postinstall"
            preremove = "/etc/lpm/packages/" + name + ".preremove"
            postremove = "/etc/lpm/packages/" + name + ".postremove"
            depends = "/etc/lpm/packages/" + name+ ".depends"

            ## Create preremove and postremove copies ##

            if os.path.isfile(preremove): shutil.copyfile(preremove, "/usr/bin/preremove")
            if os.path.isfile(postremove): shutil.copyfile(postremove, "/usr/bin/postremove")

            ## Run pre remove script ##

            if os.path.isfile ('/usr/bin/preremove'):
                subprocess.call(['chmod', '-x', '/usr/bin/preremove'])
                os.system("preremove")
                os.remove('/usr/bin/preremove')

            ## Remove depends ##

            if os.path.isfile(depends):
                depends = read_list(depends)
                for i in depends:
                    self.remove(i)

            ####################

            unpack = read_record("unpack", location)

            ## Unpacked removal ##
            filelist = read_list(list)

            for i in filelist:
                if os.path.isdir(unpack + "/" + i):
                    shutil.rmtree(unpack + "/" + i)
                elif os.path.isfile(unpack + "/" + i):
                    os.remove(unpack + "/" + i)

            ## Database removal ##

            if os.path.isfile(location): os.remove(location)
            if os.path.isfile(list): os.remove(list)
            if os.path.isfile(preinstall): os.remove(preinstall)
            if os.path.isfile(postinstall): os.remove(postinstall)
            if os.path.isfile(preremove): os.remove(preremove)
            if os.path.isfile(postremove): os.remove(postremove)
            if os.path.isfile(depends): os.remove(depends)
            if os.path.isfile(compile): os.remove(compile)

            ## Remove the source code ##

            if os.path.isdir ('/usr/src/'+name): shutil.rmtree('/usr/src/'+name)

            ## Run postremove script ##

            if os.path.isfile ('/usr/bin/postremove'):
                subprocess.call(['chmod', '-x', '/usr/bin/postremove'])
                os.system ("postremove")
                os.remove('/usr/bin/postremove')
        else:
            print (colored ("lpm: error: Permission denied","red"))

    ## Download package ##

    def download(self,packname):
        
        
        
        

        packname = packname.lower()

        if getpass.getuser()=='root':
            f = open ('/etc/lpm/mirrors' + packname,'r')
            mirror = f.read()
            f.close()

            ## Download the file ##
            url = mirror

            import requests
            r = requests.get(url, allow_redirects=True)

            ## Check permissions ##
            open('/var/cache/lpm/gets/' + packname + '.la', 'wb').write(r.content)
        else:
            print (colored ("lpm: error: Permission denied","red"))

    ## Create a mirro ##
    def add (self,mirror,name):

        if getpass.getuser()=='root':
            endsplit = mirror.replace('https://', '').replace('http://', '')
            endsplit = mirror.split('/')
            f = open ('/etc/lpm/mirrors/' + name.replace('.la',''),'w')
            f.write(mirror)
            f.close()
        else:
            print (colored ("lpm: error: Permission denied","red"))

    ## install from git source ##
    def gitinstall (self,name):
        if getpass.getuser()=='root':
            self.download(name.lower())

            ## unpack pyabr ##
            shutil.unpack_archive('/var/cache/lpm/gets/'+name.lower()+'.la', ('/tmp'), 'zip')

            self.build('/tmp/'+name+'-master/packs/'+name.lower())
            self.unpack('/tmp/'+name+'-master/packs/'+name.lower()+".la")
            shutil.rmtree('/tmp/'+name+"-master")
        else:
            print (colored ("lpm: error: Permission denied","red"))
    ##  remove a mirror ##
    def remove (self,name):
        if getpass.getuser()=='root':
            os.remove('/etc/lpm/mirrors' + name)
        else:
            print (colored ("lpm: error: Permission denied","red"))
            
pack = Package()
## Check root ##
if not getpass.getuser()=='root':
    print (colored ("lpm: error: Permission denied","red"))
    sys.exit(0)

## Check inputs ##
if sys.argv[1:]==[]:
    print (colored ("lpm: error: no inputs","red"))
    sys.exit(0)

option = sys.argv[1]

if option=="cl":
    pack.clean()

elif option=="pak":
    if os.path.isfile ("/var/cache/lpm/lock"):
        print (colored ('lpm: error: cache has already locked'))
        sys.exit(0)
    else:
        open ("/var/cache/lpm/lock",'w')

    if sys.argv[2:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    dir = sys.argv[2:]

    for i in dir:
        pack.build(i)

    pack.clean()


elif option=="upak":
    if os.path.isfile ("/var/cache/lpm/lock"):
        print (colored ('lpm: error: cache has already locked'))
        sys.exit(0)
    else:
        open ("/var/cache/lpm/lock",'w')

    if sys.argv[1:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    archive = sys.argv[2:]

    if not archive[1:]==[]:
        strv = ''
        for i in archive:
            strv+=','+i

    for i in archive:
        if os.path.isfile(i):
            print (colored(f'Unpacking \'{i}\' archive package ...','green'),end='')
            pack.unpack(i)
            print(colored('done','green'))
        else:
            print (colored (f'lpm: error: {i}: archive not found','red'))

    pack.clean()

elif option=="rm":
    if os.path.isfile ("/var/cache/lpm/lock"):
        print (colored ('lpm: error: cache has already locked'))
        sys.exit(0)
    else:
        open ("/var/cache/lpm/lock",'w')

    if sys.argv[2]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    package = sys.argv[2:]

    if not package[1:] == []:
        strv = ''
        for i in package:
            strv += ',' + i

    for i in package:
        print (colored(f"Uninstalling {i} package ... ",'green'),end='')
        pack.uninstall(i.lower())
        print(colored('done','green'))

    pack.clean()

elif option=="get":

    if sys.argv[2]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    package = sys.argv[2:]

    if not package[1:] == []:
        strv = ''
        for i in package:
            strv += ',' + i
    for i in package:
        print (colored(f'Downloading {i} archive package ... ','green'),end='')
        pack.download (i.lower())
        print(colored('done','green'))

elif option=="in":
    if os.path.isfile ("/var/cache/lpm/lock"):
        print (colored ('lpm: error: cache has already locked'))
        sys.exit(0)
    else:
        open ("/var/cache/lpm/lock",'w')

    if sys.argv[2]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    package = sys.argv[2:]

    if not package[1:]==[]:
        strv = ''
        for i in package:
            strv+=','+i

    for i in package:
        print(colored(f'Downloading {i} archive package ... ','green'), end='')
        pack.download(i.lower())
        print(colored('done','green'))

    for j in package:
        f = open ('/etc/lpm/mirrors/'+j.lower(),'r')
        checkgit = f.read(
        )
        f.close()
        if checkgit.__contains__('git'):
            print(colored(f'Cloning and Installing {j} archive package ... ','green'), end='')
            pack.gitinstall(j)
            print(colored('done','green'))
        else:
            print(colored(f'Installing {i} archive package ... ','green'), end='')
            pack.unpack("/var/cache/lpm/gets/" + j.lower() + ".la")
            print(colored('done','green'))

    pack.clean()

elif option=="info":
    if sys.argv[2:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    pack = "/etc/lpm/packages/"+sys.argv[2]+".manifest"
    if os.path.isfile(pack):

        name = read_record ("name",pack)
        build = read_record("build", pack)
        version = read_record("version", pack)
        unpack = read_record("unpack", pack)
        description = read_record("description", pack)
        depends = read_record("depends", pack)
        license = read_record("license", pack)
        copyright = read_record("copyright", pack)

        if not (name == None or name == ""):  print(
            "\t      Package name: " + name )
        if not (version == None or version == ""):  print(
            "\t   Package version: " + version )
        if not (build == None or build == ""):  print(
            "\t        Build date: " + build )
        if not (copyright == None or copyright == ""):  print(
            "\t         Copyright: " + copyright )
        if not (license == None or license == ""):  print(
            "\t          Licensce: " + license )
        if not (description == None or description == ""):  print(
            "\t       Description: " + description )
        if not (depends == None or depends == ""):  print(
            "\t   Package depends: " + depends )
        if not (unpack == None or unpack == ""):  print(
            "\t      Installed in: " + unpack )
    else:
        print (colored(f'lpm: error: {sys.argv[2]}: package has not already installed','red'))

elif option=="ls":
    list = os.listdir ("/etc/lpm/packages")
    for i in list:
        if i.endswith (".manifest"):
            name = read_record("name", "/etc/lpm/packages/"+i)
            build = read_record("build", "/etc/lpm/packages/"+i)
            version = read_record("version", "/etc/lpm/packages/"+i)
            print (name+"/"+version+"/"+build)

elif option=='add':
    if sys.argv[2:]==[] or sys.argv[3:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    pack.add (sys.argv[2],sys.argv[3])

elif option=='del':
    if sys.argv[2:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    pack.remove (sys.argv[2])

elif option=='git':
    if sys.argv[2:]==[]:
        print (colored ('lpm: error: no inputs','red'))
        sys.exit(0)

    print(colored(f'Cloning {sys.argv[2]} archive package ... ','green'), end='')
    pack.gitinstall (sys.argv[2])
    print(colored('done','green'))
elif option=='man':
    print('''
    Learniaa Package Manager (LPM) Manpage:
    
    lpm [option] ...
    
    <option>    <args>                                          <job>
    in          learniaa                                        Install 'learniaa' package from the Internet
    get         learniaa                                        Download 'learniaa' archive package from the Internet
    add         https://example.com/learniaa.la learniaa.la     Add 'learniaa' archive package to dynamic mirrors
    del         learniaa                                        Remove 'learniaa' from dynamic mirrors
    rm          learniaa                                        Uninstall 'learniaa' package
    git         learniaa                                        Install 'learniaa' from git source
    ls                                                          List installed packages
    info        learniaa                                        Show informations about 'learniaa' package
    pak         learniaa-project                                Build archive package from 'learniaa-project' project
    upak        learniaa.la                                     Unpack 'learniaa.la' archive package
    cl                                                          Clean the cache
    
    For more help: https://learniaa.com
    
    ''')
else:
    print (colored(f'lpm: error: {option}: option not found','red'))