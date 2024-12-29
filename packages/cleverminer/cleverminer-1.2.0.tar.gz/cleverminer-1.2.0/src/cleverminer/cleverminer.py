import sys #line:1
import time #line:2
import copy #line:3
from time import strftime #line:5
from time import gmtime #line:6
import pandas as pd #line:8
import numpy as np #line:9
from pandas .api .types import CategoricalDtype #line:10
import progressbar #line:11
import re #line:12
from textwrap import wrap #line:13
import seaborn as sns #line:14
import matplotlib .pyplot as plt #line:15
import re #line:16
import pickle #line:17
import json #line:18
import hashlib #line:19
from datetime import datetime #line:20
import tempfile #line:21
import os #line:22
class cleverminer :#line:25
    version_string ="1.2.0"#line:27
    temppath =tempfile .gettempdir ()#line:29
    cache_dir =os .path .join (temppath ,'clm_cache')#line:30
    def __init__ (OO0000OOO0O0OOOO0 ,**O0O00OOOO0O0OOO00 ):#line:32
        ""#line:61
        OO0000OOO0O0OOOO0 ._print_disclaimer ()#line:62
        OO0000OOO0O0OOOO0 .use_cache =False #line:63
        OO0000OOO0O0OOOO0 .cache_also_data =True #line:64
        OO0000OOO0O0OOOO0 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:73
        OO0000OOO0O0OOOO0 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:81
        OO0000OOO0O0OOOO0 .df =None #line:82
        OO0000OOO0O0OOOO0 .kwargs =None #line:83
        if len (O0O00OOOO0O0OOO00 )>0 :#line:84
            OO0000OOO0O0OOOO0 .kwargs =O0O00OOOO0O0OOO00 #line:85
        OO0000OOO0O0OOOO0 .profiles ={}#line:86
        OO0000OOO0O0OOOO0 .verbosity ={}#line:87
        OO0000OOO0O0OOOO0 .verbosity ['debug']=False #line:88
        OO0000OOO0O0OOOO0 .verbosity ['print_rules']=False #line:89
        OO0000OOO0O0OOOO0 .verbosity ['print_hashes']=True #line:90
        OO0000OOO0O0OOOO0 .verbosity ['last_hash_time']=0 #line:91
        OO0000OOO0O0OOOO0 .verbosity ['hint']=False #line:92
        if "opts"in O0O00OOOO0O0OOO00 :#line:93
            OO0000OOO0O0OOOO0 ._set_opts (O0O00OOOO0O0OOO00 .get ("opts"))#line:94
        if "opts"in O0O00OOOO0O0OOO00 :#line:95
            O00O0OO000OOOOOO0 =O0O00OOOO0O0OOO00 ['opts']#line:96
            if 'use_cache'in O00O0OO000OOOOOO0 :#line:97
                OO0000OOO0O0OOOO0 .use_cache =O00O0OO000OOOOOO0 ['use_cache']#line:98
            if 'cache_also_data'in O00O0OO000OOOOOO0 :#line:99
                OO0000OOO0O0OOOO0 .cache_also_data =O00O0OO000OOOOOO0 ['cache_also_data']#line:100
            if "verbose"in O0O00OOOO0O0OOO00 .get ('opts'):#line:101
                OO0OOO0OOO0O00O0O =O0O00OOOO0O0OOO00 .get ('opts').get ('verbose')#line:102
                if OO0OOO0OOO0O00O0O .upper ()=='FULL':#line:103
                    OO0000OOO0O0OOOO0 .verbosity ['debug']=True #line:104
                    OO0000OOO0O0OOOO0 .verbosity ['print_rules']=True #line:105
                    OO0000OOO0O0OOOO0 .verbosity ['print_hashes']=False #line:106
                    OO0000OOO0O0OOOO0 .verbosity ['hint']=True #line:107
                    OO0000OOO0O0OOOO0 .options ['progressbar']=False #line:108
                elif OO0OOO0OOO0O00O0O .upper ()=='RULES':#line:109
                    OO0000OOO0O0OOOO0 .verbosity ['debug']=False #line:110
                    OO0000OOO0O0OOOO0 .verbosity ['print_rules']=True #line:111
                    OO0000OOO0O0OOOO0 .verbosity ['print_hashes']=True #line:112
                    OO0000OOO0O0OOOO0 .verbosity ['hint']=True #line:113
                    OO0000OOO0O0OOOO0 .options ['progressbar']=False #line:114
                elif OO0OOO0OOO0O00O0O .upper ()=='HINT':#line:115
                    OO0000OOO0O0OOOO0 .verbosity ['debug']=False #line:116
                    OO0000OOO0O0OOOO0 .verbosity ['print_rules']=False #line:117
                    OO0000OOO0O0OOOO0 .verbosity ['print_hashes']=True #line:118
                    OO0000OOO0O0OOOO0 .verbosity ['last_hash_time']=0 #line:119
                    OO0000OOO0O0OOOO0 .verbosity ['hint']=True #line:120
                    OO0000OOO0O0OOOO0 .options ['progressbar']=False #line:121
                elif OO0OOO0OOO0O00O0O .upper ()=='DEBUG':#line:122
                    OO0000OOO0O0OOOO0 .verbosity ['debug']=True #line:123
                    OO0000OOO0O0OOOO0 .verbosity ['print_rules']=True #line:124
                    OO0000OOO0O0OOOO0 .verbosity ['print_hashes']=True #line:125
                    OO0000OOO0O0OOOO0 .verbosity ['last_hash_time']=0 #line:126
                    OO0000OOO0O0OOOO0 .verbosity ['hint']=True #line:127
                    OO0000OOO0O0OOOO0 .options ['progressbar']=False #line:128
        OOO0OOO0OO0OOO0OO =copy .deepcopy (O0O00OOOO0O0OOO00 )#line:130
        if 'df'in OOO0OOO0OO0OOO0OO :#line:131
            OOO0OOO0OO0OOO0OO ['df']=OOO0OOO0OO0OOO0OO ['df'].to_json ()#line:132
        O0O0O000O00O0OO0O =OO0000OOO0O0OOOO0 ._get_hash (OOO0OOO0OO0OOO0OO )#line:133
        OO0000OOO0O0OOOO0 .guid =O0O0O000O00O0OO0O #line:134
        if OO0000OOO0O0OOOO0 .use_cache :#line:135
            if not (os .path .isdir (OO0000OOO0O0OOOO0 .cache_dir )):#line:136
                os .mkdir (OO0000OOO0O0OOOO0 .cache_dir )#line:137
            OO0000OOO0O0OOOO0 .cache_fname =os .path .join (OO0000OOO0O0OOOO0 .cache_dir ,O0O0O000O00O0OO0O +'.clm')#line:138
            if os .path .isfile (OO0000OOO0O0OOOO0 .cache_fname ):#line:139
                print (f"Will use cached file {OO0000OOO0O0OOOO0.cache_fname}")#line:140
                O000000OOOO0OO0O0 ='pickle'#line:141
                if "fmt"in O0O00OOOO0O0OOO00 :#line:142
                    O000000OOOO0OO0O0 =O0O00OOOO0O0OOO00 .get ('fmt')#line:143
                OO0000OOO0O0OOOO0 .load (OO0000OOO0O0OOOO0 .cache_fname ,fmt =O000000OOOO0OO0O0 )#line:144
                return #line:145
            print (f"Task {O0O0O000O00O0OO0O} not in cache, will calculate it.")#line:146
        OO0000OOO0O0OOOO0 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:148
        if not (OO0000OOO0O0OOOO0 ._is_py310 ):#line:149
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:150
        else :#line:151
            if (OO0000OOO0O0OOOO0 .verbosity ['debug']):#line:152
                print ("Python 3.10+ detected.")#line:153
        OO0000OOO0O0OOOO0 ._initialized =False #line:154
        OO0000OOO0O0OOOO0 ._init_data ()#line:155
        OO0000OOO0O0OOOO0 ._init_task ()#line:156
        if len (O0O00OOOO0O0OOO00 )>0 :#line:157
            if "df"in O0O00OOOO0O0OOO00 :#line:158
                OO0000OOO0O0OOOO0 ._prep_data (O0O00OOOO0O0OOO00 .get ("df"))#line:159
            else :#line:160
                print ("Missing dataframe. Cannot initialize.")#line:161
                OO0000OOO0O0OOOO0 ._initialized =False #line:162
                return #line:163
            O0O0OO00O0O00OO0O =O0O00OOOO0O0OOO00 .get ("proc",None )#line:164
            if not (O0O0OO00O0O00OO0O ==None ):#line:165
                OO0000OOO0O0OOOO0 ._calculate (**O0O00OOOO0O0OOO00 )#line:166
            else :#line:167
                if OO0000OOO0O0OOOO0 .verbosity ['debug']:#line:168
                    print ("INFO: just initialized")#line:169
                OOOO0O0O0O00O00O0 ={}#line:170
                O00O0OOOOOOO0O0OO ={}#line:171
                O00O0OOOOOOO0O0OO ["varname"]=OO0000OOO0O0OOOO0 .data ["varname"]#line:172
                O00O0OOOOOOO0O0OO ["catnames"]=OO0000OOO0O0OOOO0 .data ["catnames"]#line:173
                OOOO0O0O0O00O00O0 ["datalabels"]=O00O0OOOOOOO0O0OO #line:174
                OO0000OOO0O0OOOO0 .result =OOOO0O0O0O00O00O0 #line:175
        OO0000OOO0O0OOOO0 ._initialized =True #line:177
        if OO0000OOO0O0OOOO0 .use_cache :#line:178
            OO0000OOO0O0OOOO0 .save (OO0000OOO0O0OOOO0 .cache_fname ,savedata =OO0000OOO0O0OOOO0 .cache_also_data ,embeddata =False )#line:179
            print (f"CACHE: results cache saved into {OO0000OOO0O0OOOO0.cache_fname}")#line:180
    def _get_hash (OO0000OOO0O00OO0O ,OO00O0000000O0000 ):#line:182
        O000000OOOO0000OO =hashlib .sha256 (json .dumps (OO00O0000000O0000 ,sort_keys =True ).encode ('utf-8')).hexdigest ()#line:183
        return O000000OOOO0000OO #line:185
    def _get_fast_hash (OO0O0OO0O0000OO0O ,O00OOOOOOOOO00O0O ):#line:187
        OO0OO0O00OO00O00O =pickle .dumps (O00OOOOOOOOO00O0O )#line:192
        print (f"...CALC THE HASH {datetime.now()}")#line:193
        OOO0O0OOO0000000O =hashlib .md5 (OO0OO0O00OO00O00O ).hexdigest ()#line:194
        return OOO0O0OOO0000000O #line:199
    def _set_opts (O0OOO0000O0O0000O ,OO0OOOO000OO000O0 ):#line:201
        if "no_optimizations"in OO0OOOO000OO000O0 :#line:202
            O0OOO0000O0O0000O .options ['optimizations']=not (OO0OOOO000OO000O0 ['no_optimizations'])#line:203
            print ("No optimization will be made.")#line:204
        if "disable_progressbar"in OO0OOOO000OO000O0 :#line:205
            O0OOO0000O0O0000O .options ['progressbar']=False #line:206
            print ("Progressbar will not be shown.")#line:207
        if "max_rules"in OO0OOOO000OO000O0 :#line:208
            O0OOO0000O0O0000O .options ['max_rules']=OO0OOOO000OO000O0 ['max_rules']#line:209
        if "max_categories"in OO0OOOO000OO000O0 :#line:210
            O0OOO0000O0O0000O .options ['max_categories']=OO0OOOO000OO000O0 ['max_categories']#line:211
            if O0OOO0000O0O0000O .verbosity ['debug']==True :#line:212
                print (f"Maximum number of categories set to {O0OOO0000O0O0000O.options['max_categories']}")#line:213
        if "no_automatic_data_conversions"in OO0OOOO000OO000O0 :#line:214
            O0OOO0000O0O0000O .options ['automatic_data_conversions']=not (OO0OOOO000OO000O0 ['no_automatic_data_conversions'])#line:215
            print ("No automatic data conversions will be made.")#line:216
        if "keep_df"in OO0OOOO000OO000O0 :#line:217
            O0OOO0000O0O0000O .options ['keep_df']=OO0OOOO000OO000O0 ['keep_df']#line:218
    def _init_data (OOO000O00OO0OOO0O ):#line:221
        OOO000O00OO0OOO0O .data ={}#line:223
        OOO000O00OO0OOO0O .data ["varname"]=[]#line:224
        OOO000O00OO0OOO0O .data ["catnames"]=[]#line:225
        OOO000O00OO0OOO0O .data ["vtypes"]=[]#line:226
        OOO000O00OO0OOO0O .data ["dm"]=[]#line:227
        OOO000O00OO0OOO0O .data ["rows_count"]=int (0 )#line:228
        OOO000O00OO0OOO0O .data ["data_prepared"]=0 #line:229
    def _init_task (O00O0O00O0OOO0OOO ):#line:231
        if "opts"in O00O0O00O0OOO0OOO .kwargs :#line:233
            O00O0O00O0OOO0OOO ._set_opts (O00O0O00O0OOO0OOO .kwargs .get ("opts"))#line:234
        O00O0O00O0OOO0OOO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:244
        O00O0O00O0OOO0OOO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:248
        O00O0O00O0OOO0OOO .rulelist =[]#line:249
        O00O0O00O0OOO0OOO .stats ['total_cnt']=0 #line:250
        O00O0O00O0OOO0OOO .stats ['total_valid']=0 #line:251
        O00O0O00O0OOO0OOO .stats ['control_number']=0 #line:252
        O00O0O00O0OOO0OOO .result ={}#line:253
        O00O0O00O0OOO0OOO ._opt_base =None #line:254
        O00O0O00O0OOO0OOO ._opt_relbase =None #line:255
        O00O0O00O0OOO0OOO ._opt_base1 =None #line:256
        O00O0O00O0OOO0OOO ._opt_relbase1 =None #line:257
        O00O0O00O0OOO0OOO ._opt_base2 =None #line:258
        O00O0O00O0OOO0OOO ._opt_relbase2 =None #line:259
        O000000000O0OO00O =None #line:260
        if not (O00O0O00O0OOO0OOO .kwargs ==None ):#line:261
            O000000000O0OO00O =O00O0O00O0OOO0OOO .kwargs .get ("quantifiers",None )#line:262
            if not (O000000000O0OO00O ==None ):#line:263
                for O0000OO0O0OO00OO0 in O000000000O0OO00O .keys ():#line:264
                    if O0000OO0O0OO00OO0 .upper ()=='BASE':#line:265
                        O00O0O00O0OOO0OOO ._opt_base =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:266
                    if O0000OO0O0OO00OO0 .upper ()=='RELBASE':#line:267
                        O00O0O00O0OOO0OOO ._opt_relbase =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:268
                    if (O0000OO0O0OO00OO0 .upper ()=='FRSTBASE')|(O0000OO0O0OO00OO0 .upper ()=='BASE1'):#line:269
                        O00O0O00O0OOO0OOO ._opt_base1 =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:270
                    if (O0000OO0O0OO00OO0 .upper ()=='SCNDBASE')|(O0000OO0O0OO00OO0 .upper ()=='BASE2'):#line:271
                        O00O0O00O0OOO0OOO ._opt_base2 =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:272
                    if (O0000OO0O0OO00OO0 .upper ()=='FRSTRELBASE')|(O0000OO0O0OO00OO0 .upper ()=='RELBASE1'):#line:273
                        O00O0O00O0OOO0OOO ._opt_relbase1 =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:274
                    if (O0000OO0O0OO00OO0 .upper ()=='SCNDRELBASE')|(O0000OO0O0OO00OO0 .upper ()=='RELBASE2'):#line:275
                        O00O0O00O0OOO0OOO ._opt_relbase2 =O000000000O0OO00O .get (O0000OO0O0OO00OO0 )#line:276
            else :#line:277
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:278
        else :#line:279
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:280
    def mine (O0O00OO0O0OO00O0O ,**OO00OOOOOO00000O0 ):#line:283
        ""#line:288
        if not (O0O00OO0O0OO00O0O ._initialized ):#line:289
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:290
            return #line:291
        O0O00OO0O0OO00O0O .kwargs =None #line:292
        if len (OO00OOOOOO00000O0 )>0 :#line:293
            O0O00OO0O0OO00O0O .kwargs =OO00OOOOOO00000O0 #line:294
        O0O00OO0O0OO00O0O ._init_task ()#line:295
        if len (OO00OOOOOO00000O0 )>0 :#line:296
            O0O000O0O000000OO =OO00OOOOOO00000O0 .get ("proc",None )#line:297
            if not (O0O000O0O000000OO ==None ):#line:298
                O0O00OO0O0OO00O0O ._calc_all (**OO00OOOOOO00000O0 )#line:299
            else :#line:300
                print ("Rule mining procedure missing")#line:301
    def _get_ver (OO000O0OOOOO0OOO0 ):#line:304
        return OO000O0OOOOO0OOO0 .version_string #line:305
    def _print_disclaimer (O00O0OO000OO0O0OO ):#line:307
        print (f"Cleverminer version {O00O0OO000OO0O0OO._get_ver()}.")#line:308
    def _automatic_data_conversions (O000OO0O0OO0OO00O ,OOOOOO00O0O0OO000 ):#line:309
        print ("Automatically reordering numeric categories ...")#line:310
        for OO0O0O0O0O00O00OO in range (len (OOOOOO00O0O0OO000 .columns )):#line:311
            if O000OO0O0OO0OO00O .verbosity ['debug']:#line:312
                print (f"#{OO0O0O0O0O00O00OO}: {OOOOOO00O0O0OO000.columns[OO0O0O0O0O00O00OO]} : {OOOOOO00O0O0OO000.dtypes[OO0O0O0O0O00O00OO]}.")#line:313
            try :#line:314
                OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]]=OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]].astype (str ).astype (float )#line:315
                if O000OO0O0OO0OO00O .verbosity ['debug']:#line:316
                    print (f"CONVERTED TO FLOATS #{OO0O0O0O0O00O00OO}: {OOOOOO00O0O0OO000.columns[OO0O0O0O0O00O00OO]} : {OOOOOO00O0O0OO000.dtypes[OO0O0O0O0O00O00OO]}.")#line:317
                OOO0O0O0OO0OOO0O0 =pd .unique (OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]])#line:318
                O00O0OO0OO00OOOOO =True #line:319
                for OO00O000OOO0OOO0O in OOO0O0O0OO0OOO0O0 :#line:320
                    if OO00O000OOO0OOO0O %1 !=0 :#line:321
                        O00O0OO0OO00OOOOO =False #line:322
                if O00O0OO0OO00OOOOO :#line:323
                    OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]]=OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]].astype (int )#line:324
                    if O000OO0O0OO0OO00O .verbosity ['debug']:#line:325
                        print (f"CONVERTED TO INT #{OO0O0O0O0O00O00OO}: {OOOOOO00O0O0OO000.columns[OO0O0O0O0O00O00OO]} : {OOOOOO00O0O0OO000.dtypes[OO0O0O0O0O00O00OO]}.")#line:326
                O00OO000OO0O000O0 =pd .unique (OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]])#line:327
                OO00OO00OO0OOO000 =CategoricalDtype (categories =O00OO000OO0O000O0 .sort (),ordered =True )#line:328
                OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]]=OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]].astype (OO00OO00OO0OOO000 )#line:329
                if O000OO0O0OO0OO00O .verbosity ['debug']:#line:330
                    print (f"CONVERTED TO CATEGORY #{OO0O0O0O0O00O00OO}: {OOOOOO00O0O0OO000.columns[OO0O0O0O0O00O00OO]} : {OOOOOO00O0O0OO000.dtypes[OO0O0O0O0O00O00OO]}.")#line:331
            except :#line:333
                if O000OO0O0OO0OO00O .verbosity ['debug']:#line:334
                    print ("...cannot be converted to int")#line:335
                try :#line:336
                    OO0OO0000000OO000 =OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]].unique ()#line:337
                    if O000OO0O0OO0OO00O .verbosity ['debug']:#line:338
                        print (f"Values: {OO0OO0000000OO000}")#line:339
                    O00OO0OOOOO0OO00O =True #line:340
                    OOOO00000O0O0O0OO =[]#line:341
                    for OO00O000OOO0OOO0O in OO0OO0000000OO000 :#line:342
                        O000OO00O0OOOOOO0 =re .findall (r"-?\d+",OO00O000OOO0OOO0O )#line:345
                        if len (O000OO00O0OOOOOO0 )>0 :#line:347
                            OOOO00000O0O0O0OO .append (int (O000OO00O0OOOOOO0 [0 ]))#line:348
                        else :#line:349
                            O00OO0OOOOO0OO00O =False #line:350
                    if O000OO0O0OO0OO00O .verbosity ['debug']:#line:351
                        print (f"Is ok: {O00OO0OOOOO0OO00O}, extracted {OOOO00000O0O0O0OO}")#line:352
                    if O00OO0OOOOO0OO00O :#line:353
                        O00OOOOO0O0OOO0OO =copy .deepcopy (OOOO00000O0O0O0OO )#line:354
                        O00OOOOO0O0OOO0OO .sort ()#line:355
                        O0O000O000000OO00 =[]#line:357
                        for OOO0OO0OO0OOO00OO in O00OOOOO0O0OOO0OO :#line:358
                            O0OO00000OO000O0O =OOOO00000O0O0O0OO .index (OOO0OO0OO0OOO00OO )#line:359
                            O0O000O000000OO00 .append (OO0OO0000000OO000 [O0OO00000OO000O0O ])#line:361
                        if O000OO0O0OO0OO00O .verbosity ['debug']:#line:362
                            print (f"Sorted list: {O0O000O000000OO00}")#line:363
                        OO00OO00OO0OOO000 =CategoricalDtype (categories =O0O000O000000OO00 ,ordered =True )#line:364
                        OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]]=OOOOOO00O0O0OO000 [OOOOOO00O0O0OO000 .columns [OO0O0O0O0O00O00OO ]].astype (OO00OO00OO0OOO000 )#line:365
                except :#line:366
                    if O000OO0O0OO0OO00O .verbosity ['debug']:#line:367
                        print ("...cannot extract numbers from all categories")#line:368
        print ("Automatically reordering numeric categories ...done")#line:370
    def _prep_data (OOOO0OO0OO00O00O0 ,OOO000O0OOO00O0O0 ):#line:372
        print ("Starting data preparation ...")#line:373
        OOOO0OO0OO00O00O0 ._init_data ()#line:374
        OOOO0OO0OO00O00O0 .stats ['start_prep_time']=time .time ()#line:375
        if OOOO0OO0OO00O00O0 .options ['automatic_data_conversions']:#line:376
            OOOO0OO0OO00O00O0 ._automatic_data_conversions (OOO000O0OOO00O0O0 )#line:377
        OOOO0OO0OO00O00O0 .data ["rows_count"]=OOO000O0OOO00O0O0 .shape [0 ]#line:378
        for OOOO0OOOOOO0OOO00 in OOO000O0OOO00O0O0 .select_dtypes (exclude =['category']).columns :#line:379
            OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ]=OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ].apply (str )#line:380
        try :#line:381
            O0OO0O00OO0O0O0OO =pd .DataFrame .from_records ([(OO000OO0O0OO0OOOO ,OOO000O0OOO00O0O0 [OO000OO0O0OO0OOOO ].nunique ())for OO000OO0O0OO0OOOO in OOO000O0OOO00O0O0 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:383
        except :#line:384
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:385
            O00OO0OO000OO0O00 =""#line:386
            try :#line:387
                for OOOO0OOOOOO0OOO00 in OOO000O0OOO00O0O0 .columns :#line:388
                    O00OO0OO000OO0O00 =OOOO0OOOOOO0OOO00 #line:389
                    print (f"...column {OOOO0OOOOOO0OOO00} has {int(OOO000O0OOO00O0O0[OOOO0OOOOOO0OOO00].nunique())} values")#line:390
            except :#line:391
                print (f"... detected : column {O00OO0OO000OO0O00} has unsupported type: {type(OOO000O0OOO00O0O0[OOOO0OOOOOO0OOO00])}.")#line:392
                exit (1 )#line:393
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:394
            exit (1 )#line:395
        if OOOO0OO0OO00O00O0 .verbosity ['hint']:#line:398
            print ("Quick profile of input data: unique value counts are:")#line:399
            print (O0OO0O00OO0O0O0OO )#line:400
            for OOOO0OOOOOO0OOO00 in OOO000O0OOO00O0O0 .columns :#line:401
                if OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ].nunique ()<OOOO0OO0OO00O00O0 .options ['max_categories']:#line:402
                    OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ]=OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ].astype ('category')#line:403
                else :#line:404
                    print (f"WARNING: attribute {OOOO0OOOOOO0OOO00} has more than {OOOO0OO0OO00O00O0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:405
                    del OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ]#line:406
        for OOOO0OOOOOO0OOO00 in OOO000O0OOO00O0O0 .columns :#line:408
            if OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ].nunique ()>OOOO0OO0OO00O00O0 .options ['max_categories']:#line:409
                print (f"WARNING: attribute {OOOO0OOOOOO0OOO00} has more than {OOOO0OO0OO00O00O0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:410
                del OOO000O0OOO00O0O0 [OOOO0OOOOOO0OOO00 ]#line:411
        if OOOO0OO0OO00O00O0 .options ['keep_df']:#line:412
            if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:413
                print ("Keeping df.")#line:414
            OOOO0OO0OO00O00O0 .df =OOO000O0OOO00O0O0 #line:415
        print ("Encoding columns into bit-form...")#line:416
        O00OOO00O00OOO00O =0 #line:417
        O0000OOOOO0OO000O =0 #line:418
        for O0O0O0OOOOOO000O0 in OOO000O0OOO00O0O0 :#line:419
            if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:420
                print ('Column: '+O0O0O0OOOOOO000O0 +' @ '+str (time .time ()))#line:421
            if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:422
                print ('Column: '+O0O0O0OOOOOO000O0 )#line:423
            OOOO0OO0OO00O00O0 .data ["varname"].append (O0O0O0OOOOOO000O0 )#line:424
            OOOOO0O0O000O000O =pd .get_dummies (OOO000O0OOO00O0O0 [O0O0O0OOOOOO000O0 ])#line:425
            O0O00OO00O0000OOO =0 #line:426
            if (OOO000O0OOO00O0O0 .dtypes [O0O0O0OOOOOO000O0 ].name =='category'):#line:427
                O0O00OO00O0000OOO =1 #line:428
            OOOO0OO0OO00O00O0 .data ["vtypes"].append (O0O00OO00O0000OOO )#line:429
            if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:430
                print (OOOOO0O0O000O000O )#line:431
                print (OOO000O0OOO00O0O0 [O0O0O0OOOOOO000O0 ])#line:432
            OO0OOO000O00000OO =0 #line:433
            O0O000OOO00OO00OO =[]#line:434
            O0000O00OOO0O0O0O =[]#line:435
            if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:436
                print ('...starting categories '+str (time .time ()))#line:437
            for OOOO0OOO000O000O0 in OOOOO0O0O000O000O :#line:438
                if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:439
                    print ('....category : '+str (OOOO0OOO000O000O0 )+' @ '+str (time .time ()))#line:440
                O0O000OOO00OO00OO .append (OOOO0OOO000O000O0 )#line:441
                O000O000O00O000O0 =int (0 )#line:442
                OO0OOOOOOOO0OO0OO =OOOOO0O0O000O000O [OOOO0OOO000O000O0 ].values #line:443
                if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:444
                    print (OO0OOOOOOOO0OO0OO .ndim )#line:445
                OO00O00O00OO0000O =np .packbits (OO0OOOOOOOO0OO0OO ,bitorder ='little')#line:446
                O000O000O00O000O0 =int .from_bytes (OO00O00O00OO0000O ,byteorder ='little')#line:447
                O0000O00OOO0O0O0O .append (O000O000O00O000O0 )#line:448
                if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:450
                    for OOO0O000OOOO0O0O0 in range (OOOO0OO0OO00O00O0 .data ["rows_count"]):#line:452
                        if OO0OOOOOOOO0OO0OO [OOO0O000OOOO0O0O0 ]>0 :#line:453
                            O000O000O00O000O0 +=1 <<OOO0O000OOOO0O0O0 #line:454
                            O0000O00OOO0O0O0O .append (O000O000O00O000O0 )#line:455
                    print ('....category ATTEMPT 2: '+str (OOOO0OOO000O000O0 )+" @ "+str (time .time ()))#line:458
                    OOO0O00OO0O0OOOOO =int (0 )#line:459
                    OOO00000O0OOO00OO =int (1 )#line:460
                    for OOO0O000OOOO0O0O0 in range (OOOO0OO0OO00O00O0 .data ["rows_count"]):#line:461
                        if OO0OOOOOOOO0OO0OO [OOO0O000OOOO0O0O0 ]>0 :#line:462
                            OOO0O00OO0O0OOOOO +=OOO00000O0OOO00OO #line:463
                            OOO00000O0OOO00OO *=2 #line:464
                            OOO00000O0OOO00OO =OOO00000O0OOO00OO <<1 #line:465
                            print (str (O000O000O00O000O0 ==OOO0O00OO0O0OOOOO )+" @ "+str (time .time ()))#line:466
                OO0OOO000O00000OO +=1 #line:467
                O0000OOOOO0OO000O +=1 #line:468
                if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:469
                    print (O0O000OOO00OO00OO )#line:470
            OOOO0OO0OO00O00O0 .data ["catnames"].append (O0O000OOO00OO00OO )#line:471
            OOOO0OO0OO00O00O0 .data ["dm"].append (O0000O00OOO0O0O0O )#line:472
        print ("Encoding columns into bit-form...done")#line:474
        if OOOO0OO0OO00O00O0 .verbosity ['hint']:#line:475
            print (f"List of attributes for analysis is: {OOOO0OO0OO00O00O0.data['varname']}")#line:476
            print (f"List of category names for individual attributes is : {OOOO0OO0OO00O00O0.data['catnames']}")#line:477
        if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:478
            print (f"List of vtypes is (all should be 1) : {OOOO0OO0OO00O00O0.data['vtypes']}")#line:479
        OOOO0OO0OO00O00O0 .data ["data_prepared"]=1 #line:480
        print ("Data preparation finished.")#line:481
        if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:482
            print ('Number of variables : '+str (len (OOOO0OO0OO00O00O0 .data ["dm"])))#line:483
            print ('Total number of categories in all variables : '+str (O0000OOOOO0OO000O ))#line:484
        OOOO0OO0OO00O00O0 .stats ['end_prep_time']=time .time ()#line:485
        if OOOO0OO0OO00O00O0 .verbosity ['debug']:#line:486
            print ('Time needed for data preparation : ',str (OOOO0OO0OO00O00O0 .stats ['end_prep_time']-OOOO0OO0OO00O00O0 .stats ['start_prep_time']))#line:487
    def _bitcount (O0O0000OOOOO00OO0 ,OO0OO00O0O0O0O000 ):#line:489
        OOOO000OOOOO0OO00 =None #line:490
        if (O0O0000OOOOO00OO0 ._is_py310 ):#line:491
            OOOO000OOOOO0OO00 =OO0OO00O0O0O0O000 .bit_count ()#line:492
        else :#line:493
            OOOO000OOOOO0OO00 =bin (OO0OO00O0O0O0O000 ).count ("1")#line:494
        return OOOO000OOOOO0OO00 #line:495
    def _verifyCF (OOOO0O0OO0OOO0000 ,_O0OOOOOOOO0O0OO00 ):#line:498
        O00OOOO000O0OOO0O =OOOO0O0OO0OOO0000 ._bitcount (_O0OOOOOOOO0O0OO00 )#line:499
        OOOO0O0O0O000OOOO =[]#line:500
        O0OO0000OO0O00O0O =[]#line:501
        O00000O0O0O0O00OO =0 #line:502
        OO0O0OOOO0O0O0OO0 =0 #line:503
        O00O00OOO00000OOO =0 #line:504
        O0000OOO0OO000000 =0 #line:505
        O00O0OO00OO00O0O0 =0 #line:506
        OOOOOOO0OOO00O000 =0 #line:507
        O00O0OOO00OO00000 =0 #line:508
        OOO0O0OOOO0OO0O00 =0 #line:509
        O00O0000O0O0OO000 =0 #line:510
        O0OO000000O0OO0OO =None #line:511
        O00OO0O000O0O00O0 =None #line:512
        O00O0OOOOO0O00OOO =None #line:513
        if ('min_step_size'in OOOO0O0OO0OOO0000 .quantifiers ):#line:514
            O0OO000000O0OO0OO =OOOO0O0OO0OOO0000 .quantifiers .get ('min_step_size')#line:515
        if ('min_rel_step_size'in OOOO0O0OO0OOO0000 .quantifiers ):#line:516
            O00OO0O000O0O00O0 =OOOO0O0OO0OOO0000 .quantifiers .get ('min_rel_step_size')#line:517
            if O00OO0O000O0O00O0 >=1 and O00OO0O000O0O00O0 <100 :#line:518
                O00OO0O000O0O00O0 =O00OO0O000O0O00O0 /100 #line:519
        O0OO00OOO00OO0O00 =0 #line:520
        OO00O0000OO0OOOO0 =0 #line:521
        O0OOOOO000000000O =[]#line:522
        if ('aad_weights'in OOOO0O0OO0OOO0000 .quantifiers ):#line:523
            O0OO00OOO00OO0O00 =1 #line:524
            O0OOO0O0OOO00O00O =[]#line:525
            O0OOOOO000000000O =OOOO0O0OO0OOO0000 .quantifiers .get ('aad_weights')#line:526
        O0O00OOOOO000OO00 =OOOO0O0OO0OOO0000 .data ["dm"][OOOO0O0OO0OOO0000 .data ["varname"].index (OOOO0O0OO0OOO0000 .kwargs .get ('target'))]#line:527
        def O00O0OO0OO00OOO0O (O00OO0O00OOOOO000 ,O000OO0OOOOO0O000 ):#line:528
            OOO0000000OO0OOO0 =True #line:529
            if (O00OO0O00OOOOO000 >O000OO0OOOOO0O000 ):#line:530
                if not (O0OO000000O0OO0OO is None or O00OO0O00OOOOO000 >=O000OO0OOOOO0O000 +O0OO000000O0OO0OO ):#line:531
                    OOO0000000OO0OOO0 =False #line:532
                if not (O00OO0O000O0O00O0 is None or O00OO0O00OOOOO000 >=O000OO0OOOOO0O000 *(1 +O00OO0O000O0O00O0 )):#line:533
                    OOO0000000OO0OOO0 =False #line:534
            if (O00OO0O00OOOOO000 <O000OO0OOOOO0O000 ):#line:535
                if not (O0OO000000O0OO0OO is None or O00OO0O00OOOOO000 <=O000OO0OOOOO0O000 -O0OO000000O0OO0OO ):#line:536
                    OOO0000000OO0OOO0 =False #line:537
                if not (O00OO0O000O0O00O0 is None or O00OO0O00OOOOO000 <=O000OO0OOOOO0O000 *(1 -O00OO0O000O0O00O0 )):#line:538
                    OOO0000000OO0OOO0 =False #line:539
            return OOO0000000OO0OOO0 #line:540
        for O0O00OOOOOO000OOO in range (len (O0O00OOOOO000OO00 )):#line:541
            OO0O0OOOO0O0O0OO0 =O00000O0O0O0O00OO #line:543
            O00000O0O0O0O00OO =OOOO0O0OO0OOO0000 ._bitcount (_O0OOOOOOOO0O0OO00 &O0O00OOOOO000OO00 [O0O00OOOOOO000OOO ])#line:544
            OOOO0O0O0O000OOOO .append (O00000O0O0O0O00OO )#line:545
            if O0O00OOOOOO000OOO >0 :#line:546
                if (O00000O0O0O0O00OO >OO0O0OOOO0O0O0OO0 ):#line:547
                    if (O00O00OOO00000OOO ==1 )and (O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 )):#line:548
                        OOO0O0OOOO0OO0O00 +=1 #line:549
                    else :#line:550
                        if O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 ):#line:551
                            OOO0O0OOOO0OO0O00 =1 #line:552
                        else :#line:553
                            OOO0O0OOOO0OO0O00 =0 #line:554
                    if OOO0O0OOOO0OO0O00 >O0000OOO0OO000000 :#line:555
                        O0000OOO0OO000000 =OOO0O0OOOO0OO0O00 #line:556
                    O00O00OOO00000OOO =1 #line:557
                    if O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 ):#line:558
                        OOOOOOO0OOO00O000 +=1 #line:559
                if (O00000O0O0O0O00OO <OO0O0OOOO0O0O0OO0 ):#line:560
                    if (O00O00OOO00000OOO ==-1 )and (O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 )):#line:561
                        O00O0000O0O0OO000 +=1 #line:562
                    else :#line:563
                        if O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 ):#line:564
                            O00O0000O0O0OO000 =1 #line:565
                        else :#line:566
                            O00O0000O0O0OO000 =0 #line:567
                    if O00O0000O0O0OO000 >O00O0OO00OO00O0O0 :#line:568
                        O00O0OO00OO00O0O0 =O00O0000O0O0OO000 #line:569
                    O00O00OOO00000OOO =-1 #line:570
                    if O00O0OO0OO00OOO0O (O00000O0O0O0O00OO ,OO0O0OOOO0O0O0OO0 ):#line:571
                        O00O0OOO00OO00000 +=1 #line:572
                if (O00000O0O0O0O00OO ==OO0O0OOOO0O0O0OO0 ):#line:573
                    O00O00OOO00000OOO =0 #line:574
                    O00O0000O0O0OO000 =0 #line:575
                    OOO0O0OOOO0OO0O00 =0 #line:576
            if (O0OO00OOO00OO0O00 ):#line:578
                O00O00O000OO0O0O0 =OOOO0O0OO0OOO0000 ._bitcount (O0O00OOOOO000OO00 [O0O00OOOOOO000OOO ])#line:579
                O0OOO0O0OOO00O00O .append (O00O00O000OO0O0O0 )#line:580
        if (O0OO00OOO00OO0O00 &sum (OOOO0O0O0O000OOOO )>0 ):#line:582
            for O0O00OOOOOO000OOO in range (len (O0O00OOOOO000OO00 )):#line:583
                if O0OOO0O0OOO00O00O [O0O00OOOOOO000OOO ]>0 :#line:584
                    if OOOO0O0O0O000OOOO [O0O00OOOOOO000OOO ]/sum (OOOO0O0O0O000OOOO )>O0OOO0O0OOO00O00O [O0O00OOOOOO000OOO ]/sum (O0OOO0O0OOO00O00O ):#line:585
                        OO00O0000OO0OOOO0 +=O0OOOOO000000000O [O0O00OOOOOO000OOO ]*((OOOO0O0O0O000OOOO [O0O00OOOOOO000OOO ]/sum (OOOO0O0O0O000OOOO ))/(O0OOO0O0OOO00O00O [O0O00OOOOOO000OOO ]/sum (O0OOO0O0OOO00O00O ))-1 )#line:586
        O0OO000OOOOO000OO =True #line:589
        for O0OO0O0OOOOO0O0O0 in OOOO0O0OO0OOO0000 .quantifiers .keys ():#line:590
            if O0OO0O0OOOOO0O0O0 .upper ()=='BASE':#line:591
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O00OOOO000O0OOO0O )#line:592
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELBASE':#line:593
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O00OOOO000O0OOO0O *1.0 /OOOO0O0OO0OOO0000 .data ["rows_count"])#line:594
            if O0OO0O0OOOOO0O0O0 .upper ()=='S_UP':#line:595
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O0000OOO0OO000000 )#line:596
            if O0OO0O0OOOOO0O0O0 .upper ()=='S_DOWN':#line:597
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O00O0OO00OO00O0O0 )#line:598
            if O0OO0O0OOOOO0O0O0 .upper ()=='S_ANY_UP':#line:599
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O0000OOO0OO000000 )#line:600
            if O0OO0O0OOOOO0O0O0 .upper ()=='S_ANY_DOWN':#line:601
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=O00O0OO00OO00O0O0 )#line:602
            if O0OO0O0OOOOO0O0O0 .upper ()=='MAX':#line:603
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=max (OOOO0O0O0O000OOOO ))#line:604
            if O0OO0O0OOOOO0O0O0 .upper ()=='MIN':#line:605
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=min (OOOO0O0O0O000OOOO ))#line:606
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELMAX':#line:607
                if sum (OOOO0O0O0O000OOOO )>0 :#line:608
                    O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=max (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO ))#line:609
                else :#line:610
                    O0OO000OOOOO000OO =False #line:611
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELMAX_LEQ':#line:612
                if sum (OOOO0O0O0O000OOOO )>0 :#line:613
                    O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )>=max (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO ))#line:614
                else :#line:615
                    O0OO000OOOOO000OO =False #line:616
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELMIN':#line:617
                if sum (OOOO0O0O0O000OOOO )>0 :#line:618
                    O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=min (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO ))#line:619
                else :#line:620
                    O0OO000OOOOO000OO =False #line:621
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELMIN_LEQ':#line:622
                if sum (OOOO0O0O0O000OOOO )>0 :#line:623
                    O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )>=min (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO ))#line:624
                else :#line:625
                    O0OO000OOOOO000OO =False #line:626
            if O0OO0O0OOOOO0O0O0 .upper ()=='AAD':#line:627
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )<=OO00O0000OO0OOOO0 )#line:628
            if O0OO0O0OOOOO0O0O0 .upper ()=='RELRANGE_LEQ':#line:629
                OO00O0OO00O0O0O00 =OOOO0O0OO0OOO0000 .quantifiers .get (O0OO0O0OOOOO0O0O0 )#line:630
                if OO00O0OO00O0O0O00 >=1 and OO00O0OO00O0O0O00 <100 :#line:631
                    OO00O0OO00O0O0O00 =OO00O0OO00O0O0O00 *1.0 /100 #line:632
                O0OOOOO0OOO00O000 =min (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO )#line:633
                O0000O0O0OOO0OO00 =max (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO )#line:634
                O0OO000OOOOO000OO =O0OO000OOOOO000OO and (OO00O0OO00O0O0O00 >=O0000O0O0OOO0OO00 -O0OOOOO0OOO00O000 )#line:635
        OO0O0OO00O00O000O ={}#line:636
        if O0OO000OOOOO000OO ==True :#line:637
            if OOOO0O0OO0OOO0000 .verbosity ['debug']:#line:638
                print ("Rule found: base: "+str (O00OOOO000O0OOO0O )+", hist: "+str (OOOO0O0O0O000OOOO )+", max: "+str (max (OOOO0O0O0O000OOOO ))+", min: "+str (min (OOOO0O0O0O000OOOO ))+", s_up: "+str (O0000OOO0OO000000 )+", s_down: "+str (O00O0OO00OO00O0O0 ))#line:639
            OOOO0O0OO0OOO0000 .stats ['total_valid']+=1 #line:640
            OO0O0OO00O00O000O ["base"]=O00OOOO000O0OOO0O #line:641
            OO0O0OO00O00O000O ["rel_base"]=O00OOOO000O0OOO0O *1.0 /OOOO0O0OO0OOO0000 .data ["rows_count"]#line:642
            OO0O0OO00O00O000O ["s_up"]=O0000OOO0OO000000 #line:643
            OO0O0OO00O00O000O ["s_down"]=O00O0OO00OO00O0O0 #line:644
            OO0O0OO00O00O000O ["s_any_up"]=OOOOOOO0OOO00O000 #line:645
            OO0O0OO00O00O000O ["s_any_down"]=O00O0OOO00OO00000 #line:646
            OO0O0OO00O00O000O ["max"]=max (OOOO0O0O0O000OOOO )#line:647
            OO0O0OO00O00O000O ["min"]=min (OOOO0O0O0O000OOOO )#line:648
            if OOOO0O0OO0OOO0000 .verbosity ['debug']:#line:649
                OO0O0OO00O00O000O ["rel_max"]=max (OOOO0O0O0O000OOOO )*1.0 /OOOO0O0OO0OOO0000 .data ["rows_count"]#line:650
                OO0O0OO00O00O000O ["rel_min"]=min (OOOO0O0O0O000OOOO )*1.0 /OOOO0O0OO0OOO0000 .data ["rows_count"]#line:651
            if sum (OOOO0O0O0O000OOOO )>0 :#line:652
                OO0O0OO00O00O000O ["rel_max"]=max (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO )#line:653
                OO0O0OO00O00O000O ["rel_min"]=min (OOOO0O0O0O000OOOO )*1.0 /sum (OOOO0O0O0O000OOOO )#line:654
            else :#line:655
                OO0O0OO00O00O000O ["rel_max"]=0 #line:656
                OO0O0OO00O00O000O ["rel_min"]=0 #line:657
            OO0O0OO00O00O000O ["hist"]=OOOO0O0O0O000OOOO #line:658
            if O0OO00OOO00OO0O00 :#line:659
                OO0O0OO00O00O000O ["aad"]=OO00O0000OO0OOOO0 #line:660
                OO0O0OO00O00O000O ["hist_full"]=O0OOO0O0OOO00O00O #line:661
                OO0O0OO00O00O000O ["rel_hist"]=[O0O00O0OO00OO0OOO /sum (OOOO0O0O0O000OOOO )for O0O00O0OO00OO0OOO in OOOO0O0O0O000OOOO ]#line:662
                OO0O0OO00O00O000O ["rel_hist_full"]=[O000O0OO0O000OOO0 /sum (O0OOO0O0OOO00O00O )for O000O0OO0O000OOO0 in O0OOO0O0OOO00O00O ]#line:663
        if OOOO0O0OO0OOO0000 .verbosity ['debug']:#line:664
            print ("Info: base: "+str (O00OOOO000O0OOO0O )+", hist: "+str (OOOO0O0O0O000OOOO )+", max: "+str (max (OOOO0O0O0O000OOOO ))+", min: "+str (min (OOOO0O0O0O000OOOO ))+", s_up: "+str (O0000OOO0OO000000 )+", s_down: "+str (O00O0OO00OO00O0O0 ))#line:665
        return O0OO000OOOOO000OO ,OO0O0OO00O00O000O #line:666
    def _verifyUIC (O0O00OO0OOOOO00O0 ,_OO00000O000000O0O ):#line:668
        OOOOOO000O0O0O0O0 ={}#line:669
        O00OO000OOO0O00OO =0 #line:670
        for O00OO0OOO00O000O0 in O0O00OO0OOOOO00O0 .task_actinfo ['cedents']:#line:671
            OOOOOO000O0O0O0O0 [O00OO0OOO00O000O0 ['cedent_type']]=O00OO0OOO00O000O0 ['filter_value']#line:672
            O00OO000OOO0O00OO =O00OO000OOO0O00OO +1 #line:673
        if O0O00OO0OOOOO00O0 .verbosity ['debug']:#line:674
            print (O00OO0OOO00O000O0 ['cedent_type']+" : "+str (O00OO0OOO00O000O0 ['filter_value']))#line:675
        O00O00OO000000000 =O0O00OO0OOOOO00O0 ._bitcount (_OO00000O000000O0O )#line:676
        OOOO0O0OOO0OOO000 =[]#line:677
        OOO00OO0OO0OOO0OO =0 #line:678
        OOO0O0OO00OO0O00O =0 #line:679
        OOO000O000000OO0O =0 #line:680
        OO00O0O000000O0O0 =[]#line:681
        O0000O0O000OOO00O =[]#line:682
        if ('aad_weights'in O0O00OO0OOOOO00O0 .quantifiers ):#line:683
            OO00O0O000000O0O0 =O0O00OO0OOOOO00O0 .quantifiers .get ('aad_weights')#line:684
            OOO0O0OO00OO0O00O =1 #line:685
        OO0O0000O000OOO0O =O0O00OO0OOOOO00O0 .data ["dm"][O0O00OO0OOOOO00O0 .data ["varname"].index (O0O00OO0OOOOO00O0 .kwargs .get ('target'))]#line:686
        for OOO0OO0000O0O00O0 in range (len (OO0O0000O000OOO0O )):#line:687
            OOO000OOOO0O0O0OO =OOO00OO0OO0OOO0OO #line:689
            OOO00OO0OO0OOO0OO =O0O00OO0OOOOO00O0 ._bitcount (_OO00000O000000O0O &OO0O0000O000OOO0O [OOO0OO0000O0O00O0 ])#line:690
            OOOO0O0OOO0OOO000 .append (OOO00OO0OO0OOO0OO )#line:691
            OOOOO00O0OOOO0000 =O0O00OO0OOOOO00O0 ._bitcount (OOOOOO000O0O0O0O0 ['cond']&OO0O0000O000OOO0O [OOO0OO0000O0O00O0 ])#line:693
            O0000O0O000OOO00O .append (OOOOO00O0OOOO0000 )#line:694
        OOOO0OOOO0OOO0OO0 =0 #line:696
        OO0000OO0OO0O000O =0 #line:697
        if (OOO0O0OO00OO0O00O &sum (OOOO0O0OOO0OOO000 )>0 ):#line:698
            for OOO0OO0000O0O00O0 in range (len (OO0O0000O000OOO0O )):#line:699
                if O0000O0O000OOO00O [OOO0OO0000O0O00O0 ]>0 :#line:700
                    if OOOO0O0OOO0OOO000 [OOO0OO0000O0O00O0 ]/sum (OOOO0O0OOO0OOO000 )>O0000O0O000OOO00O [OOO0OO0000O0O00O0 ]/sum (O0000O0O000OOO00O ):#line:701
                        OOO000O000000OO0O +=OO00O0O000000O0O0 [OOO0OO0000O0O00O0 ]*((OOOO0O0OOO0OOO000 [OOO0OO0000O0O00O0 ]/sum (OOOO0O0OOO0OOO000 ))/(O0000O0O000OOO00O [OOO0OO0000O0O00O0 ]/sum (O0000O0O000OOO00O ))-1 )#line:702
                if OO00O0O000000O0O0 [OOO0OO0000O0O00O0 ]>0 :#line:703
                    OOOO0OOOO0OOO0OO0 +=OOOO0O0OOO0OOO000 [OOO0OO0000O0O00O0 ]#line:704
                    OO0000OO0OO0O000O +=O0000O0O000OOO00O [OOO0OO0000O0O00O0 ]#line:705
        O0O0O0OO000O0OO00 =0 #line:706
        if sum (OOOO0O0OOO0OOO000 )>0 and OO0000OO0OO0O000O >0 :#line:707
            O0O0O0OO000O0OO00 =(OOOO0OOOO0OOO0OO0 /sum (OOOO0O0OOO0OOO000 ))/(OO0000OO0OO0O000O /sum (O0000O0O000OOO00O ))#line:708
        OOOO0O00000OOOOO0 =True #line:712
        for OOOOO0000O000O000 in O0O00OO0OOOOO00O0 .quantifiers .keys ():#line:713
            if OOOOO0000O000O000 .upper ()=='BASE':#line:714
                OOOO0O00000OOOOO0 =OOOO0O00000OOOOO0 and (O0O00OO0OOOOO00O0 .quantifiers .get (OOOOO0000O000O000 )<=O00O00OO000000000 )#line:715
            if OOOOO0000O000O000 .upper ()=='RELBASE':#line:716
                OOOO0O00000OOOOO0 =OOOO0O00000OOOOO0 and (O0O00OO0OOOOO00O0 .quantifiers .get (OOOOO0000O000O000 )<=O00O00OO000000000 *1.0 /O0O00OO0OOOOO00O0 .data ["rows_count"])#line:717
            if OOOOO0000O000O000 .upper ()=='AAD_SCORE':#line:718
                OOOO0O00000OOOOO0 =OOOO0O00000OOOOO0 and (O0O00OO0OOOOO00O0 .quantifiers .get (OOOOO0000O000O000 )<=OOO000O000000OO0O )#line:719
            if OOOOO0000O000O000 .upper ()=='RELEVANT_CAT_BASE':#line:720
                OOOO0O00000OOOOO0 =OOOO0O00000OOOOO0 and (O0O00OO0OOOOO00O0 .quantifiers .get (OOOOO0000O000O000 )<=OOOO0OOOO0OOO0OO0 )#line:721
            if OOOOO0000O000O000 .upper ()=='RELEVANT_BASE_LIFT':#line:722
                OOOO0O00000OOOOO0 =OOOO0O00000OOOOO0 and (O0O00OO0OOOOO00O0 .quantifiers .get (OOOOO0000O000O000 )<=O0O0O0OO000O0OO00 )#line:723
        OO00OO00O00O00O0O ={}#line:724
        if OOOO0O00000OOOOO0 ==True :#line:725
            O0O00OO0OOOOO00O0 .stats ['total_valid']+=1 #line:726
            OO00OO00O00O00O0O ["base"]=O00O00OO000000000 #line:727
            OO00OO00O00O00O0O ["rel_base"]=O00O00OO000000000 *1.0 /O0O00OO0OOOOO00O0 .data ["rows_count"]#line:728
            OO00OO00O00O00O0O ["hist"]=OOOO0O0OOO0OOO000 #line:729
            OO00OO00O00O00O0O ["aad_score"]=OOO000O000000OO0O #line:730
            OO00OO00O00O00O0O ["hist_cond"]=O0000O0O000OOO00O #line:731
            OO00OO00O00O00O0O ["rel_hist"]=[OOOO0O0OOOO00O0O0 /sum (OOOO0O0OOO0OOO000 )for OOOO0O0OOOO00O0O0 in OOOO0O0OOO0OOO000 ]#line:732
            OO00OO00O00O00O0O ["rel_hist_cond"]=[OO0O0O0O0O0000OOO /sum (O0000O0O000OOO00O )for OO0O0O0O0O0000OOO in O0000O0O000OOO00O ]#line:733
            OO00OO00O00O00O0O ["relevant_base_lift"]=O0O0O0OO000O0OO00 #line:734
            OO00OO00O00O00O0O ["relevant_cat_base"]=OOOO0OOOO0OOO0OO0 #line:735
            OO00OO00O00O00O0O ["relevant_cat_base_full"]=OO0000OO0OO0O000O #line:736
        return OOOO0O00000OOOOO0 ,OO00OO00O00O00O0O #line:737
    def _verify4ft (OOO00O0OO00OOOOOO ,_OO0OO000O0000OO00 ,_trace_cedent =None ,_traces =None ):#line:739
        O00OO0000O00O0O0O ={}#line:740
        O00OOO0O00O0O0000 =0 #line:741
        for OOO0O000OO000O000 in OOO00O0OO00OOOOOO .task_actinfo ['cedents']:#line:742
            O00OO0000O00O0O0O [OOO0O000OO000O000 ['cedent_type']]=OOO0O000OO000O000 ['filter_value']#line:743
            O00OOO0O00O0O0000 =O00OOO0O00O0O0000 +1 #line:744
        OOOOOO00OOO0000O0 =OOO00O0OO00OOOOOO ._bitcount (O00OO0000O00O0O0O ['ante']&O00OO0000O00O0O0O ['succ']&O00OO0000O00O0O0O ['cond'])#line:745
        O00OO00OO0O0OOOO0 =None #line:746
        O00OO00OO0O0OOOO0 =0 #line:747
        if OOOOOO00OOO0000O0 >0 :#line:748
            O00OO00OO0O0OOOO0 =OOO00O0OO00OOOOOO ._bitcount (O00OO0000O00O0O0O ['ante']&O00OO0000O00O0O0O ['succ']&O00OO0000O00O0O0O ['cond'])*1.0 /OOO00O0OO00OOOOOO ._bitcount (O00OO0000O00O0O0O ['ante']&O00OO0000O00O0O0O ['cond'])#line:749
        OO0O00OO0OOOOO00O =1 <<OOO00O0OO00OOOOOO .data ["rows_count"]#line:751
        O0O00O0OO0O0OOO0O =OOO00O0OO00OOOOOO ._bitcount (O00OO0000O00O0O0O ['ante']&O00OO0000O00O0O0O ['succ']&O00OO0000O00O0O0O ['cond'])#line:752
        O000OOOO0O000O0OO =OOO00O0OO00OOOOOO ._bitcount (O00OO0000O00O0O0O ['ante']&~(OO0O00OO0OOOOO00O |O00OO0000O00O0O0O ['succ'])&O00OO0000O00O0O0O ['cond'])#line:753
        OOO0O000OO000O000 =OOO00O0OO00OOOOOO ._bitcount (~(OO0O00OO0OOOOO00O |O00OO0000O00O0O0O ['ante'])&O00OO0000O00O0O0O ['succ']&O00OO0000O00O0O0O ['cond'])#line:754
        OOOOOO0OOOO0O0O0O =OOO00O0OO00OOOOOO ._bitcount (~(OO0O00OO0OOOOO00O |O00OO0000O00O0O0O ['ante'])&~(OO0O00OO0OOOOO00O |O00OO0000O00O0O0O ['succ'])&O00OO0000O00O0O0O ['cond'])#line:755
        OOOO00O0O000O0O00 =0 #line:756
        O0O0O0O000OOOO00O =0 #line:757
        if (O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO )*(O0O00O0OO0O0OOO0O +OOO0O000OO000O000 )>0 :#line:758
            OOOO00O0O000O0O00 =O0O00O0OO0O0OOO0O *(O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO +OOO0O000OO000O000 +OOOOOO0OOOO0O0O0O )/(O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO )/(O0O00O0OO0O0OOO0O +OOO0O000OO000O000 )-1 #line:759
            O0O0O0O000OOOO00O =OOOO00O0O000O0O00 +1 #line:760
        else :#line:761
            OOOO00O0O000O0O00 =None #line:762
            O0O0O0O000OOOO00O =None #line:763
        O0OOO00000O0O0OOO =0 #line:764
        if (O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO )*(O0O00O0OO0O0OOO0O +OOO0O000OO000O000 )>0 :#line:765
            O0OOO00000O0O0OOO =1 -O0O00O0OO0O0OOO0O *(O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO +OOO0O000OO000O000 +OOOOOO0OOOO0O0O0O )/(O0O00O0OO0O0OOO0O +O000OOOO0O000O0OO )/(O0O00O0OO0O0OOO0O +OOO0O000OO000O000 )#line:766
        else :#line:767
            O0OOO00000O0O0OOO =None #line:768
        O0OOO0000O0000O0O =True #line:769
        for OO000OOOOOO0000O0 in OOO00O0OO00OOOOOO .quantifiers .keys ():#line:770
            if OO000OOOOOO0000O0 .upper ()=='BASE':#line:771
                O0OOO0000O0000O0O =O0OOO0000O0000O0O and (OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )<=OOOOOO00OOO0000O0 )#line:772
            if OO000OOOOOO0000O0 .upper ()=='RELBASE':#line:773
                O0OOO0000O0000O0O =O0OOO0000O0000O0O and (OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )<=OOOOOO00OOO0000O0 *1.0 /OOO00O0OO00OOOOOO .data ["rows_count"])#line:774
            if (OO000OOOOOO0000O0 .upper ()=='PIM')or (OO000OOOOOO0000O0 .upper ()=='CONF'):#line:775
                O0OOO0000O0000O0O =O0OOO0000O0000O0O and (OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )<=O00OO00OO0O0OOOO0 )#line:776
            if OO000OOOOOO0000O0 .upper ()=='AAD':#line:777
                if OOOO00O0O000O0O00 !=None :#line:778
                    O0OOO0000O0000O0O =O0OOO0000O0000O0O and (OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )<=OOOO00O0O000O0O00 )#line:779
                else :#line:780
                    O0OOO0000O0000O0O =False #line:781
            if OO000OOOOOO0000O0 .upper ()=='BAD':#line:782
                if O0OOO00000O0O0OOO !=None :#line:783
                    O0OOO0000O0000O0O =O0OOO0000O0000O0O and (OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )<=O0OOO00000O0O0OOO )#line:784
                else :#line:785
                    O0OOO0000O0000O0O =False #line:786
            if OO000OOOOOO0000O0 .upper ()=='LAMBDA'or OO000OOOOOO0000O0 .upper ()=='FN':#line:787
                O0O0OO00OOOOO0000 =OOO00O0OO00OOOOOO .quantifiers .get (OO000OOOOOO0000O0 )#line:788
                OOOO000OO000O0OOO =[O0O00O0OO0O0OOO0O ,O000OOOO0O000O0OO ,OOO0O000OO000O000 ,OOOOOO0OOOO0O0O0O ]#line:789
                OOOOOO0O0OO000O0O =O0O0OO00OOOOO0000 .__code__ .co_argcount #line:790
                if OOOOOO0O0OO000O0O ==1 :#line:792
                    O0OOO0000O0000O0O =O0OOO0000O0000O0O and O0O0OO00OOOOO0000 (OOOO000OO000O0OOO )#line:793
                elif OOOOOO0O0OO000O0O ==2 :#line:794
                    OOOOO0OOO000OO000 ={}#line:795
                    OO00O0000OO00O0OO ={}#line:796
                    OO00O0000OO00O0OO ["varname"]=OOO00O0OO00OOOOOO .data ["varname"]#line:797
                    OO00O0000OO00O0OO ["catnames"]=OOO00O0OO00OOOOOO .data ["catnames"]#line:798
                    OOOOO0OOO000OO000 ['datalabels']=OO00O0000OO00O0OO #line:799
                    OOOOO0OOO000OO000 ['trace_cedent']=_trace_cedent #line:800
                    OOOOO0OOO000OO000 ['traces']=_traces #line:801
                    O0OOO0000O0000O0O =O0OOO0000O0000O0O and O0O0OO00OOOOO0000 (OOOO000OO000O0OOO ,OOOOO0OOO000OO000 )#line:804
                else :#line:805
                    print (f"Unsupported number of arguments for lambda function ({OOOOOO0O0OO000O0O} for procedure SD4ft-Miner")#line:806
            OOO00OOOOOO0000OO ={}#line:807
        if O0OOO0000O0000O0O ==True :#line:808
            OOO00O0OO00OOOOOO .stats ['total_valid']+=1 #line:809
            OOO00OOOOOO0000OO ["base"]=OOOOOO00OOO0000O0 #line:810
            OOO00OOOOOO0000OO ["rel_base"]=OOOOOO00OOO0000O0 *1.0 /OOO00O0OO00OOOOOO .data ["rows_count"]#line:811
            OOO00OOOOOO0000OO ["conf"]=O00OO00OO0O0OOOO0 #line:812
            OOO00OOOOOO0000OO ["aad"]=OOOO00O0O000O0O00 #line:813
            OOO00OOOOOO0000OO ["bad"]=O0OOO00000O0O0OOO #line:814
            OOO00OOOOOO0000OO ["fourfold"]=[O0O00O0OO0O0OOO0O ,O000OOOO0O000O0OO ,OOO0O000OO000O000 ,OOOOOO0OOOO0O0O0O ]#line:815
        return O0OOO0000O0000O0O ,OOO00OOOOOO0000OO #line:816
    def _verifysd4ft (OOOO00OO0O0OOOO0O ,_OOOO0OO0OO00O0OO0 ):#line:818
        OOOOO00OOO0O0OOOO ={}#line:819
        O00OO0O0000O00OO0 =0 #line:820
        for O0000O0000OOO0O00 in OOOO00OO0O0OOOO0O .task_actinfo ['cedents']:#line:821
            OOOOO00OOO0O0OOOO [O0000O0000OOO0O00 ['cedent_type']]=O0000O0000OOO0O00 ['filter_value']#line:822
            O00OO0O0000O00OO0 =O00OO0O0000O00OO0 +1 #line:823
        OOO0O0OOO0O0OOOO0 =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:824
        O0O00OOO00O0OO00O =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:825
        O00OO000OO0O0O0O0 =None #line:826
        O00O0O0O0000O0OO0 =0 #line:827
        O0O0OOOOO0O0OOO00 =0 #line:828
        if OOO0O0OOO0O0OOOO0 >0 :#line:829
            O00O0O0O0000O0OO0 =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])*1.0 /OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:830
        if O0O00OOO00O0OO00O >0 :#line:831
            O0O0OOOOO0O0OOO00 =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])*1.0 /OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:832
        OO0O0000O00OOOOOO =1 <<OOOO00OO0O0OOOO0O .data ["rows_count"]#line:834
        OO0O00000000OOOO0 =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:835
        OO0OO00OOOOOO0O00 =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['succ'])&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:836
        OOOO00OOOOO0OO0O0 =OOOO00OO0O0OOOO0O ._bitcount (~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['ante'])&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:837
        O0O000OO00O0O0O0O =OOOO00OO0O0OOOO0O ._bitcount (~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['ante'])&~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['succ'])&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['frst'])#line:838
        O000O0000OO0O000O =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:839
        O0OOOO000OOOOOO0O =OOOO00OO0O0OOOO0O ._bitcount (OOOOO00OOO0O0OOOO ['ante']&~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['succ'])&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:840
        OO00OOOO00O00000O =OOOO00OO0O0OOOO0O ._bitcount (~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['ante'])&OOOOO00OOO0O0OOOO ['succ']&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:841
        OOOOO00O0OOOOOO0O =OOOO00OO0O0OOOO0O ._bitcount (~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['ante'])&~(OO0O0000O00OOOOOO |OOOOO00OOO0O0OOOO ['succ'])&OOOOO00OOO0O0OOOO ['cond']&OOOOO00OOO0O0OOOO ['scnd'])#line:842
        O0OO000OOOOOO00OO =True #line:843
        for O00O00O00O00O0O0O in OOOO00OO0O0OOOO0O .quantifiers .keys ():#line:844
            if (O00O00O00O00O0O0O .upper ()=='FRSTBASE')|(O00O00O00O00O0O0O .upper ()=='BASE1'):#line:845
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=OOO0O0OOO0O0OOOO0 )#line:846
            if (O00O00O00O00O0O0O .upper ()=='SCNDBASE')|(O00O00O00O00O0O0O .upper ()=='BASE2'):#line:847
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O0O00OOO00O0OO00O )#line:848
            if (O00O00O00O00O0O0O .upper ()=='FRSTRELBASE')|(O00O00O00O00O0O0O .upper ()=='RELBASE1'):#line:849
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=OOO0O0OOO0O0OOOO0 *1.0 /OOOO00OO0O0OOOO0O .data ["rows_count"])#line:850
            if (O00O00O00O00O0O0O .upper ()=='SCNDRELBASE')|(O00O00O00O00O0O0O .upper ()=='RELBASE2'):#line:851
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O0O00OOO00O0OO00O *1.0 /OOOO00OO0O0OOOO0O .data ["rows_count"])#line:852
            if (O00O00O00O00O0O0O .upper ()=='FRSTPIM')|(O00O00O00O00O0O0O .upper ()=='PIM1')|(O00O00O00O00O0O0O .upper ()=='FRSTCONF')|(O00O00O00O00O0O0O .upper ()=='CONF1'):#line:853
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O00O0O0O0000O0OO0 )#line:854
            if (O00O00O00O00O0O0O .upper ()=='SCNDPIM')|(O00O00O00O00O0O0O .upper ()=='PIM2')|(O00O00O00O00O0O0O .upper ()=='SCNDCONF')|(O00O00O00O00O0O0O .upper ()=='CONF2'):#line:855
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O0O0OOOOO0O0OOO00 )#line:856
            if (O00O00O00O00O0O0O .upper ()=='DELTAPIM')|(O00O00O00O00O0O0O .upper ()=='DELTACONF'):#line:857
                O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O00O0O0O0000O0OO0 -O0O0OOOOO0O0OOO00 )#line:858
            if (O00O00O00O00O0O0O .upper ()=='RATIOPIM')|(O00O00O00O00O0O0O .upper ()=='RATIOCONF'):#line:859
                if (O0O0OOOOO0O0OOO00 >0 ):#line:860
                    O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )<=O00O0O0O0000O0OO0 *1.0 /O0O0OOOOO0O0OOO00 )#line:861
                else :#line:862
                    O0OO000OOOOOO00OO =False #line:863
            if (O00O00O00O00O0O0O .upper ()=='RATIOPIM_LEQ')|(O00O00O00O00O0O0O .upper ()=='RATIOCONF_LEQ'):#line:864
                if (O0O0OOOOO0O0OOO00 >0 ):#line:865
                    O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and (OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )>=O00O0O0O0000O0OO0 *1.0 /O0O0OOOOO0O0OOO00 )#line:866
                else :#line:867
                    O0OO000OOOOOO00OO =False #line:868
            if O00O00O00O00O0O0O .upper ()=='LAMBDA'or O00O00O00O00O0O0O .upper ()=='FN':#line:869
                O0OOOOO0O00O0OO0O =OOOO00OO0O0OOOO0O .quantifiers .get (O00O00O00O00O0O0O )#line:870
                OOOOO0O0OOO000O00 =O0OOOOO0O00O0OO0O .func_code .co_argcount #line:871
                O0O00O0O0OOO0OOOO =[OO0O00000000OOOO0 ,OO0OO00OOOOOO0O00 ,OOOO00OOOOO0OO0O0 ,O0O000OO00O0O0O0O ]#line:872
                OOO0O0OO00O0O0OO0 =[O000O0000OO0O000O ,O0OOOO000OOOOOO0O ,OO00OOOO00O00000O ,OOOOO00O0OOOOOO0O ]#line:873
                if OOOOO0O0OOO000O00 ==2 :#line:874
                    O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and O0OOOOO0O00O0OO0O (O0O00O0O0OOO0OOOO ,OOO0O0OO00O0O0OO0 )#line:875
                elif OOOOO0O0OOO000O00 ==3 :#line:876
                    O0OO000OOOOOO00OO =O0OO000OOOOOO00OO and O0OOOOO0O00O0OO0O (O0O00O0O0OOO0OOOO ,OOO0O0OO00O0O0OO0 ,None )#line:877
                else :#line:878
                    print (f"Unsupported number of arguments for lambda function ({OOOOO0O0OOO000O00} for procedure SD4ft-Miner")#line:879
        OOO000OOO00OOOOOO ={}#line:880
        if O0OO000OOOOOO00OO ==True :#line:881
            OOOO00OO0O0OOOO0O .stats ['total_valid']+=1 #line:882
            OOO000OOO00OOOOOO ["base1"]=OOO0O0OOO0O0OOOO0 #line:883
            OOO000OOO00OOOOOO ["base2"]=O0O00OOO00O0OO00O #line:884
            OOO000OOO00OOOOOO ["rel_base1"]=OOO0O0OOO0O0OOOO0 *1.0 /OOOO00OO0O0OOOO0O .data ["rows_count"]#line:885
            OOO000OOO00OOOOOO ["rel_base2"]=O0O00OOO00O0OO00O *1.0 /OOOO00OO0O0OOOO0O .data ["rows_count"]#line:886
            OOO000OOO00OOOOOO ["conf1"]=O00O0O0O0000O0OO0 #line:887
            OOO000OOO00OOOOOO ["conf2"]=O0O0OOOOO0O0OOO00 #line:888
            OOO000OOO00OOOOOO ["deltaconf"]=O00O0O0O0000O0OO0 -O0O0OOOOO0O0OOO00 #line:889
            if (O0O0OOOOO0O0OOO00 >0 ):#line:890
                OOO000OOO00OOOOOO ["ratioconf"]=O00O0O0O0000O0OO0 *1.0 /O0O0OOOOO0O0OOO00 #line:891
            else :#line:892
                OOO000OOO00OOOOOO ["ratioconf"]=None #line:893
            OOO000OOO00OOOOOO ["fourfold1"]=[OO0O00000000OOOO0 ,OO0OO00OOOOOO0O00 ,OOOO00OOOOO0OO0O0 ,O0O000OO00O0O0O0O ]#line:894
            OOO000OOO00OOOOOO ["fourfold2"]=[O000O0000OO0O000O ,O0OOOO000OOOOOO0O ,OO00OOOO00O00000O ,OOOOO00O0OOOOOO0O ]#line:895
        return O0OO000OOOOOO00OO ,OOO000OOO00OOOOOO #line:896
    def _verify_opt (OO0O00O00O000O0OO ,OO00O0OOOOO00OO00 ,OOOOO00OO0O0OO0O0 ):#line:899
        OO0O00O00O000O0OO .stats ['total_ver']+=1 #line:900
        OOOOO00OOO0O000O0 =False #line:901
        if not (OO00O0OOOOO00OO00 ['optim'].get ('only_con')):#line:902
            return False #line:903
        if OO0O00O00O000O0OO .verbosity ['debug']:#line:904
            print (OO0O00O00O000O0OO .options ['optimizations'])#line:905
        if not (OO0O00O00O000O0OO .options ['optimizations']):#line:906
            if OO0O00O00O000O0OO .verbosity ['debug']:#line:907
                print ("NO OPTS")#line:908
            return False #line:909
        if OO0O00O00O000O0OO .verbosity ['debug']:#line:910
            print ("OPTS")#line:911
        OOOO00000O0OO0OOO ={}#line:912
        for OO00O00O0OOOO0O0O in OO0O00O00O000O0OO .task_actinfo ['cedents']:#line:913
            if OO0O00O00O000O0OO .verbosity ['debug']:#line:914
                print (OO00O00O0OOOO0O0O ['cedent_type'])#line:915
            OOOO00000O0OO0OOO [OO00O00O0OOOO0O0O ['cedent_type']]=OO00O00O0OOOO0O0O ['filter_value']#line:916
            if OO0O00O00O000O0OO .verbosity ['debug']:#line:917
                print (OO00O00O0OOOO0O0O ['cedent_type']+" : "+str (OO00O00O0OOOO0O0O ['filter_value']))#line:918
        OOOOO0OOOO00O0O0O =1 <<OO0O00O00O000O0OO .data ["rows_count"]#line:919
        OOO0O0OO0000O0O00 =OOOOO0OOOO00O0O0O -1 #line:920
        O00O00OOOO00OOO00 =""#line:921
        O0OOOO0000OOOO00O =0 #line:922
        if (OOOO00000O0OO0OOO .get ('ante')!=None ):#line:923
            OOO0O0OO0000O0O00 =OOO0O0OO0000O0O00 &OOOO00000O0OO0OOO ['ante']#line:924
        if (OOOO00000O0OO0OOO .get ('succ')!=None ):#line:925
            OOO0O0OO0000O0O00 =OOO0O0OO0000O0O00 &OOOO00000O0OO0OOO ['succ']#line:926
        if (OOOO00000O0OO0OOO .get ('cond')!=None ):#line:927
            OOO0O0OO0000O0O00 =OOO0O0OO0000O0O00 &OOOO00000O0OO0OOO ['cond']#line:928
        O0OOO0OOO00O0OO0O =None #line:929
        if (OO0O00O00O000O0OO .proc =='CFMiner')|(OO0O00O00O000O0OO .proc =='4ftMiner')|(OO0O00O00O000O0OO .proc =='UICMiner'):#line:930
            O000O0OO00O000OO0 =OO0O00O00O000O0OO ._bitcount (OOO0O0OO0000O0O00 )#line:931
            if not (OO0O00O00O000O0OO ._opt_base ==None ):#line:932
                if not (OO0O00O00O000O0OO ._opt_base <=O000O0OO00O000OO0 ):#line:933
                    OOOOO00OOO0O000O0 =True #line:934
            if not (OO0O00O00O000O0OO ._opt_relbase ==None ):#line:935
                if not (OO0O00O00O000O0OO ._opt_relbase <=O000O0OO00O000OO0 *1.0 /OO0O00O00O000O0OO .data ["rows_count"]):#line:936
                    OOOOO00OOO0O000O0 =True #line:937
        if (OO0O00O00O000O0OO .proc =='SD4ftMiner'):#line:938
            O000O0OO00O000OO0 =OO0O00O00O000O0OO ._bitcount (OOO0O0OO0000O0O00 )#line:939
            if (not (OO0O00O00O000O0OO ._opt_base1 ==None ))&(not (OO0O00O00O000O0OO ._opt_base2 ==None )):#line:940
                if not (max (OO0O00O00O000O0OO ._opt_base1 ,OO0O00O00O000O0OO ._opt_base2 )<=O000O0OO00O000OO0 ):#line:941
                    OOOOO00OOO0O000O0 =True #line:942
            if (not (OO0O00O00O000O0OO ._opt_relbase1 ==None ))&(not (OO0O00O00O000O0OO ._opt_relbase2 ==None )):#line:943
                if not (max (OO0O00O00O000O0OO ._opt_relbase1 ,OO0O00O00O000O0OO ._opt_relbase2 )<=O000O0OO00O000OO0 *1.0 /OO0O00O00O000O0OO .data ["rows_count"]):#line:944
                    OOOOO00OOO0O000O0 =True #line:945
        return OOOOO00OOO0O000O0 #line:947
    def _print (OOO0O00O0000OO0OO ,OOOO000OO0OO00O00 ,_O0000OOO0OO0OO000 ,_OO000O000OO0OOOOO ):#line:950
        if (len (_O0000OOO0OO0OO000 ))!=len (_OO000O000OO0OOOOO ):#line:951
            print ("DIFF IN LEN for following cedent : "+str (len (_O0000OOO0OO0OO000 ))+" vs "+str (len (_OO000O000OO0OOOOO )))#line:952
            print ("trace cedent : "+str (_O0000OOO0OO0OO000 )+", traces "+str (_OO000O000OO0OOOOO ))#line:953
        O000OO0O0OOO0OOO0 =''#line:954
        O000OO0O0OOOO000O ={}#line:955
        OOO00OO0O0O0000O0 =[]#line:956
        for OOO0OOOO0OOOO0O0O in range (len (_O0000OOO0OO0OO000 )):#line:957
            OOOOO0OOO0O00O000 =OOO0O00O0000OO0OO .data ["varname"].index (OOOO000OO0OO00O00 ['defi'].get ('attributes')[_O0000OOO0OO0OO000 [OOO0OOOO0OOOO0O0O ]].get ('name'))#line:958
            O000OO0O0OOO0OOO0 =O000OO0O0OOO0OOO0 +OOO0O00O0000OO0OO .data ["varname"][OOOOO0OOO0O00O000 ]+'('#line:959
            OOO00OO0O0O0000O0 .append (OOOOO0OOO0O00O000 )#line:960
            O0O0O00O0000O0000 =[]#line:961
            for OOO00OO0OO0OO0O0O in _OO000O000OO0OOOOO [OOO0OOOO0OOOO0O0O ]:#line:962
                O000OO0O0OOO0OOO0 =O000OO0O0OOO0OOO0 +str (OOO0O00O0000OO0OO .data ["catnames"][OOOOO0OOO0O00O000 ][OOO00OO0OO0OO0O0O ])+" "#line:963
                O0O0O00O0000O0000 .append (str (OOO0O00O0000OO0OO .data ["catnames"][OOOOO0OOO0O00O000 ][OOO00OO0OO0OO0O0O ]))#line:964
            O000OO0O0OOO0OOO0 =O000OO0O0OOO0OOO0 [:-1 ]+')'#line:965
            O000OO0O0OOOO000O [OOO0O00O0000OO0OO .data ["varname"][OOOOO0OOO0O00O000 ]]=O0O0O00O0000O0000 #line:966
            if OOO0OOOO0OOOO0O0O +1 <len (_O0000OOO0OO0OO000 ):#line:967
                O000OO0O0OOO0OOO0 =O000OO0O0OOO0OOO0 +' & '#line:968
        return O000OO0O0OOO0OOO0 ,O000OO0O0OOOO000O ,OOO00OO0O0O0000O0 #line:969
    def _print_hypo (OO00O0O0O0OO00000 ,O0O0O0OO00OO0O0O0 ):#line:971
        OO00O0O0O0OO00000 .print_rule (O0O0O0OO00OO0O0O0 )#line:972
    def _print_rule (OOO00OO00O0O00O00 ,OO0O0O0O0000000O0 ):#line:974
        if OOO00OO00O0O00O00 .verbosity ['print_rules']:#line:975
            print ('Rules info : '+str (OO0O0O0O0000000O0 ['params']))#line:976
            for O00O000OO0OO0O0OO in OOO00OO00O0O00O00 .task_actinfo ['cedents']:#line:977
                print (O00O000OO0OO0O0OO ['cedent_type']+' = '+O00O000OO0OO0O0OO ['generated_string'])#line:978
    def _genvar (OOO0O0O0O0O00OOO0 ,OOOO00OOO00000OOO ,O0O000000O00O00OO ,_O0OO0O000O00O0000 ,_OO00OOOO00O000OO0 ,_OOO0OO0O00OO00000 ,_OOO0O0O0000000OO0 ,_O0000O00OOOOO000O ,_O000OO00O0O0OOOO0 ,_O00O00000OOO00O0O ):#line:980
        _OO00000O00000OOOO =0 #line:981
        _OOO0O0OOO00O0O00O =[]#line:982
        for O00OOO00OOOO00O0O in range (O0O000000O00O00OO ['num_cedent']):#line:983
            if ('force'in O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ]and O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ].get ('force')):#line:985
                _OOO0O0OOO00O0O00O .append (O00OOO00OOOO00O0O )#line:986
        if O0O000000O00O00OO ['num_cedent']>0 :#line:987
            _OO00000O00000OOOO =(_O00O00000OOO00O0O -_O000OO00O0O0OOOO0 )/O0O000000O00O00OO ['num_cedent']#line:988
        if O0O000000O00O00OO ['num_cedent']==0 :#line:989
            if len (OOOO00OOO00000OOO ['cedents_to_do'])>len (OOOO00OOO00000OOO ['cedents']):#line:990
                O000O0000OO000OO0 ,OO0O00O0O0O0OOOOO ,O0O0O0O0OOOOO0000 =OOO0O0O0O0O00OOO0 ._print (O0O000000O00O00OO ,_O0OO0O000O00O0000 ,_OO00OOOO00O000OO0 )#line:991
                O0O000000O00O00OO ['generated_string']=O000O0000OO000OO0 #line:992
                O0O000000O00O00OO ['rule']=OO0O00O0O0O0OOOOO #line:993
                O0O000000O00O00OO ['filter_value']=(1 <<OOO0O0O0O0O00OOO0 .data ["rows_count"])-1 #line:994
                O0O000000O00O00OO ['traces']=[]#line:995
                O0O000000O00O00OO ['trace_cedent']=[]#line:996
                O0O000000O00O00OO ['trace_cedent_asindata']=[]#line:997
                OOOO00OOO00000OOO ['cedents'].append (O0O000000O00O00OO )#line:998
                _O0OO0O000O00O0000 .append (None )#line:999
                OOO0O0O0O0O00OOO0 ._start_cedent (OOOO00OOO00000OOO ,_O000OO00O0O0OOOO0 ,_O00O00000OOO00O0O )#line:1000
                OOOO00OOO00000OOO ['cedents'].pop ()#line:1001
        for O00OOO00OOOO00O0O in range (O0O000000O00O00OO ['num_cedent']):#line:1004
            _OOO0O00OOOO00O0OO =True #line:1005
            for OO00O0O0OOOO0O000 in range (len (_OOO0O0OOO00O0O00O )):#line:1006
                if OO00O0O0OOOO0O000 <O00OOO00OOOO00O0O and OO00O0O0OOOO0O000 not in _O0OO0O000O00O0000 and OO00O0O0OOOO0O000 in _OOO0O0OOO00O0O00O :#line:1007
                    _OOO0O00OOOO00O0OO =False #line:1008
            if (len (_O0OO0O000O00O0000 )==0 or O00OOO00OOOO00O0O >_O0OO0O000O00O0000 [-1 ])and _OOO0O00OOOO00O0OO :#line:1010
                _O0OO0O000O00O0000 .append (O00OOO00OOOO00O0O )#line:1011
                OO0000O0OOO0OO0O0 =OOO0O0O0O0O00OOO0 .data ["varname"].index (O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ].get ('name'))#line:1012
                _O0O0OOO0OOOOOOOOO =O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ].get ('minlen')#line:1013
                _O0O000O0O000OOOO0 =O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ].get ('maxlen')#line:1014
                _OOO00OO0000O0OOOO =O0O000000O00O00OO ['defi'].get ('attributes')[O00OOO00OOOO00O0O ].get ('type')#line:1015
                O0000000OO0O0000O =len (OOO0O0O0O0O00OOO0 .data ["dm"][OO0000O0OOO0OO0O0 ])#line:1016
                _OO00OO00O0O0O0000 =[]#line:1017
                _OO00OOOO00O000OO0 .append (_OO00OO00O0O0O0000 )#line:1018
                _O000O0O00O00OO0O0 =int (0 )#line:1019
                OOO0O0O0O0O00OOO0 ._gencomb (OOOO00OOO00000OOO ,O0O000000O00O00OO ,_O0OO0O000O00O0000 ,_OO00OOOO00O000OO0 ,_OO00OO00O0O0O0000 ,_OOO0OO0O00OO00000 ,_O000O0O00O00OO0O0 ,O0000000OO0O0000O ,_OOO00OO0000O0OOOO ,_OOO0O0O0000000OO0 ,_O0000O00OOOOO000O ,_O0O0OOO0OOOOOOOOO ,_O0O000O0O000OOOO0 ,_O000OO00O0O0OOOO0 +O00OOO00OOOO00O0O *_OO00000O00000OOOO ,_O000OO00O0O0OOOO0 +(O00OOO00OOOO00O0O +1 )*_OO00000O00000OOOO )#line:1020
                _OO00OOOO00O000OO0 .pop ()#line:1021
                _O0OO0O000O00O0000 .pop ()#line:1022
    def _gencomb (O0OOOO000OOOOO000 ,OOO0OO00000O0OOOO ,OO0OOOO000OOO000O ,_OO00O000OOOOOOOO0 ,_O0O00OO00OO000000 ,_OOO0OOOO0OOO0O0O0 ,_OO0OO00O0O0OOO000 ,_OO000O0O0000000OO ,OO0O0O0O0OOO00OO0 ,_OO000O000O00OOOO0 ,_O00O00OOO0O00O000 ,_OOOO0O0O0OO0OOO00 ,_O00000000OOOO0O0O ,_O0OO0O0O00O000O0O ,_OOO0OOOOOO0OO0000 ,_OOO0O00O0OO00O000 ,val_list =None ):#line:1024
        _OOOOOO000OOOOO0O0 =[]#line:1025
        _OOO000OO00O0O0000 =val_list #line:1026
        if _OO000O000O00OOOO0 =="subset":#line:1027
            if len (_OOO0OOOO0OOO0O0O0 )==0 :#line:1028
                _OOOOOO000OOOOO0O0 =range (OO0O0O0O0OOO00OO0 )#line:1029
            else :#line:1030
                _OOOOOO000OOOOO0O0 =range (_OOO0OOOO0OOO0O0O0 [-1 ]+1 ,OO0O0O0O0OOO00OO0 )#line:1031
        elif _OO000O000O00OOOO0 =="seq":#line:1032
            if len (_OOO0OOOO0OOO0O0O0 )==0 :#line:1033
                _OOOOOO000OOOOO0O0 =range (OO0O0O0O0OOO00OO0 -_O00000000OOOO0O0O +1 )#line:1034
            else :#line:1035
                if _OOO0OOOO0OOO0O0O0 [-1 ]+1 ==OO0O0O0O0OOO00OO0 :#line:1036
                    return #line:1037
                OO000OOO0OO00O0O0 =_OOO0OOOO0OOO0O0O0 [-1 ]+1 #line:1038
                _OOOOOO000OOOOO0O0 .append (OO000OOO0OO00O0O0 )#line:1039
        elif _OO000O000O00OOOO0 =="lcut":#line:1040
            if len (_OOO0OOOO0OOO0O0O0 )==0 :#line:1041
                OO000OOO0OO00O0O0 =0 ;#line:1042
            else :#line:1043
                if _OOO0OOOO0OOO0O0O0 [-1 ]+1 ==OO0O0O0O0OOO00OO0 :#line:1044
                    return #line:1045
                OO000OOO0OO00O0O0 =_OOO0OOOO0OOO0O0O0 [-1 ]+1 #line:1046
            _OOOOOO000OOOOO0O0 .append (OO000OOO0OO00O0O0 )#line:1047
        elif _OO000O000O00OOOO0 =="rcut":#line:1048
            if len (_OOO0OOOO0OOO0O0O0 )==0 :#line:1049
                OO000OOO0OO00O0O0 =OO0O0O0O0OOO00OO0 -1 ;#line:1050
            else :#line:1051
                if _OOO0OOOO0OOO0O0O0 [-1 ]==0 :#line:1052
                    return #line:1053
                OO000OOO0OO00O0O0 =_OOO0OOOO0OOO0O0O0 [-1 ]-1 #line:1054
                if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1055
                    print ("Olditem: "+str (_OOO0OOOO0OOO0O0O0 [-1 ])+", Newitem : "+str (OO000OOO0OO00O0O0 ))#line:1056
            _OOOOOO000OOOOO0O0 .append (OO000OOO0OO00O0O0 )#line:1057
        elif _OO000O000O00OOOO0 =="one":#line:1058
            if len (_OOO0OOOO0OOO0O0O0 )==0 :#line:1059
                O0O0O00O0OOOOOOO0 =O0OOOO000OOOOO000 .data ["varname"].index (OO0OOOO000OOO000O ['defi'].get ('attributes')[_OO00O000OOOOOOOO0 [-1 ]].get ('name'))#line:1060
                try :#line:1061
                    OO000OOO0OO00O0O0 =O0OOOO000OOOOO000 .data ["catnames"][O0O0O00O0OOOOOOO0 ].index (OO0OOOO000OOO000O ['defi'].get ('attributes')[_OO00O000OOOOOOOO0 [-1 ]].get ('value'))#line:1062
                except :#line:1063
                    print (f"ERROR: attribute '{OO0OOOO000OOO000O['defi'].get('attributes')[_OO00O000OOOOOOOO0[-1]].get('name')}' has not value '{OO0OOOO000OOO000O['defi'].get('attributes')[_OO00O000OOOOOOOO0[-1]].get('value')}'")#line:1064
                    exit (1 )#line:1065
                _OOOOOO000OOOOO0O0 .append (OO000OOO0OO00O0O0 )#line:1066
                _O00000000OOOO0O0O =1 #line:1067
                _O0OO0O0O00O000O0O =1 #line:1068
            else :#line:1069
                print ("DEBUG: one category should not have more categories")#line:1070
                return #line:1071
        elif _OO000O000O00OOOO0 =="list":#line:1073
            if _OOO000OO00O0O0000 is None :#line:1074
                O0O0O00O0OOOOOOO0 =O0OOOO000OOOOO000 .data ["varname"].index (OO0OOOO000OOO000O ['defi'].get ('attributes')[_OO00O000OOOOOOOO0 [-1 ]].get ('name'))#line:1075
                O0OO00O0O0000000O =None #line:1076
                _O0O0OOO0O00OO000O =[]#line:1077
                try :#line:1078
                    O0000O000O0OOO0O0 =OO0OOOO000OOO000O ['defi'].get ('attributes')[_OO00O000OOOOOOOO0 [-1 ]].get ('value')#line:1079
                    for O0O00O0OOOOO0000O in O0000O000O0OOO0O0 :#line:1080
                        O0OO00O0O0000000O =O0O00O0OOOOO0000O #line:1081
                        OO000OOO0OO00O0O0 =O0OOOO000OOOOO000 .data ["catnames"][O0O0O00O0OOOOOOO0 ].index (O0O00O0OOOOO0000O )#line:1082
                        _O0O0OOO0O00OO000O .append (OO000OOO0OO00O0O0 )#line:1083
                except :#line:1084
                    print (f"ERROR: attribute '{OO0OOOO000OOO000O['defi'].get('attributes')[_OO00O000OOOOOOOO0[-1]].get('name')}' has not value '{O0O00O0OOOOO0000O}'")#line:1086
                    exit (1 )#line:1087
                _OOO000OO00O0O0000 =_O0O0OOO0O00OO000O #line:1088
                _O00000000OOOO0O0O =len (_OOO000OO00O0O0000 )#line:1089
                _O0OO0O0O00O000O0O =len (_OOO000OO00O0O0000 )#line:1090
            _OOOOOO000OOOOO0O0 .append (_OOO000OO00O0O0000 [len (_OOO0OOOO0OOO0O0O0 )])#line:1091
        else :#line:1093
            print ("Attribute type "+_OO000O000O00OOOO0 +" not supported.")#line:1094
            return #line:1095
        if len (_OOOOOO000OOOOO0O0 )>0 :#line:1097
            _O000O0O0OO0O0OO0O =(_OOO0O00O0OO00O000 -_OOO0OOOOOO0OO0000 )/len (_OOOOOO000OOOOO0O0 )#line:1098
        else :#line:1099
            _O000O0O0OO0O0OO0O =0 #line:1100
        _OOOO00OO0000OOOOO =0 #line:1102
        for OOOOO00O0OO0O00O0 in _OOOOOO000OOOOO0O0 :#line:1104
                _OOO0OOOO0OOO0O0O0 .append (OOOOO00O0OO0O00O0 )#line:1105
                _O0O00OO00OO000000 .pop ()#line:1106
                _O0O00OO00OO000000 .append (_OOO0OOOO0OOO0O0O0 )#line:1107
                _OO000OO000OOOOO00 =_OO000O0O0000000OO |O0OOOO000OOOOO000 .data ["dm"][O0OOOO000OOOOO000 .data ["varname"].index (OO0OOOO000OOO000O ['defi'].get ('attributes')[_OO00O000OOOOOOOO0 [-1 ]].get ('name'))][OOOOO00O0OO0O00O0 ]#line:1108
                _OO0000O000OOO0OO0 =1 #line:1109
                if (len (_OO00O000OOOOOOOO0 )<_O00O00OOO0O00O000 ):#line:1110
                    _OO0000O000OOO0OO0 =-1 #line:1111
                    if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1112
                        print ("DEBUG: will not verify, low cedent length")#line:1113
                if (len (_O0O00OO00OO000000 [-1 ])<_O00000000OOOO0O0O ):#line:1114
                    _OO0000O000OOO0OO0 =0 #line:1115
                    if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1116
                        print ("DEBUG: will not verify, low attribute length")#line:1117
                _O0000O00OO0O00O0O =0 #line:1118
                if OO0OOOO000OOO000O ['defi'].get ('type')=='con':#line:1119
                    _O0000O00OO0O00O0O =_OO0OO00O0O0OOO000 &_OO000OO000OOOOO00 #line:1120
                else :#line:1121
                    _O0000O00OO0O00O0O =_OO0OO00O0O0OOO000 |_OO000OO000OOOOO00 #line:1122
                OO0OOOO000OOO000O ['trace_cedent']=_OO00O000OOOOOOOO0 #line:1123
                OO0OOOO000OOO000O ['traces']=_O0O00OO00OO000000 #line:1124
                O0O0O0OO000OO0O0O ,OO0OOOO00000OO0OO ,OO0O00000OO000O00 =O0OOOO000OOOOO000 ._print (OO0OOOO000OOO000O ,_OO00O000OOOOOOOO0 ,_O0O00OO00OO000000 )#line:1125
                OO0OOOO000OOO000O ['generated_string']=O0O0O0OO000OO0O0O #line:1126
                OO0OOOO000OOO000O ['rule']=OO0OOOO00000OO0OO #line:1127
                OO0OOOO000OOO000O ['filter_value']=_O0000O00OO0O00O0O #line:1128
                OO0OOOO000OOO000O ['traces']=copy .deepcopy (_O0O00OO00OO000000 )#line:1129
                OO0OOOO000OOO000O ['trace_cedent']=copy .deepcopy (_OO00O000OOOOOOOO0 )#line:1130
                OO0OOOO000OOO000O ['trace_cedent_asindata']=copy .deepcopy (OO0O00000OO000O00 )#line:1131
                if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1132
                    print (f"TC :{OO0OOOO000OOO000O['trace_cedent_asindata']}")#line:1133
                OOO0OO00000O0OOOO ['cedents'].append (OO0OOOO000OOO000O )#line:1134
                OOOO0O0O0OO000000 =O0OOOO000OOOOO000 ._verify_opt (OOO0OO00000O0OOOO ,OO0OOOO000OOO000O )#line:1135
                if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1136
                    print (f"DEBUG: {OO0OOOO000OOO000O['generated_string']}.")#line:1137
                    print (f"DEBUG: {_OO00O000OOOOOOOO0},{_O00O00OOO0O00O000}.")#line:1138
                    if OOOO0O0O0OO000000 :#line:1139
                        print ("DEBUG: Optimization: cutting")#line:1140
                if not (OOOO0O0O0OO000000 ):#line:1141
                    if _OO0000O000OOO0OO0 ==1 :#line:1142
                        if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1143
                            print ("DEBUG: verifying")#line:1144
                        if len (OOO0OO00000O0OOOO ['cedents_to_do'])==len (OOO0OO00000O0OOOO ['cedents']):#line:1145
                            if O0OOOO000OOOOO000 .proc =='CFMiner':#line:1146
                                O0OO0000000OOO0OO ,OOOO0OOOO0000OO0O =O0OOOO000OOOOO000 ._verifyCF (_O0000O00OO0O00O0O )#line:1147
                            elif O0OOOO000OOOOO000 .proc =='UICMiner':#line:1148
                                O0OO0000000OOO0OO ,OOOO0OOOO0000OO0O =O0OOOO000OOOOO000 ._verifyUIC (_O0000O00OO0O00O0O )#line:1149
                            elif O0OOOO000OOOOO000 .proc =='4ftMiner':#line:1150
                                O0OO0000000OOO0OO ,OOOO0OOOO0000OO0O =O0OOOO000OOOOO000 ._verify4ft (_OO000OO000OOOOO00 ,_OO00O000OOOOOOOO0 ,_O0O00OO00OO000000 )#line:1151
                            elif O0OOOO000OOOOO000 .proc =='SD4ftMiner':#line:1152
                                O0OO0000000OOO0OO ,OOOO0OOOO0000OO0O =O0OOOO000OOOOO000 ._verifysd4ft (_OO000OO000OOOOO00 )#line:1153
                            else :#line:1154
                                print ("Unsupported procedure : "+O0OOOO000OOOOO000 .proc )#line:1155
                                exit (0 )#line:1156
                            if O0OO0000000OOO0OO ==True :#line:1157
                                OOO00O00000OO0O0O ={}#line:1158
                                OOO00O00000OO0O0O ["rule_id"]=O0OOOO000OOOOO000 .stats ['total_valid']#line:1159
                                OOO00O00000OO0O0O ["cedents_str"]={}#line:1160
                                OOO00O00000OO0O0O ["cedents_struct"]={}#line:1161
                                OOO00O00000OO0O0O ['traces']={}#line:1162
                                OOO00O00000OO0O0O ['trace_cedent_taskorder']={}#line:1163
                                OOO00O00000OO0O0O ['trace_cedent_dataorder']={}#line:1164
                                for O000O00OOOO00000O in OOO0OO00000O0OOOO ['cedents']:#line:1165
                                    if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1166
                                        print (O000O00OOOO00000O )#line:1167
                                    OOO00O00000OO0O0O ['cedents_str'][O000O00OOOO00000O ['cedent_type']]=O000O00OOOO00000O ['generated_string']#line:1168
                                    OOO00O00000OO0O0O ['cedents_struct'][O000O00OOOO00000O ['cedent_type']]=O000O00OOOO00000O ['rule']#line:1169
                                    OOO00O00000OO0O0O ['traces'][O000O00OOOO00000O ['cedent_type']]=O000O00OOOO00000O ['traces']#line:1170
                                    OOO00O00000OO0O0O ['trace_cedent_taskorder'][O000O00OOOO00000O ['cedent_type']]=O000O00OOOO00000O ['trace_cedent']#line:1171
                                    OOO00O00000OO0O0O ['trace_cedent_dataorder'][O000O00OOOO00000O ['cedent_type']]=O000O00OOOO00000O ['trace_cedent_asindata']#line:1172
                                OOO00O00000OO0O0O ["params"]=OOOO0OOOO0000OO0O #line:1173
                                if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1174
                                    OOO00O00000OO0O0O ["trace_cedent"]=copy .deepcopy (_OO00O000OOOOOOOO0 )#line:1175
                                O0OOOO000OOOOO000 ._print_rule (OOO00O00000OO0O0O )#line:1176
                                O0OOOO000OOOOO000 .rulelist .append (OOO00O00000OO0O0O )#line:1177
                            O0OOOO000OOOOO000 .stats ['total_cnt']+=1 #line:1178
                            O0OOOO000OOOOO000 .stats ['total_ver']+=1 #line:1179
                    if _OO0000O000OOO0OO0 >=1 :#line:1180
                        if len (OOO0OO00000O0OOOO ['cedents_to_do'])>len (OOO0OO00000O0OOOO ['cedents']):#line:1181
                            O0OOOO000OOOOO000 ._start_cedent (OOO0OO00000O0OOOO ,_OOO0OOOOOO0OO0000 +_OOOO00OO0000OOOOO *_O000O0O0OO0O0OO0O ,_OOO0OOOOOO0OO0000 +(_OOOO00OO0000OOOOO +0.33 )*_O000O0O0OO0O0OO0O )#line:1182
                    OOO0OO00000O0OOOO ['cedents'].pop ()#line:1183
                    if (not (_OO0000O000OOO0OO0 ==0 ))and (len (_OO00O000OOOOOOOO0 )<_OOOO0O0O0OO0OOO00 ):#line:1184
                        O0OOOO000OOOOO000 ._genvar (OOO0OO00000O0OOOO ,OO0OOOO000OOO000O ,_OO00O000OOOOOOOO0 ,_O0O00OO00OO000000 ,_O0000O00OO0O00O0O ,_O00O00OOO0O00O000 ,_OOOO0O0O0OO0OOO00 ,_OOO0OOOOOO0OO0000 +(_OOOO00OO0000OOOOO +0.33 )*_O000O0O0OO0O0OO0O ,_OOO0OOOOOO0OO0000 +(_OOOO00OO0000OOOOO +0.66 )*_O000O0O0OO0O0OO0O )#line:1185
                else :#line:1186
                    OOO0OO00000O0OOOO ['cedents'].pop ()#line:1187
                if len (_OOO0OOOO0OOO0O0O0 )<_O0OO0O0O00O000O0O :#line:1188
                    O0OOOO000OOOOO000 ._gencomb (OOO0OO00000O0OOOO ,OO0OOOO000OOO000O ,_OO00O000OOOOOOOO0 ,_O0O00OO00OO000000 ,_OOO0OOOO0OOO0O0O0 ,_OO0OO00O0O0OOO000 ,_OO000OO000OOOOO00 ,OO0O0O0O0OOO00OO0 ,_OO000O000O00OOOO0 ,_O00O00OOO0O00O000 ,_OOOO0O0O0OO0OOO00 ,_O00000000OOOO0O0O ,_O0OO0O0O00O000O0O ,_OOO0OOOOOO0OO0000 +_O000O0O0OO0O0OO0O *(_OOOO00OO0000OOOOO +0.66 ),_OOO0OOOOOO0OO0000 +_O000O0O0OO0O0OO0O *(_OOOO00OO0000OOOOO +1 ),_OOO000OO00O0O0000 )#line:1189
                _OOO0OOOO0OOO0O0O0 .pop ()#line:1190
                _OOOO00OO0000OOOOO +=1 #line:1191
                if O0OOOO000OOOOO000 .options ['progressbar']:#line:1192
                    O0OOOO000OOOOO000 .bar .update (min (100 ,_OOO0OOOOOO0OO0000 +_O000O0O0OO0O0OO0O *_OOOO00OO0000OOOOO ))#line:1193
                if O0OOOO000OOOOO000 .verbosity ['debug']:#line:1194
                    print (f"Progress : lower: {_OOO0OOOOOO0OO0000}, step: {_O000O0O0OO0O0OO0O}, step_no: {_OOOO00OO0000OOOOO} overall: {_OOO0OOOOOO0OO0000+_O000O0O0OO0O0OO0O*_OOOO00OO0000OOOOO}")#line:1195
    def _start_cedent (O0OOO00O000000O00 ,OOO00O0OO0OOOO000 ,_OOO00O0OOOOOOO00O ,_OOO000O00000OO00O ):#line:1197
        if len (OOO00O0OO0OOOO000 ['cedents_to_do'])>len (OOO00O0OO0OOOO000 ['cedents']):#line:1198
            _O0OO000O0OO000OOO =[]#line:1199
            _O0OO00O0O00OO0OOO =[]#line:1200
            OO0O00O000OO0OO0O ={}#line:1201
            OO0O00O000OO0OO0O ['cedent_type']=OOO00O0OO0OOOO000 ['cedents_to_do'][len (OOO00O0OO0OOOO000 ['cedents'])]#line:1202
            O000OO000O0OO0OOO =OO0O00O000OO0OO0O ['cedent_type']#line:1203
            if ((O000OO000O0OO0OOO [-1 ]=='-')|(O000OO000O0OO0OOO [-1 ]=='+')):#line:1204
                O000OO000O0OO0OOO =O000OO000O0OO0OOO [:-1 ]#line:1205
            OO0O00O000OO0OO0O ['defi']=O0OOO00O000000O00 .kwargs .get (O000OO000O0OO0OOO )#line:1207
            if (OO0O00O000OO0OO0O ['defi']==None ):#line:1208
                print ("Error getting cedent ",OO0O00O000OO0OO0O ['cedent_type'])#line:1209
            _O000OO0O0OOO0OO00 =int (0 )#line:1210
            OO0O00O000OO0OO0O ['num_cedent']=len (OO0O00O000OO0OO0O ['defi'].get ('attributes'))#line:1211
            if (OO0O00O000OO0OO0O ['defi'].get ('type')=='con'):#line:1212
                _O000OO0O0OOO0OO00 =(1 <<O0OOO00O000000O00 .data ["rows_count"])-1 #line:1213
            O0OOO00O000000O00 ._genvar (OOO00O0OO0OOOO000 ,OO0O00O000OO0OO0O ,_O0OO000O0OO000OOO ,_O0OO00O0O00OO0OOO ,_O000OO0O0OOO0OO00 ,OO0O00O000OO0OO0O ['defi'].get ('minlen'),OO0O00O000OO0OO0O ['defi'].get ('maxlen'),_OOO00O0OOOOOOO00O ,_OOO000O00000OO00O )#line:1214
    def _calc_all (O000OOOOOOOO00O00 ,**O00OO0OO00OO0OO00 ):#line:1217
        if "df"in O00OO0OO00OO0OO00 :#line:1218
            O000OOOOOOOO00O00 ._prep_data (O000OOOOOOOO00O00 .kwargs .get ("df"))#line:1219
        if not (O000OOOOOOOO00O00 ._initialized ):#line:1220
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1221
        else :#line:1222
            O000OOOOOOOO00O00 ._calculate (**O00OO0OO00OO0OO00 )#line:1223
    def _check_cedents (O000O000OO0OO000O ,OOOOO0O0OOO0O0OOO ,**OOO00OO0OOO0O00O0 ):#line:1225
        OOOOOO0OOO0O0O0OO =True #line:1226
        if (OOO00OO0OOO0O00O0 .get ('quantifiers',None )==None ):#line:1227
            print (f"Error: missing quantifiers.")#line:1228
            OOOOOO0OOO0O0O0OO =False #line:1229
            return OOOOOO0OOO0O0O0OO #line:1230
        if (type (OOO00OO0OOO0O00O0 .get ('quantifiers'))!=dict ):#line:1231
            print (f"Error: quantifiers are not dictionary type.")#line:1232
            OOOOOO0OOO0O0O0OO =False #line:1233
            return OOOOOO0OOO0O0O0OO #line:1234
        for OO0OOOO0000O000OO in OOOOO0O0OOO0O0OOO :#line:1236
            if (OOO00OO0OOO0O00O0 .get (OO0OOOO0000O000OO ,None )==None ):#line:1237
                print (f"Error: cedent {OO0OOOO0000O000OO} is missing in parameters.")#line:1238
                OOOOOO0OOO0O0O0OO =False #line:1239
                return OOOOOO0OOO0O0O0OO #line:1240
            O0O00O00O000O00O0 =OOO00OO0OOO0O00O0 .get (OO0OOOO0000O000OO )#line:1241
            if (O0O00O00O000O00O0 .get ('minlen'),None )==None :#line:1242
                print (f"Error: cedent {OO0OOOO0000O000OO} has no minimal length specified.")#line:1243
                OOOOOO0OOO0O0O0OO =False #line:1244
                return OOOOOO0OOO0O0O0OO #line:1245
            if not (type (O0O00O00O000O00O0 .get ('minlen'))is int ):#line:1246
                print (f"Error: cedent {OO0OOOO0000O000OO} has invalid type of minimal length ({type(O0O00O00O000O00O0.get('minlen'))}).")#line:1247
                OOOOOO0OOO0O0O0OO =False #line:1248
                return OOOOOO0OOO0O0O0OO #line:1249
            if (O0O00O00O000O00O0 .get ('maxlen'),None )==None :#line:1250
                print (f"Error: cedent {OO0OOOO0000O000OO} has no maximal length specified.")#line:1251
                OOOOOO0OOO0O0O0OO =False #line:1252
                return OOOOOO0OOO0O0O0OO #line:1253
            if not (type (O0O00O00O000O00O0 .get ('maxlen'))is int ):#line:1254
                print (f"Error: cedent {OO0OOOO0000O000OO} has invalid type of maximal length.")#line:1255
                OOOOOO0OOO0O0O0OO =False #line:1256
                return OOOOOO0OOO0O0O0OO #line:1257
            if (O0O00O00O000O00O0 .get ('type'),None )==None :#line:1258
                print (f"Error: cedent {OO0OOOO0000O000OO} has no type specified.")#line:1259
                OOOOOO0OOO0O0O0OO =False #line:1260
                return OOOOOO0OOO0O0O0OO #line:1261
            if not ((O0O00O00O000O00O0 .get ('type'))in (['con','dis'])):#line:1262
                print (f"Error: cedent {OO0OOOO0000O000OO} has invalid type. Allowed values are 'con' and 'dis'.")#line:1263
                OOOOOO0OOO0O0O0OO =False #line:1264
                return OOOOOO0OOO0O0O0OO #line:1265
            if (O0O00O00O000O00O0 .get ('attributes'),None )==None :#line:1266
                print (f"Error: cedent {OO0OOOO0000O000OO} has no attributes specified.")#line:1267
                OOOOOO0OOO0O0O0OO =False #line:1268
                return OOOOOO0OOO0O0O0OO #line:1269
            for OO0OOO00000OOO0O0 in O0O00O00O000O00O0 .get ('attributes'):#line:1270
                if (OO0OOO00000OOO0O0 .get ('name'),None )==None :#line:1271
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0} has no 'name' attribute specified.")#line:1272
                    OOOOOO0OOO0O0O0OO =False #line:1273
                    return OOOOOO0OOO0O0O0OO #line:1274
                if not ((OO0OOO00000OOO0O0 .get ('name'))in O000O000OO0OO000O .data ["varname"]):#line:1275
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} not in variable list. Please check spelling.")#line:1276
                    OOOOOO0OOO0O0O0OO =False #line:1277
                    return OOOOOO0OOO0O0O0OO #line:1278
                if (OO0OOO00000OOO0O0 .get ('type'),None )==None :#line:1279
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has no 'type' attribute specified.")#line:1280
                    OOOOOO0OOO0O0O0OO =False #line:1281
                    return OOOOOO0OOO0O0O0OO #line:1282
                if not ((OO0OOO00000OOO0O0 .get ('type'))in (['rcut','lcut','seq','subset','one','list'])):#line:1283
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has unsupported type {OO0OOO00000OOO0O0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one','list'.")#line:1284
                    OOOOOO0OOO0O0O0OO =False #line:1285
                    return OOOOOO0OOO0O0O0OO #line:1286
                if (OO0OOO00000OOO0O0 .get ('minlen'),None )==None :#line:1287
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has no minimal length specified.")#line:1288
                    OOOOOO0OOO0O0O0OO =False #line:1289
                    return OOOOOO0OOO0O0O0OO #line:1290
                if not (type (OO0OOO00000OOO0O0 .get ('minlen'))is int ):#line:1291
                    if not (OO0OOO00000OOO0O0 .get ('type')=='one'or OO0OOO00000OOO0O0 .get ('type')=='list'):#line:1292
                        print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has invalid type of minimal length.")#line:1293
                        OOOOOO0OOO0O0O0OO =False #line:1294
                        return OOOOOO0OOO0O0O0OO #line:1295
                if (OO0OOO00000OOO0O0 .get ('maxlen'),None )==None :#line:1296
                    print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has no maximal length specified.")#line:1297
                    OOOOOO0OOO0O0O0OO =False #line:1298
                    return OOOOOO0OOO0O0O0OO #line:1299
                if not (type (OO0OOO00000OOO0O0 .get ('maxlen'))is int ):#line:1300
                    if not (OO0OOO00000OOO0O0 .get ('type')=='one'or OO0OOO00000OOO0O0 .get ('type')=='list'):#line:1301
                        print (f"Error: cedent {OO0OOOO0000O000OO} / attribute {OO0OOO00000OOO0O0.get('name')} has invalid type of maximal length.")#line:1302
                        OOOOOO0OOO0O0O0OO =False #line:1303
                        return OOOOOO0OOO0O0O0OO #line:1304
        return OOOOOO0OOO0O0O0OO #line:1305


    def _calculate (O00O0OOO0O0O000OO ,**O00OOOOO000OOOOOO ):#line:3
        if O00O0OOO0O0O000OO .data ["data_prepared"]==0 :#line:4
            print ("Error: data not prepared")#line:5
            return #line:6
        O00O0OOO0O0O000OO .kwargs =O00OOOOO000OOOOOO #line:7
        O00O0OOO0O0O000OO .proc =O00OOOOO000OOOOOO .get ('proc')#line:8
        O00O0OOO0O0O000OO .quantifiers =O00OOOOO000OOOOOO .get ('quantifiers')#line:9
        O00O0OOO0O0O000OO ._init_task ()#line:11
        O00O0OOO0O0O000OO .stats ['start_proc_time']=time .time ()#line:12
        O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do']=[]#line:13
        O00O0OOO0O0O000OO .task_actinfo ['cedents']=[]#line:14
        if O00OOOOO000OOOOOO .get ("proc")=='UICMiner':#line:17
            if not (O00O0OOO0O0O000OO ._check_cedents (['ante'],**O00OOOOO000OOOOOO )):#line:18
                return #line:19
            _OO0000O0O0O0OO00O =O00OOOOO000OOOOOO .get ("cond")#line:21
            if _OO0000O0O0O0OO00O !=None :#line:22
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:23
            else :#line:24
                O0O00OO00OOO00000 =O00O0OOO0O0O000OO .cedent #line:25
                O0O00OO00OOO00000 ['cedent_type']='cond'#line:26
                O0O00OO00OOO00000 ['filter_value']=(1 <<O00O0OOO0O0O000OO .data ["rows_count"])-1 #line:27
                O0O00OO00OOO00000 ['generated_string']='---'#line:28
                if O00O0OOO0O0O000OO .verbosity ['debug']:#line:29
                    print (O0O00OO00OOO00000 ['filter_value'])#line:30
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:31
                O00O0OOO0O0O000OO .task_actinfo ['cedents'].append (O0O00OO00OOO00000 )#line:32
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('ante')#line:33
            if O00OOOOO000OOOOOO .get ('target',None )==None :#line:34
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:35
                return #line:36
            if not (O00OOOOO000OOOOOO .get ('target')in O00O0OOO0O0O000OO .data ["varname"]):#line:37
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:38
                return #line:39
            if ("aad_score"in O00O0OOO0O0O000OO .quantifiers ):#line:40
                if not ("aad_weights"in O00O0OOO0O0O000OO .quantifiers ):#line:41
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:42
                    return #line:43
                if not (len (O00O0OOO0O0O000OO .quantifiers .get ("aad_weights"))==len (O00O0OOO0O0O000OO .data ["dm"][O00O0OOO0O0O000OO .data ["varname"].index (O00O0OOO0O0O000OO .kwargs .get ('target'))])):#line:44
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:45
                    return #line:46
        elif O00OOOOO000OOOOOO .get ("proc")=='CFMiner':#line:47
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do']=['cond']#line:48
            if O00OOOOO000OOOOOO .get ('target',None )==None :#line:49
                print ("ERROR: no target variable defined for CF Miner")#line:50
                return #line:51
            O00OOO0000OO00O00 =O00OOOOO000OOOOOO .get ('target',None )#line:52
            O00O0OOO0O0O000OO .profiles ['hist_target_entire_dataset_labels']=O00O0OOO0O0O000OO .data ["catnames"][O00O0OOO0O0O000OO .data ["varname"].index (O00O0OOO0O0O000OO .kwargs .get ('target'))]#line:53
            OO0OO000O00O00OOO =O00O0OOO0O0O000OO .data ["dm"][O00O0OOO0O0O000OO .data ["varname"].index (O00O0OOO0O0O000OO .kwargs .get ('target'))]#line:54
            O00OO0OO000OO00OO =[]#line:56
            for OO0O0OOOOOO0OOOOO in range (len (OO0OO000O00O00OOO )):#line:57
                O0000O0O0O0OOOO00 =O00O0OOO0O0O000OO ._bitcount (OO0OO000O00O00OOO [OO0O0OOOOOO0OOOOO ])#line:58
                O00OO0OO000OO00OO .append (O0000O0O0O0OOOO00 )#line:59
            O00O0OOO0O0O000OO .profiles ['hist_target_entire_dataset_values']=O00OO0OO000OO00OO #line:60
            if not (O00O0OOO0O0O000OO ._check_cedents (['cond'],**O00OOOOO000OOOOOO )):#line:61
                return #line:62
            if not (O00OOOOO000OOOOOO .get ('target')in O00O0OOO0O0O000OO .data ["varname"]):#line:63
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:64
                return #line:65
            if ("aad"in O00O0OOO0O0O000OO .quantifiers ):#line:66
                if not ("aad_weights"in O00O0OOO0O0O000OO .quantifiers ):#line:67
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:68
                    return #line:69
                if not (len (O00O0OOO0O0O000OO .quantifiers .get ("aad_weights"))==len (O00O0OOO0O0O000OO .data ["dm"][O00O0OOO0O0O000OO .data ["varname"].index (O00O0OOO0O0O000OO .kwargs .get ('target'))])):#line:70
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:71
                    return #line:72
        elif O00OOOOO000OOOOOO .get ("proc")=='4ftMiner':#line:75
            if not (O00O0OOO0O0O000OO ._check_cedents (['ante','succ'],**O00OOOOO000OOOOOO )):#line:76
                return #line:77
            _OO0000O0O0O0OO00O =O00OOOOO000OOOOOO .get ("cond")#line:79
            if _OO0000O0O0O0OO00O !=None :#line:80
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:81
            else :#line:82
                O0O00OO00OOO00000 =O00O0OOO0O0O000OO .cedent #line:83
                O0O00OO00OOO00000 ['cedent_type']='cond'#line:84
                O0O00OO00OOO00000 ['filter_value']=(1 <<O00O0OOO0O0O000OO .data ["rows_count"])-1 #line:85
                O0O00OO00OOO00000 ['generated_string']='---'#line:86
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:87
                O00O0OOO0O0O000OO .task_actinfo ['cedents'].append (O0O00OO00OOO00000 )#line:88
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('ante')#line:89
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('succ')#line:90
        elif O00OOOOO000OOOOOO .get ("proc")=='SD4ftMiner':#line:91
            if not (O00O0OOO0O0O000OO ._check_cedents (['ante','succ','frst','scnd'],**O00OOOOO000OOOOOO )):#line:94
                return #line:95
            _OO0000O0O0O0OO00O =O00OOOOO000OOOOOO .get ("cond")#line:96
            if _OO0000O0O0O0OO00O !=None :#line:97
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:98
            else :#line:99
                O0O00OO00OOO00000 =O00O0OOO0O0O000OO .cedent #line:100
                O0O00OO00OOO00000 ['cedent_type']='cond'#line:101
                O0O00OO00OOO00000 ['filter_value']=(1 <<O00O0OOO0O0O000OO .data ["rows_count"])-1 #line:102
                O0O00OO00OOO00000 ['generated_string']='---'#line:103
                O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('cond')#line:104
                O00O0OOO0O0O000OO .task_actinfo ['cedents'].append (O0O00OO00OOO00000 )#line:105
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('frst')#line:106
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('scnd')#line:107
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('ante')#line:108
            O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do'].append ('succ')#line:109
        else :#line:110
            print ("Unsupported procedure")#line:111
            return #line:112
        print ("Will go for ",O00OOOOO000OOOOOO .get ("proc"))#line:113
        O00O0OOO0O0O000OO .task_actinfo ['optim']={}#line:116
        O0O00O0O00OO00O00 =True #line:117
        for O0OO00OOOO0O00O0O in O00O0OOO0O0O000OO .task_actinfo ['cedents_to_do']:#line:118
            try :#line:119
                OOOOOOO0OOO0O0OOO =O00O0OOO0O0O000OO .kwargs .get (O0OO00OOOO0O00O0O )#line:120
                if O00O0OOO0O0O000OO .verbosity ['debug']:#line:121
                    print (OOOOOOO0OOO0O0OOO )#line:122
                    print (f"...cedent {O0OO00OOOO0O00O0O} is type {OOOOOOO0OOO0O0OOO.get('type')}")#line:123
                    print (f"Will check cedent type {O0OO00OOOO0O00O0O} : {OOOOOOO0OOO0O0OOO.get('type')}")#line:124
                if OOOOOOO0OOO0O0OOO .get ('type')!='con':#line:125
                    O0O00O0O00OO00O00 =False #line:126
                    if O00O0OOO0O0O000OO .verbosity ['debug']:#line:127
                        print (f"Cannot optim due to cedent type {O0OO00OOOO0O00O0O} : {OOOOOOO0OOO0O0OOO.get('type')}")#line:128
            except :#line:129
                OOO0OO0O0O0OOO0OO =1 <2 #line:130
        if O00O0OOO0O0O000OO .options ['optimizations']==False :#line:132
            O0O00O0O00OO00O00 =False #line:133
        OO0O000OOO0000O0O ={}#line:134
        OO0O000OOO0000O0O ['only_con']=O0O00O0O00OO00O00 #line:135
        O00O0OOO0O0O000OO .task_actinfo ['optim']=OO0O000OOO0000O0O #line:136
        if O00O0OOO0O0O000OO .verbosity ['debug']:#line:140
            print ("Starting to prepare data.")#line:141
            O00O0OOO0O0O000OO ._prep_data (O00O0OOO0O0O000OO .data .df )#line:142
            O00O0OOO0O0O000OO .stats ['mid1_time']=time .time ()#line:143
            O00O0OOO0O0O000OO .quantifiers =O00OOOOO000OOOOOO .get ('self.quantifiers')#line:144
        print ("Starting to mine rules.")#line:145
        sys .stdout .flush ()#line:146
        time .sleep (0.01 )#line:147
        if O00O0OOO0O0O000OO .options ['progressbar']:#line:148
            O0OOOO000O0000OO0 =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:149
            O00O0OOO0O0O000OO .bar =progressbar .ProgressBar (widgets =O0OOOO000O0000OO0 ,max_value =100 ,fd =sys .stdout ).start ()#line:150
            O00O0OOO0O0O000OO .bar .update (0 )#line:151
        O00O0OOO0O0O000OO .progress_lower =0 #line:152
        O00O0OOO0O0O000OO .progress_upper =100 #line:153
        O00O0OOO0O0O000OO ._start_cedent (O00O0OOO0O0O000OO .task_actinfo ,O00O0OOO0O0O000OO .progress_lower ,O00O0OOO0O0O000OO .progress_upper )#line:154
        if O00O0OOO0O0O000OO .options ['progressbar']:#line:155
            O00O0OOO0O0O000OO .bar .update (100 )#line:156
            O00O0OOO0O0O000OO .bar .finish ()#line:157
        O00O0OOO0O0O000OO .stats ['end_proc_time']=time .time ()#line:158
        print ("Done. Total verifications : "+str (O00O0OOO0O0O000OO .stats ['total_cnt'])+", rules "+str (O00O0OOO0O0O000OO .stats ['total_valid'])+", times: prep "+"{:.2f}".format (O00O0OOO0O0O000OO .stats ['end_prep_time']-O00O0OOO0O0O000OO .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (O00O0OOO0O0O000OO .stats ['end_proc_time']-O00O0OOO0O0O000OO .stats ['start_proc_time'])+"sec")#line:161
        OO0OOO0O0OO0O0OO0 ={}#line:162
        OOOO0000OOOOO0OOO ={}#line:163
        OOOO0000OOOOO0OOO ["guid"]=O00O0OOO0O0O000OO .guid #line:164
        OOOO0000OOOOO0OOO ["task_type"]=O00OOOOO000OOOOOO .get ('proc')#line:165
        OOOO0000OOOOO0OOO ["target"]=O00OOOOO000OOOOOO .get ('target')#line:166
        OOOO0000OOOOO0OOO ["self.quantifiers"]=O00O0OOO0O0O000OO .quantifiers #line:167
        if O00OOOOO000OOOOOO .get ('cond')!=None :#line:168
            OOOO0000OOOOO0OOO ['cond']=O00OOOOO000OOOOOO .get ('cond')#line:169
        if O00OOOOO000OOOOOO .get ('ante')!=None :#line:170
            OOOO0000OOOOO0OOO ['ante']=O00OOOOO000OOOOOO .get ('ante')#line:171
        if O00OOOOO000OOOOOO .get ('succ')!=None :#line:172
            OOOO0000OOOOO0OOO ['succ']=O00OOOOO000OOOOOO .get ('succ')#line:173
        if O00OOOOO000OOOOOO .get ('opts')!=None :#line:174
            OOOO0000OOOOO0OOO ['opts']=O00OOOOO000OOOOOO .get ('opts')#line:175
        if O00O0OOO0O0O000OO .df is None :#line:176
            OOOO0000OOOOO0OOO ['rowcount']=O00O0OOO0O0O000OO .data ["rows_count"]#line:177
        else :#line:179
            OOOO0000OOOOO0OOO ['rowcount']=len (O00O0OOO0O0O000OO .df .index )#line:180
        OO0OOO0O0OO0O0OO0 ["taskinfo"]=OOOO0000OOOOO0OOO #line:181
        OO0O0OO0OO00O0O00 ={}#line:182
        OO0O0OO0OO00O0O00 ["total_verifications"]=O00O0OOO0O0O000OO .stats ['total_cnt']#line:183
        OO0O0OO0OO00O0O00 ["valid_rules"]=O00O0OOO0O0O000OO .stats ['total_valid']#line:184
        OO0O0OO0OO00O0O00 ["total_verifications_with_opt"]=O00O0OOO0O0O000OO .stats ['total_ver']#line:185
        OO0O0OO0OO00O0O00 ["time_prep"]=O00O0OOO0O0O000OO .stats ['end_prep_time']-O00O0OOO0O0O000OO .stats ['start_prep_time']#line:186
        OO0O0OO0OO00O0O00 ["time_processing"]=O00O0OOO0O0O000OO .stats ['end_proc_time']-O00O0OOO0O0O000OO .stats ['start_proc_time']#line:187
        OO0O0OO0OO00O0O00 ["time_total"]=O00O0OOO0O0O000OO .stats ['end_prep_time']-O00O0OOO0O0O000OO .stats ['start_prep_time']+O00O0OOO0O0O000OO .stats ['end_proc_time']-O00O0OOO0O0O000OO .stats ['start_proc_time']#line:188
        OO0OOO0O0OO0O0OO0 ["summary_statistics"]=OO0O0OO0OO00O0O00 #line:189
        OO0OOO0O0OO0O0OO0 ["rules"]=O00O0OOO0O0O000OO .rulelist #line:190
        OOO00OO0O000O0000 ={}#line:191
        OOO00OO0O000O0000 ["varname"]=O00O0OOO0O0O000OO .data ["varname"]#line:192
        OOO00OO0O000O0000 ["catnames"]=O00O0OOO0O0O000OO .data ["catnames"]#line:193
        OO0OOO0O0OO0O0OO0 ["datalabels"]=OOO00OO0O000O0000 #line:194
        O00O0OOO0O0O000OO .result =OO0OOO0O0OO0O0OO0 #line:195
    def print_summary (OO00000O00OOOO0O0 ):#line:197
        ""#line:200
        if not (OO00000O00OOOO0O0 ._is_calculated ()):#line:201
            print ("ERROR: Task has not been calculated.")#line:202
            return #line:203
        print ("")#line:204
        print ("CleverMiner task processing summary:")#line:205
        print ("")#line:206
        print (f"Task type : {OO00000O00OOOO0O0.result['taskinfo']['task_type']}")#line:207
        print (f"Number of verifications : {OO00000O00OOOO0O0.result['summary_statistics']['total_verifications']}")#line:208
        print (f"Number of rules : {OO00000O00OOOO0O0.result['summary_statistics']['valid_rules']}")#line:209
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OO00000O00OOOO0O0.result['summary_statistics']['time_total']))}")#line:210
        if OO00000O00OOOO0O0 .verbosity ['debug']:#line:211
            print (f"Total time needed : {OO00000O00OOOO0O0.result['summary_statistics']['time_total']}")#line:212
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OO00000O00OOOO0O0.result['summary_statistics']['time_prep']))}")#line:213
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OO00000O00OOOO0O0.result['summary_statistics']['time_processing']))}")#line:214
        print ("")#line:215
    def print_hypolist (OOO0O0O0OOOOOOOOO ):#line:217
        ""#line:220
        OOO0O0O0OOOOOOOOO .print_rulelist ();#line:221
    def print_rulelist (O000O0O0OO000OOOO ,sortby =None ,storesorted =False ):#line:223
        ""#line:228
        if not (O000O0O0OO000OOOO ._is_calculated ()):#line:229
            print ("ERROR: Task has not been calculated.")#line:230
            return #line:231
        def OO000OO0O0OOO00OO (O0OOOO00OOOOOO0O0 ):#line:233
            O00000OOO0OOO0OOO =O0OOOO00OOOOOO0O0 ["params"]#line:234
            return O00000OOO0OOO0OOO .get (sortby ,0 )#line:235
        print ("")#line:237
        print ("List of rules:")#line:238
        if O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:239
            print ("RULEID BASE  CONF  AAD    Rule")#line:240
        elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="UICMiner":#line:241
            print ("RULEID BASE  AAD_SCORE  Rule")#line:242
        elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:243
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:244
        elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:245
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:246
        else :#line:247
            print ("Unsupported task type for rulelist")#line:248
            return #line:249
        O0O0O0O0O00O0OOO0 =O000O0O0OO000OOOO .result ["rules"]#line:250
        if sortby is not None :#line:251
            O0O0O0O0O00O0OOO0 =sorted (O0O0O0O0O00O0OOO0 ,key =OO000OO0O0OOO00OO ,reverse =True )#line:252
            if storesorted :#line:253
                O000O0O0OO000OOOO .result ["rules"]=O0O0O0O0O00O0OOO0 #line:254
        for O0O0OOO0000OOO000 in O0O0O0O0O00O0OOO0 :#line:256
            OO0O0OOOO0OO000O0 ="{:6d}".format (O0O0OOO0000OOO000 ["rule_id"])#line:257
            if O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:258
                if O000O0O0OO000OOOO .verbosity ['debug']:#line:259
                   print (f"{O0O0OOO0000OOO000['params']}")#line:260
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["base"])+" "+"{:.3f}".format (O0O0OOO0000OOO000 ["params"]["conf"])+" "+"{:+.3f}".format (O0O0OOO0000OOO000 ["params"]["aad"])#line:261
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+O0O0OOO0000OOO000 ["cedents_str"]["ante"]+" => "+O0O0OOO0000OOO000 ["cedents_str"]["succ"]+" | "+O0O0OOO0000OOO000 ["cedents_str"]["cond"]#line:262
            elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="UICMiner":#line:263
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["base"])+" "+"{:.3f}".format (O0O0OOO0000OOO000 ["params"]["aad_score"])#line:264
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +"     "+O0O0OOO0000OOO000 ["cedents_str"]["ante"]+" => "+O000O0O0OO000OOOO .result ['taskinfo']['target']+"(*) | "+O0O0OOO0000OOO000 ["cedents_str"]["cond"]#line:265
            elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:266
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["base"])+" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["s_up"])+" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["s_down"])#line:267
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+O0O0OOO0000OOO000 ["cedents_str"]["cond"]#line:268
            elif O000O0O0OO000OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:269
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["base1"])+" "+"{:5d}".format (O0O0OOO0000OOO000 ["params"]["base2"])+"    "+"{:.3f}".format (O0O0OOO0000OOO000 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O0O0OOO0000OOO000 ["params"]["deltaconf"])#line:270
                OO0O0OOOO0OO000O0 =OO0O0OOOO0OO000O0 +"  "+O0O0OOO0000OOO000 ["cedents_str"]["ante"]+" => "+O0O0OOO0000OOO000 ["cedents_str"]["succ"]+" | "+O0O0OOO0000OOO000 ["cedents_str"]["cond"]+" : "+O0O0OOO0000OOO000 ["cedents_str"]["frst"]+" x "+O0O0OOO0000OOO000 ["cedents_str"]["scnd"]#line:271
            print (OO0O0OOOO0OO000O0 )#line:273
        print ("")#line:274
    def print_hypo (O0OOO00O0O0OOOO00 ,O00OO00O0O0O0OO0O ):#line:276
        ""#line:280
        O0OOO00O0O0OOOO00 .print_rule (O00OO00O0O0O0OO0O )#line:281
    def print_rule (OO0OO000OOOO000OO ,OO0O0O0OOOOOO0OO0 ):#line:284
        ""#line:288
        if not (OO0OO000OOOO000OO ._is_calculated ()):#line:289
            print ("ERROR: Task has not been calculated.")#line:290
            return #line:291
        print ("")#line:292
        if (OO0O0O0OOOOOO0OO0 <=len (OO0OO000OOOO000OO .result ["rules"])):#line:293
            if OO0OO000OOOO000OO .result ['taskinfo']['task_type']=="4ftMiner":#line:294
                print ("")#line:295
                O000O00OO00OO00O0 =OO0OO000OOOO000OO .result ["rules"][OO0O0O0OOOOOO0OO0 -1 ]#line:296
                print (f"Rule id : {O000O00OO00OO00O0['rule_id']}")#line:297
                print ("")#line:298
                print (f"Base : {'{:5d}'.format(O000O00OO00OO00O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_base'])}  CONF : {'{:.3f}'.format(O000O00OO00OO00O0['params']['conf'])}  AAD : {'{:+.3f}'.format(O000O00OO00OO00O0['params']['aad'])}  BAD : {'{:+.3f}'.format(O000O00OO00OO00O0['params']['bad'])}")#line:299
                print ("")#line:300
                print ("Cedents:")#line:301
                print (f"  antecedent : {O000O00OO00OO00O0['cedents_str']['ante']}")#line:302
                print (f"  succcedent : {O000O00OO00OO00O0['cedents_str']['succ']}")#line:303
                print (f"  condition  : {O000O00OO00OO00O0['cedents_str']['cond']}")#line:304
                print ("")#line:305
                print ("Fourfold table")#line:306
                print (f"    |  S  |  ¬S |")#line:307
                print (f"----|-----|-----|")#line:308
                print (f" A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold'][0])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold'][1])}|")#line:309
                print (f"----|-----|-----|")#line:310
                print (f"¬A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold'][2])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold'][3])}|")#line:311
                print (f"----|-----|-----|")#line:312
            elif OO0OO000OOOO000OO .result ['taskinfo']['task_type']=="CFMiner":#line:313
                print ("")#line:314
                O000O00OO00OO00O0 =OO0OO000OOOO000OO .result ["rules"][OO0O0O0OOOOOO0OO0 -1 ]#line:315
                print (f"Rule id : {O000O00OO00OO00O0['rule_id']}")#line:316
                print ("")#line:317
                OOO0O0OO0OOOOOOO0 =""#line:318
                if ('aad'in O000O00OO00OO00O0 ['params']):#line:319
                    OOO0O0OO0OOOOOOO0 ="aad : "+str (O000O00OO00OO00O0 ['params']['aad'])#line:320
                print (f"Base : {'{:5d}'.format(O000O00OO00OO00O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O000O00OO00OO00O0['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O000O00OO00OO00O0['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O000O00OO00OO00O0['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O000O00OO00OO00O0['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O000O00OO00OO00O0['params']['max'])}  Histogram minimum : {'{:5d}'.format(O000O00OO00OO00O0['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_min'])} {OOO0O0OO0OOOOOOO0}")#line:322
                print ("")#line:323
                print (f"Condition  : {O000O00OO00OO00O0['cedents_str']['cond']}")#line:324
                print ("")#line:325
                OOOO00O0O0OO00OO0 =OO0OO000OOOO000OO .get_category_names (OO0OO000OOOO000OO .result ["taskinfo"]["target"])#line:326
                print (f"Categories in target variable  {OOOO00O0O0OO00OO0}")#line:327
                print (f"Histogram                      {O000O00OO00OO00O0['params']['hist']}")#line:328
                if ('aad'in O000O00OO00OO00O0 ['params']):#line:329
                    print (f"Histogram on full set          {O000O00OO00OO00O0['params']['hist_full']}")#line:330
                    print (f"Relative histogram             {O000O00OO00OO00O0['params']['rel_hist']}")#line:331
                    print (f"Relative histogram on full set {O000O00OO00OO00O0['params']['rel_hist_full']}")#line:332
            elif OO0OO000OOOO000OO .result ['taskinfo']['task_type']=="UICMiner":#line:333
                print ("")#line:334
                O000O00OO00OO00O0 =OO0OO000OOOO000OO .result ["rules"][OO0O0O0OOOOOO0OO0 -1 ]#line:335
                print (f"Rule id : {O000O00OO00OO00O0['rule_id']}")#line:336
                print ("")#line:337
                OOO0O0OO0OOOOOOO0 =""#line:338
                if ('aad_score'in O000O00OO00OO00O0 ['params']):#line:339
                    OOO0O0OO0OOOOOOO0 ="aad score : "+str (O000O00OO00OO00O0 ['params']['aad_score'])#line:340
                print (f"Base : {'{:5d}'.format(O000O00OO00OO00O0['params']['base'])}  Relative base : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_base'])}   {OOO0O0OO0OOOOOOO0}")#line:342
                print ("")#line:343
                print (f"Condition  : {O000O00OO00OO00O0['cedents_str']['cond']}")#line:344
                print (f"Antecedent : {O000O00OO00OO00O0['cedents_str']['ante']}")#line:345
                print ("")#line:346
                print (f"Histogram                                        {O000O00OO00OO00O0['params']['hist']}")#line:347
                if ('aad_score'in O000O00OO00OO00O0 ['params']):#line:348
                    print (f"Histogram on full set with condition             {O000O00OO00OO00O0['params']['hist_cond']}")#line:349
                    print (f"Relative histogram                               {O000O00OO00OO00O0['params']['rel_hist']}")#line:350
                    print (f"Relative histogram on full set with condition    {O000O00OO00OO00O0['params']['rel_hist_cond']}")#line:351
                O0O00O00O000OO0OO =OO0OO000OOOO000OO .result ['datalabels']['catnames'][OO0OO000OOOO000OO .result ['datalabels']['varname'].index (OO0OO000OOOO000OO .result ['taskinfo']['target'])]#line:352
                print (" ")#line:353
                print ("Interpretation:")#line:354
                for O0OO0OO0O000O0000 in range (len (O0O00O00O000OO0OO )):#line:355
                  O0OOO00O0O00O0OO0 =0 #line:356
                  if O000O00OO00OO00O0 ['params']['rel_hist'][O0OO0OO0O000O0000 ]>0 :#line:357
                      O0OOO00O0O00O0OO0 =O000O00OO00OO00O0 ['params']['rel_hist'][O0OO0OO0O000O0000 ]/O000O00OO00OO00O0 ['params']['rel_hist_cond'][O0OO0OO0O000O0000 ]#line:358
                  OOO0000O0000O0OOO =''#line:359
                  if not (O000O00OO00OO00O0 ['cedents_str']['cond']=='---'):#line:360
                      OOO0000O0000O0OOO ="For "+O000O00OO00OO00O0 ['cedents_str']['cond']+": "#line:361
                  print (f"    {OOO0000O0000O0OOO}{OO0OO000OOOO000OO.result['taskinfo']['target']}({O0O00O00O000OO0OO[O0OO0OO0O000O0000]}) has occurence {'{:.1%}'.format(O000O00OO00OO00O0['params']['rel_hist_cond'][O0OO0OO0O000O0000])}, with antecedent it has occurence {'{:.1%}'.format(O000O00OO00OO00O0['params']['rel_hist'][O0OO0OO0O000O0000])}, that is {'{:.3f}'.format(O0OOO00O0O00O0OO0)} times more.")#line:363
            elif OO0OO000OOOO000OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:364
                print ("")#line:365
                O000O00OO00OO00O0 =OO0OO000OOOO000OO .result ["rules"][OO0O0O0OOOOOO0OO0 -1 ]#line:366
                print (f"Rule id : {O000O00OO00OO00O0['rule_id']}")#line:367
                print ("")#line:368
                print (f"Base1 : {'{:5d}'.format(O000O00OO00OO00O0['params']['base1'])} Base2 : {'{:5d}'.format(O000O00OO00OO00O0['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O000O00OO00OO00O0['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O000O00OO00OO00O0['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O000O00OO00OO00O0['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O000O00OO00OO00O0['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O000O00OO00OO00O0['params']['ratioconf'])}")#line:369
                print ("")#line:370
                print ("Cedents:")#line:371
                print (f"  antecedent : {O000O00OO00OO00O0['cedents_str']['ante']}")#line:372
                print (f"  succcedent : {O000O00OO00OO00O0['cedents_str']['succ']}")#line:373
                print (f"  condition  : {O000O00OO00OO00O0['cedents_str']['cond']}")#line:374
                print (f"  first set  : {O000O00OO00OO00O0['cedents_str']['frst']}")#line:375
                print (f"  second set : {O000O00OO00OO00O0['cedents_str']['scnd']}")#line:376
                print ("")#line:377
                print ("Fourfold tables:")#line:378
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:379
                print (f"----|-----|-----|  ----|-----|-----| ")#line:380
                print (f" A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold1'][0])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold2'][0])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold2'][1])}|")#line:381
                print (f"----|-----|-----|  ----|-----|-----|")#line:382
                print (f"¬A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold1'][2])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold2'][2])}|{'{:5d}'.format(O000O00OO00OO00O0['params']['fourfold2'][3])}|")#line:383
                print (f"----|-----|-----|  ----|-----|-----|")#line:384
            else :#line:385
                print ("Unsupported task type for rule details")#line:386
            print ("")#line:390
        else :#line:391
            print ("No such rule.")#line:392
    def get_ruletext (O00OO00OOO00OOO0O ,O0OO0O0OO0OOOOOO0 ):#line:394
        ""#line:400
        if not (O00OO00OOO00OOO0O ._is_calculated ()):#line:401
            print ("ERROR: Task has not been calculated.")#line:402
            return #line:403
        if O0OO0O0OO0OOOOOO0 <=0 or O0OO0O0OO0OOOOOO0 >O00OO00OOO00OOO0O .get_rulecount ():#line:404
            if O00OO00OOO00OOO0O .get_rulecount ()==0 :#line:405
                print ("No such rule. There are no rules in result.")#line:406
            else :#line:407
                print (f"No such rule ({O0OO0O0OO0OOOOOO0}). Available rules are 1 to {O00OO00OOO00OOO0O.get_rulecount()}")#line:408
            return None #line:409
        OOO0000O0OOO0O0OO =""#line:410
        O00000O00000OO0O0 =O00OO00OOO00OOO0O .result ["rules"][O0OO0O0OO0OOOOOO0 -1 ]#line:411
        if O00OO00OOO00OOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:412
            OOO0000O0OOO0O0OO =OOO0000O0OOO0O0OO +" "+O00000O00000OO0O0 ["cedents_str"]["ante"]+" => "+O00000O00000OO0O0 ["cedents_str"]["succ"]+" | "+O00000O00000OO0O0 ["cedents_str"]["cond"]#line:414
        elif O00OO00OOO00OOO0O .result ['taskinfo']['task_type']=="UICMiner":#line:415
            OOO0000O0OOO0O0OO =OOO0000O0OOO0O0OO +"     "+O00000O00000OO0O0 ["cedents_str"]["ante"]+" => "+O00OO00OOO00OOO0O .result ['taskinfo']['target']+"(*) | "+O00000O00000OO0O0 ["cedents_str"]["cond"]#line:417
        elif O00OO00OOO00OOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:418
            OOO0000O0OOO0O0OO =OOO0000O0OOO0O0OO +" "+O00000O00000OO0O0 ["cedents_str"]["cond"]#line:419
        elif O00OO00OOO00OOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:420
            OOO0000O0OOO0O0OO =OOO0000O0OOO0O0OO +"  "+O00000O00000OO0O0 ["cedents_str"]["ante"]+" => "+O00000O00000OO0O0 ["cedents_str"]["succ"]+" | "+O00000O00000OO0O0 ["cedents_str"]["cond"]+" : "+O00000O00000OO0O0 ["cedents_str"]["frst"]+" x "+O00000O00000OO0O0 ["cedents_str"]["scnd"]#line:422
        return OOO0000O0OOO0O0OO #line:423
    def _annotate_chart (O00OO0OO00OOOOOO0 ,O0O00OOO00OOOO00O ,OO0O000O00OOOO0OO ,cnt =2 ):#line:425
        ""#line:432
        OO0O0000O0000OO00 =O0O00OOO00OOOO00O .axes .get_ylim ()#line:433
        for OO000OO00OOOOOOO0 in O0O00OOO00OOOO00O .patches :#line:435
            OO00O0OO00O00O00O ='{:.1f}%'.format (100 *OO000OO00OOOOOOO0 .get_height ()/OO0O000O00OOOO0OO )#line:436
            O00OOO0OO0OO00OOO =OO000OO00OOOOOOO0 .get_x ()+OO000OO00OOOOOOO0 .get_width ()/4 #line:437
            O0OOO00O0OOO000O0 =OO000OO00OOOOOOO0 .get_y ()+OO000OO00OOOOOOO0 .get_height ()-OO0O0000O0000OO00 [1 ]/8 #line:438
            if OO000OO00OOOOOOO0 .get_height ()<OO0O0000O0000OO00 [1 ]/8 :#line:439
                O0OOO00O0OOO000O0 =OO000OO00OOOOOOO0 .get_y ()+OO000OO00OOOOOOO0 .get_height ()+OO0O0000O0000OO00 [1 ]*0.02 #line:440
            O0O00OOO00OOOO00O .annotate (OO00O0OO00O00O00O ,(O00OOO0OO0OO00OOO ,O0OOO00O0OOO000O0 ),size =23 /cnt )#line:441
    def draw_rule (OOOOOOO00O00OO0OO ,OOO0OOO00O00OOO00 ,show =True ,filename =None ):#line:443
        ""#line:449
        if not (OOOOOOO00O00OO0OO ._is_calculated ()):#line:450
            print ("ERROR: Task has not been calculated.")#line:451
            return #line:452
        print ("")#line:453
        if (OOO0OOO00O00OOO00 <=len (OOOOOOO00O00OO0OO .result ["rules"])):#line:454
            if OOOOOOO00O00OO0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:455
                O00OOOOOOOOO000OO ,O0O0O00O0OO0OOOO0 =plt .subplots (2 ,2 )#line:457
                OOO00OO00O00OOOOO =['S','not S']#line:458
                O00O0OOOOOO00000O =['A','not A']#line:459
                OOOOOOOOO0000O0OO =OOOOOOO00O00OO0OO .get_fourfold (OOO0OOO00O00OOO00 )#line:460
                OO000OOO000OOOO00 =[OOOOOOOOO0000O0OO [0 ],OOOOOOOOO0000O0OO [1 ]]#line:462
                O0OO00O0O000OOO0O =[OOOOOOOOO0000O0OO [2 ],OOOOOOOOO0000O0OO [3 ]]#line:463
                O00000OO000O000O0 =[OOOOOOOOO0000O0OO [0 ]+OOOOOOOOO0000O0OO [2 ],OOOOOOOOO0000O0OO [1 ]+OOOOOOOOO0000O0OO [3 ]]#line:464
                O0O0O00O0OO0OOOO0 [0 ,0 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,0 ],x =OOO00OO00O00OOOOO ,y =OO000OOO000OOOO00 ,color ='lightsteelblue')#line:465
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,0 ],OOOOOOOOO0000O0OO [0 ]+OOOOOOOOO0000O0OO [1 ])#line:467
                O0O0O00O0OO0OOOO0 [0 ,1 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,1 ],x =OOO00OO00O00OOOOO ,y =O00000OO000O000O0 ,color ="gray",edgecolor ="black")#line:469
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,1 ],sum (OOOOOOOOO0000O0OO ))#line:471
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:473
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:474
                O0O0O0O000O00OOOO =sns .color_palette ("Blues",as_cmap =True )#line:476
                OO000000O000OO00O =sns .color_palette ("Greys",as_cmap =True )#line:477
                O0O0O00O0OO0OOOO0 [1 ,0 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,0 ],data =[OO000OOO000OOOO00 ,O0OO00O0O000OOO0O ],xticklabels =OOO00OO00O00OOOOO ,yticklabels =O00O0OOOOOO00000O ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0O0O000O00OOOO )#line:481
                O0O0O00O0OO0OOOO0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:483
                O0O0O00O0OO0OOOO0 [1 ,1 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,1 ],data =np .asarray ([O00000OO000O000O0 ]),xticklabels =OOO00OO00O00OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OO000000O000OO00O )#line:487
                O0O0O00O0OO0OOOO0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:489
                O0OO000O000O00OO0 =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']['ante']#line:491
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (title ="\n".join (wrap (O0OO000O000O00OO0 ,30 )))#line:492
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (title ='Entire dataset')#line:493
                OOOO0OOOOOOO000OO =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']#line:495
                O00OOOOOOOOO000OO .suptitle ("Antecedent : "+OOOO0OOOOOOO000OO ['ante']+"\nSuccedent : "+OOOO0OOOOOOO000OO ['succ']+"\nCondition : "+OOOO0OOOOOOO000OO ['cond'],x =0 ,ha ='left',size ='small')#line:499
                O00OOOOOOOOO000OO .tight_layout ()#line:500
            elif OOOOOOO00O00OO0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:502
                O00OOOOOOOOO000OO ,O0O0O00O0OO0OOOO0 =plt .subplots (2 ,2 )#line:504
                OOO00OO00O00OOOOO =['S','not S']#line:505
                O00O0OOOOOO00000O =['A','not A']#line:506
                OO0OOOO0OOOOOO00O =OOOOOOO00O00OO0OO .get_fourfold (OOO0OOO00O00OOO00 ,order =1 )#line:508
                O0O0O0000000OO000 =OOOOOOO00O00OO0OO .get_fourfold (OOO0OOO00O00OOO00 ,order =2 )#line:509
                OOOO00O00O000OO0O =[OO0OOOO0OOOOOO00O [0 ],OO0OOOO0OOOOOO00O [1 ]]#line:511
                OO0O0O000O0000000 =[OO0OOOO0OOOOOO00O [2 ],OO0OOOO0OOOOOO00O [3 ]]#line:512
                O0OO000OOOOO0O00O =[OO0OOOO0OOOOOO00O [0 ]+OO0OOOO0OOOOOO00O [2 ],OO0OOOO0OOOOOO00O [1 ]+OO0OOOO0OOOOOO00O [3 ]]#line:513
                O00OOOO00OO0O00OO =[O0O0O0000000OO000 [0 ],O0O0O0000000OO000 [1 ]]#line:514
                O0O00O00OOO0O0O00 =[O0O0O0000000OO000 [2 ],O0O0O0000000OO000 [3 ]]#line:515
                O0000O0O00O000O00 =[O0O0O0000000OO000 [0 ]+O0O0O0000000OO000 [2 ],O0O0O0000000OO000 [1 ]+O0O0O0000000OO000 [3 ]]#line:516
                O0O0O00O0OO0OOOO0 [0 ,0 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,0 ],x =OOO00OO00O00OOOOO ,y =OOOO00O00O000OO0O ,color ='orange')#line:517
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,0 ],OO0OOOO0OOOOOO00O [0 ]+OO0OOOO0OOOOOO00O [1 ])#line:519
                O0O0O00O0OO0OOOO0 [0 ,1 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,1 ],x =OOO00OO00O00OOOOO ,y =O00OOOO00OO0O00OO ,color ="green")#line:521
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,1 ],O0O0O0000000OO000 [0 ]+O0O0O0000000OO000 [1 ])#line:523
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:525
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:526
                O0O0O0O000O00OOOO =sns .color_palette ("Oranges",as_cmap =True )#line:528
                OO000000O000OO00O =sns .color_palette ("Greens",as_cmap =True )#line:529
                O0O0O00O0OO0OOOO0 [1 ,0 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,0 ],data =[OOOO00O00O000OO0O ,OO0O0O000O0000000 ],xticklabels =OOO00OO00O00OOOOO ,yticklabels =O00O0OOOOOO00000O ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0O0O000O00OOOO )#line:532
                O0O0O00O0OO0OOOO0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:534
                O0O0O00O0OO0OOOO0 [1 ,1 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,1 ],data =[O00OOOO00OO0O00OO ,O0O00O00OOO0O0O00 ],xticklabels =OOO00OO00O00OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OO000000O000OO00O )#line:538
                O0O0O00O0OO0OOOO0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:540
                O0OO000O000O00OO0 =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']['frst']#line:542
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (title ="\n".join (wrap (O0OO000O000O00OO0 ,30 )))#line:543
                O0O0OO00OOO000O00 =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']['scnd']#line:544
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (title ="\n".join (wrap (O0O0OO00OOO000O00 ,30 )))#line:545
                OOOO0OOOOOOO000OO =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']#line:547
                O00OOOOOOOOO000OO .suptitle ("Antecedent : "+OOOO0OOOOOOO000OO ['ante']+"\nSuccedent : "+OOOO0OOOOOOO000OO ['succ']+"\nCondition : "+OOOO0OOOOOOO000OO ['cond']+"\nFirst : "+OOOO0OOOOOOO000OO ['frst']+"\nSecond : "+OOOO0OOOOOOO000OO ['scnd'],x =0 ,ha ='left',size ='small')#line:552
                O00OOOOOOOOO000OO .tight_layout ()#line:554
            elif (OOOOOOO00O00OO0OO .result ['taskinfo']['task_type']=="CFMiner")or (OOOOOOO00O00OO0OO .result ['taskinfo']['task_type']=="UICMiner"):#line:557
                O00OO000O00OO0000 =OOOOOOO00O00OO0OO .result ['taskinfo']['task_type']=="UICMiner"#line:558
                O00OOOOOOOOO000OO ,O0O0O00O0OO0OOOO0 =plt .subplots (2 ,2 ,gridspec_kw ={'height_ratios':[3 ,1 ]})#line:559
                O00OOO00O0O0O000O =OOOOOOO00O00OO0OO .result ['taskinfo']['target']#line:560
                OOO00OO00O00OOOOO =OOOOOOO00O00OO0OO .result ['datalabels']['catnames'][OOOOOOO00O00OO0OO .result ['datalabels']['varname'].index (OOOOOOO00O00OO0OO .result ['taskinfo']['target'])]#line:562
                O0O0OO0OOO0OO0OOO =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]#line:563
                O0000O000O0000O0O =OOOOOOO00O00OO0OO .get_hist (OOO0OOO00O00OOO00 )#line:564
                if O00OO000O00OO0000 :#line:565
                    O0000O000O0000O0O =O0O0OO0OOO0OO0OOO ['params']['hist']#line:566
                else :#line:567
                    O0000O000O0000O0O =OOOOOOO00O00OO0OO .get_hist (OOO0OOO00O00OOO00 )#line:568
                O0O0O00O0OO0OOOO0 [0 ,0 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,0 ],x =OOO00OO00O00OOOOO ,y =O0000O000O0000O0O ,color ='lightsteelblue')#line:569
                OO000000OO00OO000 =[]#line:571
                O000OO00O0OOOOOO0 =[]#line:572
                if O00OO000O00OO0000 :#line:573
                    OO000000OO00OO000 =OOO00OO00O00OOOOO #line:574
                    O000OO00O0OOOOOO0 =OOOOOOO00O00OO0OO .get_hist (OOO0OOO00O00OOO00 ,fullCond =True )#line:575
                else :#line:576
                    OO000000OO00OO000 =OOOOOOO00O00OO0OO .profiles ['hist_target_entire_dataset_labels']#line:577
                    O000OO00O0OOOOOO0 =OOOOOOO00O00OO0OO .profiles ['hist_target_entire_dataset_values']#line:578
                O0O0O00O0OO0OOOO0 [0 ,1 ]=sns .barplot (ax =O0O0O00O0OO0OOOO0 [0 ,1 ],x =OO000000OO00OO000 ,y =O000OO00O0OOOOOO0 ,color ="gray",edgecolor ="black")#line:579
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,0 ],sum (O0000O000O0000O0O ),len (O0000O000O0000O0O ))#line:581
                OOOOOOO00O00OO0OO ._annotate_chart (O0O0O00O0OO0OOOO0 [0 ,1 ],sum (O000OO00O0OOOOOO0 ),len (O000OO00O0OOOOOO0 ))#line:582
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:584
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:585
                OO00O0O0OOO00O0O0 =[OOO00OO00O00OOOOO ,O0000O000O0000O0O ]#line:587
                OO000000O00OO0OO0 =pd .DataFrame (OO00O0O0OOO00O0O0 ).transpose ()#line:588
                OO000000O00OO0OO0 .columns =[O00OOO00O0O0O000O ,'No of observatios']#line:589
                O0O0O0O000O00OOOO =sns .color_palette ("Blues",as_cmap =True )#line:591
                OO000000O000OO00O =sns .color_palette ("Greys",as_cmap =True )#line:592
                O0O0O00O0OO0OOOO0 [1 ,0 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,0 ],data =np .asarray ([O0000O000O0000O0O ]),xticklabels =OOO00OO00O00OOOOO ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =O0O0O0O000O00OOOO )#line:596
                O0O0O00O0OO0OOOO0 [1 ,0 ].set (xlabel =O00OOO00O0O0O000O ,ylabel ='Count')#line:598
                O0O0O00O0OO0OOOO0 [1 ,1 ]=sns .heatmap (ax =O0O0O00O0OO0OOOO0 [1 ,1 ],data =np .asarray ([O000OO00O0OOOOOO0 ]),xticklabels =OO000000OO00OO000 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OO000000O000OO00O )#line:602
                O0O0O00O0OO0OOOO0 [1 ,1 ].set (xlabel =O00OOO00O0O0O000O ,ylabel ='Count')#line:604
                O00000OOO0O0OOO0O =""#line:605
                OO0OOO00O0O0OOOOO ='Entire dataset'#line:606
                if O00OO000O00OO0000 :#line:607
                    if len (O0O0OO0OOO0OO0OOO ['cedents_struct']['cond'])>0 :#line:608
                        OO0OOO00O0O0OOOOO =O0O0OO0OOO0OO0OOO ['cedents_str']['cond']#line:609
                        O00000OOO0O0OOO0O =" & "+O0O0OO0OOO0OO0OOO ['cedents_str']['cond']#line:610
                O0O0O00O0OO0OOOO0 [0 ,1 ].set (title =OO0OOO00O0O0OOOOO )#line:611
                if O00OO000O00OO0000 :#line:612
                    O0OO000O000O00OO0 =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']['ante']+O00000OOO0O0OOO0O #line:613
                else :#line:614
                    O0OO000O000O00OO0 =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']['cond']#line:615
                O0O0O00O0OO0OOOO0 [0 ,0 ].set (title ="\n".join (wrap (O0OO000O000O00OO0 ,30 )))#line:616
                OOOO0OOOOOOO000OO =OOOOOOO00O00OO0OO .result ["rules"][OOO0OOO00O00OOO00 -1 ]['cedents_str']#line:618
                OO0OOO00O0O0OOOOO ="Condition : "+OOOO0OOOOOOO000OO ['cond']#line:619
                if O00OO000O00OO0000 :#line:620
                    OO0OOO00O0O0OOOOO =OO0OOO00O0O0OOOOO +"\nAntecedent : "+OOOO0OOOOOOO000OO ['ante']#line:621
                O00OOOOOOOOO000OO .suptitle (OO0OOO00O0O0OOOOO ,x =0 ,ha ='left',size ='small')#line:622
                O00OOOOOOOOO000OO .tight_layout ()#line:624
            else :#line:625
                print ("Unsupported task type for rule details")#line:626
                return #line:627
            if filename is not None :#line:628
                plt .savefig (filename =filename )#line:629
            if show :#line:630
                plt .show ()#line:631
            print ("")#line:633
        else :#line:634
            print ("No such rule.")#line:635
    def get_rulecount (O000OOOOOO0O0OO0O ):#line:637
        ""#line:642
        if not (O000OOOOOO0O0OO0O ._is_calculated ()):#line:643
            print ("ERROR: Task has not been calculated.")#line:644
            return #line:645
        return len (O000OOOOOO0O0OO0O .result ["rules"])#line:646
    def get_fourfold (O0OOO0000O00O000O ,O0O000O0OO0OO0O00 ,order =0 ):#line:648
        ""#line:655
        if not (O0OOO0000O00O000O ._is_calculated ()):#line:656
            print ("ERROR: Task has not been calculated.")#line:657
            return #line:658
        if (O0O000O0OO0OO0O00 <=len (O0OOO0000O00O000O .result ["rules"])):#line:659
            if O0OOO0000O00O000O .result ['taskinfo']['task_type']=="4ftMiner":#line:660
                O0O0O00OOOO0O0000 =O0OOO0000O00O000O .result ["rules"][O0O000O0OO0OO0O00 -1 ]#line:661
                return O0O0O00OOOO0O0000 ['params']['fourfold']#line:662
            elif O0OOO0000O00O000O .result ['taskinfo']['task_type']=="CFMiner":#line:663
                print ("Error: fourfold for CFMiner is not defined")#line:664
                return None #line:665
            elif O0OOO0000O00O000O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:666
                O0O0O00OOOO0O0000 =O0OOO0000O00O000O .result ["rules"][O0O000O0OO0OO0O00 -1 ]#line:667
                if order ==1 :#line:668
                    return O0O0O00OOOO0O0000 ['params']['fourfold1']#line:669
                if order ==2 :#line:670
                    return O0O0O00OOOO0O0000 ['params']['fourfold2']#line:671
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:672
                return None #line:673
            else :#line:674
                print ("Unsupported task type for rule details")#line:675
        else :#line:676
            print ("No such rule.")#line:677
    def get_hist (OO0000O0O0O00O0OO ,O000000O0O0O0O0OO ,fullCond =True ):#line:679
        ""#line:686
        if not (OO0000O0O0O00O0OO ._is_calculated ()):#line:687
            print ("ERROR: Task has not been calculated.")#line:688
            return #line:689
        if (O000000O0O0O0O0OO <=len (OO0000O0O0O00O0OO .result ["rules"])):#line:690
            if OO0000O0O0O00O0OO .result ['taskinfo']['task_type']=="CFMiner":#line:691
                OOO00O00O00OO0O00 =OO0000O0O0O00O0OO .result ["rules"][O000000O0O0O0O0OO -1 ]#line:692
                return OOO00O00O00OO0O00 ['params']['hist']#line:693
            elif OO0000O0O0O00O0OO .result ['taskinfo']['task_type']=="UICMiner":#line:694
                OOO00O00O00OO0O00 =OO0000O0O0O00O0OO .result ["rules"][O000000O0O0O0O0OO -1 ]#line:695
                O0O00OOOOOOO00O00 =None #line:696
                if fullCond :#line:697
                    O0O00OOOOOOO00O00 =OOO00O00O00OO0O00 ['params']['hist_cond']#line:698
                else :#line:699
                    O0O00OOOOOOO00O00 =OOO00O00O00OO0O00 ['params']['hist']#line:700
                return O0O00OOOOOOO00O00 #line:701
            elif OO0000O0O0O00O0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:702
                print ("Error: SD4ft-Miner has no histogram")#line:703
                return None #line:704
            elif OO0000O0O0O00O0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:705
                print ("Error: 4ft-Miner has no histogram")#line:706
                return None #line:707
            else :#line:708
                print ("Unsupported task type for rule details")#line:709
        else :#line:710
            print ("No such rule.")#line:711
    def get_hist_cond (O0O000OO00OO0OOOO ,O0OOOO00OO0OO0O00 ):#line:714
        ""#line:720
        if not (O0O000OO00OO0OOOO ._is_calculated ()):#line:721
            print ("ERROR: Task has not been calculated.")#line:722
            return #line:723
        if (O0OOOO00OO0OO0O00 <=len (O0O000OO00OO0OOOO .result ["rules"])):#line:725
            if O0O000OO00OO0OOOO .result ['taskinfo']['task_type']=="UICMiner":#line:726
                OO0OOO0O0OO00OO00 =O0O000OO00OO0OOOO .result ["rules"][O0OOOO00OO0OO0O00 -1 ]#line:727
                return OO0OOO0O0OO00OO00 ['params']['hist_cond']#line:728
            elif O0O000OO00OO0OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:729
                OO0OOO0O0OO00OO00 =O0O000OO00OO0OOOO .result ["rules"][O0OOOO00OO0OO0O00 -1 ]#line:730
                return OO0OOO0O0OO00OO00 ['params']['hist']#line:731
            elif O0O000OO00OO0OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:732
                print ("Error: SD4ft-Miner has no histogram")#line:733
                return None #line:734
            elif O0O000OO00OO0OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:735
                print ("Error: 4ft-Miner has no histogram")#line:736
                return None #line:737
            else :#line:738
                print ("Unsupported task type for rule details")#line:739
        else :#line:740
            print ("No such rule.")#line:741
    def get_quantifiers (OOO00OO0O00O00000 ,O0O00OO0O00OO0OOO ,order =0 ):#line:743
        ""#line:752
        if not (OOO00OO0O00O00000 ._is_calculated ()):#line:753
            print ("ERROR: Task has not been calculated.")#line:754
            return None #line:755
        if (O0O00OO0O00OO0OOO <=len (OOO00OO0O00O00000 .result ["rules"])):#line:757
            OOO00OO0OO0O0O00O =OOO00OO0O00O00000 .result ["rules"][O0O00OO0O00OO0OOO -1 ]#line:758
            if OOO00OO0O00O00000 .result ['taskinfo']['task_type']=="4ftMiner":#line:759
                return OOO00OO0OO0O0O00O ['params']#line:760
            elif OOO00OO0O00O00000 .result ['taskinfo']['task_type']=="CFMiner":#line:761
                return OOO00OO0OO0O0O00O ['params']#line:762
            elif OOO00OO0O00O00000 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:763
                return OOO00OO0OO0O0O00O ['params']#line:764
            else :#line:765
                print ("Unsupported task type for rule details")#line:766
        else :#line:767
            print ("No such rule.")#line:768
    def get_varlist (O0O0000OO00OO00OO ):#line:770
        ""#line:774
        return O0O0000OO00OO00OO .result ["datalabels"]["varname"]#line:776
    def get_category_names (OO00OOO0OOO0000OO ,varname =None ,varindex =None ):#line:778
        ""#line:785
        O0OO00OO0000O00OO =0 #line:786
        if varindex is not None :#line:787
            if O0OO00OO0000O00OO >=0 &O0OO00OO0000O00OO <len (OO00OOO0OOO0000OO .get_varlist ()):#line:788
                O0OO00OO0000O00OO =varindex #line:789
            else :#line:790
                print ("Error: no such variable.")#line:791
                return #line:792
        if (varname is not None ):#line:793
            OO00O00OOOO0OOO0O =OO00OOO0OOO0000OO .get_varlist ()#line:794
            O0OO00OO0000O00OO =OO00O00OOOO0OOO0O .index (varname )#line:795
            if O0OO00OO0000O00OO ==-1 |O0OO00OO0000O00OO <0 |O0OO00OO0000O00OO >=len (OO00OOO0OOO0000OO .get_varlist ()):#line:796
                print ("Error: no such variable.")#line:797
                return #line:798
        return OO00OOO0OOO0000OO .result ["datalabels"]["catnames"][O0OO00OO0000O00OO ]#line:799
    def print_data_definition (OO0OO000OOOOO0000 ):#line:801
        ""#line:804
        O000OO0OO0O0O0O0O =OO0OO000OOOOO0000 .get_varlist ()#line:805
        print (f"Dataset has {len(O000OO0OO0O0O0O0O)} variables.")#line:806
        for O0OO0O0O0OO00OO0O in O000OO0OO0O0O0O0O :#line:807
            OO0OOOO0O0OOO0OO0 =OO0OO000OOOOO0000 .get_category_names (O0OO0O0O0OO00OO0O )#line:808
            O000OOO0OO00OOO00 =""#line:809
            for O00O0OO000000000O in OO0OOOO0O0OOO0OO0 :#line:810
                O000OOO0OO00OOO00 =O000OOO0OO00OOO00 +str (O00O0OO000000000O )+" "#line:811
            O000OOO0OO00OOO00 =O000OOO0OO00OOO00 [:-1 ]#line:812
            print (f"Variable {O0OO0O0O0OO00OO0O} has {len(OO0OOOO0O0OOO0OO0)} categories: {O000OOO0OO00OOO00}")#line:813
    def _is_calculated (O0OO0OOOOO0O0O0OO ):#line:815
        ""#line:820
        OOO00O0O00O0O0OOO =False #line:821
        if 'taskinfo'in O0OO0OOOOO0O0O0OO .result :#line:822
            OOO00O0O00O0O0OOO =True #line:823
        return OOO00O0O00O0O0OOO #line:824
    def save (O0000O00OO0O0O000 ,O0OO0OOOO0O000000 ,savedata =False ,embeddata =True ,fmt ='pickle'):#line:826
        if not (O0000O00OO0O0O000 ._is_calculated ()):#line:827
            print ("ERROR: Task has not been calculated.")#line:828
            return None #line:829
        O00O000O000OOOOO0 ={'program':'CleverMiner','version':O0000O00OO0O0O000 .get_version_string ()}#line:830
        OOOO0O00OO0OOO000 ={}#line:831
        OOOO0O00OO0OOO000 ['control']=O00O000O000OOOOO0 #line:832
        OOOO0O00OO0OOO000 ['result']=O0000O00OO0O0O000 .result #line:833
        OOOO0O00OO0OOO000 ['stats']=O0000O00OO0O0O000 .stats #line:835
        OOOO0O00OO0OOO000 ['options']=O0000O00OO0O0O000 .options #line:836
        OOOO0O00OO0OOO000 ['profiles']=O0000O00OO0O0O000 .profiles #line:837
        if savedata :#line:838
            if embeddata :#line:839
                OOOO0O00OO0OOO000 ['data']=O0000O00OO0O0O000 .data #line:840
                OOOO0O00OO0OOO000 ['df']=O0000O00OO0O0O000 .df #line:841
            else :#line:842
                O0O00OO0O0OOO0000 ={}#line:843
                O0O00OO0O0OOO0000 ['data']=O0000O00OO0O0O000 .data #line:844
                O0O00OO0O0OOO0000 ['df']=O0000O00OO0O0O000 .df #line:845
                print (f"CALC HASH {datetime.now()}")#line:846
                OO0OO00O0OO00OO0O =O0000O00OO0O0O000 ._get_fast_hash (O0O00OO0O0OOO0000 )#line:848
                print (f"CALC HASH ...done {datetime.now()}")#line:849
                O0000OO0O0OO000OO =os .path .join (O0000O00OO0O0O000 .cache_dir ,OO0OO00O0OO00OO0O +'.clmdata')#line:850
                O00O00OO00OO0OO0O =open (O0000OO0O0OO000OO ,'wb')#line:853
                pickle .dump (O0O00OO0O0OOO0000 ,O00O00OO00OO0OO0O ,protocol =pickle .HIGHEST_PROTOCOL )#line:854
                OOOO0O00OO0OOO000 ['datafile']=O0000OO0O0OO000OO #line:857
        if fmt =='pickle':#line:859
            O0O0O0O00000OO0O0 =open (O0OO0OOOO0O000000 ,'wb')#line:860
            pickle .dump (OOOO0O00OO0OOO000 ,O0O0O0O00000OO0O0 ,protocol =pickle .HIGHEST_PROTOCOL )#line:861
        elif fmt =='json':#line:862
            O0O0O0O00000OO0O0 =open (O0OO0OOOO0O000000 ,'w')#line:863
            json .dump (OOOO0O00OO0OOO000 ,O0O0O0O00000OO0O0 )#line:864
        else :#line:865
            print (f"Unsupported format - {fmt}. Supported formats are pickle, json.")#line:866
    def load (O00O00O0000000O0O ,O0000OO0O00000000 ,fmt ='pickle'):#line:870
        if fmt =='pickle':#line:871
            O00O0O0O0OOO0OOOO =open (O0000OO0O00000000 ,'rb')#line:872
            OOOO0O0OOOO0OO00O =pickle .load (O00O0O0O0OOO0OOOO )#line:873
        elif fmt =='json':#line:874
            O00O0O0O0OOO0OOOO =open (O0000OO0O00000000 ,'r')#line:875
            OOOO0O0OOOO0OO00O =json .load (O00O0O0O0OOO0OOOO )#line:876
        else :#line:877
            print (f"Unsupported format - {fmt}. Supported formats are pickle, json.")#line:878
            return #line:879
        if not 'control'in OOOO0O0OOOO0OO00O :#line:880
            print ('Error: not a CleverMiner save file (1)')#line:881
            return None #line:882
        OO0O0O00O00000000 =OOOO0O0OOOO0OO00O ['control']#line:883
        if not ('program'in OO0O0O00O00000000 )or not ('version'in OO0O0O00O00000000 ):#line:884
            print ('Error: not a CleverMiner save file (2)')#line:885
            return None #line:886
        if not (OO0O0O00O00000000 ['program']=='CleverMiner'):#line:887
            print ('Error: not a CleverMiner save file (3)')#line:888
            return None #line:889
        O00O00O0000000O0O .result =OOOO0O0OOOO0OO00O ['result']#line:890
        O00O00O0000000O0O .stats =OOOO0O0OOOO0OO00O ['stats']#line:892
        O00O00O0000000O0O .options =OOOO0O0OOOO0OO00O ['options']#line:893
        if 'profiles'in OOOO0O0OOOO0OO00O :#line:894
            O00O00O0000000O0O .profiles =OOOO0O0OOOO0OO00O ['profiles']#line:895
        if 'data'in OOOO0O0OOOO0OO00O :#line:896
            O00O00O0000000O0O .data =OOOO0O0OOOO0OO00O ['data']#line:897
            O00O00O0000000O0O ._initialized =True #line:898
        if 'df'in OOOO0O0OOOO0OO00O :#line:899
            O00O00O0000000O0O .df =OOOO0O0OOOO0OO00O ['df']#line:900
        if 'datafile'in OOOO0O0OOOO0OO00O :#line:901
            try :#line:902
                OO00O00000000O000 =open (OOOO0O0OOOO0OO00O ['datafile'],'rb')#line:903
                OOO0OOO0OOO00OO0O =pickle .load (OO00O00000000O000 )#line:904
                O00O00O0000000O0O .data =OOO0OOO0OOO00OO0O ['data']#line:905
                O00O00O0000000O0O .df =OOO0OOO0OOO00OO0O ['df']#line:906
                print (f"...data loaded from file {OOOO0O0OOOO0OO00O['datafile']}.")#line:907
            except :#line:908
                print (f"Error loading saved file. Linked data file does not exists or it is in incorrect structure or path. If you are transferring saved file to another computer, please embed also data.")#line:910
                exit (1 )#line:911
        print (f"File {O0000OO0O00000000} loaded ok.")#line:912
    def get_version_string (OO00OO0OO0O0OOO00 ):#line:915
        ""#line:920
        return OO00OO0OO0O0OOO00 .version_string #line:921
    def get_rule_cedent_list (OO0000000O000O00O ,O0OO00OO0OOO0OOOO ):#line:923
        ""#line:929
        if not (OO0000000O000O00O ._is_calculated ()):#line:930
            print ("ERROR: Task has not been calculated.")#line:931
            return #line:932
        if O0OO00OO0OOO0OOOO <=0 or O0OO00OO0OOO0OOOO >OO0000000O000O00O .get_rulecount ():#line:933
            if OO0000000O000O00O .get_rulecount ()==0 :#line:934
                print ("No such rule. There are no rules in result.")#line:935
            else :#line:936
                print (f"No such rule ({O0OO00OO0OOO0OOOO}). Available rules are 1 to {OO0000000O000O00O.get_rulecount()}")#line:937
            return None #line:938
        O00000OO0OO000OO0 =[]#line:939
        O0000O0OO000O0OOO =OO0000000O000O00O .result ["rules"][O0OO00OO0OOO0OOOO -1 ]#line:940
        O00000OO0OO000OO0 =list (O0000O0OO000O0OOO ['trace_cedent_dataorder'].keys ())#line:941
        return O00000OO0OO000OO0 #line:943
    def get_rule_variables (O0O00OOO0OOO00000 ,O00000OOOO00OO000 ,OO0O000000OO0OOOO ,get_names =True ):#line:946
        ""#line:954
        if not (O0O00OOO0OOO00000 ._is_calculated ()):#line:955
            print ("ERROR: Task has not been calculated.")#line:956
            return #line:957
        if O00000OOOO00OO000 <=0 or O00000OOOO00OO000 >O0O00OOO0OOO00000 .get_rulecount ():#line:958
            if O0O00OOO0OOO00000 .get_rulecount ()==0 :#line:959
                print ("No such rule. There are no rules in result.")#line:960
            else :#line:961
                print (f"No such rule ({O00000OOOO00OO000}). Available rules are 1 to {O0O00OOO0OOO00000.get_rulecount()}")#line:962
            return None #line:963
        O0O0OOOO00OOO0O00 =[]#line:964
        OOO0OOO000O0O0OOO =O0O00OOO0OOO00000 .result ["rules"][O00000OOOO00OO000 -1 ]#line:965
        O00OO0O0O00O0O000 =O0O00OOO0OOO00000 .result ["datalabels"]['varname']#line:966
        if not (OO0O000000OO0OOOO in OOO0OOO000O0O0OOO ['trace_cedent_dataorder']):#line:967
            print (f"ERROR: cedent {OO0O000000OO0OOOO} not in result.")#line:968
            exit (1 )#line:969
        for OO00OOOOOOOOO0O0O in OOO0OOO000O0O0OOO ['trace_cedent_dataorder'][OO0O000000OO0OOOO ]:#line:970
            if get_names :#line:971
                O0O0OOOO00OOO0O00 .append (O00OO0O0O00O0O000 [OO00OOOOOOOOO0O0O ])#line:972
            else :#line:973
                O0O0OOOO00OOO0O00 .append (OO00OOOOOOOOO0O0O )#line:974
        return O0O0OOOO00OOO0O00 #line:976
    def get_rule_categories (OO0OO0OOO0OOO00OO ,OO00OO000O0O00OOO ,OOOO0O00OO0OOOOOO ,OO000OOO0000OO00O ,get_names =True ):#line:979
        ""#line:988
        if not (OO0OO0OOO0OOO00OO ._is_calculated ()):#line:989
            print ("ERROR: Task has not been calculated.")#line:990
            return #line:991
        if OO00OO000O0O00OOO <=0 or OO00OO000O0O00OOO >OO0OO0OOO0OOO00OO .get_rulecount ():#line:992
            if OO0OO0OOO0OOO00OO .get_rulecount ()==0 :#line:993
                print ("No such rule. There are no rules in result.")#line:994
            else :#line:995
                print (f"No such rule ({OO00OO000O0O00OOO}). Available rules are 1 to {OO0OO0OOO0OOO00OO.get_rulecount()}")#line:996
            return None #line:997
        OO0OOO0O000O000OO =[]#line:998
        OOOOOOO0OOOOO000O =OO0OO0OOO0OOO00OO .result ["rules"][OO00OO000O0O00OOO -1 ]#line:999
        OOOOOO000OOO0O000 =OO0OO0OOO0OOO00OO .result ["datalabels"]['varname']#line:1000
        if OO000OOO0000OO00O in OOOOOO000OOO0O000 :#line:1001
            O0O00OO00O0OOO0OO =OOOOOO000OOO0O000 .index (OO000OOO0000OO00O )#line:1002
            OOOO0O0OO00OOO0OO =OO0OO0OOO0OOO00OO .result ['datalabels']['catnames'][O0O00OO00O0OOO0OO ]#line:1003
            if not (OOOO0O00OO0OOOOOO in OOOOOOO0OOOOO000O ['trace_cedent_dataorder']):#line:1004
                print (f"ERROR: cedent {OOOO0O00OO0OOOOOO} not in result.")#line:1005
                exit (1 )#line:1006
            OOO000OOOO0O0O0OO =OOOOOOO0OOOOO000O ['trace_cedent_dataorder'][OOOO0O00OO0OOOOOO ].index (O0O00OO00O0OOO0OO )#line:1007
            for OOOO0O00000000OO0 in OOOOOOO0OOOOO000O ['traces'][OOOO0O00OO0OOOOOO ][OOO000OOOO0O0O0OO ]:#line:1008
                if get_names :#line:1009
                    OO0OOO0O000O000OO .append (OOOO0O0OO00OOO0OO [OOOO0O00000000OO0 ])#line:1010
                else :#line:1011
                    OO0OOO0O000O000OO .append (OOOO0O00000000OO0 )#line:1012
        else :#line:1013
            print (f"ERROR: variable not found: {OOOO0O00OO0OOOOOO},{OO000OOO0000OO00O}. Possible variables are {OOOOOO000OOO0O000}")#line:1014
            exit (1 )#line:1015
        return OO0OOO0O000O000OO #line:1016
    def get_dataset_variable_count (O00O0OO0OO00OOO00 ):#line:1019
        ""#line:1024
        if not (O00O0OO0OO00OOO00 ._is_calculated ()):#line:1025
            print ("ERROR: Task has not been calculated.")#line:1026
            return #line:1027
        O0OOO00OOO0O0OO0O =O00O0OO0OO00OOO00 .result ["datalabels"]['varname']#line:1028
        return len (O0OOO00OOO0O0OO0O )#line:1029
    def get_dataset_variable_list (OO0OOO0OO0OOO0O0O ):#line:1032
        ""#line:1037
        if not (OO0OOO0OO0OOO0O0O ._is_calculated ()):#line:1038
            print ("ERROR: Task has not been calculated.")#line:1039
            return #line:1040
        O00OO00OO0OOOO00O =OO0OOO0OO0OOO0O0O .result ["datalabels"]['varname']#line:1041
        return O00OO00OO0OOOO00O #line:1042
    def get_dataset_variable_name (OO0OO0OOOO0000O0O ,O000OO000O000O0OO ):#line:1045
        ""#line:1051
        if not (OO0OO0OOOO0000O0O ._is_calculated ()):#line:1052
            print ("ERROR: Task has not been calculated.")#line:1053
            return #line:1054
        OOO0OOO00OOO0OOOO =OO0OO0OOOO0000O0O .get_dataset_variable_list ()#line:1055
        if O000OO000O000O0OO >=0 and O000OO000O000O0OO <len (OOO0OOO00OOO0OOOO ):#line:1056
            return OOO0OOO00OOO0OOOO [O000OO000O000O0OO ]#line:1057
        else :#line:1058
            print (f"ERROR: dataset has only {len(OOO0OOO00OOO0OOOO)} variables, required index is {O000OO000O000O0OO}, but available values are 0-{len(OOO0OOO00OOO0OOOO)-1}.")#line:1059
            exit (1 )#line:1060
    def get_dataset_variable_index (O0000O0OO0OOO0O00 ,OO0OOO0OOO000O000 ):#line:1062
        ""#line:1068
        if not (O0000O0OO0OOO0O00 ._is_calculated ()):#line:1069
            print ("ERROR: Task has not been calculated.")#line:1070
            return #line:1071
        OOO0O0OOO0O00OO00 =O0000O0OO0OOO0O00 .get_dataset_variable_list ()#line:1072
        if OO0OOO0OOO000O000 in OOO0O0OOO0O00OO00 :#line:1073
            return OOO0O0OOO0O00OO00 .index (OO0OOO0OOO000O000 )#line:1074
        else :#line:1075
            print (f"ERROR: attribute {OO0OOO0OOO000O000} is not in dataset. The list of attribute names is  {OOO0O0OOO0O00OO00}.")#line:1076
            exit (1 )#line:1077
    def get_dataset_category_list (OO0000OOO0OO00000 ,O0O0O00O000O00OO0 ):#line:1080
        ""#line:1086
        if not (OO0000OOO0OO00000 ._is_calculated ()):#line:1087
            print ("ERROR: Task has not been calculated.")#line:1088
            return #line:1089
        OO000O0000OOO0O0O =OO0000OOO0OO00000 .result ["datalabels"]['catnames']#line:1090
        O0O00OO0OOO0OOOO0 =None #line:1091
        if isinstance (O0O0O00O000O00OO0 ,int ):#line:1092
            O0O00OO0OOO0OOOO0 =O0O0O00O000O00OO0 #line:1093
        else :#line:1094
            O0O00OO0OOO0OOOO0 =OO0000OOO0OO00000 .get_dataset_variable_index (O0O0O00O000O00OO0 )#line:1095
        if O0O00OO0OOO0OOOO0 >=0 and O0O00OO0OOO0OOOO0 <len (OO000O0000OOO0O0O ):#line:1097
            return OO000O0000OOO0O0O [O0O00OO0OOO0OOOO0 ]#line:1098
        else :#line:1099
            print (f"ERROR: dataset has only {len(OO000O0000OOO0O0O)} variables, required index is {O0O00OO0OOO0OOOO0}, but available values are 0-{len(OO000O0000OOO0O0O)-1}.")#line:1100
            exit (1 )#line:1101
    def get_dataset_category_count (OOO00OO0O00O0OOOO ,O00OOOOOO0O000O0O ):#line:1103
        ""#line:1109
        if not (OOO00OO0O00O0OOOO ._is_calculated ()):#line:1110
            print ("ERROR: Task has not been calculated.")#line:1111
            return #line:1112
        O00O0OO0OO0OOO0OO =None #line:1113
        if isinstance (O00OOOOOO0O000O0O ,int ):#line:1114
            O00O0OO0OO0OOO0OO =O00OOOOOO0O000O0O #line:1115
        else :#line:1116
            O00O0OO0OO0OOO0OO =OOO00OO0O00O0OOOO .get_dataset_variable_index (O00OOOOOO0O000O0O )#line:1117
        O0OOOO00OOO0OOO00 =OOO00OO0O00O0OOOO .get_dataset_category_list (O00O0OO0OO0OOO0OO )#line:1118
        return len (O0OOOO00OOO0OOO00 )#line:1119
    def get_dataset_category_name (O00000O0OO000OO00 ,OO00OOO0O00O000OO ,O0O0OOO0000OO0000 ):#line:1122
        ""#line:1129
        if not (O00000O0OO000OO00 ._is_calculated ()):#line:1130
            print ("ERROR: Task has not been calculated.")#line:1131
            return #line:1132
        OOO0O0OO00000O00O =None #line:1133
        if isinstance (OO00OOO0O00O000OO ,int ):#line:1134
            OOO0O0OO00000O00O =OO00OOO0O00O000OO #line:1135
        else :#line:1136
            OOO0O0OO00000O00O =O00000O0OO000OO00 .get_dataset_variable_index (OO00OOO0O00O000OO )#line:1137
        O0000O000O0OO0OO0 =O00000O0OO000OO00 .get_dataset_category_list (OOO0O0OO00000O00O )#line:1139
        if O0O0OOO0000OO0000 >=0 and O0O0OOO0000OO0000 <len (O0000O000O0OO0OO0 ):#line:1140
            return O0000O000O0OO0OO0 [O0O0OOO0000OO0000 ]#line:1141
        else :#line:1142
            print (f"ERROR: variable has only {len(O0000O000O0OO0OO0)} categories, required index is {O0O0OOO0000OO0000}, but available values are 0-{len(O0000O000O0OO0OO0)-1}.")#line:1143
            exit (1 )#line:1144
    def get_dataset_category_index (OO000OOO00OOOO0OO ,OO0OO000OOO0OO0O0 ,OOO00OOOO0OOOOOOO ):#line:1147
        ""#line:1154
        if not (OO000OOO00OOOO0OO ._is_calculated ()):#line:1155
            print ("ERROR: Task has not been calculated.")#line:1156
            return #line:1157
        O0000OOOO0OO0O0OO =None #line:1158
        if isinstance (OO0OO000OOO0OO0O0 ,int ):#line:1159
            O0000OOOO0OO0O0OO =OO0OO000OOO0OO0O0 #line:1160
        else :#line:1161
            O0000OOOO0OO0O0OO =OO000OOO00OOOO0OO .get_dataset_variable_index (OO0OO000OOO0OO0O0 )#line:1162
        OOO00OOO00O0O000O =OO000OOO00OOOO0OO .get_dataset_category_list (O0000OOOO0OO0O0OO )#line:1163
        if OOO00OOOO0OOOOOOO in OOO00OOO00O0O000O :#line:1164
            return OOO00OOO00O0O000O .index (OOO00OOOO0OOOOOOO )#line:1165
        else :#line:1166
            print (f"ERROR: value {OOO00OOOO0OOOOOOO} is invalid for the variable {OO000OOO00OOOO0OO.get_dataset_variable_name(O0000OOOO0OO0O0OO)}. Available category names are {OOO00OOO00O0O000O}.")#line:1167
            exit (1 )#line:1168
