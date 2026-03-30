import os
from jinja2 import Environment, FileSystemLoader

template_filename = 'switch-1-ml.yml.j2'
output_filename = 'switch-1-ml-rendered.yml'

def render_yaml_template(variables, output_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    env = Environment(loader=FileSystemLoader(current_dir))
    
    try:
        template = env.get_template(template_filename)
        
        rendered_content = template.render(variables)
        
        with open(output_dir + '/ansible/' + output_filename, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
            
        print(f"Generated ansible config file as: {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: Template file '{template_filename}' not found in working directory.")
    except Exception as e:
        print(f"An error has occured: {e}")

if __name__ == "__main__":
    render_yaml_template()
