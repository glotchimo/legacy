# satellite-spy (Competitive Intelligence)

satellite-spy was a Django microservice, operable via a REST API, that powered the first iteration of the SmartSpy app. It provided a full data model and dynamic API that enabled collection and management of competitive intelligence data.

## Understanding the Dynamic API

First of all, we need to break down the _data model_. The data model is what the database of the platform looks like. Here's a list of all the current objects (tables) and their purposes.

| Name       | Description                                                                                                                                                                                                                  |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Competitor | This is the primary object used, and is typically an ultimate parent. It stores high-level data about a given competitor, and serves as a parent for more detailed objects.                                                  |
| Advantage  | Models the SmartAdvantage concept, consisting primarily of a `name` field, being the given advantage, and a `script` field, being a brief quote of how to address the advantage, is the child of a `Competitor`.             |
| Objection  | Is like `Advantage`, but for potential objections from the given competitor, is the child of a `Competitor`.                                                                                                                 |
| Resource   | Allows the connection or storage of an internal resource, from PDFs to decks to spreadsheets, is the child of a `Competitor`. Note that while it's built to allow file upload, the S3 protocol is not currently operational. |
| Insight    | Is like `Resource` but only allows linking of external articles, studies, and other bits of intel, is the child of a `Competitor`.                                                                                           |
| Comment    | Other than meta, has a `content` field and must be the child of an `Insight`.                                                                                                                                                |
| Page       | Stores HTML data from collected pages, is the child of a `Competitor`.                                                                                                                                                       |

Now that we know what the data model looks like, we can start using the dynamic API. This API uses dynamic paths to allow for quick scaling and easy access. All the paths look the same, except for directives. Here's the URL format for all CRUD endpoints:

    Base: https://e.satellites.smartian.space/api

    To get (GET): /<str:model_name>
    To create (POST): /<str:model_name>/create
    To update (POST): /<str:model_name>/<str:id>/update
    To delete (DELETE): /<str:model_name>/<str:id>/delete

So, for example, if I wanted to get and then update a Competitor with the ID of `abc123`, here's what my requests would look like:

    GET https://e.satellites.smartian.space/api/Competitor?id=abc123

    POST https://e.satellites.smartian.space/api/Competitor/abc123/update
    Content-Type: application/json
    Body: {"name": "My Competitor"}

This schema works for any of the objects listed above. All responses are in JSON format, and all data being posted should be in JSON format.
