import os

def cmd(src, dst):
    return f'cp {src} {dst}'


def copy_yaml_template(output_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.system(cmd(current_dir + '/' + 'host-1.yml', output_dir + '/ansible'))
    os.system(cmd(current_dir + '/' + 'host-2.yml', output_dir + '/ansible'))
    os.system(cmd(current_dir + '/' + 'Vagrantfile', output_dir))
    os.system(cmd(current_dir + '/' + 'ansible.cfg', output_dir))
    os.system(cmd(current_dir + '/' + 'inventory.ini', output_dir))
