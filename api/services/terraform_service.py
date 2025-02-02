import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import json

class TerraformService:
    def __init__(self):
        self.terraform_dir = "terraform"
        self.template_dir = os.path.join(self.terraform_dir, "templates")

    def generate_config(self, config):
        """Generate Terraform configuration files from templates"""
        env = Environment(loader=FileSystemLoader(self.template_dir))

        main_template = env.get_template("postgresql.tftpl")
        main_content = main_template.render(
            postgresql_version=config.postgresql_version,
            instance_type=config.instance_type,
            replica_count=config.replica_count,
            vpc_id=config.vpc_id,
            subnet_ids=config.subnet_ids,
            environment=config.environment,
            key_name=config.key_name or "${var.key_name}"
        )
        with open(os.path.join(self.terraform_dir, "main.tf"), "w") as f:
            f.write(main_content)
        return "Configuration generated successfully"
    def apply(self):
        """Apply Terraform configuration"""
        try:
            subprocess.run(["terraform", "init"], cwd=self.terraform_dir, check=True)

            subprocess.run(
                ["terraform", "apply", "-auto-approve"],
                cwd=self.terraform_dir,
                check=True
            )

            output = subprocess.check_output(
                ["terraform", "output", "-json"],
                cwd=self.terraform_dir
            )
            return json.loads(output)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Terraform apply failed: {str(e)}")
