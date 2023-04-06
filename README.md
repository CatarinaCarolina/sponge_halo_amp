## This is the Github repository for the scrips and input files used to perform the analysis described in the following project: "PhD thesis chapter - Halogenated small molecule producing BGC diversity in marine sponges"

### Requirements:

Please keep in mind that these scripts have only been tested in python3.

#### Software:

- antiSMASH v6.0
- BiG-SCAPE
- dREP
- GTDB-Tk
- Pyhton 3+

#### Pyhton Packages:

- argparse
- pandas
- SeqIO

### Guidelines:

#### antiSMASH post processing: Extract and trim antiSMASH6 BGCs based on Halo_AMP protocluster

```
python3 as6_extract_haloAMP.py -g /all_BGC_as6_halo_amp -o /all_BGC_as6_extracted_Halo_AM
```

#### dREP post processing: make bin_cluster info table bin_cluster bins rep_bin samples
```
ls ../dereplicated_all_reassembled_bins_gANI95_c50/dereplicated_genomes/ > representative_genomes_c50.txt

python3 compile_bin_cluster_info.py -r dREP_representative_genomes_c50.txt -c /dREP_dereplicated/data_tables/Cdb.csv -o rep_bins_samples_c50.txt
```


#### BiG-SCAPE post processing: extract BGC, contig
```
cat /bigscape/network_files/hybrids_auto/Network_Annotations_Full.tsv | grep -v 'BGC0' | awk -F '\t' '{print $1"\t"$3"}' >  BSas6_halo_AMP_BGC_contig.tsv
```


#### BiG-SCAPE post processing: extract GCF, BGC sample
```
python3 as6halo_BGC_to_GFC.py -i BSas6_halo_AMP_BGC_contig.tsv -g /bigscape/network_files/2022-10-06_14-20-36_hybrids_auto/mix/mix_clustering_c0.30.tsv -o BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample.tsv
```


#### BiG-SCAPE post processing: extract bin
```
python3 from_contig_get_bin.py -i BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample.tsv -o BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin.tsv -b /all_refined_bins/
# uses contig header, so will not work on reassembled bins
```

#### BiG-SCAPE post processing: add representative bin
```
python3 add_binrep_GCF.py -b cluster_rep_bins_samples.tsv -g BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin.tsv -o BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin_brep.tsv
```

#### BiG-SCAPE post processing: add bin class and binrep class
```
python3 add_binrepclass_domexpinfo.py -c bin_gtdbtk/classify/gtdbtk.bac120.summary.tsv -t BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin_brep.tsv -o BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin_brep_class.tsv
```

#### BiG-SCAPE post processing: make a gcf oriented table with bin and sample info ap
```
python3 GCF_to_sample_binrep_as6haloamp.py -g BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin_brep_class.tsv -o BSas6_halo_AMP_co0_3_GCF_samples_bins_binrep_classrep.tsv
```

#### BiG-SCAPE BGC + MAG post processing
```
cat /bigscape/network_files/hybrids_auto/Network_Annotations_Full.tsv | grep -v 'BGC0' | awk -F '\t' '{print $1"\t"$3}' > BSas6_halo_AMP_co0_3_BGCbin_contig.tsv

python3 as6halo_BGC_to_GFC.py -i BSas6_halo_AMP_co0_3_BGCbin_contig.tsv -g /bigscape_BGCbin/network_files/hybrids_auto/mix/mix_clustering_c0.30.tsv -o BSas6_halo_AMP_co0_3_BGCbin_contig_gcf_sample.tsv

```

#### BiG-SCAPE BGC + MAG post processing: BCG MAG reduce (for contigs in both metagenome and MAG, choose the longest one) and annotate
```
python3 as6halo_bigscape_mix_BCGmagR_reduce_annotate.py -i BSas6_halo_AMP_co0_3_BGC_contig_gcf_sample_bin_brep_class.tsv -m BSas6_halo_AMP_co0_3_BGCbin_contig_gcf.tsv -o BSas6_halo_AMP_co0_3_BGCbin_contig_gcf_derep.tsv
```

#### GBK miscellaneous: extract gbk seqs as fasta
```
python3 gbks_extract_dnaseq.py -g all_BGC_as6_extracted_Halo_AMP/ -o all_BGC_as6_extracted_Halo_AMP_seq.fa
```

#### GBK miscellaneous: extract CDS prot seqs from a gbk
```
python3 gbk_to_cds_fasta.py -g Halo_AMP_1.gbk -o Halo_AMP_1_cds.faa
```

#### GBK miscellaneous: extract CDS by sec_met_domain
```
python3 gbk_extract_genebysecmetdomain.py -g /all_BGC_as6_halo_amp/ -d 'AMP-binding' -o AMP-binding_all_BGC_as6.faa
```
