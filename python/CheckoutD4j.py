'''

Created on Dec. 15, 2017

@author Andrew Habib

'''

import os
import subprocess
import sys

from joblib import Parallel, delayed


def exec_cmd(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def check_out_each_project(d4j_binary, dist, proj, ver, ver_type):
    print("Checkingout:", proj, ver, ver_type)
    ver = str(ver)
    proj_dist = dist + '/' + proj + '-' + ver
    
    cmd = [d4j_binary, 'checkout', '-p', proj, '-v', ver + ver_type, '-w', proj_dist]
    exec_cmd(cmd)
    
    print("Getting properties:", proj, ver, ver_type)
    os.chdir(proj_dist)
    
    cmd = [d4j_binary, 'export', '-p', 'classes.modified', '-o', 'prop-buggy-classes']
    exec_cmd(cmd)
 
    cmd = [d4j_binary, 'export', '-p', 'dir.src.classes', '-o', 'prop-source-dir']
    exec_cmd(cmd)
 
    cmd = [d4j_binary, 'export', '-p', 'cp.compile', '-o', 'prop-compile-path']
    exec_cmd(cmd)

    print("Compiling:", proj, ver, ver_type)
    cmd = [d4j_binary, 'compile']
    exec_cmd(cmd)

if __name__ == '__main__':
    
    path_d4j = sys.argv[1] if sys.argv[1].startswith("/") else os.path.join(os.getcwd(), sys.argv[1])
    ver_type = sys.argv[2]
    jobs = int(sys.argv[3])
    
    d4j_binary = os.path.join(path_d4j, 'framework/bin/defects4j')
    dist = os.path.join(path_d4j, 'projects', ver_type)
    
    print(dist)
    if not os.path.isdir(dist):
        os.makedirs(dist)

    cli_list = list(range(1, 6))
    cli_list += list(range(7, 41))
    closure_list = list(range(1, 63))
    closure_list += list(range(64, 93))
    closure_list += list(range(94, 177))
    collection_list = list(range(25, 29))
    lang_list = list(range(1, 2))
    lang_list += list(range(3, 66))
    time_list = list(range(1, 21))
    time_list += list(range(22, 28))

    projects = {
        # 'Chart': list(range(1, 27)),
        'Cli': cli_list,
        # 'Closure': closure_list,
        # 'Codec': list(range(1, 19)),
        # 'Collections': collection_list,
        # 'Compress': list(range(1, 48)),
        # 'Csv': list(range(1, 17)),
        # 'Gson': list(range(1, 19)),
        # 'JacksonCore': list(range(1, 27)),
        # 'JacksonDatabind': list(range(1, 113)),
        # 'JacksonXml': list(range(1, 7)),
        # 'Jsoup': list(range(1, 94)),
        # 'JxPath': list(range(1, 23)),
        # 'Lang': lang_list,
        # 'Math': list(range(1, 107)),
        # 'Mockito': list(range(1, 39)),
        # 'Time': time_list
    }
    
    Parallel(n_jobs=jobs)(delayed(check_out_each_project)
                          (d4j_binary, dist, proj, bug_list[bug_num], ver_type)
                            for proj, bug_list in projects.items()
                            for bug_num in range(0, len(bug_list))
                          )
