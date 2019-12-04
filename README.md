# Mutalyzer_2_VCF
Fetches chromosome, position, reference, and alternate from Mutalyzer batch output files.

## TL;DR;
```python
python mutalyzer_2_vcf \
    -i mutalyzer_batch_output.file \    # Batch file from mutalyzer
    -o conveted.out \                   # Name of file to write
    -f /path/to/fasta                   # path to fasta file
```  

## Input file
This is an example of what the mutalyzer batch output file looks like. Only the first three columns are used. Anything else is ignored.

|Input Variant|Errors|Chromosomal Variant|Coding Variant(s)|			
|-------------|------|-------------------|-----------------|			
|NM_007194.3:c.846+4AGTA>-|(grammar): Expected "[" (at char 23), (line:1, col:24)| | |
|NM_000051.3:c.6176C>T||NC_000011.9:g.108186818C>T|LRG_135t1:c.6176C>T|	
|NM_000051.3:c.4324T>C||NC_000011.9:g.108160416T>C|LRG_135t1:c.4324T>C|		
|NM_000051.3:c.4066A>G||NC_000011.9:g.108158399A>G|LRG_135t1:c.4066A>G|		


## Output file
This is the format of the file output by `mutalyzer_2_vcf.py`.

|Submitted Variant|Chromosomal-based representation|Event Type|CHROM|POS|REF|ALT|
|---------------------|--------------------------|---|------|--------|---|---|
|NM_000051.3:c.6176C>T|NC_000011.9:g.108186818C>T|snp|chr11|108186818|C|T|
|NM_000051.3:c.4324T>C|NC_000011.9:g.108160416T>C|snp|chr11|108160416|T|C|
|NM_000051.3:c.4066A>G|NC_000011.9:g.108158399A>G|snp|chr11|108158399|A|G|
|NM_000051.3:c.7187C>G|NC_000011.9:g.108199845C>G|snp|chr11|108199845|C|G|
|NM_000051.3:c.3693_3695delATC|NC_000011.9:g.108153553_108153555delATC|del|chr11|108153552|TATC|T|
|NM_000051.3:c.2446_2447delGCinsCT|NC_000011.9:g.108129782_108129783delinsCT|delins|chr11|108129779|TGC|TCT|
|NM_000051.3:c.-32_-31dupTG|NC_000011.9:g.108093912_108093913dupTG|dup|chr11|108093911|G|GTG|
|NM_000051.3:c.5791delGinsCCT|NC_000011.9:g.108180915delinsCCT|delins|chr11|108180912|TGC|TCCT|
|NM_000051.3:c.6404_6405insTT|NC_000011.9:g.108190737_108190738insTT|ins|chr11|108190736|C|CTT|