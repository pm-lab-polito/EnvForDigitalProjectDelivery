# Project Management API

Every endpoint and specification is not final, it may change until the development is complete.
For more details about endpoints run FastApi then read the docs at 127.0.0.1/docs

## API Endpoints

| Method | Endpoint | Description | Requires Auth | Requires Perms |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| **POST** |  /register | Register User  | False | False |
| **GET** |  /token | Get Bearer Token | False | False |
| **GET** |  /me | Get current authenticated User | True | False |
| **Projects** |  |  |  |  |
| **GET** |  /projects | Get all projects visible to the current authenticated user | True | True |
| **POST** |  /projects | Create a project (see **[Schemas](#Schemas)** sections) | True | True |
| **GET** |  /projects/**{project_name}** | Get project by name | True | True |
| **DELETE** |  /projects/**{project_name}** | Delete project by name | True | True |
| **POST** |  /projects/**{project_name}**/permissions | Add project permissions | True | True |
| **DELETE** |  /projects/**{project_name}**/permissions | Delete project permissions | True | True |
| **GET** |  /projects/**{project_name}**/permissions/**{user_name}** | Get project permissions for user | True | True |
| **Documents** |  |  |  |  |
| **POST** |  /projects/**{project_name}**/documents | Add document schema to project | True | True |
| **GET** |  /projects/**{project_name}**/documents/**{document_name}** | Get document of project | True | True |
| **PUT** |  /projects/**{project_name}**/documents/**{document_name}** | Insert document content | True | True |
| **PATCH** |  /projects/**{project_name}**/documents/**{document_name}** | Patch document content | True | True |
| **DELETE** |  /projects/**{project_name}**/documents/**{document_name}** | Delete document | True | True |
| **GET** |  /projects/**{project_name}**/documents/**{document_name}**/**{field}**/**{path}**| Get document field, specifying the path | True | True |
| **POST** |  /projects/**{project_name}**/documents/**{document_name}**/last/**{path}**| Create document content at specifyied path | True | True |
| **PUT** |  /projects/**{project_name}**/documents/**{document_name}**/last/**{path}**| Edit document content at specifyied path | True | True |
| **PATCH** |  /projects/**{project_name}**/documents/**{document_name}**/last/**{path}**| Patch document content at specifyied path | True | True |
| **DELETE** |  /projects/**{project_name}**/documents/**{document_name}**/last/**{path}**| Delete document content at specifyied path | True | True |
| **POST** |  /projects/**{project_name}**/documents/**{document_name}**/permissions | Add document permissions | True | True |
| **DELETE** |  /projects/**{project_name}**/documents/**{document_name}**/permissions | Delete document permissions | True | True |
| **GET** |  /projects/**{project_name}**/documents/**{document_name}**/permissions/**{user_name}** | Get document permissions for user | True | True |

## Schemas

### Project POST schema (both YAML/JSON are accepted)
```yaml
# Project name
project_name: example_project
# document schemas
documents:
  # document name
  project_charter:
    # jsonschema of the document
    properties:
      overview: { type: string }
      impact: { type: string }
      organization: { type: string }
    additionalProperties: false
  # other document
  work_breakdown_structure:
    type: array
    items:
      properties:
        code: { type: string }
        name: { type: string }
        description: { type: string }
      additionalProperties: false
processes:
  # process name
  develop_project_charter:
    inputs:
    outputs: [ project_charter ]
  develop_work_breakdown_structure:
    inputs: [ project_charter ]
    outputs: [ work_breakdown_structure ]
permissions:
  # user name
  dogeweb:
    documents:
      project_charter: [ view, edit, delete ]
      work_breakdown_structure: [ view, edit, delete ]
```

### Document POST schema (both YAML/JSON are accepted)
```yaml
project_charter:
    # jsonschema of the document
    properties:
      overview: { type: string }
      impact: { type: string }
      organization: { type: string }
    additionalProperties: false
```

### Document PUT schema
```json
{
  "overview": "Academic research for implementing an environment for digital delivery of projects",
  "impact": "Creation of the environment...",
  "organization": "PoliTo Project Management Lab"
}
```
