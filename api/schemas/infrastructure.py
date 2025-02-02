from pydantic import BaseModel, Field, constr
from typing import List, Optional

class PostgreSQLConfig(BaseModel):
    postgresql_version: str = Field(..., pattern=r'^\d+(\.\d+)?$')
    instance_type: str = Field(..., pattern=r'^[a-z]+\d+\.[a-z]+$')
    replica_count: int = Field(..., ge=1, le=5)
    max_connections: int = Field(..., ge=100, le=1000)
    shared_buffers: str = Field(..., pattern=r'^\d+[MG]B$')
    vpc_id: str = Field(..., pattern=r'^vpc-[a-f0-9]+$')
    subnet_ids: List[str] = Field(..., min_items=1)
    environment: constr(regex='^(development|staging|production)$')
    key_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "postgresql_version": "14",
                "instance_type": "t3.medium",
                "replica_count": 2,
                "max_connections": 100,
                "shared_buffers": "1GB",
                "vpc_id": "vpc-0646a2c159a57cacc",
                "subnet_ids": ["subnet-02f8c65f9dd60f416", "subnet-0689d9105cd410e26"],
                "environment": "development",
                "key_name": "temp"
            }
        }