from dependency_injector import containers, providers
from api.services.terraform_service import TerraformService
from api.services.ansible_service import AnsibleService
from api.config.settings import settings

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api.routes"]
    )

    config = providers.Configuration()

    terraform_service = providers.Singleton(
        TerraformService,
        terraform_dir="terraform",
    )

    ansible_service = providers.Singleton(
        AnsibleService,
        ansible_dir="ansible",
        ssh_key_path=settings.SSH_KEY_PATH,
    )