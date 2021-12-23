#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys # ,subprocess,shutil
#import urllib2
import re

#sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')
#sys.path.append('/eos/project-c/cmsweb/www/egamma/validation/Electrons/ChiLib')
sys.path.append('/afs/cern.ch/work/a/archiron/private/TEST_GITCLONE/ChiLib_CMS_Validation')

from networkFunctions import networkFunctions # list_search_0, list_search_1, cmd_load_files
from functions import quickRD_Tools
from getEnv import cms_env

class quickRD(): 
    def __init__(self):
        print('begin to run')
        net = networkFunctions()
        cms = cms_env()
        RDT = quickRD_Tools()
        
        actual_dir = os.getcwd()
        print('actual_dir : %s' % actual_dir)
        #self.CMSSWBASE = os.environ['CMSSW_BASE'] # donne le repertoire de travail
        #self.CMSSWBASECMSSWRELEASEBASE = os.environ['CMSSW_RELEASE_BASE'] # donne la release et l'architecture
        #self.CMSSWBASECMSSWVERSION = os.environ['CMSSW_VERSION'] # donne la release (CMSSW_7_1_0 par exemple)

        # TEMP before modifications
        self.CMSSWBASE = cms.getCMSSWBASE() # 'afs/cern.ch/user/a/archiron/public/CMSSW_12_2_0_pre2'
        self.CMSSWBASECMSSWRELEASEBASE = cms.getCMSSWBASECMSSWRELEASEBASE() # '/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0_pre2'
        self.CMSSWBASECMSSWVERSION = cms.getCMSSWBASECMSSWVERSION() # 'CMSSW_12_2_0_pre2'
        print('CMSSWBASE : %s' % self.CMSSWBASE) # /afs/cern.ch/user/a/archiron/public/CMSSW_12_2_0_pre2
        print('CMSSWBASECMSSWRELEASEBASE : %s' % self.CMSSWBASECMSSWRELEASEBASE) # /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0_pre2
        print('CMSSWBASECMSSWVERSION : %s' % self.CMSSWBASECMSSWVERSION) # CMSSW_12_2_0_pre2
        
        datasets_default = ['TTbar_13', 'ZEE_13']
        #datasets_default = ['TTbar_14TeV', 'ZEE_14']
        
        if len(sys.argv) > 1:
            print("argv 0 - arg. 0 :", sys.argv[0])
            print("step 1 - arg. 1 :", sys.argv[1])
            text = sys.argv[1]
        else:
            print("rien")            
            text = raw_input("prompt : ")  # Python 2
            #text = input("prompt : ")  # Python 3
            print('text : %s' % text)
        if (text == 'q'):
            exit()
        elif (text == ''):
            RELEASE = self.CMSSWBASECMSSWVERSION
        else:
            RELEASE = text
        print('RELEASE : %s' % RELEASE)
        
        # get the list for RELEASE
        list_0 = net.list_search_0()
        item_0 = ''
        #print(list_0)
        for item in list_0:
            it = item[:-1]
            #print(it, RELEASE)
            if re.search(it, RELEASE):
                print('OK pour %s' % item)
                item_0 = it

        if (item_0 == ''):
            print('\n===\nno match\n===')
            exit()
        else:
            print('item_0 : %s' % item_0)

        releasesList_1 = net.list_search_1(item_0 + 'x')
        print('there is %d files for %s' % (len(releasesList_1), item_0))
        
        list_1 = []
        for item in releasesList_1:
            if re.search(RELEASE, item):
                list_1.append(item)
        print('there is %d files for %s' % (len(list_1), RELEASE))
        #print(list_1)
        
        datasets = RDT.getDataSet(list_1)
        print('there is %d datasets for %s' % (len(datasets), RELEASE))
        '''for it in datasets:
            print(it)
        '''
        for i in range(0, len(datasets), 3):
            if (i+1 == len(datasets)):
                print('%50s [%2d]' % (datasets[i], i))
            elif (i+2 == len(datasets)):
                print('%50s [%2d] %50s [%2d]' % (datasets[i], i, datasets[i+1], i+1))
            else:
                print('%50s [%2d] %50s [%2d] %50s [%2d]' % (datasets[i], i, datasets[i+1], i+1, datasets[i+2], i+2))
        
        # test if datasets_default is included into datasets
        v = 0
        for item in datasets:
            for item2 in datasets_default:
                if item == item2:
                    v += 1
        if (v == 2): # we can use default datasets
            print('default datasets : ' + '[' + ' '.join("{:s}".format(x) for x in datasets_default) + ']')
            text_to_prompt = 'insert the # of the datasets you want separated by a comma or d to use default : '
            dts_list_txt = raw_input(text_to_prompt)
            if (dts_list_txt == 'd'):
                dts_list_2 = datasets_default
            else:
                dts_list = RDT.analyzeDTS(dts_list_txt)
        else: # we cannot use default datasets
            text_to_prompt = 'insert the # of the datasets you want separated by a comma : '
            dts_list_txt = raw_input(text_to_prompt)
            dts_list = RDT.analyzeDTS(dts_list_txt)

        # test if all # are < len(datasets)
        if (dts_list_txt != 'd'):
            dts_list_2 = []
            for item in dts_list:
                if (item >= len(datasets) or item < 0):
                    dts_list.remove(item)
                else:
                    dts_list_2.append(datasets[item])
            
        print('datasets final list : ' + '[' + ' '.join("{:s}".format(x) for x in dts_list_2) + ']')
        print('default datasets : ' + '[' + ' '.join("{:s}".format(x) for x in datasets_default) + ']')
        #stop
        
        list_2 = [] # get the list of the files for all the datasets
        nb_2 = [] # get the number of files per dataset
        for item1 in dts_list_2:
            i = 0
            for item2 in list_1:
                if re.search(item1, item2):
                    print(item2, item1)
                    list_2.append(item2)
                    i += 1
            nb_2.append(i)
                    
        for item1 in enumerate(list_2):
            print('[%2d] : %s' %(item1[0], list_2[item1[0]]))
            
        text_to_prompt = 'insert the # of the files you want to download separated by a comma or a for all : '
        files_list_txt = raw_input(text_to_prompt)
        if (files_list_txt == 'a'):
            files_list = range(0, len(list_2))
        else:
            files_list = RDT.analyzeDTS(files_list_txt)
        print(files_list)

        # test if all # are < len(datasets)
        files_list_2 = []
        for item in files_list:
            if (item >= len(list_2) or item < 0):
                files_list.remove(item)
            else:
                files_list_2.append(list_2[item])
        print('files final list : ' + '[' + ' '.join("{:s}".format(x) for x in files_list_2) + ']')
        
        # download
        net.cmd_load_files(files_list_2, item_0+'x')
        
        print('end of run')
        