# SearchIssues200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | [**List[SearchIssues200ResponseIssuesInner]**](SearchIssues200ResponseIssuesInner.md) |  | [optional] 

## Example

```python
from plane.models.search_issues200_response import SearchIssues200Response

# TODO update the JSON string below
json = "{}"
# create an instance of SearchIssues200Response from a JSON string
search_issues200_response_instance = SearchIssues200Response.from_json(json)
# print the JSON string representation of the object
print SearchIssues200Response.to_json()

# convert the object into a dict
search_issues200_response_dict = search_issues200_response_instance.to_dict()
# create an instance of SearchIssues200Response from a dict
search_issues200_response_from_dict = SearchIssues200Response.from_dict(search_issues200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


