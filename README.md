## CpGtools -- Tools to analyze and visualize DNA methylation data


- [Installation](#p1)
	- [Prerequisites](#p1.1)
	- [Python Dependencies](#p1.2)
	- [Install pip3](#p1.3)
	- [Install CpGtools](#p1.4)
- [BED file format](#p2)
- [Usage information](#p3)
	- [annotate_CpG.py](#p3.1)
	- [beta_profile.py](#p3.2)
	- [chrom_distribution.py](#p3.3)
	- [dmc_glm.py](#p3.4)
	- [dmc_nonparametric.py](#p3.5)
	- [dmc_ttest.py](#p3.6)
	- [genomic_distribution_1.py](#p3.7)
	- [genomic_distribution_2.py](#p3.8)
	- [methyl_logo.py](#p3.9)
	- [region_profile.py](#p3.10)
	- [region_stat.py](#p3.11)
	- [trichotmize.py](#p3.12)



## <a name="p1"></a>Part 1: Installation


### <a name="p1.1"></a>Part 1.1: Prerequisites
CpGtools are written in [Python](https://www.python.org/). In particular,  **Python3 (v3.5.x)**
is required to run all scripts in CpGtools. Some scripts also need **R** to generate graphs and 
run generalized linear model (GLM).  

- [Python 3](https://www.python.org/downloads/) and [pip3](https://pip.pypa.io/en/stable/installing/)
- [R](https://www.r-project.org/)


### <a name="p1.2"></a>Part 1.2: Python Dependencies
Note: these packages will be automatically installed when you use [pip3](https://pip.pypa.io/en/stable/installing/)
to install CpGtools.

- [numpy](http://www.numpy.org/)
- [scipy](https://www.scipy.org/)
- [pysam](https://pypi.org/project/pysam/)
- [bx-python](https://pypi.org/project/bx-python/)
- [pyBigWig](https://pypi.org/project/pyBigWig/)
- [sklearn](https://www.scilearn.com/)
- [weblogo](https://pypi.org/project/weblogo/)


### <a name="p1.3"></a>Part 1.3: Install [pip3](https://pip.pypa.io/en/stable/installing/) (Skip this step if you already have [pip3](https://pip.pypa.io/en/stable/installing/))

1. First, download **[get-pip.py](https://bootstrap.pypa.io/get-pip.py)**
		
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

2. Then run the following:
		
		python get-pip.py

3. Run the following code to check:
		pip3 --version
		pip 18.1 from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pip (python 3.6)
		
		which pip3
		/Library/Frameworks/Python.framework/Versions/3.6/bin/pip
		
		which pip	
		/Library/Frameworks/Python.framework/Versions/3.6/bin/pip
Note that **pip** is actualy a soft link to the same executable file path with **pip3**. so you can use pip directly. 


### <a name="p1.4"></a>Part 1.4: Install CpGtools

You can run the following command to install CpGtools and all its dependencies. 
	
	pip install cpgtools (not ready)		

You can run the following command to **upgrade** CpGtools and all its dependencies. 	
	
	pip install cpgtools --upgrade (not ready)


## <a name="p2"></a>Part 2: BED (Browser Extensible Data) format conventions

BED file is 0-based	 (i.e. the first base of chromosome is index as '0'For example, the first 100 bases of a chromosome are defined as chromStart=0, chromEnd=100, and span the bases numbered 0-99.

- **BED12** file (also called the standarded BED file) which has 12 fields. It is used to describe gene models. Details are described [here](https://genome.ucsc.edu/FAQ/FAQformat.html#format1). 
- **BED3** file only has the first 3 required columns (chrom, chromStart, chromEnd). It is commonly used to represent genomic regions when "score" and "strand" are not important. 
- **BED3+** file has at least 3 columns (chrom, chromStart, chromEnd). It could have additional columns, but these additional columns will be ignored.
- **BED6** file has the first 6 columns (chrom, chromStart, chromEnd, name, score, stand). It can be used to represent genomic regions and their associated scores, or in cases where "stand" information is important.  
- **BED6+** file has at least 6 columns (chrom, chromStart, chromEnd, name, score, stand). It could have additional columns, but these additional columns will be ignored.

Note:
1. The coordinates in a BED record are both 0-based, meaning the first base on a chromosome is numbered 0.
2. A BED interval is left-open, right-closed. So, "chr1 10 15" contains the 11-th, 12-th, 13-th, 14-th and 15-th bases of chromosome-1. 


## <a name="p3"></a>Part 3: Usage Information

<a name="p3.1"></a>annotate_CpG.py
---
This program annotate CpGs by assigning them to gene's regulatory domains. Follows the
"[Basel plus extension rules](http://great.stanford.edu/public/html/index.php)" used by [GREAT](http://great.stanford.edu/public/html/):

**Basal regulatory domain**:
A gene's basal regulatory domain is a window around its TSS (transcription start site). In 
particular, basal regulatory domain is obtained by extending '-u' basepairs (default = 5 kb)
to the upstream and '-d' basepairs (default = 1 kb) to the downstream of TSS regardless of
other nearby genes.

**Extended regulatory domain**:
The gene's basal regulatory domain is further extended in both directions to the nearest gene's
basal regulatory domain but no more than the maximum extension (specified by '-e', default =
1000 kb) in one direction.	

![basal & extended regulatory domain](https://github.com/liguowang/cpgtools/blob/master/img/gene_domain.png)

#### Basic usage

```text

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED file specifying the C position. Must have at least
                        3 columns (chrom start end). Note: the first base in a
                        chromosome is numbered 0. BED file can be regular or
                        compressed by 'gzip' or 'bz'. [required]
  -r GENE_FILE, --refgene=GENE_FILE
                        Reference gene model in standard BED-12 format
                        (https://genome.ucsc.edu/FAQ/FAQformat.html#format1).
  -u BASAL_UP_SIZE, --basal-up=BASAL_UP_SIZE
                        Size of extension to upstream of TSS (used to define
                        gene's "basal regulatory domain"). default=5000 (bp)
  -d BASAL_DOWN_SIZE, --basal-down=BASAL_DOWN_SIZE
                        Size of extension to downstream of TSS (used to define
                        gene's basal regulatory domain). default=1000 (bp)
  -e EXTENSION_SIZE, --extension=EXTENSION_SIZE
                        Size of extension to both up- and down-stream of TSS
                        (used to define gene's "extended regulatory domain").
                        default=1000000 (bp)
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file. Two addtional columns will be
                        appended to the orignal BED file with the last column
                        indicating "genes whose extended regulatory domain are
                        overlapped with the CpG", the 2nd last column
                        indicating "genes whose basal regulatory domain are
                        overlapped with the CpG". [required]
```	                        

#### Input files
- BED3+ file specifying the C position. Download test file [test_01.bed6](https://github.com/liguowang/cpgtools/blob/master/test/test_01.bed6)
- Reference gene model in BED12 format. Download test file [hg19.RefSeq.union.bed](https://github.com/liguowang/cpgtools/blob/master/test/hg19.RefSeq.union.bed)

#### Output file
Two addtional columns will be appended to the orignal BED file (-i):
- the last column indicating genes whose **extended regulatory domain** are overlapped with the CpG
-  the 2nd last column indicating genes whose **basal regulatory domain** are overlapped with the CpG

#### Example

```

$ python3 ../bin/annotate_CpG.py -r hg19.RefSeq.union.bed -i test_01.bed6 -o OUT1

@ 2018-12-07 12:49:21: Calculate basal regulatory domain from: "hg19.RefSeq.union.bed" ...
@ 2018-12-07 12:49:21: Calculate extended regulatory domain from: "hg19.RefSeq.union.bed" ...
@ 2018-12-07 12:49:22: Assigning CpG to gene ...

$ head OUT1.annotatio.txt

#Chrom	Start	End	Name	Beta	Strand
chr1	10847	10848	cg26928153	0.8965	+	DDX11L1	//
chr1	10849	10850	cg16269199	0.7915	+	DDX11L1	//
chr1	15864	15865	cg13869341	0.9325	+	//	MIR6859-1;MIR6859-2
chr1	534241	534242	cg24669183	0.7941	+	//	OR4F29;OR4F3;LOC101928626;OR4F16
chr1	564500	564501	cg26679879	0.3746	+	LOC101928626	//
chr1	564503	564504	cg22519184	0.395	+	LOC101928626	//
chr1	710096	710097	cg15560884	0.8106	+	//	LOC100133331;LOC100288069
chr1	714176	714177	cg01014490	0.0275	+	LOC100288069	//
chr1	714620	714621	cg24063007	0.0368	+	LOC100288069	//

```


<a name="p3.2"></a>beta_profile.py
---	
beta_profile.py calculates the average methylation level (i.e. average beta value) across
regions including: 5'UTR exon, CDS exon, 3'UTR exon, first intron, internal intron, last
intron,  up-stream intergenic and down-stream intergenic.

#### Basic usage

```text

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED6+ file specifying the C position. This BED file
                        should have at least 6 columns (Chrom, ChromStart,
                        ChromeEnd, Name, Beta_value, Strand). BED file can be
                        regular or compressed by 'gzip' or 'bz'.
  -r GENE_FILE, --refgene=GENE_FILE
                        Reference gene model in standard BED12 format
                        (https://genome.ucsc.edu/FAQ/FAQformat.html#format1).
  -d DOWNSTREAM_SIZE, --downstream=DOWNSTREAM_SIZE
                        Size of down-stream genomic region added to gene.
                        default=2000 (bp)
  -u UPSTREAM_SIZE, --upstream=UPSTREAM_SIZE
                        Size of up-stream genomic region added to gene.
                        default=2000 (bp)
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
                        
```

#### Input files
- BED3+ file specifying the C position. Download test file [test_02.bed6.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_02.bed6.gz)
- Reference gene model in BED12 format. Download test file [hg19.RefSeq.union.bed](https://github.com/liguowang/cpgtools/blob/master/test/hg19.RefSeq.union.bed)

#### Example

```
$ python3 ../bin/beta_profile.py -r hg19.RefSeq.union.bed -i test_02.bed6.gz -o OUT2

@ 2018-12-07 13:43:00: Reading CpG file: "test_02.bed6.gz"
@ 2018-12-07 13:43:09: Reading reference gene model: "hg19.RefSeq.union.bed"
@ 2018-12-07 13:43:09: Process upstream regions ...
@ 2018-12-07 13:43:10: Process 5' UTR exons ...
@ 2018-12-07 13:43:10: Process Coding exons ...
@ 2018-12-07 13:43:11: Process first introns ...
@ 2018-12-07 13:43:12: Process internal introns ...
@ 2018-12-07 13:43:13: Process last introns ...
@ 2018-12-07 13:43:14: Process 3' UTR exons ...
@ 2018-12-07 13:43:15: Process downstream regions ...

```

#### Output
- The red curve represents average profile of beta values, aggregated from all regions in each class. 
- Upstream: intergenic region (defined by '-u' ) before TSS (transcription start site)
- Downstream: intergenic region (defined by '-d') after TES (transcription end site)
![beta_profile.png](https://github.com/liguowang/cpgtools/blob/master/img/beta_profile.png)


<a name="p3.3"></a>chrom_distribution.py
---	
This program calculates the distribution of CpG over chromosomes.

#### Basic usage

```text

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILES, --input-files=INPUT_FILES
                        Input CpG file(s) in BED3+ format. Multiple BED files
                        should be separated by "," (eg: "-i
                        file_1.bed,file_2.bed,file_3.bed"). BED file can be
                        regular or compressed by 'gzip' or 'bz'. The barplot
                        figures will NOT be generated if you provide more than
                        12 samples (bed files). [required]
  -n FILE_NAMES, --names=FILE_NAMES
                        Shorter and meaningful names to label samples. Should
                        be separated by "," and match CpG BED files in number.
                        If not provided, basenames of CpG BED files will be
                        used to label samples. [optional]
  -s CHROM_SIZE, --chrom-size=CHROM_SIZE
                        Chromosome size file. Tab or space separated text file
                        with 2 columns: first column is chromosome name/ID,
                        second column is chromosome size. This file will
                        determine: (1) which chromosomes are included in the
                        final barplots, so do NOT inlude 'unplaced',
                        'alternative' contigs in this file. (2) The order of
                        chrosomes in the final barplots.  [required]
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file. [required]

```
#### Input files

- BED3+ files: [test_03a.bed3.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_03a.bed3.gz), [test_03b.bed3.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_03b.bed3.gz)
- chromosome size file: [hg19.chrom.sizes](https://github.com/liguowang/cpgtools/blob/master/test/hg19.chrom.sizes)
#### Example

```text

$ python3 ../bin/chrom_distribution.py -i test_03a.bed3.gz,test_03b.bed3.gz -n 450K,850K -s hg19.chrom.sizes -o chromDist

```

#### Output files

1. Total CpG count per chromsome 
![chromDist.CpG_total.png](https://github.com/liguowang/cpgtools/blob/master/img/chromDist.CpG_total.png) 
2. CpG percent on each chromosome
![chromDist.CpG_percent.png](https://github.com/liguowang/cpgtools/blob/master/img/chromDist.CpG_percent.png)
3. CpG per Mb 
![chromDist.CpG_perMb.png](https://github.com/liguowang/cpgtools/blob/master/img/chromDist.CpG_perMb.png)

<a name="p3.4"></a>dmc_glm.py
---
This program performs differential CpG analysis using logistic regression model based on
methylation proportions. It allows for covariable analysis.

#### Basic usage

```text

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        Data file containing beta values (represented by
                        "methyl_count,total_count", eg. "20,30") with the 1st
                        row containing sample IDs (must be unique) and the 1st
                        column containing CpG positions or probe IDs (must be
                        unique). This file can be regular or compressed by
                        'gzip' or 'bz'.
  -g GROUP_FILE, --group=GROUP_FILE
                        Group file define the biological groups of each
                        samples as well as other covariables such as gender,
                        age.  Sample IDs shoud match to the "Data file".
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
                        
```

#### Input files
**Data file**.
Below example showing input data on 2 CpGs of 2 groups (A,B) with each group has 3 replicates.
methylation proportions is represented by two non-negative integers separated by "," (in the form of "c,n", 
where "c" indicates "Number of reads with methylated C", and "n" indicates "Number of total
reads", c <= n). Any other forms will be considered as "missing values".

|cgID  | A_1    |A_2      |A_3     |B_1     |B_2     |B_3     |
|:---- |:-------|:-------:|:------:|:------:|:------:|-------:|
|CpG_1 |129,170 |166,178  |7,9     |8,16    |11,15   |100,230 |
|CpG_2 |0,7     |2,18     |4,39    |32,37   |14,15   |20,23   |



**Group file**.
Below example specified two variables. "survival" (1=long-term survival, 2=short-term survival), and "sex" (1=Male, 2=Female)
```text
sampleID,survival,Sex
A_1,1,1
A_2,1,2
A_3,1,2
B_1,2,1
B_2,2,1
B_3,2,2
```
Download test data file: [test_04_TwoGroup.tsv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_04_TwoGroup.tsv.gz)
Download test group file: [test_04_TwoGroup.grp.csv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_04_TwoGroup.grp.csv.gz)

#### Example
```text
$ python3 ../bin/dmc_glm.py -i test_04_TwoGroup.tsv.gz -g test_04_TwoGroup.grp.csv.gz -o OUT_4
```

#### Output file
Additional columns (pvalue and coefficient) will be appended to the original data file. In the example above, 
4 additional columns were added to "test_04_TwoGroup.tsv":

- survival.pval
- Sex.pval
- survival.coef
- Sex.coef

<a name="p3.5"></a>dmc_nonparametric.py
---
This program performs differential CpG analysis based on **beta values**.
- use [Mann-Whitney U test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html) for two group comparison.
- use [Kruskal-Wallis H-test](https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_one-way_analysis_of_variance) for multiple groups comparison.

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        Data file containing beta values with the 1st row
                        containing sample IDs (must be unique) and the 1st
                        column containing CpG positions or probe IDs (must be
                        unique). Except for the 1st row and 1st column, any
                        non-numerical values will be considered as "missing
                        values" and ignored. This file can be regular or
                        compressed by 'gzip' or 'bz'.
  -g GROUP_FILE, --group=GROUP_FILE
                        Group file define the biological groups of each
                        samples. It is a comma-separated 2 columns file with
                        the 1st column containing sample IDs, and the 2nd
                        column containing group IDs. It must have a header
                        row. Sample IDs shoud match to the "Data file". Note:
                        automatically switch to use  Kruskal-Wallis H-test if
                        more than 2 groups were defined in this file.
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
```

#### Input files
- [test_05_TwoGroup.tsv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_05_TwoGroup.tsv.gz) 
- [test_05_TwoGroup.grp.csv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_05_TwoGroup.grp.csv.gz)      
- [test_06_ThreeGroup.tsv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_06_ThreeGroup.tsv.gz)    
- [test_06_ThreeGroup.grp.csv.gz](https://github.com/liguowang/cpgtools/blob/master/test/test_06_ThreeGroup.grp.csv.gz)          

#### Example
```text
$ python3 ../bin/dmc_nonparametric.py -i test_05_TwoGroup.tsv.gz -g test_05_TwoGroup.grp.csv.gz -o OUT_05
@ 2018-12-11 11:17:42: Read group file "test_05_TwoGroup.grp.csv.gz" ...
	Group 1 has 10 samples:
		Normal_01,Normal_02,Normal_03,Normal_04,Normal_05,Normal_06,Normal_07,Normal_08,Normal_09,Normal_10
	Group 2 has 10 samples:
		CirrHCV_01,CirrHCV_02,CirrHCV_03,CirrHCV_04,CirrHCV_05,CirrHCV_06,CirrHCV_07,CirrHCV_08,CirrHCV_09,CirrHCV_10
@ 2018-12-11 11:17:42: Perfrom Mann-Whitney rank test of two samples ...
@ 2018-12-11 11:17:45: Perfrom Benjamini-Hochberg (aka FDR) correction ...
@ 2018-12-11 11:17:46: Writing to OUT_05.pval.txt



$ python3 ../bin/dmc_nonparametric.py -i test_06_ThreeGroup.tsv.gz -g test_06_ThreeGroup.grp.csv.gz -o OUT_06
@ 2018-12-11 11:18:34: Read group file "test_06_ThreeGroup.grp.csv.gz" ...
	Group 1 has 10 samples:
		Normal_01,Normal_02,Normal_03,Normal_04,Normal_05,Normal_06,Normal_07,Normal_08,Normal_09,Normal_10
	Group 2 has 10 samples:
		CirrHCV_01,CirrHCV_02,CirrHCV_03,CirrHCV_04,CirrHCV_05,CirrHCV_06,CirrHCV_07,CirrHCV_08,CirrHCV_09,CirrHCV_10
	Group 3 has 10 samples:
		HCCHCV_01,HCCHCV_02,HCCHCV_03,HCCHCV_04,HCCHCV_05,HCCHCV_06,HCCHCV_07,HCCHCV_08,HCCHCV_09,HCCHCV_10
@ 2018-12-11 11:18:34: Perfrom Kruskal-Wallis H-test ...
@ 2018-12-11 11:18:40: Perfrom Benjamini-Hochberg (aka FDR) correction ...
@ 2018-12-11 11:18:40: Writing to OUT_06.pval.txt

```   
#### Output file
Additional two columns ("pval", and "adj.pval") will be appended to the orignal data file.


<a name="p3.6"></a>dmc_ttest.py
---
This program performs differential CpG analysis based on beta values.

* use Student's t-test for two group comparison.
* use ANOVA for multiple groups comparison.

Notes: The ANOVA test has important assumptions that must be satisfied in order for the associated p-value to be valid.

* The samples are independent.
* Each sample is from a normally distributed population.
* The population standard deviations of the groups are all equal.  This property is known as homoscedasticity.

If these assumptions are not true for a given set of data, it may still be
    possible to use the Kruskal-Wallis H-test although with some loss of power.

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        Data file containing beta values with the 1st row
                        containing sample IDs (must be unique) and the 1st
                        column containing CpG positions or probe IDs (must be
                        unique). Except for the 1st row and 1st column, any
                        non-numerical values will be considered as "missing
                        values" and ignored. This file can be regular or
                        compressed by 'gzip' or 'bz'.
  -g GROUP_FILE, --group=GROUP_FILE
                        Group file define the biological groups of each
                        samples. It is a comma-separated 2 columns file with
                        the 1st column containing sample IDs, and the 2nd
                        column containing group IDs.  It must have a header
                        row. Sample IDs shoud match to the "Data file". Note:
                        automatically switch to use ANOVA if more than 2
                        groups were defined in this file.
  -p, --paired          If '-p/--paired' flag was specified, use paired t-test
                        which requires the equal number of samples in both
                        group. Paired sampels are matched by the order. This
                        option will be ignored for multiple group analysis.
  -w, --welch           If '-w/--welch' flag was specified, using Welch's
                        t-test which does not assume the two samples have
                        equal variance.  If omited , use standard two sample
                        t-test (i.e. assuming the two samples have equal
                        variance). This option will be ignored for paired
                        t-test and multiple group analysis.
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.    
```

#### Example
```text
$ python3 ../bin/dmc_ttest.py -i test_05_TwoGroup.tsv.gz -g test_05_TwoGroup.grp.csv.gz -o OUT_05

@ 2018-12-11 12:36:48: Read group file "test_05_TwoGroup.grp.csv.gz" ...
	Group 1 has 10 samples:
		Normal_01,Normal_02,Normal_03,Normal_04,Normal_05,Normal_06,Normal_07,Normal_08,Normal_09,Normal_10
	Group 2 has 10 samples:
		CirrHCV_01,CirrHCV_02,CirrHCV_03,CirrHCV_04,CirrHCV_05,CirrHCV_06,CirrHCV_07,CirrHCV_08,CirrHCV_09,CirrHCV_10
@ 2018-12-11 12:36:48: Perfrom standard t-test of two independent samples ...

@ 2018-12-11 12:36:52: Perfrom Benjamini-Hochberg (aka FDR) correction ...
@ 2018-12-11 12:36:52: Writing to OUT_05.pval.txt



$ python3 ../bin/dmc_ttest.py -i test_06_ThreeGroup.tsv.gz -g test_06_ThreeGroup.grp.csv.gz -o OUT_06

@ 2018-12-11 12:37:43: Read group file "test_06_ThreeGroup.grp.csv.gz" ...
	Group 1 has 10 samples:
		Normal_01,Normal_02,Normal_03,Normal_04,Normal_05,Normal_06,Normal_07,Normal_08,Normal_09,Normal_10
	Group 2 has 10 samples:
		CirrHCV_01,CirrHCV_02,CirrHCV_03,CirrHCV_04,CirrHCV_05,CirrHCV_06,CirrHCV_07,CirrHCV_08,CirrHCV_09,CirrHCV_10
	Group 3 has 10 samples:
		HCCHCV_01,HCCHCV_02,HCCHCV_03,HCCHCV_04,HCCHCV_05,HCCHCV_06,HCCHCV_07,HCCHCV_08,HCCHCV_09,HCCHCV_10
@ 2018-12-11 12:37:43: Perfrom ANOVA ...
@ 2018-12-11 12:37:45: Perfrom Benjamini-Hochberg (aka FDR) correction ...
@ 2018-12-11 12:37:45: Writing to OUT_06.pval.txt
```
#### Output file
Additional two columns ("pval", and "adj.pval") will be appended to the orignal data file.

<a name="p3.7"></a>genomic_distribution_1.py
----
This program counts number of CpGs falling into genomic regions defined by **genes** (5 groups):

1. Coding exons
2. UTR exons
3. Introns
4. Upstream intergenic regions (regions upstream of TSS)
5. Downsteam intergenic regions (regions downstream of TES)

Please note, a particular genomic region can be assigned to different groups listed above,
because most genes have multiple transcripts, and different genes could overlap on the
genome. For example, a exon of gene A could be located in a intron of gene B. To address
this issue, we define the following priority order:

Coding exons > UTR exons > Introns > Upstream intergenic regions > Downsteam intergenic regions

Higher-priority group override the low-priority group. For example, if a certain part
of a **intron** is overlapped with **exon** of other transcripts/genes, the overlapped part will
be considered as exon (i.e. removed from intron) since "exon" has higher priority.

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED file specifying the methylated C position. This
                        BED file should have at least 3 columns (Chrom,
                        ChromStart, ChromeEnd).  Note: the first base in a
                        chromosome is numbered 0. BED file can be regular or
                        compressed by 'gzip' or 'bz'.
  -r GENE_FILE, --refgene=GENE_FILE
                        Reference gene model in standard BED-12 format
                        (https://genome.ucsc.edu/FAQ/FAQformat.html#format1).
  -d DOWNSTREAM_SIZE, --downstream=DOWNSTREAM_SIZE
                        Size of down-stream intergenic region w.r.t. TES
                        (transcription end site). default=2000 (bp)
  -u UPSTREAM_SIZE, --upstream=UPSTREAM_SIZE
                        Size of up-stream intergenic region w.r.t. TSS
                        (transcription start site). default=2000 (bp)
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.

```

#### Example
```text

$ python3 ../bin/genomic_distribution_1.py -i test_03b.bed3.gz -r hg19.RefSeq.union.bed -o OUT_7

```

#### Output files
```text
$ cat OUT_7.tsv

Priority_order	Name	Number_of_regions	Size_of_regions(bp)	CpG_raw_count	CpG_count_per_KB
0	Coding exons	204685	39119881	65488	1.674033722137345
1	UTR exons	69937	38385741	61510	1.6024179395156133
2	Introns	214085	1228745034	329012	0.26776262845103793
3	Upstream of TSS	20507	37014855	120353	3.251478359161477
4	Downstream of TES	18790	35709088	10999	0.3080168275370124

The barplot "OUT_7.pdf" was also generated.
```         
![Genomic distribution.png](https://github.com/liguowang/cpgtools/blob/master/img/genomic_dist1.png)  

<a name="p3.8"></a>genomic_distribution_2.py
----
This program counts number of CpGs falling into genomic regions defined by **users**.
A maximum of 10 BED files (define 10 different genomic regions) can be analyzed.

Please note:
The **order** of BED files is important (i.e. considered as "priority order"). Overlapped
genomic regions will be kept only in the BED file with the highest priority and removed from
BED files of lower priority.  For example, users provided 3 BED files via
"-i promoters.bed,enhancers.bed,intergenic.bed", then if an enhancer region is overlapped
with promoters, **the overlapped part** will be removed from "enhancers.bed".

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i CPG_FILE, --cpg=CPG_FILE
                        BED file specifying the methylated C position. This
                        BED file should have at least 3 columns (Chrom,
                        ChromStart, ChromeEnd).  Note: the first base in a
                        chromosome is numbered 0. BED file can be regular or
                        compressed by 'gzip' or 'bz'.
  -b BED_FILES, --bed=BED_FILES
                        List of BED files specifying the genomic regions.
                        Note: (1) This program can only analyze a maximum of
                        10 BED files. (2) BED files should be separated by
                        comma (eg. " -i
                        promoters.bed,enhancers.bed,intergenic.bed"). (3) The
                        *order* of BED files is used to determine the
                        *priority* of BED files, and overlapped genomic
                        regions will be kept only in the BED file of the
                        highest priority and removed from BED files of lower
                        priority. For example, if an enhancer region is
                        overlapped with promoters, the *overlapped part* will
                        be removed from "enhancers.bed". (4) Each BED file
                        should have at least 3 columns (Chrom, ChromStart,
                        ChromeEnd), and the first base in a chromosome is
                        numbered 0. (5) BED files can be regular or compressed
                        by 'gzip' or 'bz'.
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
```

#### Input files
- [hg19_H3K4me3.bed4](https://github.com/liguowang/cpgtools/blob/master/test/hg19_H3K4me3.bed4)
- [hg19_CGI.bed4](https://github.com/liguowang/cpgtools/blob/master/test/hg19_CGI.bed4)
- [hg19_H3K27ac_with_H3K4me1.bed4](https://github.com/liguowang/cpgtools/blob/master/test/hg19_H3K27ac_with_H3K4me1.bed4)
- [hg19_H3K27me3.bed4](https://github.com/liguowang/cpgtools/blob/master/test/hg19_H3K27me3.bed4)
            
#### Example
```text
$ python3 ../bin/genomic_distribution_2.py -i test_03b.bed3.gz  -b  hg19_H3K4me3.bed4,hg19_CGI.bed4,hg19_H3K27ac_with_H3K4me1.bed4,hg19_H3K27me3.bed4 -o OUT_8

```

#### Output files
Similar to "genomic_distribution_1.py"      

<a name="p3.9"></a>methyl_logo.py
----
This program generates DNA sequence logo around methylated Cs in 3 steps:

1. Extract genomic sequences around methylated C postion
2. Generate [motif matrices](https://en.wikipedia.org/wiki/Position_weight_matrix) include:
	- position frequency matrix (PFM)
	- position probability matrix (PPM)
	- position weight matrix (PWM)
	- [MEME](http://meme-suite.org/doc/meme-format.html) format matrix
	- [Jaspar](http://jaspar.genereg.net/) format matrix
3. Generate motif logo using [weblogo](https://github.com/WebLogo/weblogo)

Note: **input file** must provide correct stand information. 

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED file specifying the methylated C position. This
                        BED file should have at least 6 columns (Chrom,
                        ChromStart, ChromeEnd, name, score, strand).  Note:
                        Must provide correct *strand* information. BED file
                        can be regular or compressed by 'gzip' or 'bz'.
  -r GENOME_FILE, --refgenome=GENOME_FILE
                        Reference genome seqeunces in FASTA format.
  -e EXTEND_SIZE, --extend=EXTEND_SIZE
                        Number of bases extended to up- and down-stream.
                        default=5 (bp)
  -n MOTIF_NAME, --name=MOTIF_NAME
                        Motif name. default=motif
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
```                        
#### Input file
[test_07_450K_CH.bed](https://github.com/liguowang/cpgtools/blob/master/test/test_07_450K_CH.bed)

#### Example
```text
$ python3 ../bin/methyl_logo.py -i test_07_450K_CH.bed -r /database/hg19.fa -o OUT_9
```

#### Output

Motif logo

![methyl_logo.png](https://github.com/liguowang/cpgtools/blob/master/img/methyl_logo.png)

Motif marices
```text
$ cat OUT_9.pfm
Base	1	2	3	4	5	6	7	8	9	10	11
A	969.0	979.0	299.0	211.0	2838.0	26.0	2891.0	262.0	81.0	1122.0	1083.0
C	412.0	447.0	831.0	190.0	22.0	2898.0	1.0	168.0	1291.0	1242.0	860.0
G	876.0	571.0	194.0	35.0	48.0	7.0	9.0	2477.0	739.0	58.0	462.0
T	675.0	935.0	1608.0	2496.0	24.0	1.0	31.0	25.0	821.0	510.0	527.0

$ cat OUT_9.meme
----------------------------------------
motif position-specific probability matrix
----------------------------------------
letter-probability matrix: alength= 4 w= 11 nsites= 2932
 0.3304691762138571 0.1405482815057283 0.2987588652482269 0.23022367703218768
 0.33387888707037644 0.1524822695035461 0.19476268412438624 0.3188761593016912
 0.10201854882705945 0.2834151663938898 0.0662165848336061 0.5483496999454446
 0.07201309328968904 0.06485270049099837 0.012002182214948174 0.8511320240043645
 0.967744135297327 0.007569558101472996 0.016434806328423354 0.00825150027277687
 0.008933442444080744 0.9882024004364431 0.0024549918166939452 0.00040916530278232413
 0.9858156028368796 0.00040916530278232413 0.0031369339879978183 0.010638297872340429
 0.0894026186579378 0.057351336606655756 0.8446535733769777 0.008592471358428807
 0.02768685215493726 0.4402618657937807 0.2520458265139116 0.28000545553737044
 0.3826377523186034 0.42355428259683586 0.01984451718494272 0.17396344789961812
 0.36933987997817785 0.29330332787779595 0.15759683578832515 0.17975995635570105
```

<a name="p3.10"></a>region_profile.py
----
This program calculates the overall methylation level (i.e. average beta value) over
particular genomic regions (eg. promoters, TF bindings). 

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED6 file specifying the C position. This BED file
                        should have at least 6 columns (Chrom, ChromStart,
                        ChromeEnd, Name, Beta_value, Strand).  Note: the first
                        base in a chromosome is numbered 0. BED file can be
                        regular or compressed by 'gzip' or 'bz'.
  -r REGION_FILE, --region=REGION_FILE
                        BED file specificy genomic regions. This BED file
                        should have at least 3 columns (Chrom, ChromStart,
                        ChromeEnd). If the 6-th column does not exist, all
                        regions will be considered as on "+" strand.
  -d DOWNSTREAM_SIZE, --downstream=DOWNSTREAM_SIZE
                        Size of extension to downstream. default=2000 (bp)
  -u UPSTREAM_SIZE, --upstream=UPSTREAM_SIZE
                        Size of extension to upstream. default=2000 (bp)
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
```                        
#### Example
```text
python3 ../bin/region_profile.py -i test_02.bed6.gz -r hg19.RefSeq.union.1Kpromoter.bed -o OUT_10
```

#### Output
Average methylation profile over "upstream"(left), "user-specified" (center), and "down-stream"(right) genomic regions. 
Note: All groups ("upstream", "user-specified", and "down-stream") were scaled into 100 nt long, regardless of their 
actual genomic sizes.   

![region_profile.png](https://github.com/liguowang/cpgtools/blob/master/img/region_profile.png)

<a name="p3.11"></a>region_stat.py
----
This program gives basic statistics for each genomic region. Add 6 columns to the input BED file:

1. Number of CpGs detected in the genomic region
2. Min methylation level
3. Max methylation level
4. Average methylation level across all CpGs
5. Median methylation level across all CpGs
6. Standard deviation

#### Basic usage
```text
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file=INPUT_FILE
                        BED file specifying the methylated C position. This
                        BED file should have at least 6 columns (Chrom,
                        ChromStart, ChromeEnd, Name, Beta_value, Strand).
                        Note: the first base in a chromosome is numbered 0.
                        BED file can be regular or compressed by 'gzip' or
                        'bz'.
  -r REGION_FILE, --region=REGION_FILE
                        BED file specificy genomic regions. This BED file
                        should have at least 3 columns (Chrom, ChromStart,
                        ChromeEnd).
  -o OUT_FILE, --output=OUT_FILE
                        Prefix of output file.
```

#### Example
```text

$ python3 ../bin/region_stat.py -i test_02.bed6.gz -r hg19.RefSeq.union.1Kpromoter.bed -o OUT_11

$ grep -v "NA" OUT_11.txt |head
chr1	563888	564889	LOC101928626	0	-	2	0.3746	0.395	0.3848	0.3848	0.0144
chr1	752250	753251	FAM87B	0	+	2	0.4641	0.6485	0.5563	0.5563	0.1304
chr1	811681	812682	FAM41C	0	-	3	0.7784	0.8494	0.8228	0.8407	0.0387
chr1	854571	855572	LOC100130417	0	-	11	0.4197	0.9319	0.8018	0.8744	0.1602
chr1	860620	861621	SAMD11	0	+	8	0.0252	0.5	0.1595	0.0505	0.1972
chr1	894178	895179	NOC2L	0	-	4	0.0571	0.234	0.137	0.1285	0.0755
chr1	895466	896467	KLHL17	0	+	7	0.0339	0.4091	0.1589	0.0924	0.1405
chr1	901376	902377	PLEKHN1	0	+	7	0.0294	0.7146	0.2418	0.1511	0.2615
chr1	916996	917997	PERM1	0	-	8	0.2443	0.6882	0.4772	0.481	0.1363
chr1	935051	936052	HES4	0	-	3	0.0863	0.1507	0.1145	0.1066	0.0329


```     

<a name="p3.12"></a>trichotmize.py
----
                        