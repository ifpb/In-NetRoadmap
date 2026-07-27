from pathlib import Path
from ..renderer import render_template
import docker
import threading

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

def _build_iteration(client: docker.DockerClient, subdir: Path):
    """Worker function executed by each thread to build an individual image."""
    dockerfile_path = subdir / "Dockerfile"

    if dockerfile_path.exists():
        image_name = subdir.name
        tag_name = f"inetrm-{image_name}"

        print(f"Building image {tag_name}...")
        try:
            client.images.build(
                path=str(subdir.resolve()), tag=tag_name, rm=True
            )
            print(f"Successfully built {tag_name}")
        except Exception as e:
            print(f"Failed to build {tag_name}: {e}")

def build(root):
    client = docker.from_env()

    images_path = Path(root) / "images"
    if not images_path.exists() or not images_path.is_dir():
        raise FileNotFoundError("Images directory is missing")

    threads = []

    for subdir in images_path.iterdir():
        if subdir.is_dir():
            # Passamos o cliente e o caminho do subdiretório como argumentos para a thread
            t = threading.Thread(
                target=_build_iteration, args=(client, subdir)
            )
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

def up(params: dict, duration: int = 60):
    """Unpacks the configuration dictionary to run the container."""
    if not params:
        raise Exception("Parameters are empty")
    
    print("Provisioning topology...")
    client = docker.from_env()
    container = client.containers.run(**params)
    container.exec_run("bash -c 'openvswitch-switch start'")
    print(f"Will be up for {duration} seconds.")
    exit_code, output = container.exec_run(f"bash -c 'python3 /scripts/topology.py -t {duration}'")
    print(f"Containernet status: {exit_code}, {output}")
    print("Provision successful")
