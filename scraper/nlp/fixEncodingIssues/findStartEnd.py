from pathlib import Path
import json


newFile = Path("./scraper/nlp/companyNER/uberNER_new.json")

try:
    newData = json.loads(newFile.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"Failed to parse {newFile}: {e}")
    newData = []

strings = {
        0: [
            'USD$187,000 per year - USD$205,000 per year',
'5+ years',
'Dallas, Texas',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Chicago, Illinois',
'Washington, District of Columbia',
        ],
        1: [
            'USD$171,000 per year - USD$190,000 per year',
'3+ years',
'Seattle, Washington',
'San Francisco, California',
        ],
        2: [
            'USD$232,000 per year - USD$258,000 per year',
'8+ years',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        3: [
            'USD$114,000 per year - USD$127,000',
'5+ years',
'Dallas, Texas',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Miami, Florida',
'Chicago, Illinois',
'Sunnyvale, California',
'Washington, District of Columbia',
        ],
        4: [
            'USD$171,000 per year - USD$190,000 per year',
'2+ year',
'New York, New York',
'San Francisco, California',
'Sunnyvale, California',
        ],
        5: [
            'USD$202,000 per year - USD$224,000 per year',
'6+ year',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        6: [
            'USD$171,000 per year - USD$190,000 per year',
'4+ years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        7: [
            'USD$171,000 per year - USD$190,000',
'1 year',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        8: [
            'USD$202,000 per year - USD$224,000 per year',
'5+ years',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        9: [
            'USD$202,000 per year - USD$224,000 per year',
'4+ years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        10: [
            'USD$202,000 per year - USD$224,000 per year',
'4+ years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        11: [
            'USD$202,000 per year - USD$224,000 per year',
'4+ years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        12: [
            'USD$202,000 per year - USD$224,000 per year',
'3 years',
'New York, New York',
'San Francisco, California',
'Sunnyvale, California',
        ],
        13: [
            'USD$171,000 per year - USD$190,000',
'1 year',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        14: [
            'USD$171,000 per year - USD$190,000 per year',
'4+ years',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        15: [
            'USD$134,000 per year - USD$148,500 per year',
'5+ years',
'Atlanta, Georgia',
'Dallas, Texas',
'New York, New York',
'Houston, Texas',
'Miami, Florida',
'Washington, District of Columbia',
        ],
        16: [
            'USD$83,500 per year - USD$92,750',
'3+ years',
'Dallas, Texas',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Miami, Florida',
'Chicago, Illinois',
'Sunnyvale, California',
'Washington, District of Columbia',
        ],
        17: [
            'USD$171,000 per year - USD$190,000 per year',
'3+ years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        18: [
            'USD$171,000 per year - USD$190,000 per year',
'4-years',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        19: [
            'USD$171,000 per year - USD$190,000 per year',
'3+ years',
'San Francisco, California',
'Sunnyvale, California',
        ],
        20: [
            'USD$202,000 per year - USD$224,000',
'3 years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        21: [
            'USD$202,000 per year - USD$224,000',
'3 years',
'New York, New York',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        22: [
            'USD$202,000 per year - USD$224,000 per year',
'New York, New York',
'San Francisco, California',
'Sunnyvale, California',
        ],
        23: [
'USD$202,000 per year - USD$224,000 per year',
'6+ years',
'Seattle, Washington',
'San Francisco, California',
'Sunnyvale, California',
        ],
        24: [
            'USD$150,000 per year - USD$167,000 per year',
'5+ years',
'Dallas, Texas',
'New York, New York',
'Austin, Texas',
'Orlando, Florida',
'Houston, Texas',
'San Francisco, California',
'Miami, Florida',
'Washington, District of Columbia',
        ],
        25: [
            
        ]
}
for i, dic in enumerate(newData):
    print(i)
    jobDesc = dic['jobDesc']
    locations = dic['locations']
    for j, (start, end, entityType) in enumerate(dic['entities']):
        # print(i, j, start, end, entityType)
        curString = strings[i][j]
        newStart = locations.find(curString) if entityType == 'LOCATION' else jobDesc.find(curString)
        newEnd = newStart + len(curString)
        # if newStart == -1:
        #     print(i, j, dic['jobUrl'])
        if j == len(dic['entities'])-1:
            print(f'{json.dumps([newStart, newEnd, entityType])}')
        else:
            print(f'{json.dumps([newStart, newEnd, entityType])}, ')
    print()
