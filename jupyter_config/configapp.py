import glob
import os
import sys
import re 

from jupyter_core.application import JupyterApp, base_aliases, base_flags
import jupyter_core.paths as jpaths
from traitlets.config import catch_config_error

config_aliases = {}
config_aliases.update(base_aliases)

config_flags = {}
config_flags.update(base_flags)

class JupyterConfigApp(JupyterApp):
    name = "jupyter-config"
    description = "A Jupyter Application for searching in and finding config files."
    # aliases = config_aliases
    # flags = config_flags
    
    
    # subcommands = dict(
    #     list=(JupyterConfigListApp, JupyterConfigListApp.description.splitlines()[0]),
    #     search=(JupyterConfigSearchApp, JupyterConfigSearchApp.description.splitlines()[0]),
    # )
    
    @catch_config_error
    def initialize(self, argv=None):
        super(JupyterConfigApp, self).initialize(argv)
        search_jupyter_paths(self.extra_args)
        
    # @classmethod
    # def launch_instance(cls, argv=None, **kwargs):
    #     import ipdb; ipdb.set_trace()
    #     super(JupyterConfigApp, cls).launch_instance(argv=argv, **kwargs)
        
    
    
    # @classmethod
    # def main(cls):
    #     if len(sys.argv)==1:
    #         search_jupyter_paths()
    #     elif len(sys.argv)==2:
    #         search_jupyter_paths(sys.argv[1])
    #     else:
    #         raise RuntimeError("You can only pass in a single string at this time.")

def valid_conf_file(file_name):
# replace with canonical config validation checker
    return (os.path.isfile(file_name) 
            and os.path.splitext(file_name)[1] in ['.py', '.json'])
    

canonical_names_regex = re.compile(r"jupyter_(\w*_|)config")

def valid_local_conf_file(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return (valid_conf_file(file_path) 
            and canonical_names_regex.match(file_name))
    
def valid_gen_conf_file(file_path, name_regex):
    file_name = os.path.basename(file_path)
    return (valid_conf_file(file_path) 
            and name_regex.match(file_name))
        
def search_jupyter_paths(search_term=''):
    
    if search_term is not '' and isinstance(search_term, list) and len(search_term)>0:
        search_term = search_term[0]
         
    # print(search_term)
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
    for file_name in conf_file_list:
        if len(search_term)>0:
            print_indexed_content(file_name=file_name, search_term=search_term)
        else:
            print(file_name)
        
def print_indexed_content(file_name='', search_term=''):
    with open(file_name,"r") as f:
        if search_term in f.read():
            f.seek(0)
            line_numbers_match = []
            for line_no, text in enumerate(f,1):
                if search_term in text:
                    line_numbers_match.append((line_no,text.strip()))
            output = ["{}: {}".format(x,y) for x,y in line_numbers_match]
            print(file_name + "\n" + "\n".join(output),"\n")


main = launch_new_instance = JupyterConfigApp.launch_instance
