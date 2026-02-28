patterns = [
    {
        "label": "LOCATION",
        "pattern": [                        #$ddd,ddd [—–-] $ddd,ddd
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"TEXT": {"REGEX": r"[—–-]"}},
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True}
        ]
    },
    {
        "label": "LOCATION",
        "pattern": [                        #$ddd,ddd and $ddd,ddd
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True},
            {"ORTH": "and"},
            {"IS_CURRENCY": True},
            {"LIKE_NUM": True}
        ]
    },
    {
        "label": "LOCATION",
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
        "label": "LOCATION",
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
    {
        "label": "EXPERIENCE",
        "pattern": [                       
            
            {"TEXT": {"REGEX": r"\d{1,2}"}},                     #d(+) year(s)
            {"ORTH": "+", "OP": "?"},
            {"TEXT": {"REGEX": r"years?"}}
        ]
    },
    {
        "label": "EXPERIENCE",
        "pattern": [                       
            
            {"TEXT": {"REGEX": r"\d{1,2}"}},                     #d-d or d - d
            {"TEXT": {"REGEX": r"[—–-]"}},
            {"TEXT": {"REGEX": r"\d{1,2}"}}
        ]
    }
        
]