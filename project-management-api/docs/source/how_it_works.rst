How it works
============

**Introduction**
This project management api provides the interface to manage projects and their tasks.
It is built on top of the FastApi framework.

**Routers**
Routers modules define the endpoints for the api.
Four routers are defined: main, projects, douments, msprojects

.. code-block:: python

        @router.get('/{path_param}')
        def router(path_param):
            ...

**Dependencies**
This project uses FastApi's dependency injection to perform a series of checks
before executing the request.
The following checks are currently implemented:

* **Authentication check**

The dependency checks if the user is authenticated and returns the associated object.
If the user isn't authenticated, raises a 401 unauthorized http error

.. code-block:: python

    @router.get("/{project_name}")
    def get_project_by_name(user: User = Depends(get_current_active_user))

* **Authorization check and user retrieval**

This dependency checks if the user has the argument permission on the selected resource, if not it raises a 401 unauthorized error

.. code-block:: python

    @router.post("/", dependencies=[Depends(require_project_permission(Permissions.create))])

* **Input validation and retrieval**

It checks that the request body is either a JSON or YAML document, then returns the parsed Dictionary.
If the request body is not valid, it raises a 400 bad request error

.. code-block:: python

    @router.post("/", ...)
    async def add_document_schema_to_project(request_body: Dict = Depends(get_request_body), ...)

* **Resource retrieval**
Resource retrieval methods (get_project, get_document, ...) read the path string and return the resource, raising 404 not found if the resource is not in the database

.. code-block:: python

    @router.get("/{project_name}", ...)
    def get_project_by_name(..., db_project: Project = Depends(get_project)):
        ...


* **Database session retrieval**

Getting the database session from dependencies ensures that all dependencies use the same sessions, enabling object edit compatibility between the various methods

.. code-block:: python

    @router.put("/{document_name}", ...)
    async def put_document_to_project(..., session: Session = Depends(get_session)):

**Models**
`SQLModel`_ is used to define the database structure.
In order to increase code readability, all models have a Fields subclass to associate the field name with its string representation

.. _SQLModel: https://sqlmodel.tiangolo.com

.. code-block:: python

    class Document(SQLModel, table=True):
    # field name   | type | options
    project_name   : str  = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    document_name  : str  = Field(default=None, primary_key=True)
    author_name    : str  = Field(default=None,                   foreign_key=User.Fields.user_name)
    ...

        class Fields(metaclass=StringFields):
            table_name      = "document"
            project_name    = "project_name"
            document_name   = "document_name"
            author_name     = "author_name"
            ...

**Security**
Security has been implemented using bearer token authentication

