# IssueRelationResponse

Serializer for issue relations response showing grouped relation types.  Returns issue IDs organized by relation type for efficient client-side processing.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**blocking** | **List[str]** | List of issue IDs that are blocking this issue | 
**blocked_by** | **List[str]** | List of issue IDs that this issue is blocked by | 
**duplicate** | **List[str]** | List of issue IDs that are duplicates of this issue | 
**relates_to** | **List[str]** | List of issue IDs that relate to this issue | 
**start_after** | **List[str]** | List of issue IDs that start after this issue | 
**start_before** | **List[str]** | List of issue IDs that start before this issue | 
**finish_after** | **List[str]** | List of issue IDs that finish after this issue | 
**finish_before** | **List[str]** | List of issue IDs that finish before this issue | 

## Example

```python
from plane.models.issue_relation_response import IssueRelationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRelationResponse from a JSON string
issue_relation_response_instance = IssueRelationResponse.from_json(json)
# print the JSON string representation of the object
print(IssueRelationResponse.to_json())

# convert the object into a dict
issue_relation_response_dict = issue_relation_response_instance.to_dict()
# create an instance of IssueRelationResponse from a dict
issue_relation_response_from_dict = IssueRelationResponse.from_dict(issue_relation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


