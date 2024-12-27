"""
Module: patterns.py
========================
Regular Expression Patterns for Parsing Sections in Forms SC 13D and SC 13G

This module contains regex patterns designed to capture specific sections in SEC filings,
These patterns identify and extract relevant information
from the text based on predefined section headers and their associated descriptions.
"""

import re


# Define a pattern to capture "Item 1.01" to "Item 9.01" sections in Form 8-K
section_pattern_8k = re.compile(
    r"(item\s*\d\.\d{2}[\.\s]*)(entry\s+into\s+a\s+material\s+definitive\s+agreement|termination\s+of\s+a\s+material\s+definitive\s+agreement|"
    r"bankruptcy\s+or\s+receivership|"
    r"mine\s+safety\s+–\s+reporting\s+of\s+shutdowns\s+and\s+patterns\s+of\s+violations|"
    r"material\s+cybersecurity\s+incidents|"
    r"completion\s+of\s+acquisition\s+or\s+disposition\s+of\s+assets|"
    r"results\s+of\s+operations\s+and\s+financial\s+condition|"
    r"creation\s+of\s+a\s+direct\s+financial\s+obligation\s+or\s+an\s+obligation\s+under\s+an\s+off-balance\s+sheet\s+arrangement\s+of\s+a\s+registrant|"
    r"triggering\s+events\s+that\s+accelerate\s+or\s+increase\s+a\s+direct\s+financial\s+obligation\s+or\s+an\s+obligation\s+under\s+an\s+off-balance\s+sheet\s+arrangement|"
    r"costs\s+associated\s+with\s+exit\s+or\s+disposal\s+activities|"
    r"material\s+impairments|"
    r"notice\s+of\s+delisting\s+or\s+failure\s+to\s+satisfy\s+a\s+continued\s+listing\s+rule\s+or\s+standard;\s+transfer\s+of\s+listing|"
    r"unregistered\s+sales\s+of\s+equity\s+securities|"
    r"material\s+modification\s+to\s+rights\s+of\s+security\s+holders|"
    r"changes\s+in\s+\bregistrant’s\s+certifying\s+accountant|"
    r"non-reliance\s+on\s+previously\s+issued\s+financial\s+statements\s+or\s+a\s+related\s+audit\s+report\s+or\s+completed\s+interim\s+review|"
    r"changes\s+in\s+control\s+of\s+registrant|"
    r"departure\s+of\s+directors\s+or\s+certain\s+officers;\s+election\s+of\s+directors;\s+appointment\s+of\s+certain\s+officers;\s+compensatory\s+arrangements\s+of\s+certain\s+officers|"
    r"amendments\s+to\s+articles\s+of\s+incorporation\s+or\s+bylaws;\s+change\s+in\s+fiscal\s+year|"
    r"temporary\s+suspension\s+of\s+trading\s+under\s+registrant’s\s+employee\s+benefit\s+plans|"
    r"amendments\s+to\s+the\s+registrant’s\s+code\s+of\s+ethics,\s+or\s+waiver\s+of\s+a\s+provision\s+of\s+the\s+code\s+of\s+ethics|"
    r"change\s+in\s+shell\s+company\s+status|"
    r"submission\s+of\s+matters\s+to\s+a\s+vote\s+of\s+security\s+holders|"
    r"shareholder\s+director\s+nominations|"
    r"ABS\s+informational\s+and\s+computational\s+material|"
    r"change\s+of\s+servicer\s+or\s+trustee|"
    r"change\s+in\s+credit\s+enhancement\s+or\s+other\s+external\s+support|"
    r"failure\s+to\s+make\s+a\s+required\s+distribution|"
    r"securities\s+act\s+updating\s+disclosure|"
    r"static\s+pool|"
    r"regulation\s+FD\s+disclosure|"
    r"other\s+events|"
    r"financial\s+statements\s+and\s+exhibits)",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


# Define a pattern to capture "Item 1" to "Item 16" sections in Form 10-K
section_pattern_10k = re.compile(
    r"(item\s*(1|1a|1b|1c|2|3|4|5|6|7|7a|8|9|9a|9b|9c|10|11|12|13|14|15|16)[\.\s]*)"
    r"(business|risk\s+factors|"
    r"unresolved\s+staff\s+comments|"
    r"cybersecurity|"
    r"(?:properties|description\s+of\s+property)|"
    r"legal\s+proceedings|"
    r"mine\s+safety\s+disclosu(?:re|res)|"
    r"market\s+(?:for\s+the|for)\s+registrant’s\b\s+common\s+equity,\s+related\s+(?:stockholder|shareholder)\s+matters\s+and\s+issuer\s+purchases\s+of\s+equity\s+securities|"
    r"(?:\[reserved\]|reserved|selected\s+financial\s+data)|"
    r"management’s\b\s+discussion\s+and\s+analysis\s+of\s+financial\s+condition\s+and\s+results\s+of\s+operations|"
    r"quantitative\s+and\s+qualitative\s+disclosures\s+about\s+market\s+risk|"
    r"(?:consolidated\s+financial|financial)\s+statements\s+and\s+supplementary\s+data|"
    r"changes\s+in\s+and\s+disagreements\s+with\s+accountants\s+on\s+accounting\s+and\s+financial\s+disclosure.|"
    r"controls\s+and\s+procedures|"
    r"other\s+information|"
    r"disclosure\s+regarding\s+foreign\s+jurisdictions\s+that\s+prevent\s+inspections|"
    r"directors(?:,|;)\s+executive\s+officers\s+and\s+corporate\s+governance|"
    r"executive\s+compensation|"
    r"security\s+ownership\s+of\s+certain\s+beneficial\s+owners\s+and\s+management\s+and\s+related\s+stockholder\s+matters|"
    r"certain\s+relationships\s+and\s+related\s+transactions,\s+and\s+director\s+independence|certain\s+relationships\s+and\s+related\s+transactions|"
    r"principal\s+(?:accountant|accounting)\s+fees\s+and\s+services|"
    r"exhibits,\s+financial\s+statement\s+schedules|exhibits\s+and\s+financial\s+statement\s+schedules|"
    r"form\s+10-K\s+summary)",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


# Define a pattern to capture "Item 1" to "Item 7" sections in FORM SC 13D
section_pattern_13d = re.compile(
    r"(item\s*(1|2|3|4|5|6|7)[\.\s]*)(security\s+and\s+issuer|identity\s+and\s+background|"
    r"source\s+and\s+amount\s+of\s+funds\s+or\s+other\s+consideration|"
    r"purpose\s+of\s+transaction|purpose\s+of\s+the\s+transaction|"
    r"interest\s+in\s+securities\s+of\s+the\s+issuer|"
    r"contracts,\s+(?:arrangements|agreements),\s+understandings\s+or\s+relationships\s+with\s+respect\s+to\s+securities\s+of\s+the\s+issuer|"
    r"materi(?:al|als)\s+to\s+be\s+filed\s+as\s+exhibits)",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


# Define a pattern to capture "Item 1" to "Item 3" sections in Form SC 13G
section_pattern_13g_1 = re.compile(
    r"\b[Ii][Tt][Ee][Mm]\s*((1|2|3)(?:\([a-zA-Z]\)|[a-zA-Z])?)[\.\)]?\s*"
    r"(.*?)(?=\b[Ii][Tt][Ee][Mm]\s*(1|2|3)(?:\([a-zA-Z]\)|[a-zA-Z])?[\.\)]?|\Z)",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


# Define a pattern to capture "Item 4" to "Item 10" sections in a flexible way
section_pattern_13g_2 = re.compile(
    r"(item\s*(4|5|6|7|8|9|10)[\.\s]*)("
    r"ownership(?:\s+of\s+(?:(?:5|five)\s+percent\s+or\s+less\s+of\s+a\s+class|more\s+than\s+(?:5|five)\s+percent\s+on\s+behalf\s+of\s+another\s+person))?|"
    r"identification\s+and\s+classification\s+of\s+the\s+subsidiary\s+(?:that|which)\s+acquired\s+the\s+security\s+being\s+reported\s+on\s+by\s+the\s+parent\s+holding\s+(?:company\s+or\s+control\s+person|company)|"
    r"identification\s+and\s+classification\s+of\s+(?:member|members\s+of\s+the)\s+group|"
    r"notice\s+of\s+dissolution\s+of\s+(?:the\s+group|group)|"
    r"certificat(?:ion|ions))",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


# Define a pattern to capture the numbers "1" to "14" of the table in SC 13D & SC 13G
doc_num_pattern = re.compile(
    r"((1|2|3|4|5|6|7|8|9|10|11|12|13|14)[\.\s]*)(nam(?:e|es)\s+of\s+reporting\s+persons|check\s+the\s+appropriate\s+box\s+if\s+a\s+member\s+of\s+a\s+group|"
    r"sec\s+use\s+only|"
    r"source\s+of\s+funds|"
    r"check\s+bos\s+if\s+disclosure\s+of\s+legal\s+proceedings\s+is\s+required\s+pursuant\s+to\s+item\s+2\(d\)\s+or\s+2\(e\)|"
    r"citizenship\s+or\s+place\s+of\s+organization|"
    r"sole\s+voting\s+power|"
    r"sole\s+dispositive\s+power|"
    r"shared\s+dispositive\s+power|"
    r"aggregate\s+amount\s+beneficially\s+owned\s+by\s+each\s+reporting\s+person|"
    r"check\s+bos\s+if\s+the\s+aggregate\s+amount\s+in\s+row\s+\(11\)\s+excludes\s+certain\s+shares|"
    r"percent\s+of\s+class\s+represented\s+by\s+amount\s+in\s+row\s+\(11\)|"
    r"type\s+of\s+reporting\s+person)",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)
