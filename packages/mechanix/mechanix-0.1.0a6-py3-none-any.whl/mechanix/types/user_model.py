# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["UserModel", "Workspace", "WorkspaceAPIKey", "WorkspaceAPIKeyWorkspace"]


class WorkspaceAPIKeyWorkspace(BaseModel):
    id: str

    created_at: datetime

    deleted_at: Optional[datetime] = None

    display_name: str


class WorkspaceAPIKey(BaseModel):
    id: str

    created_at: datetime

    deactivated_at: Optional[datetime] = None

    key: str

    name: str

    workspace: Optional[WorkspaceAPIKeyWorkspace] = None


class Workspace(BaseModel):
    id: str

    api_keys: Optional[List[WorkspaceAPIKey]] = None

    display_name: str

    joined_at: datetime

    role: str


class UserModel(BaseModel):
    id: str

    email: str

    workspaces: Optional[List[Workspace]] = None
