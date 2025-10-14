import requests
import json

# SSL certificate configuration
cert_file = 'cert.pem'
key_file = 'key.pem'
ca_file = 'ca.pem'
base_url = 'https://localhost:2376'

# Configure SSL certificates for requests
cert = (cert_file, key_file)
verify = ca_file

def pull_nginx_image():
    """Pull the nginx:latest image"""
    url = f"{base_url}/images/create"
    params = {
        'fromImage': 'nginx',
        'tag': 'latest'
    }
    
    response = requests.post(
        url,
        params=params,
        cert=cert,
        verify=verify
    )
    
    if response.status_code == 200:
        print("Image pulled successfully")
        return True
    else:
        print(f"Failed to pull image: {response.status_code} - {response.text}")
        return False

def create_nginx_container():
    """Create nginx container with port mapping"""
    url = f"{base_url}/containers/create"
    params = {'name': 'testmynginx'}
    
    container_config = {
        "Image": "nginx",
        "HostConfig": {
            "PortBindings": {
                "80/tcp": [{"HostPort": "8080"}]
            }
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(
        url,
        params=params,
        json=container_config,
        headers=headers,
        cert=cert,
        verify=verify
    )
    
    if response.status_code == 201:
        container_data = response.json()
        container_id = container_data.get('Id')
        print(f"Container created successfully: {container_id}")
        return container_id
    else:
        print(f"Failed to create container: {response.status_code} - {response.text}")
        return None

def start_container(container_id):
    """Start the specified container"""
    url = f"{base_url}/containers/{container_id}/start"
    
    response = requests.post(
        url,
        cert=cert,
        verify=verify
    )
    
    if response.status_code == 204:
        print(f"Container {container_id} started successfully")
        return True
    else:
        print(f"Failed to start container: {response.status_code} - {response.text}")
        return False

# Main execution
if __name__ == "__main__":
    try:
        # Step 1: Pull nginx image
        if pull_nginx_image():
            # Step 2: Create container
            container_id = create_nginx_container()
            
            if container_id:
                # Step 3: Start container
                start_container(container_id)
            else:
                print("Could not create container")
        else:
            print("Could not pull image")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")