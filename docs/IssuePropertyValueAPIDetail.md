# IssuePropertyValueAPIDetail

Serializer for aggregated issue property values response. This serializer handles the response format from the query_annotator method which returns property_id and values (ArrayAgg of property values).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**property_id** | **str** | The ID of the issue property | 
**values** | **List[str]** | List of aggregated property values for the given property | 

## Example

```python
from plane.models.issue_property_value_api_detail import IssuePropertyValueAPIDetail

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyValueAPIDetail from a JSON string
issue_property_value_api_detail_instance = IssuePropertyValueAPIDetail.from_json(json)
# print the JSON string representation of the object
print IssuePropertyValueAPIDetail.to_json()

# convert the object into a dict
issue_property_value_api_detail_dict = issue_property_value_api_detail_instance.to_dict()
# create an instance of IssuePropertyValueAPIDetail from a dict
issue_property_value_api_detail_from_dict = IssuePropertyValueAPIDetail.from_dict(issue_property_value_api_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


