import jsonschema
import json

from behave import then
from behave.api.async_step import async_run_until_complete


@then('The result obeys the schema given by "{schema_url}"')
@async_run_until_complete
async def validate_against_schema(context, schema_url):
    """
    Checks that the result stored in `context.result`
    satisfies the schema retrieved from `schema_url`.

    ```gherkin
    Then The result obeys the schema given by "https://domain.example/schema.json"
    ```
    """
    response = await context.session.get(
        schema_url, headers={"accept": "application/json"}
    )
    schema = json.loads(await response.text())

    jsonschema.validate(context.result, schema)


@then('The result has the type "{activity_type}"')
def check_type(context, activity_type):
    """
    Checks that the result stored in `context.result`
    has the `type` property given by `activity_type`.

    ```gherkin
    Then The result has the type "Follow"
    ```
    """
    assert context.result.get("type") == activity_type
