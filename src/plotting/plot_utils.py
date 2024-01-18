'''
Utility file for containing information which needs to be referenced by multiple plots scripts

Mainly contains dictionaries used for handling the translation between the nceplibs output and readable formats or satinfo files.
'''

#Dictionary of satellite names used for getting sat info files
#For scripts to run successfully, they expect every sat we have data for to have a dictionary entry
sat_dictionary={"NOAA 5": "n05", "NOAA 6": "n06", "NOAA 7": "n07", "NOAA 8": "n08", "NOAA 9": "n09", 
                "NOAA 10":"n10", "NOAA 11":"n11","NOAA 12":"n12","NOAA 13":"n13","NOAA 14":"n14",
               "NOAA 15":"n15","NOAA 16":"n16","NOAA 17":"n17","NOAA 18":"n18","NOAA 19":"n19","NOAA 20":"n20", "NOAA 21":"n21",
               "METOP-1":"metop-b","METOP-2":"metop-a","METOP-3":"metop-c",
               "METOP-1 (Metop-A":"metop-b","METOP-2 (Metop-B":"metop-a","METOP-3 (Metop-C":"metop-c",
               "METOP-1 (Metop-B":"metop-b","METOP-2 (Metop-A":"metop-a",
               "AQUA":"aqua", "NPP":"npp",
               "GOES 7" : "g07", "GOES 8": "g08", "GOES 9": "g09", "GOES 10": "g10","GOES 11": "g11","GOES 12": "g12",
               "GOES 13": "g13", "GOES 14": "g14", "GOES 15": "g15", "GOES 16" : "g16", "GOES 17":"g17",
               "MTSAT-2":"MTSAT-2", "MTSAT-1R":"MTSAT-1R",
               "METEOSAT 2" : "m02", "METEOSAT 3": "m03", "METEOSAT 4": "m04","METEOSAT 5": "m05", "METEOSAT 6": "m06", "METEOSAT 7": "m07",
               "METEOSAT 8": "m08", "METEOSAT 9": "m09", "METEOSAT 10": "m10", "METEOSAT 11": "m11",
               "":"",
               "DMSP 8":"f08", "DMSP 9":"f09", "DMSP 10": "f10", "DMSP 11": "f11", "DMSP 12": "f12", "DMSP 13": "f13", 
               "DMSP 14": "f14", "DMSP 15": "f15","DMSP 16": "f16", "DMSP17": "f17", "DMSP18": "f18",
               "CHAMP":"CHAMP","COSMIC-1":"COSMIC-1","COSMIC-2":"COSMIC-2","COSMIC-3":"COSMIC-3","COSMIC-4":"COSMIC-4",
               "COSMIC-5":"COSMIC-5","COSMIC-6":"COSMIC-6","COSMIC-7":"COSMIC-7",
               "COSMIC-2 E1":"COSMIC-2 E1", "COSMIC-2 E2":"COSMIC-2 E2", "COSMIC-2 E3":"COSMIC-2 E3",
                "COSMIC-2 E4":"COSMIC-2 E4", "COSMIC-2 E5":"COSMIC-2 E5", "COSMIC-2 E6":"COSMIC-2 E6",
               "GRACE A":"GRACE A","GRACE B":"GRACE B", "GRACE C (GRACE-F":"GRACE C", "GRACE D (GRACE-F":"GRACE D",
               "SAC-C":"SAC C","TerraSAR-X":"TerraSAR-X","TERRA":"TERRA",
               "ERS 2":"ERS 2", "GMS 3" : "GMS 3 ","GMS 4":"GMS 4","GMS 5":"GMS 5",
               "INSAT 3A":"INSAT 3A","INSAT 3D":"INSAT 3D","INSAT 3DR":"INSAT 3DR",
               "TIROS-N": "TIROS-N",  "Megha-Tropiques": "meghat",
                "TanDEM-X": "TanDEM-X", "PAZ":"PAZ", "KOMPSAT-5": "KOMPSAT-5",
               "LANDSAT 5":"LANDSAT 5", "GPM-core":"GPM-core", "TRMM":"TRMM",
               "Himawari-8":"himawari8", "Himawari-9":"himawari9", "Spire Lemur 3U C":"Spire L3UC", "Sentinel 6A":"Sentinel 6A",
               "PlanetiQ GNOMES-":"PlanetiQ GNOMES"}

#Dictionary for translating typ numbers from cmpbqm output into their full names
typ_dictionary = {
    111:"SYNDAT (110)", 112:"n/a (112)", 120:"ADPUPA (120)", 122:"ADPUPA (122)", 126:"RASSDA (126)", 130:"AIRCFT (130)", 
    131:"AIRCFT (131)", 132:"ADPUPA (132)", 133:"AIRCAR (133)", 134:"AIRCFT (134)", 135:"AIRCFT (135)", 150: "SPSSMI (150)",
    151:"GOESND (151)", 152:"SPSSMI (152)", 153:"GPSIPW (153)", 156:"GOESND (156)", 157:"GOESND (157)", 158:"GOESND (158)", 
    159:"GOESND (159)", 164:"GOESND (164)", 165:"GOESND (165)", 174:"GOESND (174)", 175:"GOESND (175)", 180:"SFCSHP (180)", 
    181:"ADPSFC (181)", 182:"SFCSHP (182)", 183:"ADPSFC,SFCSHP (183)", 187:"ADPSFC (187)", 188:"MSONET (188)", 191:"SFCBOG (191)",
    192:"ADPSFC (192)", 193:"ADPSFC (193)", 194:"SFCSHP (194)", 195:"MSONET (195)", 210:"SYNDAT (210)", 220:"ADPUPA (220)", 
    221:"ADPUPA (221)", 222:"ADPUPA (222)", 223:"PROFLR (223)", 224:"VADWND (224)", 227:"PROFLR (227)", 228:"PROFLR (228)",
    229:"PROFLR (229)", 230:"AIRCFT (230)", 231:"AIRCFT (231)", 232:"ADPUPA (232)", 233:"AIRCAR (233)", 234:"AIRCFT (234)",
    235:"AIRCFT (235)", 240:"SATWND (240)", 241:"SATWND (241)", 242:"SATWND (242)", 243:"SATWND (243)", 244:"SATWND (244)",
    245:"SATWND (245)", 246:"SATWND (246)", 247:"SATWND (247)", 248:"SATWND (248)", 249:"SATWND (249)", 250:"SATWND (250)",
    251:"SATWND (251)", 252:"SATWND (252)", 253:"SATWND (253)", 254:"SATWND (254)", 255:"SATWND (255)", 256:"SATWND (256)",
    257:"SATWND (257)", 258:"SATWND (258)", 259:"SATWND (259)", 260:"SATWND (260)", 270:"(270)", 271:"(271)",
    280:"SFCSHP (280)", 281:"ADPSFC (281)", 282:"SFCSHP (282)", 283:"SPSSMI (283)", 284:"ADPSFC,SFCSHP (284)", 
    285:"QKSWND (285)", 286:"ERS1DA (286)", 287:"ADPSFC (287)", 288:"MSONET (288)", 289:"WDSATR (289)", 
    290:"ASCATW (290)", 291:"(291)", 292:"ADPSFC (292)", 293:"ADPSFC (293)", 294:"SFCSHP (294)", 295:"MSONET (295)"
}

#The naming convention for some satinfo files does not match the basic sensor_satname format so update them from sensor_satname
#into the name used in the satinfo files (for example our sensor is just listed as hirs but the sat info is for each number)
satinfo_translate_dictionary={
    "hirs_n06":"hirs2_n06", "hirs_n07":"hirs2_n07", "hirs_n08":"hirs2_n08", "hirs_n09":"hirs2_n09", "hirs_n10":"hirs2_n10",
    "hirs_n11":"hirs2_n11", "hirs_n12":"hirs2_n12", "hirs_n14":"hirs2_n14", "hirs_n15":"hirs3_n15",
    "hirs_n16":"hirs3_n16", "hirs_n17":"hirs3_n17", "hirs_metop-a":"hirs4_metop-a", 
    "hirs_metop-b":"hirs4_metop-b", "hirs_n19":"hirs4_n19", "hirs_tirosn":"hirs2_tirosn", "avhrr_n14":"avhrr2_n14",
    "avhrr_metop-a":"avhrr3_metop-a", "avhrr_metop-b":"avhrr3_metop-b", "avhrr_n15":"avhrr3_n15",
    "avhrr_n16":"avhrr3_n16", "avhrr_n17":"avhrr3_n17", "avhrr_n18":"avhrr3_n18", "avhrr_n19":"avhrr3_n19",
    "goesnd_g11":"sndrD_g11", "goesnd_g12":"sndrD_g12", "goesnd_g13":"sndrD_g13", "goesnd_g14":"sndrD_g14",
    "goesnd_g15":"sndrD_g15", "goesnd_g08":"sndr_g08", "goesnd_g10":"sndr_g10", "goesnd_g11":"sndr_g11",
    "goesnd_g12":"sndr_g12"
}