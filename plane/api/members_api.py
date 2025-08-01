# coding: utf-8

"""
    The Plane REST API

    The Plane REST API  Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

    The version of the API Spec: 0.0.1
    Contact: support@plane.so
    This class is auto generated.

    Do not edit the class manually.
"""  # noqa: E501


import re  # noqa: F401

from pydantic import validate_arguments

from typing_extensions import Annotated
from pydantic import Field, StrictStr

from typing import List

from plane.models.get_workspace_members200_response_inner import GetWorkspaceMembers200ResponseInner
from plane.models.user_lite import UserLite

from plane.api_client import ApiClient
from plane.api_response import ApiResponse
from plane.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class MembersApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def get_project_members(self, project_id : Annotated[StrictStr, Field(..., description="Project ID")], slug : Annotated[StrictStr, Field(..., description="Workspace slug")], **kwargs) -> List[UserLite]:  # noqa: E501
        """List project members  # noqa: E501

        Retrieve all users who are members of the specified project.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_project_members(project_id, slug, async_req=True)
        >>> result = thread.get()

        :param project_id: Project ID (required)
        :type project_id: str
        :param slug: Workspace slug (required)
        :type slug: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: List[UserLite]
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the get_project_members_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.get_project_members_with_http_info(project_id, slug, **kwargs)  # noqa: E501

    @validate_arguments
    def get_project_members_with_http_info(self, project_id : Annotated[StrictStr, Field(..., description="Project ID")], slug : Annotated[StrictStr, Field(..., description="Workspace slug")], **kwargs) -> ApiResponse:  # noqa: E501
        """List project members  # noqa: E501

        Retrieve all users who are members of the specified project.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_project_members_with_http_info(project_id, slug, async_req=True)
        >>> result = thread.get()

        :param project_id: Project ID (required)
        :type project_id: str
        :param slug: Workspace slug (required)
        :type slug: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(List[UserLite], status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'project_id',
            'slug'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_project_members" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['project_id'] is not None:
            _path_params['project_id'] = _params['project_id']

        if _params['slug'] is not None:
            _path_params['slug'] = _params['slug']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['ApiKeyAuthentication', 'OAuth2Authentication', 'OAuth2Authentication']  # noqa: E501

        _response_types_map = {
            '200': "List[UserLite]",
            '401': None,
            '403': None,
            '404': None,
        }

        return self.api_client.call_api(
            '/api/v1/workspaces/{slug}/projects/{project_id}/members/', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_workspace_members(self, slug : Annotated[StrictStr, Field(..., description="Workspace slug")], **kwargs) -> List[GetWorkspaceMembers200ResponseInner]:  # noqa: E501
        """List workspace members  # noqa: E501

        Retrieve all users who are members of the specified workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_workspace_members(slug, async_req=True)
        >>> result = thread.get()

        :param slug: Workspace slug (required)
        :type slug: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: List[GetWorkspaceMembers200ResponseInner]
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the get_workspace_members_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.get_workspace_members_with_http_info(slug, **kwargs)  # noqa: E501

    @validate_arguments
    def get_workspace_members_with_http_info(self, slug : Annotated[StrictStr, Field(..., description="Workspace slug")], **kwargs) -> ApiResponse:  # noqa: E501
        """List workspace members  # noqa: E501

        Retrieve all users who are members of the specified workspace.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_workspace_members_with_http_info(slug, async_req=True)
        >>> result = thread.get()

        :param slug: Workspace slug (required)
        :type slug: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(List[GetWorkspaceMembers200ResponseInner], status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'slug'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_workspace_members" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['slug'] is not None:
            _path_params['slug'] = _params['slug']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['ApiKeyAuthentication', 'OAuth2Authentication', 'OAuth2Authentication']  # noqa: E501

        _response_types_map = {
            '200': "List[GetWorkspaceMembers200ResponseInner]",
            '401': None,
            '403': None,
            '404': None,
        }

        return self.api_client.call_api(
            '/api/v1/workspaces/{slug}/members/', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
