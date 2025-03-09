import os
import pandas as pd

# Define the input directories
list1_dir = "/mnt/c/Bioinformatics/Heck_USDA_Pathology/Aphid_siRNA_analysis_Summer_REU/siRNA_discovery/Just_samtools_analysis/All_viruses/Filtered_bams/Samtools_depth_outputs/Averaged_samtool_depths"
list2_dir = "/mnt/c/Bioinformatics/Heck_USDA_Pathology/Aphid_siRNA_analysis_Summer_REU/siRNA_discovery/Just_samtools_analysis/All_viruses/Averaged_samtool_mapped/Times_virus_length"

# Function to get filenames without the suffix starting from 'output'
def get_prefix(filename):
    return filename.split("output")[0]

# Read the list of files from both directories
list1_files = os.listdir(list1_dir)
list2_files = os.listdir(list2_dir)

# Create a dictionary to map prefixes to list2 files
list2_dict = {get_prefix(f): f for f in list2_files}

# Iterate through list1 files and process matching files
for list1_file in list1_files:
    prefix = get_prefix(list1_file)
    list2_file = list2_dict.get(prefix)
    
    if list2_file:
        # Read the data from both files
        list1_path = os.path.join(list1_dir, list1_file)
        list2_path = os.path.join(list2_dir, list2_file)
        
        df_list1 = pd.read_csv(list1_path, sep='\t', header=None)
        df_list2 = pd.read_csv(list2_path, sep='\t', header=None)
        
        # Convert the third column of df_list1 to numeric
        df_list1[2] = pd.to_numeric(df_list1[2], errors='coerce')
        
        # Get the divisor from list2 file (second row, third column) and convert it to numeric
        divisor = pd.to_numeric(df_list2.iloc[1, 2], errors='coerce')
        
        # Ensure divisor is not zero to avoid division errors
        if divisor != 0:
            # Divide column 3 of list1 by the divisor
            df_list1[2] = (df_list1[2] / divisor) * 1000000
        
        # Output the result to a new file in list1 directory with a modified name
        output_filename = f"{prefix}output_FPKM_mapped.txt"
        output_path = os.path.join(list1_dir, output_filename)
        df_list1.to_csv(output_path, sep='\t', header=False, index=False)
        
        print(f"Processed {list1_file} and {list2_file}, output saved to {output_filename}")

print("Processing complete.")
