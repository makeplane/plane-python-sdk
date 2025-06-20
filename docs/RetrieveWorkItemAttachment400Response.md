# RetrieveWorkItemAttachment400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Error message | [optional] 
**status** | **bool** | Request status | [optional] 

## Example

```python
from plane.models.retrieve_work_item_attachment400_response import RetrieveWorkItemAttachment400Response

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveWorkItemAttachment400Response from a JSON string
retrieve_work_item_attachment400_response_instance = RetrieveWorkItemAttachment400Response.from_json(json)
# print the JSON string representation of the object
print RetrieveWorkItemAttachment400Response.to_json()

# convert the object into a dict
retrieve_work_item_attachment400_response_dict = retrieve_work_item_attachment400_response_instance.to_dict()
# create an instance of RetrieveWorkItemAttachment400Response from a dict
retrieve_work_item_attachment400_response_from_dict = RetrieveWorkItemAttachment400Response.from_dict(retrieve_work_item_attachment400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


