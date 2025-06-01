# CreateIssueLinkRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 
**title** | **str** |  | 
**metadata** | **object** |  | 

## Example

```python
from plane.models.create_issue_link_request import CreateIssueLinkRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIssueLinkRequest from a JSON string
create_issue_link_request_instance = CreateIssueLinkRequest.from_json(json)
# print the JSON string representation of the object
print CreateIssueLinkRequest.to_json()

# convert the object into a dict
create_issue_link_request_dict = create_issue_link_request_instance.to_dict()
# create an instance of CreateIssueLinkRequest from a dict
create_issue_link_request_from_dict = CreateIssueLinkRequest.from_dict(create_issue_link_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


