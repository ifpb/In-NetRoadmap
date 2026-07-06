from pathlib import Path
from ..renderer import render_template
import docker

def get_params(root):
    client = docker.from_env()

    network_name = "lab-network"
    try:
        client.networks.get(network_name)
    except docker.errors.NotFound:
        try:
            client.networks.create(network_name, driver="bridge")
        except Exception as e:
            print(f"❌ Failed to create network {network_name}: {e}")
            return {}

    pwd_path = Path(root).resolve()
    scripts_source = pwd_path / "containernet"

    params = {
        "image": "containernet/containernet:latest",
        "name": "containernet-lab",
        "detach": True,
        "privileged": True,
        "pid_mode": "host",
        "tty": True,
        "stdin_open": True,
        "working_dir": "/scripts",
        "entrypoint": "/bin/bash",
        "network": network_name,
        "environment": {
            "PYTHONUNBUFFERED": "1"
        },
        "volumes": {
            "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"},
            "/tmp": {"bind": "/tmp", "mode": "rw"},
            str(scripts_source): {"bind": "/scripts", "mode": "rw"}
        },
        "healthcheck": {
            "test": ["CMD", "docker", "ps"],
            "interval": 10_000_000_000,  # 10s in nanoseconds
            "timeout": 5_000_000_000,    # 5s in nanoseconds
            "retries": 5
        }
    }
    
    return params

def generate(cfg, output_path):
    # context = cfg["provision"]
    context = cfg.get("provision", {})

    template_dir = (Path(__file__).parent / "templates").resolve()
    template_file = "topology.py.j2"

    output_path = Path(output_path)

    render_template(str(template_dir), template_file, context, str(output_path))

def build(root):
    client = docker.from_env()

    images_path = Path(root) / "images"
    if not images_path.exists() or not images_path.is_dir(): raise FileNotFoundError("Images directory is missing")

    for subdir in images_path.iterdir():
        if subdir.is_dir():
            dockerfile_path = subdir / "Dockerfile"
            
            if dockerfile_path.exists():
                image_name = subdir.name
                tag_name = f"inetrm-{image_name}"

                print(f"Building image {tag_name}...")
                client.images.build(
                    path=str(subdir.resolve()),
                    tag=tag_name,
                    rm=True
                )
    

def up(params: dict):
    """Unpacks the configuration dictionary to run the container."""
    if not params:
        raise Exception("Parameters are empty")

    client = docker.from_env()
    container = client.containers.run(**params)
