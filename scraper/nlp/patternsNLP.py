salaryPatterns = [
    #SPOTIFY SUCKS
    #If salary range has 0 $ signs, patterns can grab stuff like 200630263-0836, NOT GOOD
    {
        "label": "SALARY",                  #$ddd,ddd [—–-] $?ddd,ddd
        "pattern": [                        #$ddd,ddd [—–-]$?ddd,ddd  SPOTIFY SUCKS
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"TEXT": {"REGEX": r"[—–-]"}},
            {"IS_CURRENCY": True, "OP": "?"},
            {"LIKE_NUM": True}
        ]
    },
    {
        "label": "SALARY",
        "pattern": [                        #$ddd,ddd and $ddd,ddd
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"ORTH": "and"},
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True}
        ]
    },
    {
        "label": "SALARY",
        "pattern": [                        #USD$ddd,ddd per year [—–-] USD$ddd,ddd per year
            {"TEXT": {"REGEX": r"USD\$\d{2,3},\d{3}"}},
            {"ORTH": "per"},
            {"ORTH": "year"},
            {"TEXT": {"REGEX": r"[—–-]"}},
            {"TEXT": {"REGEX": r"USD\$\d{2,3},\d{3}"}},
            {"ORTH": "per"},
            {"ORTH": "year"}
        ]
    },
    {
        "label": "SALARY",
        "pattern": [                        #$dddK [—–-] $dddK
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"TEXT": {"REGEX": r"[kK]"}},
            {"TEXT": {"REGEX": r"[—–-]"}},
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"TEXT": {"REGEX": r"[kK]"}}
        ]
    },
    { ###SPOITFY_SUCKS
        "label": "SALARY",                 #$ddd,ddd[—–-]$?ddd,ddd
        "pattern": [
            {"IS_CURRENCY": True},
            {"TEXT": {"REGEX": r"\$?\d{2,3},\d{3}[—–-]\$?\d{2,3},\d{3}"}},
        ]
    },
    { ###SPOTIFY SUCKS
        "label": "SALARY",                 #$ddd,ddd[—–-] $?ddd,ddd
        "pattern": [
            {"IS_CURRENCY": True},
            {"TEXT": {"REGEX": r"\$?\d{2,3},\d{3}[—–-]"}},
            {"IS_CURRENCY": True, "OP": "?"},
            {"LIKE_NUM": True}
        ]
    } 
]

experiencePatterns = [

    {
        "label": "EXPERIENCE",
        "pattern": [                       
            
            {"TEXT": {"REGEX": r"^\d{1,2}$"}},                     #d(+) year(s)
            {"ORTH": "+", "OP": "?"},
            {"TEXT": {"REGEX": r"years?"}}
        ]
    },
    {
        "label": "EXPERIENCE",
        "pattern": [                       
            
            {"TEXT": {"REGEX": r"^\d{1,2}$"}},                     #d-d or d - d
            {"TEXT": {"REGEX": r"^[—–-]$"}},
            {"TEXT": {"REGEX": r"^\d{1,2}$"}},
            {"TEXT": {"REGEX": r"years?"}}
        ]
    }
]