#!/usr/bin/python
import urllib
import urllib2
import hashlib
import optparse
import sys
import os


UPDATE_URL='http://areoles.local/api_update.php'
MOD_DIR='/usr/local/lib/areoles'
CONFIG_FILE='/etc/areoles.cfg'
MODULE_NAME='core.py'

sys.path.append(MOD_DIR)


class Updater():
    
    '''
    Params: 
        module: module.py to update
    '''
    def __init__(self, module, module_dir):
        self.module = module
        self.module_dir = module_dir
        
    '''
    Helper function to get the current module checksum
    '''
    def md5Checksum(self, filePath):
        fh = open(filePath, 'rb')
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)

        return m.hexdigest()

    '''
    Connects to the update server and checks for the 
    latest of a module, returns False if up to date
    '''    
    def checkForLatest(self):
        query_params = {'module': self.module}

        # Grab the current checksum
        # if it exists
        try:
            current_checksum = self.md5Checksum(self.module_dir + '/' + self.module)
        except:
            current_checksum = None

        if current_checksum is not None:
            query_params['checksum'] = current_checksum

        encoded_args = urllib.urlencode(query_params)
        response = urllib2.urlopen(UPDATE_URL+'?'+encoded_args).read()
        if response == '1':
            return False

        return response

    '''
    Ensure that this module is up to date
    '''
    def upToDate(self):
        response = self.checkForLatest()
        if response:
            try:
                update = open(self.module_dir + '/' + self.module, 'w')
                update.write(response)
                update.close()
            except:
                print 'Error updating. Check permissions'
                return False

        return True

'''
Init class, this will always be there
'''
class Init():

    '''
    Construct
    '''
    def __init__(self, conf):
        self.module_dir = MOD_DIR
        self.conf = conf

    '''
    Initialise 
    '''
    def initialise(self, key):
        if self.isInstalled():
            print 'Host is already installed'
            return True

        print 'Initialising...'
        #self.install()
        updater = Updater(MODULE_NAME, self.module_dir)
        if not updater.upToDate():
            return False

        from core import Core
        core = Core(self.conf)
        core.initialise(key) 
        
    def run(self):
        if not self.isInstalled():
            print 'Not installed try running with --init [provided key]'
            return False
        else:
            from core import Core
            core = Core(self.conf)
            core.run() 

    '''
    Checking the config file exists
    '''
    def isInstalled(self):
        return os.path.isfile(self.conf)

    ''' 
    Install
    '''
    #def install(self):
        # determine the mocule directory
        #while True:
            #sys.stdout.write('Enter path for module dir? [' + MOD_DIR + '] :')
            #self.module_dir = raw_input()
            #if str(self.module_dir).strip() == '':
        #self.module_dir = MOD_DIR
            #break

        # also check if the directory exists
        #while True:
        #    if os.path.isdir(self.module_dir) is False:
        #        sys.stdout.write("Module directory [" + self.module_dir + "] doesn't exist. Attempt to create it? [Y/n] :")
        #        create = raw_input().lower()
        #        if str(create).strip() == 'y':
        #            os.makedirs(self.module_dir, 0665)
        #            print 'Creating module directory'
        #        else:
        #            return True
        #    else:
        #        print 'Module directory exists checking for updates'
        #        break

    def update(self):
        if not self.isInstalled():
            print 'Not installed try running with --init [provided key]'
            return False
        else:
            print 'Checking for core updates'
            updater = Updater(MODULE_NAME, self.module_dir)
            if not updater.upToDate():
                print 'Error updating core, check permissions'
                return False
            
            from core import Core
            core = Core(self.conf)
            core.update() 


# parse cmd line arguments
parser = optparse.OptionParser()
parser.add_option('-i', '--init', help='Install and initialise host', dest='init')
parser.add_option('-u', '--update', action="store_true",  dest='update', help='Check for updates    ')
parser.add_option('-d', '--dry-run', action="store_true", dest='dry', help='Dry run (no communication with server)')
(opts, args) = parser.parse_args()

#if opts.init is not None:
#    print 'initializing'
#else:
#    print 'run normally'

init = Init(CONFIG_FILE)

if opts.init is not None:
    init.initialise(opts.init)
    exit()
else:
    if opts.update is True:
        init.update()
        exit()

init.run()
exit()