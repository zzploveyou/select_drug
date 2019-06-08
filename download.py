import threadpool
from urllib.request import urlretrieve
import csv
import os
import re


def download():
    """download pdb from list with threadpool."""
    ids = []
    for line in open("protein.list"):
        ids.append(line.strip())
    pool = threadpool.ThreadPool(8)
    requests = threadpool.makeRequests(download_pdb, ids)
    for req in requests:
        pool.putRequest(req)
    pool.wait()


def download_pdb(pdb_id):
    """download pdb file if not exists in ./pdb."""
    url = "https://files.rcsb.org/view/{}.pdb".format(pdb_id.upper())
    filename = "pdb/{}.pdb".format(pdb_id.upper())
    if not os.path.exists(filename):
        try:
            urlretrieve(url, filename)
        except Exception as e:
            print(e)


def get_mer_number():
    f = open("bio_unit_number2.csv", 'w')
    writer = csv.writer(f)
    """BIOLOGICAL UNIT of pdb file."""
    n_dict = {
        "DIMERIC": 2,
        "MONOMERIC": 1,
        "TRIMERIC": 3,
        "TETRAMERIC": 4,
        "HEXAMERIC": 6,
        "HEXADECAMERIC": 16,
        "HEPTAMERIC": 7,
        "24-MERIC": 24,
        "DECAMERIC": 10,
        "28-MERIC": 28,
        "PENTAMERIC": 5,
        "DODECAMERIC": 12,
        "OCTAMERIC": 8
    }
    for line in open("protein.list"):
        pdb_id = line.strip().upper()
        pdbfile = "pdb/{}.pdb".format(pdb_id)
        try:
            res = re.findall("AUTHOR DETERMINED BIOLOGICAL UNIT: (.*)",
                             open(pdbfile).read())[0].strip()
        except:
            res = re.findall("AUTHOR DETERMINED BIOLOGICAL UNIT: (.*)",
                             open(pdbfile).read())
        try:
            number = n_dict[res]
        except:
            number = res
        writer.writerow([pdb_id, number])
    f.close()
