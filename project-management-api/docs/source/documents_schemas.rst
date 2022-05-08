Document Schemas
================

This API accepts JSON and YAML schemas to define projects and documents.
Documents fields are user-defined and follow constraints based on a jsonschema the user uploads

**Projects**

All projects must provide an unique name

.. code-block:: yaml

    project_name: example_project

Documents are defined in the "documents" field. A document must have a jsonschema and may have computed fields from other documents or ms project files.
Documents use `jsonschema`_ specifications to enforce content's defined field names and types.
Computed fields use `jsonpath`_ for filtering and selecting content.

.. _jsonschema: https://json-schema.org/
.. _jsonpath: https://github.com/json-path/JsonPath

.. code-block:: yaml

    documents:

      project_charter:
        jsonschema:
          properties:
            overview: { type: string }
            impact: { type: string }
            organization: { type: string }
          additionalProperties: false
        computed_fields:
          scope:
            reference_document: work_breakdown_structure
            jsonpath: $.elements[?(@.level == 1)].name
        ms_computed_fields:
          scope:
            ms_project_name: example
            field_from: tasks
            jsonpath: $[?(@.level < 3)].name

      work_breakdown_structure:
        jsonschema:
          properties:
            elements:
              type: array
              items:
                properties:
                  level: { type: integer }
                  code: { type: string }
                  name: { type: string }
                  description: { type: string }
                additionalProperties: false
            additionalProperties: false

Processes define order constraint for content insertion, checking that all inputs documents have content

.. code-block:: yaml

    processes:

      develop_project_charter:
        inputs:
        outputs: [ project_charter ]

      develop_work_breakdown_structure:
        inputs: [ project_charter ]
        outputs: [ work_breakdown_structure ]

Permissions can be defined for specific users

.. code-block:: yaml

    permissions:

      doge:
        documents:
          project_charter: [ view, edit, delete ]
          work_breakdown_structure: [ view, edit, delete ]


Documents are returned in a fixed schema, in a JSON file
In the document are stored the first and the last content uploaded, and with a system of patches the intermediate edits are recorded.
The patch system is implemented with 'jsonpatch'_

.. _jsonpatch: http://jsonpatch.com/

.. code-block:: json

    {
        "project_name": "example_project",
        "document_name": "project_charter",
        "author_name": "doge",
        "jsonschema": {
            "properties": {
                "overview": {
                    "type": "string"
                },
                "impact": {
                    "type": "string"
                },
                "organization": {
                    "type": "string"
                }
            },
            "additionalProperties": false
        },
        "first": {
            "overview": "Academic research for implementing an environment for digital delivery of projects",
            "impact": "Creation of the environment...",
            "organization": "PoliTo"
        },
        "last": {
            "overview": "Academic research for implementing an environment for digital delivery of projects",
            "impact": "Creation of the environment...",
            "organization": "PoliTo Project Management Lab"
        },
        "creation_date": "2022-04-11T16:05:06.575202",
        "patches": [
            {
                "id": 1,
                "user_name": "doge",
                "updated_date": "2022-04-11T16:05:57.498469",
                "patch": [
                    {
                        "op": "replace",
                        "path": "/organization",
                        "value": "PoliTo Project Management Lab"
                    }
                ]
            }
        ],
        "computed_fields": {
              "scope": [
                  "Task 1",
                  "Task 2"
              ]
        },
        "ms_computed_fields": {
              "scope": [
                  "2018-PMTermProject_BID_baseline",
                  "New production line",
                  ...
              ]
        }
    }