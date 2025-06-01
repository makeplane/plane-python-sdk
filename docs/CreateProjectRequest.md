# CreateProjectRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Project name | [optional] 
**identifier** | **str** | Project identifier | [optional] 
**description** | **str** | Project description | [optional] 
**project_lead** | **str** | Project lead | [optional] 
**intake_view** | **bool** | Intake view | [optional] 
**module_view** | **bool** | Module view | [optional] 
**cycle_view** | **bool** | Cycle view | [optional] 
**issue_views_view** | **bool** | Issue views view | [optional] 
**page_view** | **bool** | Page view | [optional] 
**network** | **int** | Network | [optional] 

## Example

```python
from plane.models.create_project_request import CreateProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateProjectRequest from a JSON string
create_project_request_instance = CreateProjectRequest.from_json(json)
# print the JSON string representation of the object
print CreateProjectRequest.to_json()

# convert the object into a dict
create_project_request_dict = create_project_request_instance.to_dict()
# create an instance of CreateProjectRequest from a dict
create_project_request_from_dict = CreateProjectRequest.from_dict(create_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


