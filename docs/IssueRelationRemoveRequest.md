# IssueRelationRemoveRequest

Serializer for removing issue relations.  Removes existing relationships between work items by specifying the related issue ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**related_issue** | **str** | ID of the related work item to remove relation with | 

## Example

```python
from plane.models.issue_relation_remove_request import IssueRelationRemoveRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRelationRemoveRequest from a JSON string
issue_relation_remove_request_instance = IssueRelationRemoveRequest.from_json(json)
# print the JSON string representation of the object
print(IssueRelationRemoveRequest.to_json())

# convert the object into a dict
issue_relation_remove_request_dict = issue_relation_remove_request_instance.to_dict()
# create an instance of IssueRelationRemoveRequest from a dict
issue_relation_remove_request_from_dict = IssueRelationRemoveRequest.from_dict(issue_relation_remove_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


