import spacy
# from spacy import displacy
import sqlite3
import pandas as pd
import re
#need to find locations, salary range (min max salary), experience range (min max experience)
qSelectJobDescs = '''
    select id, job_url, job_desc
    from Job
    where id > 1000
    '''

# with sqlite3.connect('./db/jobert.db') as conn:
#     dbJobDescs = pd.read_sql_query(qSelectJobDescs, conn)

# jobUrl = dbJobDescs['job_url'][0]
# jobDesc = dbJobDescs['job_desc'][0][2200:2400]
jobDesc = """
Who we are\nAbout Stripe\n\nStripe is a financial infrastructure platform for businesses. Millions of companies—from the world’s largest enterprises to the most ambitious startups—use Stripe to accept payments, grow their revenue, and accelerate new business opportunities. Our mission is to increase the GDP of the internet, and we have a staggering amount of work ahead. That means you have an unprecedented opportunity to put the global economy within everyone’s reach while doing the most important work of your career.\n\nAbout the team\n\nThe Data Platform delivers data infrastructure and tools that power Stripe products and enable internal employees to make informed decisions and build data-centric products. We keep security, performance, and reliability as top priorities, so we can create clean interfaces on our platform to enable Stripe engineers to focus on building great products for our users. We operate at large scale on servers across the world and on hundreds of petabytes of data. The Data Platform includes a wide range of well-known open source technologies, including Spark, Hadoop, Airflow, Presto/Trino, Iceberg, Kafka, Pinot, Flink, and Elasticsearch, as well as a number of vendor-provided and internally-developed technologies.\n\nWhat you’ll do\n\nAs a Technical Leader, you’ll be responsible for driving forward progress across multiple organizations for Stripe’s most critical initiatives. Your work will have a direct correlation between Stripe\'s (and our user\'s) bottom line.\n\nResponsibilities\nDefine and own the technical roadmaps for large cross-cutting efforts that span the Data Platform, with Stripe-wide impact\n\nOwn 
and drive cross functional partnerships with organizations spanning Infrastructure, Data Engineering, Data Science, ML Engineering, Product Engineering, Finance, Risk, Operations, and GTM teams, and partner closely with the leadership/stakeholders of various teams within those organizations\xa0\n\nEstablish project owners and contribute to prioritization and execution with the appropriate amount of urgency\n\nPresent clear, thoughtful, and opinionated analysis to 
senior leaders, enabling them to make tough and thoughtful decisions with clear tradeoffs\n\nHave excellent judgment and operate with minimal oversight\n\nMake impactful, hands-on contributions throughout the project lifecycle, from scoping to design, coding, and operations\n\nMentor and sponsor experienced managers and/or very experienced engineers, assist with team growth and development, and set the culture bar for excellence and technical curiosity\n\nWho you 
are\n\nWe’re looking for someone who meets the minimum requirements to be considered for the role. If you meet these requirements, you are encouraged to apply. The preferred qualifications are a bonus, not a requirement.\n\nMinimum requirements\nMinimum of 15+ years of engineering experience OR equivalent combined work experience reflecting domain expertise as relevant to this position\xa0\n\nDemonstrated experience of leading company-wide initiatives spanning hundreds of engineers across multiple teams and organizations while leveraging deep domain expertise to influence technical roadmaps, planning,and execution\n\nDemonstrated ability to effectively collaborate across multiple teams and stakeholders to drive business outcomes\xa0\n\nDemonstrated ability to balance execution and velocity with security, reliability, and efficiency\n\nExperience, mentoring, and investing in the development engineers and peers\xa0\n\nDemonstrated adaptability and resilience in the face of novel technical and organizational challenges\n\nPreferred qualifications\nExpertise with tackling complex, distributed systems/infrastructure challenges at scale\n\nRelevant domain experience with Data Platforms, Machine Learning, and AI\xa0\n\nPractical experience architecting and operating modern Data and AI/ML infrastructure\xa0\n\nUser-centric orientation and track record for productizing complex infrastructure\n\nEnjoy staying close to the code and technical details\n\nHybrid work at Stripe\n\nThis role is available either in an office or a remote location (typically, 35+ miles or 56+ km from a Stripe office).\n\nOffice-assigned Stripes spend at least 50% of the time in a given month in their local office or with users. This hits a balance between bringing people together for in-person collaboration and learning from each other, while supporting flexibility about how 
to do this in a way that makes sense for individuals and their teams.\n\nA remote location, in most cases, is defined as being 35 miles (56 kilometers) or more from one of our offices. While you would be welcome to come into the office for team/business meetings, on-sites, meet-ups, and events, our expectation 
is you would regularly work from home rather than a Stripe office. Stripe does not cover the cost of relocating to a remote location. We encourage you to apply for roles that match the location where you currently or plan to live.\n\nPay and benefits\n\nThe annual US base salary range for this role is $242,700 - 
$364,000. For sales roles, the range provided is the role’s On Target Earnings ("OTE") range, meaning that the range includes both the sales commissions/sales bonuses target and annual base salary for the role. This salary range may be inclusive of several career levels at Stripe and will be narrowed during the interview process based on a number of factors, including the candidate’s experience, qualifications, and location. Applicants interested in this role and who are not located in the US may request the annual salary range for their location during the interview process.\n\nAdditional benefits for this role may include: equity, company bonus or sales commissions/bonuses; 401(k) plan; medical, dental, and vision benefits; and wellness stipends.
"""
jobDesc += ' \n\n\n Chicago, Toronto, New York, South San Francisco HQ, or Seattle'
jobDesc += ' \n\n\n Remote in Canada, or United States'

TRAINING_DATA = [
    (jobDesc, 
    {'entities': [
        (5009, 5029, 'SALARY'), 
        (2825, 2828, 'EXPERIENCE'), 
        (5783, 5790, 'LOCATION'),
        (5792, 5799, 'LOCATION'),
        (5801, 5809, 'LOCATION'),
        (5817, 5830, 'LOCATION'),
        (5838, 5845, 'LOCATION'),
        (5850, 5866, 'LOCATION'),
        (5871, 5884, 'LOCATION')
    ]})
]
print(len(repr(jobDesc)))
for jobListing in TRAINING_DATA:
    jobDescription, dict = jobListing
    for start, stop, label in dict['entities']:
        entity = re.sub(r"[\n\t\r]", "", jobDescription[start:stop])
        print(repr(entity))

nlp = spacy.load('en_core_web_md')
doc = nlp(jobDesc)
# print(nlp.pipe_names)
# print(nlp.pipeline)
# displacy.serve(doc, style="dep", host="127.0.0.1", port=8000)

# print(jobUrl)
# print(doc)

# for token in doc:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)

# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)