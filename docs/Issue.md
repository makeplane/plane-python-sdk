# Issue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**assignees** | **List[str]** |  | [optional] 
**labels** | **List[str]** |  | [optional] 
**type_id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**point** | **int** |  | [optional] 
**name** | **str** |  | 
**description_html** | **str** |  | [optional] 
**description_binary** | **bytearray** |  | [readonly] 
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
**updated_by** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 
**parent** | **str** |  | [optional] 
**state** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from plane.models.issue import Issue

# TODO update the JSON string below
json = "{}"
# create an instance of Issue from a JSON string
issue_instance = Issue.from_json(json)
# print the JSON string representation of the object
print Issue.to_json()

# convert the object into a dict
issue_dict = issue_instance.to_dict()
# create an instance of Issue from a dict
issue_from_dict = Issue.from_dict(issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


