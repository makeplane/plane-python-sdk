# IssueLinkCreateRequest

Serializer for creating work item external links with validation.  Handles URL validation, format checking, and duplicate prevention for attaching external resources to work items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 

## Example

```python
from plane.models.issue_link_create_request import IssueLinkCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueLinkCreateRequest from a JSON string
issue_link_create_request_instance = IssueLinkCreateRequest.from_json(json)
# print the JSON string representation of the object
print(IssueLinkCreateRequest.to_json())

# convert the object into a dict
issue_link_create_request_dict = issue_link_create_request_instance.to_dict()
# create an instance of IssueLinkCreateRequest from a dict
issue_link_create_request_from_dict = IssueLinkCreateRequest.from_dict(issue_link_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


