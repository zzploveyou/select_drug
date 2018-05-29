import pandas as pd
import csv
import os
import re


def read_bio_number(csvfile="bio_unit_number.csv"):
    dic = {}
    with open(csvfile) as f:
        reader = csv.reader(f)
        for items in reader:
            pro = items[0]
            num = items[1]
            dic[pro] = int(num)
    return dic


def read_ligands(csvfile="ligands.csv"):
    f = open(csvfile)
    reader = csv.reader(f)
    protein_pocket_dict = {}
    for items in reader:
        protein = items[0].upper()
        pocks = items[4:]
        pockets = {}
        idx = 0
        while idx < len(pocks):
            pockets[pocks[idx]] = pocks[idx + 1:idx + 3]
            idx += 3
        protein_pocket_dict[protein] = pockets
    f.close()
    return protein_pocket_dict


def select_from_csv(csvfile):
    protein_pocket_dict = read_ligands(csvfile="ligands.csv")
    protein_bio_unit_dict = read_bio_number(csvfile="bio_unit_number.csv")
    df = pd.read_csv(csvfile, index_col=0)
    print("before selected: {}".format(df.shape))
    nopockets = [
        df.index[idx] for idx, nopocket in enumerate(pd.isnull(df.pocket))
        if nopocket is True
    ]
    # 舍弃没有pocket
    df.drop(nopockets, axis=0, inplace=True)
    for protein in df.index:
        pocket = (df['pocket'].loc[protein]).split("_")[0].strip()
        error = False
        try:
            weight, isDrug = protein_pocket_dict[protein][pocket]
        except KeyError:
            error = True
        try:
            weight = float(weight)
        except ValueError:
            # 舍弃未知重量的pocket
            df.drop(protein, axis=0, inplace=True)
            error = True
        if not error:
            if weight < 0.8 * float(df['u3(weight of Drug)'].loc[protein]):
                # 蛋白的pocket足够重
                df.drop(protein, axis=0, inplace=True)
            elif isDrug == 'Not Drug' or isDrug == 'Not Available':
                # pocket是药物
                df.drop(protein, axis=0, inplace=True)

    # u4, u5, u6, u7
    condition1 = df['u5(Vina satisfied count)'] >= 10
    condition2 = df['u6(maxClusterElementCount)'] >= 10
    condition3 = df['u7(u6satisfiedu5)'] >= df['u6(maxClusterElementCount)'] / 2
    condition4 = df['u4(<3A pose count)'] != 0
    new_df = df[condition1 & condition2 & condition3 & condition4]

    # 添加n聚体信息
    new_df = new_df.assign(
        n_mer=[protein_bio_unit_dict[ind] for ind in new_df.index])
    new_df = new_df[[
        'ligand', 'pocket', 'x0(ilbindScore)', 'y(vinaScore)', 'Max1', 'Max2',
        'Max3', 'x', 'u1(number of chains)', 'u2(number of templates)',
        'u3(weight of Drug)', 'n_mer', 'u4(<3A pose count)',
        'u5(Vina satisfied count)', 'u6(maxClusterElementCount)',
        'u7(u6satisfiedu5)', 'u8(radius)', 'u9(center)', 'u10(minDistance)',
        'Neighbor', 'v1(type of Protein)', 'v2(FS cardinal)',
        'v3(medical interest of ligand)', 'v4(weight of ligand)',
        'v5(type of ligand)', 'v6(type of drug)', 'v7(pose min distance)',
        'v8(pose mean distance)', 'v9(pose max distance)',
        'v10(pose distance sd)'
    ]]
    result_csv = "{}.result.csv".format(os.path.splitext(csvfile)[0])
    print("after  selected: {}".format(new_df.shape))
    print("result csv write into {}.".format(result_csv))
    new_df.to_csv(result_csv)


if __name__ == '__main__':

    select_from_csv(csvfile="017.csv")
