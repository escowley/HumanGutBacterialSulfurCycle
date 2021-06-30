import sys
import logging
import os
import subprocess

information_file = sys.argv[1]
output_location = sys.argv[2]
threads = sys.argv[3]

genome_and_read_list = []
genome_and_read_dict = {}

'''
bowtie2-build [genome_fasta_file_location] [genome_fasta_file_location_minus_extension]

For Hannigan and Yu:
    bowtie2 -p [threads] -x [genome_fasta_file_location_minus_extension] -1 [read1_location_zipped] -2 [read2_location_zipped] -S output_location_[genome_fasta_file_minus_extension]_vs_read1_name.sam
For Feng:
    bowtie2 -p [threads] -x [genome_fasta_file_location_minus_extension] -U [read_location_zipped] -S output_location_[genome_fasta_file_minus_extension]_vs_read1_name.sam

shrinksam -i output_location_[genome_fasta_file_minus_extension]_vs_read1_name.sam -k output_location_[genome_fasta_file_minus_extension]_vs_read1_name.shrink.sam

iRep -f [genome_fasta_file_location] -s output_location_[genome_fasta_file_minus_extension]_vs_read1_name.shrink.sam -o output_location_genome_fasta_file_minus_extension]_iRep_vs_read1_name
'''

if output_location == "./" or output_location == ".":
    output_location = os.getcwd()
if output_location.endswith("/"):
    output_location = output_location[:-1]

with open(information_file, "r") as info_file:
    for line in info_file:
        if "Genome Name" in line:
            continue
        elif "FengQ" in line:
            genome_file_location = line.split(",")[5].strip()
            read_file_location = line.split(",")[7].strip()
            sam_file_output = output_location + "/" + genome_file_location[:-6].split("/")[-1] + "_vs_" + read_file_location.split("/")[-1].split(".")[0] + ".sam"
            zipped_genome_file_location = genome_file_location + ".gz"
            shrinksam_output = sam_file_output.replace(".sam", ".shrink.sam")
            irep_output = output_location + "/" + genome_file_location[:-6].split("/")[-1] + "_vs_" + read_file_location.split("/")[-1].split(".")[0] + "_iRep"
            
            unzip_genomes = subprocess.Popen(["gzip", "-d", zipped_genome_file_location], shell=False)
            unzip_genomes.wait()
            bowtie_build = subprocess.Popen(["bowtie2-build", genome_file_location, genome_file_location[:-6]], shell=False)
            bowtie_build.wait()
            bowtie_mapping = subprocess.Popen(["bowtie2", "--reorder", "-p", threads, "-x", genome_file_location[:-6], "-U", read_file_location, "-S", sam_file_output], shell=False)
            bowtie_mapping.wait()
            shrinksam_run = subprocess.Popen(["shrinksam", "-u", "-i", sam_file_output, "-k", shrinksam_output], shell=False)
            shrinksam_run.wait()
            irep_run = subprocess.Popen(["iRep", "-f", genome_file_location, "-s", shrinksam_output, "-o", irep_output, "-t", threads], shell=False)
            irep_run.wait()
            sam_removal = subprocess.Popen(["rm", sam_file_output], shell=False)
            sam_removal.wait()
            zip_genomes = subprocess.Popen(["pigz", "-p", threads, genome_file_location], shell=False)
            zip_genomes.wait()
            
        elif "YuJ" in line or "HanniganGD" or "ZellerG" in line:
            genome_file_location = line.split(",")[5].strip()
            read1_file_location = line.split(",")[7].strip()
            read2_file_location = line.split(",")[8].strip().replace("\n", "")
            sam_file_output = output_location + "/" + genome_file_location[:-6].split("/")[-1] + "_vs_" + read1_file_location.split("/")[-1].split("_")[0] + ".sam"
            zipped_genome_file_location = genome_file_location + ".gz"
            shrinksam_output = sam_file_output.replace(".sam", ".shrink.sam")
            irep_output = output_location + "/" + genome_file_location[:-6].split("/")[-1] + "_vs_" + read1_file_location.split("/")[-1].split("_")[0] + "_iRep"
            
            unzip_genomes = subprocess.Popen(["gzip", "-d", zipped_genome_file_location], shell=False)
            unzip_genomes.wait()
            bowtie_build = subprocess.Popen(["bowtie2-build", genome_file_location, genome_file_location[:-6]], shell=False)
            bowtie_build.wait()
            bowtie_mapping = subprocess.Popen(["bowtie2", "--reorder", "-p", threads, "-x", genome_file_location[:-6], "-1", read1_file_location, "-2", read2_file_location, "-S", sam_file_output], shell=False)
            bowtie_mapping.wait()
            shrinksam_run = subprocess.Popen(["shrinksam", "-i", sam_file_output, "-k", shrinksam_output], shell=False)
            shrinksam_run.wait()
            irep_run = subprocess.Popen(["iRep", "-f", genome_file_location, "-s", shrinksam_output, "-o", irep_output, "-t", threads], shell=False)
            irep_run.wait()
            sam_removal = subprocess.Popen(["rm", sam_file_output], shell=False)
            sam_removal.wait()
            zip_genomes = subprocess.Popen(["pigz", "-p", threads, genome_file_location], shell=False)
            zip_genomes.wait()
