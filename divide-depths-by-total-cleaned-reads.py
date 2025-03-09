import os

# Directories for list1 and list2 files
list1_dir = '/mnt/c/Bioinformatics/Heck_USDA_Pathology/Aphid_siRNA_analysis_Summer_REU/siRNA_discovery/Just_samtools_analysis/All_viruses/Cleaned_reads_counts'
list2_dir = '/mnt/c/Bioinformatics/Heck_USDA_Pathology/Aphid_siRNA_analysis_Summer_REU/siRNA_discovery/Just_samtools_analysis/All_viruses/Filtered_bams/Samtools_depth_outputs'
output_dir = '/mnt/c/Bioinformatics/Heck_USDA_Pathology/Aphid_siRNA_analysis_Summer_REU/siRNA_discovery/Just_samtools_analysis/All_viruses/Filtered_bams/Samtools_depth_outputs/Depths_divided_by_total_reads'

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Read list1 files and extract sample values
list1_values = {}
for file in os.listdir(list1_dir):
    if file.endswith(".txt"):
        file_path = os.path.join(list1_dir, file)
        with open(file_path, 'r') as f:
            value = float(f.readline().strip())
            sample_id = "-".join(file.split("-")[:4])
            list1_values[sample_id] = value

# Process list2 files
for file in os.listdir(list2_dir):
    if file.endswith(".txt"):
        file_path = os.path.join(list2_dir, file)
        sample_id = "-".join(file.split("-")[:4])
        if sample_id in list1_values:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            output_file_path = os.path.join(output_dir, file)
            with open(output_file_path, 'w') as f:
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        parts[2] = str(float(parts[2]) / list1_values[sample_id])
                    f.write("\t".join(parts) + "\n")

print("Processing complete. Output files are saved in:", output_dir)
