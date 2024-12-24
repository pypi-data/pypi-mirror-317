import dbm
import pluggy
from typing import TypedDict, Literal

hookspec = pluggy.HookspecMarker("hubapi")
hookimpl = pluggy.HookimplMarker("hubapi")


class Person(TypedDict):
    username: str
    email: str
    password_hash: str
    is_admin: bool
    
class Project(TypedDict):
    uuid: str
    name: str
    annotation_type: str
    
class ProjectMembership(TypedDict):
    project_uuid: str
    person_username: str
    role: str
    
class ImageAnnotation(TypedDict):
    uuid: str
    project_uuid: str
    annotation_json: dict
    image_url: str
    state: str
    annotated_at: str
    annotated_by_uuid: str
    train_val_test: str
    
class Credential(TypedDict):
    key: str
    value: str
    team_uuid: str
    credential_type: str
    added_at: str
    status: str

@hookspec
def insert_credentials(credential: Credential):
    """Insert credentials into the database."""

@hookspec
def delete_credentials(key: str):
    """Delete credentials from the database."""


class MemoryPlugin:
    @hookimpl
    def insert_credentials(self, credential: Credential):
        with dbm.open('credentials', 'c') as db:
            db[credential['key']] = credential['value']
        return f"Inserted {credential['key']}"

    @hookimpl
    def delete_credentials(self, key: str):
        with dbm.open('credentials', 'c') as db:
            if key in db:
                del db[key]
                return f"Deleted {key}"
            else:
                return f"Key {key} not found"

pm = pluggy.PluginManager("hubapi")
pm.add_hookspecs(sys.modules[__name__])
pm.register(HubAPIPlugin())

def insert_credentials(credential: Credential):
    return pm.hook.insert_credentials(credential=credential)

def delete_credentials(key: str):
    return pm.hook.delete_credentials(key=key)