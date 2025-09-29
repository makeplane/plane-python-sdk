# IssueRelationCreateRequest

Serializer for creating issue relations.  Creates issue relations with the specified relation type and issues. Validates relation types and ensures proper issue ID format.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relation_type** | [**IssueRelationCreateRelationTypeEnum**](IssueRelationCreateRelationTypeEnum.md) | Type of relationship between work items  * &#x60;blocking&#x60; - Blocking * &#x60;blocked_by&#x60; - Blocked By * &#x60;duplicate&#x60; - Duplicate * &#x60;relates_to&#x60; - Relates To * &#x60;start_before&#x60; - Start Before * &#x60;start_after&#x60; - Start After * &#x60;finish_before&#x60; - Finish Before * &#x60;finish_after&#x60; - Finish After | 
**issues** | **List[str]** | Array of work item IDs to create relations with | 

## Example

```python
from plane.models.issue_relation_create_request import IssueRelationCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRelationCreateRequest from a JSON string
issue_relation_create_request_instance = IssueRelationCreateRequest.from_json(json)
# print the JSON string representation of the object
print(IssueRelationCreateRequest.to_json())

# convert the object into a dict
issue_relation_create_request_dict = issue_relation_create_request_instance.to_dict()
# create an instance of IssueRelationCreateRequest from a dict
issue_relation_create_request_from_dict = IssueRelationCreateRequest.from_dict(issue_relation_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


