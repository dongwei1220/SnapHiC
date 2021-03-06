import os
import sys
import glob
import pandas as pd
import pickle

def main(args):
    outdir = args[1]
    input_filenames = glob.glob(f'{outdir}/rwr/*.normalized.rwr.bedpe')
    del_len = len(".normalized.rwr.bedpe")
    line_counts = get_line_counts(input_filenames)
    with open(f'{outdir}/linecounts.pkl', 'wb') as ifile:
        pickle.dump(line_counts, ifile)
    line_counts['chrom'] = line_counts['name'].str.slice(start = 0, stop = - del_len)
    line_counts['chrom'] = line_counts['chrom'].str.split('.').apply(lambda x: x[-1])
    missing = line_counts.groupby('chrom').apply(get_missing)
    missing = [j for i in missing for j in i]
    print(f'{len(missing)} files have been detected to have faulty rwr files. Check the missig.txt file for a list of their names.')
    with open(f'{outdir}/rwr/missing.txt', 'w') as ofile:
        ofile.write('\n'.join(missing))

def get_missing(df):
    print(df.shape, df.iloc[0]['chrom'], df.iloc[0]['name'])
    max_count = max(df['count'])
    missing = df[df['count'] != max_count]['name'].tolist()
    return missing

def get_line_counts(input_filenames):
    counts = pd.DataFrame({'name': input_filenames})
    counts['count'] = 0
    for i, fname in enumerate(input_filenames):
        count = 0
        for line in open(fname).readlines(): count += 1
        counts.iloc[i, 1] = count
    return counts
    

args = sys.argv
main(args)
