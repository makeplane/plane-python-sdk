# PatchedIssueLinkUpdateRequest

Serializer for updating work item external links.  Extends link creation with update-specific validation to prevent URL conflicts and maintain link integrity during modifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_link_update_request import PatchedIssueLinkUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueLinkUpdateRequest from a JSON string
patched_issue_link_update_request_instance = PatchedIssueLinkUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedIssueLinkUpdateRequest.to_json())

# convert the object into a dict
patched_issue_link_update_request_dict = patched_issue_link_update_request_instance.to_dict()
# create an instance of PatchedIssueLinkUpdateRequest from a dict
patched_issue_link_update_request_from_dict = PatchedIssueLinkUpdateRequest.from_dict(patched_issue_link_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


