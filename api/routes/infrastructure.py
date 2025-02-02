from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from api.services.terraform_service import TerraformService
from api.services.ansible_service import AnsibleService

router = APIRouter()

class PostgreSQLConfig(BaseModel):
    postgresql_version: str
    instance_type: str
    replica_count: int
    max_connections: int
    shared_buffers: str
    vpc_id: str
    subnet_ids: List[str]
    environment: str
    key_name: Optional[str] = None

@router.post("/generate")
async def generate_infrastructure(config: PostgreSQLConfig):
    try:
        terraform_service = TerraformService()
        ansible_service = AnsibleService()

        tf_config = terraform_service.generate_config(config)
        ansible_config = ansible_service.generate_config(config)
        return {
            "status": "success",
            "message": "Infrastructure configurations generated successfully",
            "terraform_config": tf_config,
            "ansible_config": ansible_config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apply")
async def apply_infrastructure(background_tasks: BackgroundTasks):
    try:
        terraform_service = TerraformService()
        background_tasks.add_task(terraform_service.apply)
        return {
            "status": "success",
            "message": "Infrastructure creation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/configure")
async def configure_postgresql(background_tasks: BackgroundTasks):
    try:
        ansible_service = AnsibleService()
        background_tasks.add_task(ansible_service.configure)
        return {
            "status": "success",
            "message": "PostgreSQL configuration started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
