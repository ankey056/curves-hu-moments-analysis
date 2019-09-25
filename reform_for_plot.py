#!/usr/bin/env python2

from collections import deque
from enum import Enum #, auto
from sys import argv
import os
import numpy as np

class ContourData:
    pass

class Transformation(Enum):
    FLAT = 1
    REF = 2
    NA1 = 3
    NA2 = 4
    ROT = 5

    @staticmethod
    def from_string(s):
        # s = s.upper()
        if s == "FLAT":
            return Transformation.FLAT
        elif s == "REF":
            return Transformation.REF
        elif s == "NA1":
            return Transformation.NA1
        elif s == "NA2":
            return Transformation.NA2
        elif s == "ROT":
            return Transformation.ROT
        else:
            raise Exception("{!r} is unknown transformation".format(s))

    @staticmethod
    def list_to_string(transformations):
        if transformations is None or len(transformations) == 0:
            return "NONE"
        else:
            return '*'.join(map(lambda x: x.name,
                                transformations))


def transformations_string(v):
    if v is None:
        return ""
    else:
        m = map(lambda t: t.name, v)
        return '*'.join(m)

def load_contours_data(hu_file, ca_file):
    c = deque()
    with open(hu_file, "r") as f:
        for line in f:
            l1 = line.split()
            x = ContourData()
            x.id = l1[0]
            x.resolution = int(l1[1])

            m = map(float, l1[2:9])
            x.hu = list(m)

            s = l1[9].upper()
            if s == "NONE":
                x.transformations = None
            else:
                m = map(Transformation.from_string,
                        s.split('_'))
                x.transformations = list(m)

            c.append(x)

    c = list(c)
    i = 0
    with open(ca_file, "r") as f:
        for line in f:
            d = c[i]
            m = map(np.double, line.split())
            l = list(m)
            d.pca = l[0:2]
            d.ica = l[2:5]
            i+=1

    return c
            
def collect_data(data, extractor, sorting_args={}):
    c = deque()
    for d in data:
        x = extractor(d)
        if x not in c:
            c.append(x)
    c = list(c)
    c.sort(**sorting_args)
    return c
    

def collect_contours_ids(data):
    return collect_data(data, lambda x: x.id)

def collect_contours_resolutions(data):
    return collect_data(data, lambda x: x.resolution)

def collect_different_transformations(data):
    return collect_data(data,
                        lambda x: x.transformations,
                        {'key': lambda x: len(x) if x is not None else 0})

def write_trajectory_in_file(points, path, header=None):
    size = len(points) - 1
    a = np.ndarray((size, 4),
                   dtype = np.double)
    for i in range(size):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        a[i, 0] = x1
        a[i, 1] = y1
        a[i, 2] = x2 - x1
        a[i, 3] = y2 - y1

    with open(path, "w") as f:
        if header is not None: f.write(header + '\n')
        np.savetxt(f, a,
                   fmt='%16.8e')

def write_group_gnuplot_init_file(directory, group_name,
                                  group_number, trajectories_count):
    with open(directory + "init.gp","w") as f:
        f.write("\n")
        for p, v in (("tcount", trajectories_count),
                     ("group_number", group_number),
                     ("group_name", '"' + group_name + '"')):
            f.write("{} = {}\n".format(p, v))

def get_trajectory_key_for_sorting(x):
    x = x.transformations
    if x is None:
        return 0
    else:
        return len(x)

def data_extractor_for_resolution(r):
    return lambda x: x.resolution == r

def make_trajectories_files(data, id, num, directory,
                            cs_extractor=collect_contours_resolutions,
                            dclass_extractor=data_extractor_for_resolution,
                            title_fun=str,
                            sort_key=get_trajectory_key_for_sorting):
    m = filter(lambda x: x.id == id,
               data)
    l = list(m)
    n = 0

    try:
        os.makedirs(directory)
    except:
        if not os.path.isdir(directory):
            raise

    clist = cs_extractor(l)
    write_group_gnuplot_init_file(directory, id, num, len(clist))

    for c in clist:
        n += 1
        header = title_fun(c)
        m = filter(dclass_extractor(c),
                   l)
        d = list(m)
        if sort_key is not None: d.sort(key=sort_key)

        l1 = (("PCA", lambda x: x.pca),
              ("ICA", lambda x: x.ica))
        for s, ex in l1:
            m = map(ex, d)
            p = "{}{}_trajectory_{:03d}.dat".format(directory,s , n)
            write_trajectory_in_file(list(m), p,
                                     header=header)

    return n

def data_extractor_for_transformations(ts):
    return lambda x: x.transformations == ts

def make_resolution_trajectories_files(data, id, num, directory):
    class_ex = collect_different_transformations
    data_ex = data_extractor_for_transformations
    return make_trajectories_files(data, id, num, directory,
                                   cs_extractor=class_ex,
                                   dclass_extractor=data_ex,
                                   title_fun=Transformation.list_to_string,
                                   sort_key=lambda x: x.resolution)


def make_transformation_trajectories_files(data, id, num, directory):
    return make_trajectories_files(data, id, num, directory)

def write_gnuplot_init_file(groups_count):
    with open("output/trajectories/init.gp","w") as f:
        f.write("\n")
        n = groups_count
        if n > 10: n = 10
        for i in range(1,n + 1):
            templ = "bind \"alt-{}\" \"eval loadDataGroup({})\";\n"
            f.write(templ.format(i % 10, i))

        f.write("\neval loadDataGroup(1);\n")

def write_gnuplot_plot_all_file(path, tp):
    ii = 0
    tmpl1 = "datfile({},{}) using 1:2:3:4 with vectors \\\n"
    indent = "     "
    addstr = ", \\\n" + indent
    with open(path, "w") as f:
        f.write("\n")
        for i, tcount, name in tp:
            ii+=1
            if ii == 1:
                f.write("plot ")
            else:
                f.write(addstr)

            f.write(tmpl1.format(i, 1))
            f.write("{}linetype {} title {!r}".format(indent, ii, name))

            if tcount > 1:
                for s in (addstr,
                          "for [i=2:{}] ".format(tcount),
                          tmpl1.format(i, "i"),
                          indent,
                          "linetype {} title ''".format(ii)):
                    f.write(s)

        f.write(";\n")
            

def reform_data(data, tmaker=make_resolution_trajectories_files):
    q = deque()
    n = 0
    ids = collect_contours_ids(data)
    for id in ids:
        n+=1
        dirname = "output/trajectories/group-{:03d}/".format(n)
        c = tmaker(data, id, n, dirname)
        q.append((n, c, id))

    write_gnuplot_init_file(len(ids))
    write_gnuplot_plot_all_file("output/trajectories/plot_all.gp",
                                tuple(q))


if __name__ == "__main__":
    data = load_contours_data("output/painted-contours-hu.dat",
                              "output/pca-ica-analysis.dat")

    if (argv > 2) and (argv[1:3] == ["by", "resolutions"]):
        reform_data(data, tmaker=make_transformation_trajectories_files)
    else:
        reform_data(data)


