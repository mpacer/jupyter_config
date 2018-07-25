import glob
import os
import sys
import re 
import itertools

from jupyter_core.application import JupyterApp, base_aliases, base_flags
from notebook.nbextensions import NBCONFIG_SECTIONS
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
        

def generate_potential_paths():
    """Generate all of the potential paths available in the current context.
    
    
    """
    base_conf_paths = list(filter(os.path.isdir, jpaths.jupyter_config_path()[::-1]))
        
    nbconfig_base_paths = list(filter(os.path.isdir, (os.path.join(d, 'nbconfig') 
                                                      for d in base_conf_paths)))
    conf_d_paths = list(filter(os.path.isdir, (os.path.join(d, 'jupyter_notebook_config.d') 
                                                            for d in base_conf_paths)))
    for d in nbconfig_base_paths:
        config_path_segment = list(filter(os.path.isdir, (os.path.join(d, section+'.d') 
                                                          for section in NBCONFIG_SECTIONS)))
        conf_d_paths.extend(config_path_segment)
    
    
    return {'base_conf_paths': base_conf_paths,
            'nbconfig_base_paths': nbconfig_base_paths,
            'conf_d_paths': conf_d_paths,
            }
    
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
