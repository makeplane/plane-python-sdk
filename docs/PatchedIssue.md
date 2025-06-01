# PatchedIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**assignees** | **List[str]** |  | [optional] 
**labels** | **List[str]** |  | [optional] 
**type_id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**point** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**description_html** | **str** |  | [optional] 
**description_binary** | **bytearray** |  | [optional] [readonly] 
**priority** | **str** | * &#x60;urgent&#x60; - Urgent * &#x60;high&#x60; - High * &#x60;medium&#x60; - Medium * &#x60;low&#x60; - Low * &#x60;none&#x60; - None | [optional] 
**start_date** | **date** |  | [optional] 
**target_date** | **date** |  | [optional] 
**sequence_id** | **int** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 
**archived_at** | **date** |  | [optional] 
**is_draft** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**parent** | **str** |  | [optional] 
**state** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue import PatchedIssue

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssue from a JSON string
patched_issue_instance = PatchedIssue.from_json(json)
# print the JSON string representation of the object
print PatchedIssue.to_json()

# convert the object into a dict
patched_issue_dict = patched_issue_instance.to_dict()
# create an instance of PatchedIssue from a dict
patched_issue_from_dict = PatchedIssue.from_dict(patched_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


