# Shared Types

```python
from evrim.types import Profile, Report, Snapshot
```

# Blank

## Profiles

Types:

```python
from evrim.types.blank import BlankProfile
```

Methods:

- <code title="post /prod/blank/profile/">client.blank.profiles.<a href="./src/evrim/resources/blank/profiles.py">create</a>() -> <a href="./src/evrim/types/blank/blank_profile.py">BlankProfile</a></code>

## Templates

Types:

```python
from evrim.types.blank import BlankTemplate
```

Methods:

- <code title="post /prod/blank/template/">client.blank.templates.<a href="./src/evrim/resources/blank/templates.py">create</a>() -> <a href="./src/evrim/types/blank/blank_template.py">BlankTemplate</a></code>

# Bulk

## Collections

### Profiles

Types:

```python
from evrim.types.bulk.collections import BulkProfilesToCollection
```

Methods:

- <code title="post /prod/bulk/collections/profiles/">client.bulk.collections.profiles.<a href="./src/evrim/resources/bulk/collections/profiles.py">create</a>(\*\*<a href="src/evrim/types/bulk/collections/profile_create_params.py">params</a>) -> <a href="./src/evrim/types/bulk/collections/bulk_profiles_to_collection.py">BulkProfilesToCollection</a></code>

## CreatedFields

Types:

```python
from evrim.types.bulk import BulkCreatedField, CreatedFieldListResponse
```

Methods:

- <code title="post /prod/bulk/created-fields/">client.bulk.created_fields.<a href="./src/evrim/resources/bulk/created_fields.py">create</a>(\*\*<a href="src/evrim/types/bulk/created_field_create_params.py">params</a>) -> <a href="./src/evrim/types/bulk/bulk_created_field.py">BulkCreatedField</a></code>
- <code title="get /prod/bulk/created-fields/{id}/">client.bulk.created_fields.<a href="./src/evrim/resources/bulk/created_fields.py">retrieve</a>(id) -> <a href="./src/evrim/types/bulk/bulk_created_field.py">BulkCreatedField</a></code>
- <code title="get /prod/bulk/created-fields/">client.bulk.created_fields.<a href="./src/evrim/resources/bulk/created_fields.py">list</a>() -> <a href="./src/evrim/types/bulk/created_field_list_response.py">CreatedFieldListResponse</a></code>

## Templates

### Profiles

Types:

```python
from evrim.types.bulk.templates import BulkJob, ProfileListResponse
```

Methods:

- <code title="post /prod/bulk/templates/profiles/">client.bulk.templates.profiles.<a href="./src/evrim/resources/bulk/templates/profiles.py">create</a>(\*\*<a href="src/evrim/types/bulk/templates/profile_create_params.py">params</a>) -> <a href="./src/evrim/types/bulk/templates/bulk_job.py">BulkJob</a></code>
- <code title="get /prod/bulk/templates/profiles/{id}/">client.bulk.templates.profiles.<a href="./src/evrim/resources/bulk/templates/profiles.py">retrieve</a>(id) -> <a href="./src/evrim/types/bulk/templates/bulk_job.py">BulkJob</a></code>
- <code title="get /prod/bulk/templates/profiles/">client.bulk.templates.profiles.<a href="./src/evrim/resources/bulk/templates/profiles.py">list</a>() -> <a href="./src/evrim/types/bulk/templates/profile_list_response.py">ProfileListResponse</a></code>

# Collections

Types:

```python
from evrim.types import Collection, CollectionListResponse
```

Methods:

- <code title="post /prod/collections/">client.collections.<a href="./src/evrim/resources/collections.py">create</a>(\*\*<a href="src/evrim/types/collection_create_params.py">params</a>) -> <a href="./src/evrim/types/collection.py">Collection</a></code>
- <code title="get /prod/collections/{id}/">client.collections.<a href="./src/evrim/resources/collections.py">retrieve</a>(id) -> <a href="./src/evrim/types/collection.py">Collection</a></code>
- <code title="patch /prod/collections/{id}/">client.collections.<a href="./src/evrim/resources/collections.py">update</a>(id, \*\*<a href="src/evrim/types/collection_update_params.py">params</a>) -> <a href="./src/evrim/types/collection.py">Collection</a></code>
- <code title="get /prod/collections/">client.collections.<a href="./src/evrim/resources/collections.py">list</a>() -> <a href="./src/evrim/types/collection_list_response.py">CollectionListResponse</a></code>
- <code title="delete /prod/collections/{id}/">client.collections.<a href="./src/evrim/resources/collections.py">delete</a>(id) -> None</code>

# CreatedFields

Types:

```python
from evrim.types import CreatedField, CreatedFieldListResponse
```

Methods:

- <code title="post /prod/created-fields/">client.created_fields.<a href="./src/evrim/resources/created_fields.py">create</a>(\*\*<a href="src/evrim/types/created_field_create_params.py">params</a>) -> <a href="./src/evrim/types/created_field.py">CreatedField</a></code>
- <code title="get /prod/created-fields/{id}/">client.created_fields.<a href="./src/evrim/resources/created_fields.py">retrieve</a>(id) -> <a href="./src/evrim/types/created_field.py">CreatedField</a></code>
- <code title="put /prod/created-fields/{id}/">client.created_fields.<a href="./src/evrim/resources/created_fields.py">update</a>(id, \*\*<a href="src/evrim/types/created_field_update_params.py">params</a>) -> <a href="./src/evrim/types/created_field.py">CreatedField</a></code>
- <code title="get /prod/created-fields/">client.created_fields.<a href="./src/evrim/resources/created_fields.py">list</a>() -> <a href="./src/evrim/types/created_field_list_response.py">CreatedFieldListResponse</a></code>
- <code title="post /prod/created-fields/{field_id}/profile/">client.created_fields.<a href="./src/evrim/resources/created_fields.py">profile</a>(field_id, \*\*<a href="src/evrim/types/created_field_profile_params.py">params</a>) -> None</code>

# Outlines

Types:

```python
from evrim.types import Outline
```

Methods:

- <code title="post /prod/outlines/">client.outlines.<a href="./src/evrim/resources/outlines.py">create</a>(\*\*<a href="src/evrim/types/outline_create_params.py">params</a>) -> <a href="./src/evrim/types/outline.py">Outline</a></code>
- <code title="get /prod/outlines/{id}/">client.outlines.<a href="./src/evrim/resources/outlines.py">retrieve</a>(id) -> <a href="./src/evrim/types/outline.py">Outline</a></code>
- <code title="patch /prod/outlines/{id}/">client.outlines.<a href="./src/evrim/resources/outlines.py">update</a>(id, \*\*<a href="src/evrim/types/outline_update_params.py">params</a>) -> <a href="./src/evrim/types/outline.py">Outline</a></code>
- <code title="delete /prod/outlines/{id}/">client.outlines.<a href="./src/evrim/resources/outlines.py">delete</a>(id) -> None</code>

# Profiles

Types:

```python
from evrim.types import TagProfile, ProfileListResponse
```

Methods:

- <code title="post /prod/profiles/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">create</a>(\*\*<a href="src/evrim/types/profile_create_params.py">params</a>) -> <a href="./src/evrim/types/shared/profile.py">Profile</a></code>
- <code title="get /prod/profiles/{id}/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">retrieve</a>(id) -> <a href="./src/evrim/types/shared/profile.py">Profile</a></code>
- <code title="patch /prod/profiles/{id}/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">update</a>(id, \*\*<a href="src/evrim/types/profile_update_params.py">params</a>) -> <a href="./src/evrim/types/shared/profile.py">Profile</a></code>
- <code title="get /prod/profiles/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">list</a>() -> <a href="./src/evrim/types/profile_list_response.py">ProfileListResponse</a></code>
- <code title="delete /prod/profiles/{id}/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">delete</a>(id) -> None</code>
- <code title="post /prod/profiles/{profile_id}/tag/">client.profiles.<a href="./src/evrim/resources/profiles/profiles.py">tag</a>(profile_id, \*\*<a href="src/evrim/types/profile_tag_params.py">params</a>) -> <a href="./src/evrim/types/tag_profile.py">TagProfile</a></code>

## Collections

Types:

```python
from evrim.types.profiles import ProfileToCollection
```

Methods:

- <code title="post /prod/profiles/{profile_id}/collections/">client.profiles.collections.<a href="./src/evrim/resources/profiles/collections.py">create</a>(profile_id, \*\*<a href="src/evrim/types/profiles/collection_create_params.py">params</a>) -> <a href="./src/evrim/types/profiles/profile_to_collection.py">ProfileToCollection</a></code>

## CreatedFields

Types:

```python
from evrim.types.profiles import CreatedFieldsToProfile
```

Methods:

- <code title="post /prod/profiles/{profile_id}/created-fields/">client.profiles.created_fields.<a href="./src/evrim/resources/profiles/created_fields.py">create</a>(profile_id, \*\*<a href="src/evrim/types/profiles/created_field_create_params.py">params</a>) -> <a href="./src/evrim/types/profiles/created_fields_to_profile.py">CreatedFieldsToProfile</a></code>

## Latest

Types:

```python
from evrim.types.profiles import LatestRetrieveResponse
```

Methods:

- <code title="get /prod/profiles/{profile_id}/latest/">client.profiles.latest.<a href="./src/evrim/resources/profiles/latest.py">retrieve</a>(profile_id) -> <a href="./src/evrim/types/profiles/latest_retrieve_response.py">LatestRetrieveResponse</a></code>

## Reports

Types:

```python
from evrim.types.profiles import ReportListResponse
```

Methods:

- <code title="get /prod/profiles/{profile_id}/reports/">client.profiles.reports.<a href="./src/evrim/resources/profiles/reports.py">list</a>(profile_id) -> <a href="./src/evrim/types/profiles/report_list_response.py">ReportListResponse</a></code>

## Snapshots

Types:

```python
from evrim.types.profiles import CreateProfileSnapshot, SnapshotListResponse
```

Methods:

- <code title="post /prod/profiles/{profile_id}/snapshots/">client.profiles.snapshots.<a href="./src/evrim/resources/profiles/snapshots.py">create</a>(profile_id) -> <a href="./src/evrim/types/profiles/create_profile_snapshot.py">CreateProfileSnapshot</a></code>
- <code title="get /prod/profiles/{profile_id}/snapshots/{snapshot_id}/">client.profiles.snapshots.<a href="./src/evrim/resources/profiles/snapshots.py">retrieve</a>(snapshot_id, \*, profile_id) -> <a href="./src/evrim/types/profiles/create_profile_snapshot.py">CreateProfileSnapshot</a></code>
- <code title="get /prod/profiles/{profile_id}/snapshots/">client.profiles.snapshots.<a href="./src/evrim/resources/profiles/snapshots.py">list</a>(profile_id) -> <a href="./src/evrim/types/profiles/snapshot_list_response.py">SnapshotListResponse</a></code>

# PromptTemplates

Methods:

- <code title="post /prod/prompt-template/">client.prompt_templates.<a href="./src/evrim/resources/prompt_templates.py">create</a>(\*\*<a href="src/evrim/types/prompt_template_create_params.py">params</a>) -> None</code>
- <code title="post /prod/prompt-template/save">client.prompt_templates.<a href="./src/evrim/resources/prompt_templates.py">save</a>(\*\*<a href="src/evrim/types/prompt_template_save_params.py">params</a>) -> None</code>

# ReportsV3

Types:

```python
from evrim.types import ReportsV3ListResponse
```

Methods:

- <code title="post /prod/reports-v3/">client.reports_v3.<a href="./src/evrim/resources/reports_v3.py">create</a>(\*\*<a href="src/evrim/types/reports_v3_create_params.py">params</a>) -> <a href="./src/evrim/types/shared/report.py">Report</a></code>
- <code title="get /prod/reports-v3/{id}/">client.reports_v3.<a href="./src/evrim/resources/reports_v3.py">retrieve</a>(id) -> <a href="./src/evrim/types/shared/report.py">Report</a></code>
- <code title="patch /prod/reports-v3/{id}/">client.reports_v3.<a href="./src/evrim/resources/reports_v3.py">update</a>(id, \*\*<a href="src/evrim/types/reports_v3_update_params.py">params</a>) -> <a href="./src/evrim/types/shared/report.py">Report</a></code>
- <code title="get /prod/reports-v3/">client.reports_v3.<a href="./src/evrim/resources/reports_v3.py">list</a>() -> <a href="./src/evrim/types/reports_v3_list_response.py">ReportsV3ListResponse</a></code>
- <code title="delete /prod/reports-v3/{id}/">client.reports_v3.<a href="./src/evrim/resources/reports_v3.py">delete</a>(id) -> None</code>

# Schemas

Types:

```python
from evrim.types import SchemaRetrieveResponse
```

Methods:

- <code title="get /prod/schema/">client.schemas.<a href="./src/evrim/resources/schemas.py">retrieve</a>(\*\*<a href="src/evrim/types/schema_retrieve_params.py">params</a>) -> <a href="./src/evrim/types/schema_retrieve_response.py">SchemaRetrieveResponse</a></code>

# Snapshots

Types:

```python
from evrim.types import SnapshotListResponse
```

Methods:

- <code title="get /prod/snapshots/{id}/">client.snapshots.<a href="./src/evrim/resources/snapshots.py">retrieve</a>(id) -> <a href="./src/evrim/types/shared/snapshot.py">Snapshot</a></code>
- <code title="get /prod/snapshots/">client.snapshots.<a href="./src/evrim/resources/snapshots.py">list</a>() -> <a href="./src/evrim/types/snapshot_list_response.py">SnapshotListResponse</a></code>

# Tags

Types:

```python
from evrim.types import Tag, TagListResponse
```

Methods:

- <code title="post /prod/tags/">client.tags.<a href="./src/evrim/resources/tags/tags.py">create</a>(\*\*<a href="src/evrim/types/tag_create_params.py">params</a>) -> <a href="./src/evrim/types/tag.py">Tag</a></code>
- <code title="get /prod/tags/{id}/">client.tags.<a href="./src/evrim/resources/tags/tags.py">retrieve</a>(id) -> <a href="./src/evrim/types/tag.py">Tag</a></code>
- <code title="patch /prod/tags/{id}/">client.tags.<a href="./src/evrim/resources/tags/tags.py">update</a>(id, \*\*<a href="src/evrim/types/tag_update_params.py">params</a>) -> <a href="./src/evrim/types/tag.py">Tag</a></code>
- <code title="get /prod/tags/">client.tags.<a href="./src/evrim/resources/tags/tags.py">list</a>() -> <a href="./src/evrim/types/tag_list_response.py">TagListResponse</a></code>
- <code title="delete /prod/tags/{id}/">client.tags.<a href="./src/evrim/resources/tags/tags.py">delete</a>(id) -> None</code>

## Collections

Types:

```python
from evrim.types.tags import TagToCollection
```

Methods:

- <code title="post /prod/tags/{tag_id}/collections/">client.tags.collections.<a href="./src/evrim/resources/tags/collections.py">tag</a>(tag_id, \*\*<a href="src/evrim/types/tags/collection_tag_params.py">params</a>) -> <a href="./src/evrim/types/tags/tag_to_collection.py">TagToCollection</a></code>

## Profiles

Types:

```python
from evrim.types.tags import ProfileListResponse
```

Methods:

- <code title="get /prod/tags/{tag_id}/profiles/">client.tags.profiles.<a href="./src/evrim/resources/tags/profiles.py">list</a>(tag_id) -> <a href="./src/evrim/types/tags/profile_list_response.py">ProfileListResponse</a></code>
- <code title="post /prod/tags/{tag_id}/profiles/">client.tags.profiles.<a href="./src/evrim/resources/tags/profiles.py">tag</a>(tag_id, \*\*<a href="src/evrim/types/tags/profile_tag_params.py">params</a>) -> None</code>

# Templates

Types:

```python
from evrim.types import Template, TemplateListResponse
```

Methods:

- <code title="post /prod/templates/">client.templates.<a href="./src/evrim/resources/templates/templates.py">create</a>(\*\*<a href="src/evrim/types/template_create_params.py">params</a>) -> <a href="./src/evrim/types/template.py">Template</a></code>
- <code title="get /prod/templates/{id}/">client.templates.<a href="./src/evrim/resources/templates/templates.py">retrieve</a>(id) -> <a href="./src/evrim/types/template.py">Template</a></code>
- <code title="patch /prod/templates/{id}/">client.templates.<a href="./src/evrim/resources/templates/templates.py">update</a>(id, \*\*<a href="src/evrim/types/template_update_params.py">params</a>) -> <a href="./src/evrim/types/template.py">Template</a></code>
- <code title="get /prod/templates/">client.templates.<a href="./src/evrim/resources/templates/templates.py">list</a>() -> <a href="./src/evrim/types/template_list_response.py">TemplateListResponse</a></code>
- <code title="delete /prod/templates/{id}/">client.templates.<a href="./src/evrim/resources/templates/templates.py">delete</a>(id) -> None</code>

## Profiles

Types:

```python
from evrim.types.templates import ProfileListResponse
```

Methods:

- <code title="get /prod/templates/{template_id}/profiles/">client.templates.profiles.<a href="./src/evrim/resources/templates/profiles.py">list</a>(template_id) -> <a href="./src/evrim/types/templates/profile_list_response.py">ProfileListResponse</a></code>
