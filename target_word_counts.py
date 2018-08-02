
import os,time,glob
import numpy as np
from PyPDF2 import PdfFileReader


targets = ['asset',
           'bankruptcy',
           'bank',
           'bank account',
           'bankrupt',
           'bankruptcy',
           'beneficiary',
           'bond',
           'budget',
           'capital',
           'capital gain',
           'capital loss',
           'cash',
           'cash flow',
           'checking account',
           'chequing account',
           'collateral',
           'compound interest',
           'cost',
           'cost of living',
           'credit',
           'credit card',
           'credit rating',
           'credit risk',
           'credit score',
           'debit',
           'debit card',
           'debt',
           'deficit',
           'down payment',
           'economy',
           'economic',
           'economies of scale',
           'emergency fund',
           'employment',
           'face value',
           'fair market value',
           'finance',
           'financial aid',
           'financial need',
           'financial plan',
           'foreclosure',
           'grant',
           'gross domestic product',
           'identity theft',
           'inflation',
           'insufficient funds',
           'interest',
           'insurance',
           'lease',
           'liability',
           'line of credit',
           'loan',
           'money',
           'mortgage',
           'mutual fund',
           'national deficit',
           'net income',
           'net worth',
           'PIN',
           'portfolio',
           'price-to-earnings ration',
           'principal',
           'profit',
           'rate of return',
           'risk',
           'RRSP',
           'Registered retirement savings plan',
           'retirement',
           'savings account',
           'scholarship',
           'social assistance',
           'stock',
           'stock market',
           'tax',
           'taxes',
           'tax free savings account',
           'tax-free savings account',
           'TFSA',
           'tax return',
           'welfare',
           'yield',
           'accountable',
           'accountability',
           'action research',
           'activation of prior knowledge',
           'active learning',
           'aesthetic response',
           'affective domain',
           'aptitude',
           'assessment',
           'behaviour',
           'behavior',
           'bias',
           'bibliography',
           'Bloom taxonomy',
           'brainstorming',
           'case study',
           'coach',
           'coaching',
           'cognition',
           'cognitive',
           'collaboration',
           'collaborate',
           'collaborative',
           'competency',
           'competencies',
           'competent',
           'comprehension',
           'concept mapping',
           'constructivist',
           'constructivism',
           'context',
           'creative',
           'creativity',
           'criteria',
           'critical thinking',
           'deep learning',
           'deficit thinking',
           'democracy',
           'diagnostic test',
           'disadvantage',
           'disadvantaged',
           'discriminate',
           'discriminated',
           'discrimination',
           'diversity',
           'e-learning',
           'emergent literacy',
           'English language learners',
           'essay',
           'evaluation',
           'exercise',
           'examination',
           'exam',
           'experiential learning',
           'facilitate',
           'facilitator',
           'feedback',
           'field work',
           'fluency',
           'fluent',
           'formative assessment',
           'grading',
           'group work',
           'guided reading',
           'handout',
           'independent learning',
           'independent reading',
           'information technology',
           'instruction',
           'instructional support',
           'inquiry',
           'inquiry-based',
           'internet',
           'interactive',
           'jargon',
           'journal writing',
           'learn',
           'learning',
           'learning centres',
           'learning logs',
           'lifelong learning',
           'LGBT',
           'LGBTQ',
           'media',
           'mentor',
           'meta-cognition',
           'millennial',
           'mission statement',
           'model',
           'motivate',
           'motivation',
           'module',
           'multiple choice',
           'multicultural',
           'multiculturalism',
           'native',
           'native language',
           'native people',
           'network',
           'networking',
           'object',
           'objective',
           'objectivity',
           'online',
           'open-ended',
           'oral',
           'pedagogy',
           'peer',
           'peer assessment',
           'peer learning',
           'performance',
           'performance criteria',
           'phonemes',
           'phonics',
           'plagiarism',
           'portfolio assessment',
           'positive feedback',
           'post',
           'problem-based learning',
           'process of learning',
           'qualtitative assessment',
           'quality',
           'quiz',
           'race',
           'racist',
           'racism',
           'range',
           'record of achievement',
           'references',
           'reflection',
           'reflective practice',
           'rehearsal',
           'reports',
           'research',
           'research skills',
           'resource',
           'review',
           'role play',
           'rubric',
           'remedial',
           'scaffold',
           'self assessment',
           'sight words',
           'skills',
           'software',
           'standards',
           'strategic learning',
           'strategy',
           'standards',
           'student',
           'student-centred learning',
           'study',
           'summary',
           'summative assessment',
           'taxonomy',
           'team assessment',
           'teamwork',
           'thesis',
           'time management',
           'transcript',
           'transferable skills',
           'transparency',
           'tutor',
           'valid',
           'validity',
           'values',
           'video',
           'video conference',
           'virtual',
           'vocation',
           'vocational',
           'web',
           'web browser',
           'web page',
           'website',
           'work',
           'work placement',
           'work load',
           'world wide web',                              
]


def _get_counts(lines):
	counts  = [0] * len(targets)
	for line in lines:
		for i,target in enumerate(targets):
			counts[i] += line.lower().count( target )
	return np.array(counts)
	

def get_counts_txt(fname):
	with open(fname, 'r', encoding = "ISO-8859-1") as fid:
		lines  = fid.readlines()
		counts = _get_counts(lines)
	return counts
	
def get_counts_pdf(fname, display=True):
	with open(fname, 'rb') as fid:
		pdf    = PdfFileReader( fid )
		nPages = pdf.getNumPages()
		counts = np.array( [0] * len(targets) )
		for i in range(nPages):
			if display:
				print('Processing page %d of %d...' %(i+1,nPages))
			page  = pdf.getPage(i)
			lines = page.extractText().split('\n')
			c     = _get_counts(lines)
			counts += c
	return counts

def get_counts(fname, display=True):
	ext  = os.path.splitext(fname)[-1]
	if ext == '.pdf':
		counts = get_counts_pdf(fname, display=display)
	elif ext == '.txt':
		counts = get_counts_txt(fname)
	return counts

def write_csv(fnameCSV, fnames, counts):
	with open(fnameCSV, 'w') as fid:
		fmt0    = '%s' + ',%s'*len(targets) + '\n'
		fid.write(fmt0 %tuple( ['FileName'] + list(targets)) )
		fmt     = '%s' + ',%d'*len(targets) + '\n'
		for fname,c in zip(fnames,counts):
			f   = os.path.split(fname)[-1]
			fid.write(fmt %tuple( [f] + list(c)) )
		
	


# #(0) Process a single TXT file:
# dir0   = os.path.dirname( __file__ )
# dir0   = os.path.join(dir0, 'Ontario Curriculum Documents')
# fname  = os.path.join(dir0, '2009science11_12.txt')
# counts = get_counts_txt(fname)



# #(1) Process a single PDF file:
# dir0   = os.path.dirname( __file__ )
# dir0   = os.path.join(dir0, 'Ontario Curriculum Documents')
# fname  = os.path.join(dir0, 'FinLitGr4to8.pdf')
# counts = get_counts_pdf(fname)


# #(2) Process multiple files:
# dir0   = os.path.dirname( __file__ )
# dir0   = os.path.join(dir0, 'Ontario Curriculum Documents')
# fname0 = os.path.join(dir0, '2009science11_12.txt')
# fname1 = os.path.join(dir0, '2009teched1112curr.txt')
# fname1 = os.path.join(dir0, 'FinLitGr4to8.pdf')
# fnames = [fname0, fname1]
# counts = []
# for fname in fnames:
# 	counts.append( get_counts(fname) )
# counts = np.array( counts )
# ### write:
# fnameCSV = '/Users/todd/Desktop/counts.csv'
# write_csv(fnameCSV, fnames, counts)



#(3) Process all files in a directory:
dir0   = os.path.dirname( __file__ )
dir0   = os.path.join(dir0, 'Ontario Curriculum Documents')
fnames = glob.glob( os.path.join(dir0, '*')  )
counts = []
t0     = time.time()
for i,fname in enumerate(fnames):
	print('Processing file %d of %d (%s)...' %(i+1,len(fnames),os.path.split(fname)[-1]))
	counts.append( get_counts(fname, display=False) )
print('\nTotal elapsed time: %.1f s\n\n' %(time.time() - t0))
### write:
fnameCSV = os.path.join( dir0, 'word_counts.csv' )
fnameCSV = os.path.join( os.path.dirname( __file__ ) , 'word_counts.csv' )


write_csv(fnameCSV, fnames, counts)






