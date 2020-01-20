import os
import pandas as pd
import numpy as np


def get_basic_file():
    df_all_cpg = pd.read_csv('res/cpg.csv', sep='\t', names=['chr', 'start', 'end', 'Index'])
    df_all_cpg = df_all_cpg.reindex(columns=(['Index'] + list([a for a in df_all_cpg.columns if a != 'Index'])))
    df_all_cpg.set_index('Index')
    df_all_cpg['Index'] = df_all_cpg['Index'].str.replace('CpG', '')
    df_all_cpg.insert(loc=4, column='is_in_island', value=0)
    df_all_cpg.insert(loc=5, column='M_percentage', value=0.0)
    df_islands = pd.read_csv('res/cpg_islands.csv', sep='\t', header=None, names=['chr', 'start', 'end'])
    for island_indx in range(df_islands.shape[0]):
        print(island_indx)
        start, end = df_islands.loc[island_indx, 'start'], df_islands.loc[island_indx, 'end']
        indx = np.logical_and(df_all_cpg.end.values <= end, df_all_cpg.start.values >= start)
        cpgs = df_all_cpg[indx]
        df_all_cpg.loc[indx, 'is_in_island'] = 1
    df_all_cpg.set_index('Index')
    df_all_cpg.to_csv('res/data.csv', sep='\t', index=False, index_label='Index')


if __name__ == '__main__':
    # os.system("tabix /cs/zbio/tommy/CBIO/2020/Roei/hg19.CpG.bed.gz chr15:62898527-62898675 > trail.csv")
    # os.system("tabix /cs/zbio/tommy/CBIO/2020/Roei/hg19.CpG-islands.bed.gz chr15 > cpg_islands.csv")
    # os.system("/cs/zbio/tommy/CBIO/2020/Roei/wgbstools view -r chr15 /cs/zbio/tommy/CBIO/2020/Roei/Liver_STL011.pat.gz > reads.csv")

    # df_all_cpg = pd.read_csv('res/res/cpg.csv', sep='\t', index_col=3, header=None, names=['chr', 'start', 'end'])
    # df_islands = pd.read_csv('res/cpg_islands.csv', sep='\t', header=None, names=['chr', 'start', 'end'])
    # print(df_all_cpg.shape[0])
    # print(df_islands.shape[0])

    # get_basic_file()
    # data = pd.read_csv('res/data.csv', sep='\t', index_col='Index')
    # reads = pd.read_csv('res/reads.csv', sep='\t', names=['chr', 'Index', 'read', 'amount'])
    #
    #
    # M_dict = {index:[0, 0] for index in data.index.unique()}
    #
    # for i, row in enumerate(reads.iterrows()):
    #     if i % 1000 == 0:
    #         print(i)
    #     start_index = row[1]['Index']
    #     read = row[1]['read']
    #     for j, r in enumerate(read):
    #         if (start_index + j) in M_dict.keys():
    #             if r == 'C':
    #                 M_dict[start_index + j][0] += 1
    #                 M_dict[start_index + j][1] += 1
    #                 # M_df.loc[start_index + j]['M_count'] += 1
    #                 # M_df.loc[start_index + j]['all_count'] += 1
    #             if r == 'T':
    #                 # M_df.loc[start_index + j]['all_count'] += 1
    #                 M_dict[start_index + j][1] += 1
    #
    #         else:
    #             print('Whoops!')
    #
    # M_df = pd.DataFrame.from_dict(M_dict, orient='index', columns=['M_count', 'all_count'])
    # percentage = np.divide(M_df['M_count'], M_df['all_count'], where = M_df['all_count'] != 0)
    # data['M_percentage'] = percentage
    # data.to_csv('res/full_data.csv', sep='\t')

    data = pd.read_csv('res/full_data.csv', sep='\t')
    data.insert(loc=6, column='distance', value=0)
    starts = data['start'].values
    ends = data['end'].values
    distances = (starts[1:] - ends[:-1] - 1)
    data['distance'] = [None] + distances.tolist()

    data.to_csv('res/data_final.csv', sep='\t')

    # df_all_cpg = reads.reindex(columns=(['Index'] + list([a for a in reads.columns if a != 'Index'])))
    # df_all_cpg.set_index('Index')
