import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import json

class AnsibleService:
    def __init__(self):
        self.ansible_dir = "ansible"
        self.inventory_file = os.path.join(self.ansible_dir, "inventory.yml")
        self.playbook_file = os.path.join(self.ansible_dir, "postgresql.yml")

    def generate_config(self, config):
        """Generate Ansible configuration files"""
        try:
            terraform_output = self._get_terraform_outputs()
            self._generate_inventory(terraform_output)
            self._generate_postgresql_config(config)
            return "Ansible configurations generated successfully"
        except Exception as e:
            raise Exception(f"Failed to generate Ansible configs: {str(e)}")
    
    def _get_terraform_outputs(self):
        """Get outputs from Terraform"""
        try:
            output = subprocess.check_output(
                ["terraform", "output", "-json"],
                cwd="terraform"
            )
            return json.loads(output)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get Terraform outputs: {str(e)}")
    
    def _generate_inventory(self, terraform_output):
        """Generate Ansible inventory from Terraform outputs"""
        inventory = {
            "all": {
                "children": {
                    "postgresql": {
                        "children": {
                            "primary": {
                                "hosts": {
                                    "postgresql_primary": {
                                        "ansible_host": terraform_output["primary_instance_ip"]["value"]
                                    }
                                }
                            },
                            "replicas": {
                                "hosts": {}
                            }
                        },
                        "vars": {
                            "ansible_user": "ubuntu",
                            "ansible_ssh_private_key_file": os.getenv("SSH_KEY_PATH"),
                            "ansible_python_interpreter": "/usr/bin/python3"
                        }
                    }
                }
            }
        }

        replica_ips = terraform_output["replica_instance_ips"]["value"]
        for idx, ip in enumerate(replica_ips):
            inventory["all"]["children"]["postgresql"]["children"]["replicas"]["hosts"][f"postgresql_replica_{idx + 1}"] = {
                "ansible_host": ip
            }

        with open(self.inventory_file, "w") as f:
            json.dump(inventory, f, indent=2)
    
    def _generate_postgresql_config(self, config):
        """Generate PostgreSQL configuration files"""
        pass
    
    def configure(self):
        """Execute Ansible playbook"""
        try:
            subprocess.run(
                ["ansible-playbook", "-i", self.inventory_file, self.playbook_file],
                check=True
            )
            return "PostgreSQL configured successfully"
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ansible playbook execution failed: {str(e)}")
