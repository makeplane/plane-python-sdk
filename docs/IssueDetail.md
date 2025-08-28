# IssueDetail

Comprehensive work item serializer with full relationship management.  Handles complete work item lifecycle including assignees, labels, validation, and related model updates. Supports dynamic field expansion and HTML content processing.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**assignees** | [**List[UserLite]**](UserLite.md) |  | 
**labels** | [**List[Label]**](Label.md) |  | 
**type_id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**point** | **int** |  | [optional] 
**name** | **str** |  | 
**description_html** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 
**description_binary** | **bytearray** |  | [optional] [readonly] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 
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
from plane.models.issue_detail import IssueDetail

# TODO update the JSON string below
json = "{}"
# create an instance of IssueDetail from a JSON string
issue_detail_instance = IssueDetail.from_json(json)
# print the JSON string representation of the object
print(IssueDetail.to_json())

# convert the object into a dict
issue_detail_dict = issue_detail_instance.to_dict()
# create an instance of IssueDetail from a dict
issue_detail_from_dict = IssueDetail.from_dict(issue_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


