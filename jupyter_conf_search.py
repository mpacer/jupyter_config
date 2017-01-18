import jupyter_core.paths as jpaths
import glob
import os
import sys

def valid_conf_file(file_name):
# replace with canonical config validation checker
    if not os.path.isfile(file_name):
        return False
    if os.path.splitext(file_name)[1]=='.py':
        return True
    if os.path.splitext(file_name)[1]=='.json':
        return True
    
def valid_local_conf_file(file_path, canonical_names=None):
    if canonical_names is None:
        canonical_names = ["jupyter_config",
                           "jupyter_notebook_config",
                           "jupyter_nbconvert_config"]

    file_name = os.path.splitext(os.path.split(file_path)[1])[0]
    return valid_conf_file(file_path) and file_name in canonical_names
    
def search_jupyter_paths(search_term=''):
    
    conf_path_list = []
    for dir in jpaths.jupyter_config_path():
        conf_path_list.extend(glob.glob(dir+"/**", recursive=True))
        
    conf_file_list = [f for f in conf_path_list if valid_conf_file(f)]
    local_path_list = glob.glob(os.getcwd()+"/**", recursive=True)
    
    conf_file_list.extend([f for f in local_path_list if valid_local_conf_file(f)])
    
    # go through files, 
    # if search term found in file
    # print name, line_no, content 
    conf_file_list.reverse()
    for file in conf_file_list:
        print_indexed_content(file=file, search_term=search_term)
        
        
def print_indexed_content(file='', search_term=''):
    with open(file,"r") as f:
        if search_term in f.read():
            f.seek(0)
            line_numbers_match = []
            for line_no, text in enumerate(f,1):
                if search_term in text:
                    line_numbers_match.append((line_no,text.strip()))
            output = ["{}: {}".format(x,y) for x,y in line_numbers_match]
            print(file + "\n" + "\n".join(output),"\n")


if __name__ == "__main__":
    search_jupyter_paths(sys.argv[1])

