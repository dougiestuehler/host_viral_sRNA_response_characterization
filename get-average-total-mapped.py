import os
import pandas as pd
from glob import glob
import subprocess

def parse_filename(filename):
    """Extracts sample name, replicate number, and reference from filename."""
    parts = filename.split('-')
    sample = '-'.join(parts[:3])
    replicate = int(parts[3])
    reference = filename.split('bbmap-')[1].split('-antisense')[0]
    return sample, replicate, reference

def count_mapped_reads(file):
    """Counts the number of mapped reads in the provided BAM file using samtools."""
    result = subprocess.run(['samtools', 'view', '-c', '-F', '260', file], stdout=subprocess.PIPE, text=True)
    mapped_reads = int(result.stdout.strip())
    return mapped_reads

def read_and_process_files(file_pattern):
    """Reads BAM files matching the pattern and processes them to compute the average number of mapped reads."""
    files = glob(file_pattern)
    data = {}

    for file in files:
        sample, replicate, reference = parse_filename(os.path.basename(file))
        mapped_reads = count_mapped_reads(file)
        
        key = (sample, reference)
        if key not in data:
            data[key] = []
        data[key].append(mapped_reads)
    
    results = []

    for (sample, reference), counts in data.items():
        average_mapped_reads = sum(counts) / len(counts)
        results.append({
            'sample': sample,
            'reference': reference,
            'average_mapped_reads': average_mapped_reads
        })

    final_df = pd.DataFrame(results)
    return final_df

def main():
    file_pattern = "*.bam"
    output_dir = "Averaged_samtool_mapped"
    os.makedirs(output_dir, exist_ok=True)
    
    averaged_df = read_and_process_files(file_pattern)
    for _, row in averaged_df.iterrows():
        output_filename = os.path.join(output_dir, f"{row['sample']}_{row['reference']}_averaged_mapped_reads.txt")
        with open(output_filename, 'w') as f:
            f.write(f"sample\treference\taverage_mapped_reads\n")
            f.write(f"{row['sample']}\t{row['reference']}\t{row['average_mapped_reads']}\n")
        print(f"Output written to {output_filename}")

if __name__ == "__main__":
    main()
