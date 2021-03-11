import os.path
import hetnetpy.readwrite
from hetnetpy.pathtools import paths_between

my_path = os.path.abspath(os.path.dirname(__file__))
graph = hetnetpy.readwrite.read_graph(os.path.join(my_path, "hetnet\\hetionet-v1.0.json"))
metagraph = graph.metagraph

# # Define source and target nodes
source_id = "Compound", "DB01234"
target_id = "Disease", "DOID:1612"

abbrevs = ["CcSEcCpD", "CdGdCpD", "CdGiGaD", "CdGr>GaD", "CdGaD", "CuGuCpD", "CbGbCpD", "CdGr>GuD", "CdG<rGaD",
           "CdGeAlD", "CuGr>GuD", "CuGr>GaD", "CdGiGdD", "CdGuCtD", "CpDrD", "CpD", "CbGdD", "CdGdAlD", "CuGeAlD",
           "CdGuAlD", "CpDaGaD", "CpDpSpD", "CrCbGdD", "CpDtCpD", "CpDdGdD", "CrCrCpD", "CuGiGaD", "CdG<rGdD",
           "CuGdCtD", "CpDuGuD", "CuGdAlD", "CuGuAlD", "CuGdDrD", "CpDpCpD", "CdGcGuD", "CpDtCtD", "CdGcGaD", "CdGiGuD",
           "CtDdGdD", "CpDuGaD", "CrCdGaD", "CdGuCpD", "CuG<rGaD", "CpDaGdD", "CiPCiCpD", "CuGiGuD", "CpDrDrD",
           "CbGdDrD", "CuGdD", "CbGbCtD", "CrCpDrD", "CbGiGdD", "CdGuDrD", "CuGcGdD", "CtDuGuD", "CdGdD", "CbGeAlD",
           "CtDtCpD", "CrCuGdD", "CuGdCpD", "CuG<rGuD", "CbGuAlD", "CbGiGaD", "CtDuGaD", "CpDdGaD", "CrCtD", "CtDdGaD",
           "CuGuCtD", "CuGcGaD", "CpDuGdD", "CdGr>GdD", "CrCdGuD", "CrCdGdD", "CbGaD", "CuG<rGdD", "CuGiGdD", "CtDdGuD",
           "CbGiGuD", "CuGr>GdD", "CuGaD", "CbGcGaD", "CbGaDrD", "CuGuDrD", "CdGbCtD", "CrCuGaD", "CrCrCtD", "CuGaDrD",
           "CrCpD", "CdGaDrD", "CdGdDrD", "CtDpSpD", "CdG<rGuD", "CpDaGuD", "CdGcGdD", "CbG<rGdD", "CtDuGdD", "CuGcGuD",
           "CuGbCtD", "CrCuGuD", "CbGuCtD", "CtDaGdD", "CpDdGuD", "CbGdAlD", "CtDlAlD", "CbGcGuD", "CdGuD", "CpDlAlD",
           "CbG<rGuD", "CbG<rGaD", "CbGr>GuD", "CdGdCtD", "CtDrDrD", "CbGr>GaD", "CrCbGaD", "CtDtCtD", "CtDaGuD",
           "CcSEcCtD", "CuGuD", "CbGr>GdD", "CtDaGaD"]

file = open(os.path.join(my_path, "hetnet\\DB01234.DOID1612.paths.txt"), "w", encoding="utf-8")
for abb in abbrevs:
    metapath = metagraph.metapath_from_abbrev(abb)
    print(metapath.get_unicode_str())
    paths = paths_between(graph, source_id, target_id, metapath)
    for p in paths:
        file.write(str(p))
        file.write("\n")
file.close()

