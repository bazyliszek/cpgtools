#!/usr/bin/env python
"""
#=========================================================================================
This program performs differential CpG analysis using logistic regression model based on
methylation proportions (in the form of "c,n", where "c" indicates "Number of reads with
methylated C", and "n" indicates "Number of total reads". Both c and n are  non-negative
integers and c <= n). Below example showing input data on 2 CpGs of 3 groups (A,B, and C)
with each group has 3 replicates:
 
cgID  A_1   A_2   A_3   B_1   B_2   B_3   C_1   C_2   C_3
CpG_1 129,170 166,178 7,9 1 6,16  10,10 10,15 11,15 16,22 20,36     
CpG_2 0,77  0,99  0,85  0,77  1,37  3,37  0,42  0,153 0,6

allow for covariables. 
...

#=========================================================================================
"""


import sys,os
import collections
import subprocess
import numpy as np
import re
from scipy import stats
from optparse import OptionParser
from cpgmodule import ireader
from cpgmodule.utils import *
from cpgmodule import BED
from cpgmodule import padjust

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "GPL"
__version__="0.1.0"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"

	
def main():
	usage="%prog [options]" + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--input-file",action="store",type="string",dest="input_file",help="Data file containing methylation proportions (represented by \"methyl_count,total_count\", eg. \"20,30\") with the 1st row containing sample IDs (must be unique) and the 1st column containing CpG positions or probe IDs (must be unique). This file can be a regular text file or compressed file (*.gz, *.bz2) or accessible url..")
	parser.add_option("-g","--group",action="store",type="string",dest="group_file",help="Group file define the biological groups of each samples as well as other covariables such as gender, age.  Sample IDs shoud match to the \"Data file\".")
	parser.add_option("-f","--family",action="store",type="int",dest="family_func",default=1, help="Error distribution and link function to be used in the GLM model. Can be integer 1 or 2 with 1 = \"binomial\" and 2 = \"quasibinomial\". Default=%default.")
	parser.add_option("-o","--output",action="store",type='string', dest="out_file",help="Prefix of output file.")
	(options,args)=parser.parse_args()
	
	print ()
	if not (options.input_file):
		print (__doc__)
		parser.print_help()
		sys.exit(101)

	if not (options.group_file):
		print (__doc__)
		parser.print_help()
		sys.exit(102)
				
	if not (options.out_file):
		print (__doc__)
		parser.print_help()
		sys.exit(103)	
	if not os.path.isfile(options.input_file):
		print ("Input data file \"%s\" does not exist\n" % options.input_file) 
		sys.exit(104)
	if not os.path.isfile(options.group_file):
		print ("Input group file \"%s\" does not exist\n" % options.input_file) 
		sys.exit(105)
	
	FOUT = open(options.out_file + '.pval.txt','w')
	ROUT = open(options.out_file + '.r','w')
	family = {1:'binomial',2:'quasibinomial'}
	if not options.family_func in family.keys():
		print ("Incorrect value of '-f'!") 
		sys.exit(106)
		
	printlog("Read group file \"%s\" ..." % (options.group_file))
	(samples,cv_names, cvs) = read_grp_file2(options.group_file)
	for cv_name in cv_names:
		print (cv_name)
		for sample in samples:
			print ('\t' + sample + '\t' + cvs[cv_name][sample])
	
	printlog("Processing file \"%s\" ..." % (options.input_file))
	line_num = 0
	probe_list = []
	p_list = []
	for l in ireader.reader(options.input_file):
		line_num += 1
		f = l.split()
		if line_num == 1:
			sample_IDs = f[1:]
			# check if sample ID matches
			for s in samples:
				if s not in sample_IDs:
					printlog("Cannot find sample ID \"%s\" from file \"%s\"" % (s, options.input_file))
					sys.exit(3)
			continue
		else:
			methyl_reads = []			# c
			total_reads = []	# n
			cg_id = f[0]
			for i in f[1:]:
				#try:
				m = re.match(r'(\d+)\s*\,\s*(\d+)', i)
				if m is None:
					methyl_reads.append("NaN")
					total_reads.append("NaN")
					continue
				else:
					c = int(m.group(1))
					n = int(m.group(2))
					if n >= c and n > 0:
						methyl_reads.append(c)
						total_reads.append(n)
					else:
						printlog("Incorrect data format!")
						print (f)
						sys.exit(1)						
			print ('',file=ROUT)
			print ('cgid <- \"!%s\"' % cg_id, file=ROUT)
			print ("y <- c(%s)" % (','.join([str(read) for read in methyl_reads])), file=ROUT)	#response variable
			print ("total_reads <- c(%s)" % (','.join([str(read) for read in total_reads])), file=ROUT)	#For a binomial GLM prior weights are used to give the number of trials when the response is the proportion of successes
			for cv_name in cv_names:
				print (cv_name + ' <- c(%s)' % (','.join([str(cvs[cv_name][s]) for s in  sample_IDs  ])), file = ROUT)
			#print ('try(fit <- glm(y/total_reads ~ %s, weights=total_reads, family=binomial))' % ('+'.join(cv_names)), file = ROUT)
			print ('try(fit <- glm(cbind(y,total_reads-y) ~ %s, family=%s))' % ('+'.join(cv_names), family[options.family_func]), file = ROUT)
			print ('pval <- coef(summary(fit))[,4]',file=ROUT)
			print ('coef <- coef(summary(fit))[,1]',file=ROUT)
			print ('cat(cgid, names(pval),pval,coef, sep="\\t")', file=ROUT)
			print ('cat("\\n")', file=ROUT)
	ROUT.close()
	
	
	try:
		printlog("Runing Rscript file \"%s\" ..." % (options.out_file + '.r'))
		subprocess.call("Rscript %s >%s 2>%s" % (options.out_file + '.r', options.out_file + '.r.results.txt',options.out_file + '.r.warnings.txt' ), shell=True)
	except:
		print ("Error: cannot run Rscript: \"%s\"" % (options.out_file + '.r'), file=sys.stderr)
		sys.exit(1)
	
	
	printlog("Reading file \"%s\" ..." % (options.out_file + '.r.results.txt'))
	glm_results = {}
	for l in open(options.out_file + '.r.results.txt'):
		l = l.strip()
		if not l.startswith('!'):continue
		l = l.replace(')','')
		l = l.replace('(','')
		f = l.split('\t')
		cgID = f[0].replace('!','')
		tmp = f[1:]
		
		if len(tmp)%3 == 0:
			chunk_size = int(len(tmp)/3)
			sub_lists = [tmp[i:i+chunk_size] for i in range(0,len(tmp),chunk_size)]
			v_names = sub_lists[0][1:]
			v_pvals = sub_lists[1][1:]
			v_coefs = sub_lists[2][1:]
			glm_results[cgID] = [v_coefs, v_pvals]
		else:
			glm_results[cgID] = [["NaN"]* len(cv_names), ["NaN"]* len(cv_names)]
	
	printlog("Results saved to \"%s\" ..." % (options.out_file + '.pval.txt'))
	line_num = 0
	for l in ireader.reader(options.input_file):
		line_num += 1
		f = l.split()
		if line_num == 1:
			print (l + '\t' + '\t'.join([i + '.coef' for i in v_names]) + '\t' + '\t'.join([i + '.pval' for i in v_names]), file=FOUT)
		else:
			cgID = f[0]
			print (l + '\t' + '\t'.join(glm_results[cgID][0]) + '\t' + '\t'.join(glm_results[cgID][1]), file=FOUT)
	
	FOUT.close()

if __name__=='__main__':
	main()
