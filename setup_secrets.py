"""
One-time setup script: creates the Databricks secret scope and stores the
Massive API key. Run this locally (with the Databricks CLI configured) or
from a notebook - never commit the resulting secret value anywhere.

Usage:
    python setup_secrets.py
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
from databricks.sdk.errors import ResourceAlreadyExists
import os

w = WorkspaceClient()

MASSIVE_API_KEY = dbutils.widgets.get("MASSIVE_API_KEY")
LAKEBASE_URL = dbutils.widgets.get("LAKEBASE_URL")

try:
    w.secrets.create_scope(scope="rajeshmassive")
except ResourceAlreadyExists:
    pass

w.secrets.put_secret(
    scope="rajeshmassive",
    key="api-key",
    string_value=MASSIVE_API_KEY
)

try:
    w.secrets.create_scope(scope="rajeshdatabase")
except ResourceAlreadyExists:
    pass

w.secrets.put_secret(
    scope="rajeshdatabase",
    key="lakebase-url",
    string_value=LAKEBASE_URL
)


w.secrets.put_acl(
    scope="rajeshdatabase",
    principal="users",
    permission=workspace.AclPermission.READ,
)

w.secrets.put_acl(
    scope="rajeshmassive",
    principal="users",
    permission=workspace.AclPermission.READ,
)
