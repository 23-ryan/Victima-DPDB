# I need to read a csv file and use pivot tables
# to create a plot of the data
# I will use the pandas library to read the csv file

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Set Seaborn style
sns.set(style="whitegrid")

# Increase font size
plt.rcParams.update({'font.size': 14})
# Read the csv file into a dataframe
orca_art = """
                                       _
                                     / |
                                    /  |
                                   /   |
                                  /    |
                ,____.-----------'     `.______,                         ._
           ._--"                                "-----.______,          / /
         ,/__o_~##mm                                          "-----__./  |
         ==--    ~~                                 ____               \_ |
          "~###**~~~|   \                    ./####"            _________(
               ~~~##|    |~~~      _________/###/                /###\.   |
                    (    |##################~__________--------~~~~~~~~\  |
                     \   |  ~~###########~~~~~~                         \._
                      \__\
            :- Orcinus Orca wishes a nice summer  -:
"""
summer_art = """
          ... ....                     .. ...                           ____,--
  .. ...... .                           ........__                  __,'MMII;:.
...                                      ......|__|            _,--'MMI;:.
                                    @         /|. .          ,'MMI;:.WI;;:.
            ,d888b,                |.\       / |\           /MWI;;  WWI;.
           J8888888L               |' \     /^^|^\        ,'MWI;   WWWI;;:.
           888888888               |. o\ __/___|__\_   ,-'MWI;:.  WI;;::.
-----------------------------------|.  L\-`--------'--'_MWI;:.   WWI;;:.
      - -__--__--__--__ -           \.   \                `---. WI;:.     ____-
       - __--__--__-- _             |:    :.                   `/|-------'
        _ -__--__--_ -              |:     ::.                ,''/
          - _--__- _                |/       ::.             /: |
___        _ --__ -                 /'         :`--.______,-::  /
###\        _ -_ -                 /'   ._ .     ``        '    `-_
,--'         --__              _,-'   __/. .... .  .  ___,---.__,-'-.
              -_         __,--/'   __/##`-._____,----'::::::::::::::#\
                              `---'`````##:::::::::::::::::::::::::::#`---.
With sun and seals                                      `````::::::::::::#######:::####\
//

"""


def print_separator():
    print("\n===============================================================\n")


print(orca_art)


desired_order_labels = [
    "bfs",
    "cc"
]
desired_order_labels_gmean = [
    "BFS",
    "CC",
    "GMEAN"
]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
print_separator()
print("Plotting Figure 2: L2 TLB MPKI for different traces")
print_separator()
# Reindex the DataFrame to change the order of experiments

df = pd.read_csv('./results.csv')
df.fillna(0, inplace=True)

# Create a pivot table of the data
selected_experiments = ['tlb_base_ideal',
                        'victima_ptw_1MBL2',
                        'victima_ptw_1MBL2',
                        'victima_dpp_dbp_ptw_1MBL2',
                        'victima_dpp_dbp_ptw_2MBL2']

df['stlb.mpki'] = (df['stlb.miss'] * 1000) / \
    df['performance_model.instruction_count']

df['host_ptw_latency'] = df["ptw_radix_1.page_level_latency_0"]+df["ptw_radix_1.page_level_latency_1"] + \
    df["ptw_radix_1.page_level_latency_2"] + \
    df["ptw_radix_1.page_level_latency_3"]
df['guest_ptw_latency'] = df["ptw_radix_0.page_level_latency_0"]+df["ptw_radix_0.page_level_latency_1"] + \
    df["ptw_radix_0.page_level_latency_2"] + \
    df["ptw_radix_0.page_level_latency_3"]

df['total_ptw_latency'] = df['host_ptw_latency'] + df['guest_ptw_latency']

# total_latency_baseline = (df.loc[df['Exp'] == 'baseline_radix_virtualized', 'total_ptw_latency']).values
# print(total_latency_baseline)
# total_latency_baseline = (df.loc[df['Exp'] == 'tlb_base_ideal', 'total_ptw_latency']).values
# print(total_latency_baseline)
# Filter the DataFrame for the selected experiments

df_selected = df[df['Exp'].isin(selected_experiments)]

# Create the pivot table with the selected experiments and GMEAN
geometric_mean = df_selected.groupby('Exp')['stlb.mpki'].apply(
    lambda x: np.prod(x) ** (1 / len(x)))


pivot_table_fig2 = df_selected.pivot_table(
    index='Trace', columns='Exp', values='stlb.mpki')
pivot_table_fig2 = pivot_table_fig2.reindex(desired_order_labels)
pivot_table_fig2.loc['GMEAN'] = geometric_mean.values
print(pivot_table_fig2)

# Sort the columns based on the 'selected_experiments' list
pivot_table_fig2 = pivot_table_fig2[selected_experiments]

ax = pivot_table_fig2.plot(kind='bar', figsize=(12, 3))
ax.set_xticklabels(desired_order_labels_gmean)

# Modify this list as per your requirements
new_legend_labels = ['L2 TLB 1.5K entries',
                     'Victima 1MB', 'Victima 2MB', 'Victima DPP DBP 1MB', 'Victima DPP DBP 2MB']
# ax.legend(new_legend_labels, title='Configuration',
#           bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xlabel('Trace')
plt.ylabel('L2 TLB MPKI')
plt.title('Figure 2: L2 TLB MPKI for different configurations')
plt.legend(new_legend_labels, title='Configuration',
           bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Replace 'output_path.png' with the desired file path and name for the saved image
plt.savefig('./plots/figure2.png')

print_separator()
print("Plotting Figure 15: Normalized Speedup for different configurations")
print_separator()

selected_experiments = ['tlb_base_ideal',
                        'pomtlb_64K',
                        'L3TLB_ideal_15',
                        'tlb_64x_ideal',
                        'tlb_128x_ideal',
                        'victima_ptw_1MBL2',
                        'victima_ptw_2MBL2',
                        'victima_dpp_dbp_ptw_1MBL2',
                        'victima_dpp_dbp_ptw_2MBL2']

df_selected = df[df['Exp'].isin(selected_experiments)]

pivot_table_fig15 = df_selected.pivot_table(
    index='Trace', columns='Exp', values='performance_model.cycle_count')
pivot_table_fig15 = pivot_table_fig15.rdiv(
    pivot_table_fig15['tlb_base_ideal'], axis=0)

pivot_table_fig15 = pivot_table_fig15[selected_experiments]
pivot_table_fig15 = pivot_table_fig15.reindex(desired_order_labels)

geometric_mean_perf = pivot_table_fig15.apply(
    lambda x: np.prod(x) ** (1 / len(x)))
pivot_table_fig15.loc['GMEAN'] = geometric_mean_perf.values

print(pivot_table_fig15)
# Drop the "Exp1" column as it will always be 1 in the relative pivot table

pivot_table_fig15.drop('tlb_base_ideal', axis=1, inplace=True)
ax = pivot_table_fig15.plot(kind='bar', figsize=(12, 3))

ax.set_xticklabels(desired_order_labels_gmean)
new_legend_labels = ['POM-TLB 64K',
                     'Opt. L3 TLB 64K', 'Opt. L2 TLB 64K', 'Opt. L2 TLB 128K', 'Victima 1MB', 'Victima 2MB', 'Victima DPP DBP 1MB', 'Victima DPP DBP 2MB']

plt.xlabel('Trace')
plt.ylabel('Normalized Speedup')
plt.title('Figure 15: Normalized Speedup')
plt.legend(new_legend_labels, title='Configuration',
           bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylim(0.9, 1.3)

plt.tight_layout()
plt.savefig('./plots/figure15.png')

print_separator()
print("Plotting Figure 16: PTW Reduction for different configurations")
print_separator()

selected_experiments = ['tlb_base_ideal',
                        'pomtlb_64K',
                        'tlb_64x_ideal',
                        'tlb_128x_ideal',
                        'victima_ptw_1MBL2',
                        'victima_ptw_2MBL2',
                        'victima_dpp_dbp_ptw_1MBL2',
                        'victima_dpp_dbp_ptw_2MBL2']

df_selected = df[df['Exp'].isin(selected_experiments)]

pivot_table_fig16 = df_selected.pivot_table(
    index='Trace', columns='Exp', values='PTW_0.page_walks')
pivot_table_fig16_subbed = pivot_table_fig16.rsub(
    pivot_table_fig16['tlb_base_ideal'], axis=0)
pivot_table_fig16_subbed = pivot_table_fig16_subbed.div(
    pivot_table_fig16['tlb_base_ideal'], axis=0)
pivot_table_fig16_subbed *= 100

pivot_table_fig16_subbed = pivot_table_fig16_subbed.reindex(
    desired_order_labels)

geometric_mean_perf = pivot_table_fig16_subbed.apply(
    lambda x: np.prod(x) ** (1 / len(x)))

pivot_table_fig16_subbed.loc['GMEAN'] = geometric_mean_perf.values
pivot_table_fig16_subbed = pivot_table_fig16_subbed[selected_experiments]
print(pivot_table_fig16_subbed)
# Drop the "Exp1" column as it will always be 1 in the relative pivot table

pivot_table_fig16_subbed.drop('tlb_base_ideal', axis=1, inplace=True)

ax = pivot_table_fig16_subbed.plot(kind='bar', figsize=(12, 3))

ax.set_xticklabels(desired_order_labels_gmean)
new_legend_labels = ['POM-TLB 64K',
                     'Opt. L2 TLB 64K', 'Opt. L2 TLB 128K', 'Victima 1MB', 'Victima 2MB', 'Victima DPP DBP 1MB', 'Victima DPP DBP 2MB']
plt.xlabel('Trace')
plt.ylabel('PTW Reduction (%)')
plt.title('Figure 16: Reduction of PTWs across different configurations')
plt.legend(new_legend_labels, title='Configuration',
           bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('./plots/figure16.png')

print_separator()
print("Plotting Figure 19: L2 Cache TLB Reuse with Victima DPDB 2MB")
print_separator()

selected_experiments = [
    'victima_dpp_dbp_ptw_2MBL2'
]

selected_metrics = [
    "L2.tlb-reuse-0",
    "L2.tlb-reuse-1",
    "L2.tlb-reuse-2",
    "L2.tlb-reuse-3",
    "L2.tlb-reuse-4",
]

df_selected = df[df['Exp'].isin(selected_experiments)]

pivot_table_fig19 = df_selected.pivot_table(
    index='Trace', columns='Exp', values=selected_metrics)

pivot_table_fig19 = pivot_table_fig19.div(
    pivot_table_fig19.sum(axis=1), axis=0) * 100
pivot_table_fig19 = pivot_table_fig19.reindex(desired_order_labels)

pivot_table_fig19.loc['GMEAN'] = pivot_table_fig19.mean()
print(pivot_table_fig19)


ax = pivot_table_fig19.plot(kind='bar', stacked=True, figsize=(12, 6))

ax.set_xticklabels(desired_order_labels_gmean)
new_legend_labels = ['Reuse 0',
                     '1-5', '5-10', '10-20', '>20']

plt.title('Figure 19: L2 Cache TLB Reuse with Victima DP DB')
plt.xlabel('Traces')
plt.ylabel('Breakdown of L2 TLB Reuse (%)')
plt.legend(new_legend_labels, loc='upper right',
           title='Reuse', bbox_to_anchor=(1.1, 1))

plt.tight_layout()
plt.ylim(0, 100)

# Replace 'output_path.png' with the desired file path and name for the saved image
plt.savefig('./plots/figure21.png')


#print_separator()
#print("Plotting Figure 20: PTW Reduction across different L2 Cache Sizes")
#print_separator()
#
#selected_experiments = ['baseline_radix_1MB',
#                        'baseline_radix_2MB',
#                        'baseline_radix_4MB',
#                        'baseline_radix_8MB',
#                        'victima_ptw_1MBL2',
#                        'victima_ptw_2MBL2',
#                        'victima_ptw_4MBL2',
#                        'victima_ptw_8MBL2',
#                        'victima_dpp_dbp_ptw_1MBL2',
#                        'victima_dpp_dbp_ptw_2MBL2',
#                        'victima_dpp_dbp_ptw_4MBL2',
#                        'victima_dpp_dbp_ptw_8MBL2'
#                        ]
#
#df_selected = df[df['Exp'].isin(selected_experiments)]
#
#pivot_table_fig20 = df_selected.pivot_table(
#    index='Trace', columns='Exp', values='PTW_0.page_walks')
#pivot_table_fig20['1MB'] = (pivot_table_fig20['baseline_radix_1MB'] -
#                            pivot_table_fig20['victima_ptw_1MBL2'])/pivot_table_fig20['baseline_radix_1MB']*100
#pivot_table_fig20['2MB'] = (pivot_table_fig20['baseline_radix_2MB'] -
#                            pivot_table_fig20['victima_ptw_2MBL2'])/pivot_table_fig20['baseline_radix_2MB']*100
#pivot_table_fig20['4MB'] = (pivot_table_fig20['baseline_radix_4MB'] -
#                            pivot_table_fig20['victima_ptw_4MBL2'])/pivot_table_fig20['baseline_radix_4MB']*100
#pivot_table_fig20['8MB'] = (pivot_table_fig20['baseline_radix_8MB'] -
#                            pivot_table_fig20['victima_ptw_8MBL2'])/pivot_table_fig20['baseline_radix_8MB']*100
#
#pivot_table_fig20.drop('baseline_radix_1MB', axis=1, inplace=True)
#pivot_table_fig20.drop('baseline_radix_2MB', axis=1, inplace=True)
#pivot_table_fig20.drop('baseline_radix_4MB', axis=1, inplace=True)
#pivot_table_fig20.drop('baseline_radix_8MB', axis=1, inplace=True)
#
#pivot_table_fig20.drop('victima_ptw_1MBL2', axis=1, inplace=True)
#pivot_table_fig20.drop('victima_ptw_2MBL2', axis=1, inplace=True)
#pivot_table_fig20.drop('victima_ptw_4MBL2', axis=1, inplace=True)
#pivot_table_fig20.drop('victima_ptw_8MBL2', axis=1, inplace=True)
#
#
#geometric_mean_perf = pivot_table_fig20.apply(
#    lambda x: np.prod(x) ** (1 / len(x)))
#pivot_table_fig20.loc['GMEAN'] = geometric_mean_perf.values
#
## Drop the "Exp1" column as it will always be 1 in the relative pivot table
#
#print(pivot_table_fig20)
#
#ax = pivot_table_fig20.plot(kind='bar', figsize=(12, 3))
#
#ax.set_xticklabels(desired_order_labels_gmean)
#new_legend_labels = ['1MB', '2MB', '4MB', '8MB']
#plt.xlabel('Trace')
#plt.ylabel('Reduction of PTWs (%)')
#plt.title('Figure 20: Reduction of PTWs across different L2 Cache Sizes')
#plt.legend(new_legend_labels, title='Configuration',
#           bbox_to_anchor=(1.05, 1), loc='upper left')
#
#plt.tight_layout()
#plt.savefig('./plots/figure20.png')
#
