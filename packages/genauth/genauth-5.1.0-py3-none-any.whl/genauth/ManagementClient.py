# coding: utf-8
import json

from .http.ManagementHttpClient import ManagementHttpClient
from .utils.signatureComposer import getAuthorization
from .utils.wss import handleMessage


class ManagementClient(object):
    """GenAuth Management Client"""

    def __init__(
            self,
            access_key_id,
            access_key_secret,
            host=None,
            timeout=10.0,
            lang=None,
            use_unverified_ssl=False,
            websocket_host=None,
            websocket_endpoint=None
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.host = host or "https://api.genauth.ai"
        self.timeout = timeout
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl
        self.websocket_host = websocket_host or "wss://events.genauth.ai"
        self.websocket_endpoint = websocket_endpoint or "/events/v1/management/sub"
        self.http_client = ManagementHttpClient(
            host=self.host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
        )

    def list_row(self, model_id, keywords=None, conjunction=None, conditions=None, sort=None, page=None, limit=None,
                 fetch_all=None, with_path=None, show_field_id=None, preview_relation=None,
                 get_relation_field_detail=None, scope=None, filter_relation=None, expand=None):
        """Advanced Search for Data Objects

        Advanced Search for Data Objects

        Attributes:
            model_id (str): Function id
            keywords (str): Keywords
            conjunction (str): The relationship between multiple search conditions:
    - and: and
    - or: or
    
            conditions (list): Search conditions
            sort (list): Sort conditions
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            fetch_all (bool): Whether to return all without pagination (only supports scenarios where child nodes of tree structures are retrieved)
            with_path (bool): Whether to return the full path of the node (only supports scenarios where child nodes of tree structures are retrieved)
            show_field_id (bool): Whether to use field id as key in the return result
            preview_relation (bool): Whether to include a preview of related data in the return result (first three)
            get_relation_field_detail (bool): Whether to return detailed user information of related data, currently only supports users.
            scope (dict): Limit the search scope to parts related to a certain function
            filter_relation (dict): Filter specific related data
            expand (list): Get detailed fields of corresponding related data
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/filter',
            json={
                'modelId': model_id,
                'keywords': keywords,
                'conjunction': conjunction,
                'conditions': conditions,
                'sort': sort,
                'page': page,
                'limit': limit,
                'fetchAll': fetch_all,
                'withPath': with_path,
                'showFieldId': show_field_id,
                'previewRelation': preview_relation,
                'getRelationFieldDetail': get_relation_field_detail,
                'scope': scope,
                'filterRelation': filter_relation,
                'expand': expand,
            },
        )

    def get_row(self, model_id, row_id, show_field_id):
        """Get Data Object Row Information

        Get Data Object Row Information

        Attributes:
            modelId (str): Function id
            rowId (str): Row id
            showFieldId (str): Whether to use field id as key in the return result
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row',
            params={
                'modelId': model_id,
                'rowId': row_id,
                'showFieldId': show_field_id,
            },
        )

    def get_row_by_value(self, model_id, key, value, show_field_id):
        """Get Data Object Row Information by Value

        Get Data Object Row Information by Value, only allows precise queries through unique fields.

        Attributes:
            modelId (str): Function id
            key (str): Field key
            value (str): Field value
            showFieldId (str): Whether to use field id as key in the return result
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row-by-value',
            params={
                'modelId': model_id,
                'key': key,
                'value': value,
                'showFieldId': show_field_id,
            },
        )

    def get_row_batch(self, row_ids, model_id):
        """Batch Get Row Information

        Batch Get Row Information

        Attributes:
            row_ids (list): List of row ids
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/get-row-batch',
            json={
                'rowIds': row_ids,
                'modelId': model_id,
            },
        )

    def create_row(self, data, model_id, row_id=None):
        """Add Row

        Add Row

        Attributes:
            data (dict): Data content
            model_id (str): Function id
            row_id (str): Custom row id, default is automatically generated. The maximum length is only allowed to be 32.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-row',
            json={
                'data': data,
                'modelId': model_id,
                'rowId': row_id,
            },
        )

    def update_row(self, data, row_id, model_id, show_field_id=None):
        """Update Row

        Update Row

        Attributes:
            data (dict): Data content
            row_id (str): Row id
            model_id (str): Function id
            show_field_id (bool): Whether the key in the response is FieldId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-row',
            json={
                'data': data,
                'rowId': row_id,
                'modelId': model_id,
                'showFieldId': show_field_id,
            },
        )

    def remove_row(self, row_id_list, model_id, recursive=None):
        """Delete Row

        Delete Row

        Attributes:
            row_id_list (list): List of row ids
            model_id (str): Function id
            recursive (bool): If the current row has child nodes, whether to recursively delete, default is false. When false, if there are child nodes, an error will be prompted.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-row',
            json={
                'rowIdList': row_id_list,
                'modelId': model_id,
                'recursive': recursive,
            },
        )

    def create_model(self, parent_key, enable, type, description, name, data_type=None):
        """Create Data Object

        Create a custom data object using this interface, defining the basic information of the data object

        Attributes:
            parent_key (str): Parent menu
            enable (bool): Whether the function is enabled:
    - true: Enabled
    - false: Not enabled
    
            type (str): Function type:
    - user: User
    - post: Post
    - group: Group
    - ueba: Ueba
    - organization: Organization
    - device: Device
    - custom: Custom
    
            description (str): Function description
            name (str): Function name
            data_type (str): Data type:
    - list: List type data
    - tree: Tree-structured data
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-model',
            json={
                'parentKey': parent_key,
                'enable': enable,
                'type': type,
                'description': description,
                'name': name,
                'dataType': data_type,
            },
        )

    def get_model(self, id):
        """Get Data Object Details

        Get detailed information of the data object using the function id

        Attributes:
            id (str): Function id can be obtained from the console page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-model',
            params={
                'id': id,
            },
        )

    def list_model(self, ):
        """Get Data Object List

        Get Data Object List

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-model',
        )

    def remove_model(self, id):
        """Delete Data Object

        Delete the corresponding data object based on the requested function id

        Attributes:
            id (str): Function id can be obtained from the console page
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-model',
            json={
                'id': id,
            },
        )

    def update_model(self, config, field_order, type, parent_key, enable, description, name, id):
        """Update Data Object

        Update the information of the data object corresponding to the requested function id

        Attributes:
            config (dict): Details page configuration
            field_order (str): Field order
            type (str): Function type
            parent_key (str): Parent menu
            enable (bool): Whether the function is enabled
            description (str): Function description
            name (str): Function name
            id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-model',
            json={
                'config': config,
                'fieldOrder': field_order,
                'type': type,
                'parentKey': parent_key,
                'enable': enable,
                'description': description,
                'name': name,
                'id': id,
            },
        )

    def create_field(self, user_visible, relation_optional_range, relation_show_key, relation_multiple, relation_type,
                     for_login, fuzzy_search, drop_down, format, regexp, min, max, max_length, unique, require, default,
                     help, editable, show, type, key, name, model_id):
        """Create field of data object

        Create the field of related data object, configure the field information and basic validation rules

        Attributes:
            user_visible (bool): Whether the user center is displayed, only meaningful under the user module:
    - true: User center display
    - false: User center does not display
    
            relation_optional_range (dict): Optional range of related data
            relation_show_key (str): The property to be displayed for related data
            relation_multiple (bool): Whether the relationship is 1-N:
    - true: It is a 1-N relationship
    - false: It is not a 1-N relationship
    
            relation_type (str): Type of relationship
            for_login (bool): Whether it can be used for login, only meaningful under the user module:
    - true: Used for login
    - false: Not used for login
    
            fuzzy_search (bool): Whether fuzzy search is supported:
    - true: Supports fuzzy search
    - false: Does not support fuzzy search
    
            drop_down (dict): Drop-down menu options
            format (int): Front-end formatting display rules:
            regexp (str): String validation matching rules
            min (int): If the type is a number, it represents the lower limit of the number. If the type is a date, it represents the start date
            max (int): If the type is a number, it represents the upper limit of the number. If the type is a date, it represents the end date
            max_length (int): String length limit
            unique (bool): Whether it is unique:
    - true: Unique
    - false: Not unique
    
            require (bool): Whether it is required:
    - true: Required
    - false: Not required
    
            default (dict): Default value
            help (str): Help description
            editable (bool): Whether it is editable:
    - true: Editable
    - false: Not editable
    
            show (bool): Whether to display:
    - true: Display
    - false: Do not display
    
            type (str): Field type:
    - 1: Single-line text
    - 2: Multi-line text
    - 3: Number
    - 4: Boolean type
    - 5: Date
    - 6: Enumeration
    - 7: Related type
    - 8: Reverse related data display
    
            key (str): Field attribute name
            name (str): Field name
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-field',
            json={
                'userVisible': user_visible,
                'relationOptionalRange': relation_optional_range,
                'relationShowKey': relation_show_key,
                'relationMultiple': relation_multiple,
                'relationType': relation_type,
                'forLogin': for_login,
                'fuzzySearch': fuzzy_search,
                'dropDown': drop_down,
                'format': format,
                'regexp': regexp,
                'min': min,
                'max': max,
                'maxLength': max_length,
                'unique': unique,
                'require': require,
                'default': default,
                'help': help,
                'editable': editable,
                'show': show,
                'type': type,
                'key': key,
                'name': name,
                'modelId': model_id,
            },
        )

    def update_field(self, user_visible, relation_optional_range, relation_show_key, for_login, fuzzy_search, drop_down,
                     format, regexp, min, max, max_length, unique, require, default, help, editable, show, name,
                     model_id, id):
        """Update field of data object

        Update the field information and basic validation rules of the related data object

        Attributes:
            user_visible (bool): Whether the user center is displayed, only meaningful under the user module:
    - true: User center display
    - false: User center does not display
    
            relation_optional_range (dict): Optional range of related data
            relation_show_key (str): The property to be displayed for related data
            for_login (bool): Whether it can be used for login, only meaningful under the user module:
    - true: Used for login
    - false: Not used for login
    
            fuzzy_search (bool): Whether fuzzy search is supported:
    - true: Supports fuzzy search
    - false: Does not support fuzzy search
    
            drop_down (list): Drop-down menu options
            format (int): Front-end formatting rules
            regexp (str): String validation matching rules
            min (int): If the type is a number, it represents the lower limit of the number. If the type is a date, it represents the start date
            max (int): If the type is a number, it represents the upper limit of the number. If the type is a date, it represents the end date
            max_length (int): String length limit
            unique (bool): Whether it is unique:
    - true: Unique
    - false: Not unique
    
            require (bool): Whether it is required:
    - true: Required
    - false: Not required
    
            default (dict): Default value
            help (str): Help description
            editable (bool): Whether it is editable:
    - true: Editable
    - false: Not editable
    
            show (bool): Whether to display:
    - true: Display
    - false: Do not display
    
            name (str): Field name
            model_id (str): Function id
            id (str): Field id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-field',
            json={
                'userVisible': user_visible,
                'relationOptionalRange': relation_optional_range,
                'relationShowKey': relation_show_key,
                'forLogin': for_login,
                'fuzzySearch': fuzzy_search,
                'dropDown': drop_down,
                'format': format,
                'regexp': regexp,
                'min': min,
                'max': max,
                'maxLength': max_length,
                'unique': unique,
                'require': require,
                'default': default,
                'help': help,
                'editable': editable,
                'show': show,
                'name': name,
                'modelId': model_id,
                'id': id,
            },
        )

    def remote_field(self, model_id, id):
        """Remove field of data object

        Remove the corresponding field based on the requested field id and function id

        Attributes:
            model_id (str): Function id
            id (str): Field id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-field',
            json={
                'modelId': model_id,
                'id': id,
            },
        )

    def list_field(self, model_id):
        """Get the field list of data object

        Get the field list of data object

        Attributes:
            modelId (str): Function id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-field',
            params={
                'modelId': model_id,
            },
        )

    def export_meatdata(self, id_list, model_id):
        """Export all data

        Export all data

        Attributes:
            id_list (list): Export range
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/export',
            json={
                'idList': id_list,
                'modelId': model_id,
            },
        )

    def import_metadata(self, file, model_id):
        """Import data

        Import data

        Attributes:
            file (str): Import the excel file address
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/import',
            json={
                'file': file,
                'modelId': model_id,
            },
        )

    def get_import_template(self, model_id):
        """Get import template

        Get import template

        Attributes:
            modelId (str): Function id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-import-template',
            params={
                'modelId': model_id,
            },
        )

    def create_operate(self, show, icon, config, operate_name, operate_key, model_id):
        """Create custom operation

        Create custom operation

        Attributes:
            show (bool): Whether to display:
    - true: Display
    - true: Do not display
    
            icon (str): Icon
            config (dict): Operation configuration
            operate_name (str): Operation name
            operate_key (str): Operation type:
    - openPage: Open a web page
    
            model_id (str): modelId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-operate',
            json={
                'show': show,
                'icon': icon,
                'config': config,
                'operateName': operate_name,
                'operateKey': operate_key,
                'modelId': model_id,
            },
        )

    def remove_operate(self, custom_config, model_id, id):
        """Remove custom operation

        Remove custom operation

        Attributes:
            custom_config (dict): Custom parameters at execution time
            model_id (str): Function id
            id (str): Custom operation id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def execute_operate(self, custom_config, model_id, id):
        """Execute custom operation

        Execute custom operation

        Attributes:
            custom_config (dict): Custom parameters at execution time
            model_id (str): Function id
            id (str): Custom operation id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/execute-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def copy_operate(self, custom_config, model_id, id):
        """Copy custom operation

        Copy custom operation

        Attributes:
            custom_config (dict): Custom parameters at execution time
            model_id (str): Function id
            id (str): Custom operation id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/copy-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def list_operate(self, model_id, keywords=None, page=None, limit=None):
        """Operation management list (paging)

        Operation management list (paging)

        Attributes:
            modelId (str): model Id
            keywords (str): Search function name
            page (int): Current page number, starting from 1
            limit (int): Number of pages, the maximum cannot exceed 50, the default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-operate',
            params={
                'keywords': keywords,
                'modelId': model_id,
                'page': page,
                'limit': limit,
            },
        )

    def list_operate_all(self, model_id):
        """All operation management list

        All operation management list

        Attributes:
            modelId (str): model Id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/all-operate',
            params={
                'modelId': model_id,
            },
        )

    def update_operate(self, icon, config, operate_name, operate_key, show, model_id, id):
        """Update operation management

        Update operation management

        Attributes:
            icon (str): Icon
            config (dict): Operation configuration
            operate_name (str): Operation name
            operate_key (str): Operation Key value
            show (bool): Whether to display:
    - true: Display
    - true: Do not display
    
            model_id (str): modelId
            id (str): id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-operate',
            json={
                'icon': icon,
                'config': config,
                'operateName': operate_name,
                'operateKey': operate_key,
                'show': show,
                'modelId': model_id,
                'id': id,
            },
        )

    def get_relation_info(self, id_list, model_id):
        """Get relation data details

        Get relation data details

        Attributes:
            id_list (list): Relation id list
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/get-relation-info',
            json={
                'idList': id_list,
                'modelId': model_id,
            },
        )

    def create_row_relation(self, value_list, row_id, field_id, model_id):
        """Create row relation data

        Create row relation data

        Attributes:
            value_list (list): Related data
            row_id (str): Row id
            field_id (str): Field id
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-row-relation',
            json={
                'valueList': value_list,
                'rowId': row_id,
                'fieldId': field_id,
                'modelId': model_id,
            },
        )

    def get_relation_value(self, model_id, field_id, row_id, page=None, limit=None):
        """Get row relation data

        Get row relation data

        Attributes:
            modelId (str): Function id
            fieldId (str): Field id
            rowId (str): Row id
            page (int): Current page number, starting from 1
            limit (int): Number of pages, the maximum cannot exceed 50, the default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row-relation',
            params={
                'modelId': model_id,
                'fieldId': field_id,
                'rowId': row_id,
                'page': page,
                'limit': limit,
            },
        )

    def remove_relation_value(self, value, field_ids, row_id, model_id):
        """Remove row relation data

        Remove row relation data

        Attributes:
            value (str): Related data
            field_ids (list): Field id
            row_id (str): Row id
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-row-relation',
            json={
                'value': value,
                'fieldIds': field_ids,
                'rowId': row_id,
                'modelId': model_id,
            },
        )

    def export_model(self, model_id):
        """Export data object

        Export data object

        Attributes:
            model_id (str): Function id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/export/model',
            json={
                'modelId': model_id,
            },
        )

    def import_model(self, file):
        """Import data object

        Import data object

        Attributes:
            file (str): Import the json file address
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/import/model',
            json={
                'file': file,
            },
        )

    def capture(self, data, model_id=None):
        """UEBA upload

        UEBA upload

        Attributes:
            data (dict): Data content
            model_id (str): Function id, if it does not exist, the first type found in the database is ueba
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/ueba/capture',
            json={
                'data': data,
                'modelId': model_id,
            },
        )

    def delete_device(self, user_id, id):
        """Remove binding (user details page)

        Remove binding (user details page).

        Attributes:
            user_id (str): User ID
            id (str): Data row id, returned when creating the device `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-device-by-user',
            json={
                'userId': user_id,
                'id': id,
            },
        )

    def suspend_device(self, end_time, user_id, id):
        """Suspend device (user details page)

        Suspend device (user details page).

        Attributes:
            end_time (str): Suspend expiration time, timestamp (milliseconds)
            user_id (str): User ID
            id (str): Data row id, returned when creating the device `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/suspend-device-by-user',
            json={
                'endTime': end_time,
                'userId': user_id,
                'id': id,
            },
        )

    def disable_device(self, id, user_id):
        """Disable device (user details page)

        Disable device (user details page).

        Attributes:
            id (str): Data row id, returned when creating the device `id`
            user_id (str): User ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/disable-device-by-user',
            json={
                'id': id,
                'userId': user_id,
            },
        )

    def enable_device(self, id, user_id):
        """Enable device (user details page)

        Enable device (user details page).

        Attributes:
            id (str): Data row id, returned when creating the device `id`
            user_id (str): User ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enable-device-by-user',
            json={
                'id': id,
                'userId': user_id,
            },
        )

    def get_device_status(self, id):
        """Get device status

        Get device status.

        Attributes:
            id (str): Data row id, returned when creating the device `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/device-status',
            json={
                'id': id,
            },
        )

    def list_public_accounts(self, keywords=None, advanced_filter=None, search_query=None, options=None):
        """Get/search public account list

        This interface is used to get the user list, supports fuzzy search, and filters users through user basic fields, user custom fields, user historical login applications and other dimensions.

        ### Fuzzy search example

        Fuzzy search will default to fuzzy search users from the `phone`, `email`, `name`, `username`, `nickname` five fields, you can also decide the range of fuzzy matching by setting `options.fuzzySearchOn`:

        ```json
        {
          "keywords": "Beijing",
          "options": {
            "fuzzySearchOn": [
              "address"
            ]
          }
        }
        ```

        ### Advanced search example

        You can use `advancedFilter` for advanced search, which supports filtering users through user's basic information, custom data, user source, login application, external identity source information and other dimensions.
        **And these filtering conditions can be combined arbitrarily.**

        #### Filter users with status as disabled

        The user status (`status`) is a string type, optional values are `Activated` and `Suspended`:

        ```json
        {
          "advancedFilter": [
            {
              "field": "status",
              "operator": "EQUAL",
              "value": "Suspended"
            }
          ]
        }
        ```

        #### Filter users whose email contains `@example.com`

        The user's email (`email`) is a string type and can be fuzzy searched:

        ```json
        {
          "advancedFilter": [
            {
              "field": "email",
              "operator": "CONTAINS",
              "value": "@example.com"
            }
          ]
        }
        ```

        #### Search based on any extension field of the user

        ```json
        {
          "advancedFilter": [
            {
              "field": "some-custom-key",
              "operator": "EQUAL",
              "value": "some-value"
            }
          ]
        }
        ```

        #### Filter users by login count

        Filter users with more than 10 logins:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "GREATER",
              "value": 10
            }
          ]
        }
        ```

        Filter users with 10 - 100 logins:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "BETWEEN",
              "value": [10, 100]
            }
          ]
        }
        ```

        #### Filter users by last login time

        Filter users who logged in within the last 7 days:

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLoginTime",
              "operator": "GREATER",
              "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
            }
          ]
        }
        ```

        Filter users who logged in within a certain period of time:

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLogin",
              "operator": "BETWEEN",
              "value": [
                Date.now() - 14 * 24 * 60 * 60 * 1000,
                Date.now() - 7 * 24 * 60 * 60 * 1000
              ]
            }
          ]
        }
        ```

        #### Filter users by the application they have logged in to

        Filter out users who have logged in to application `appId1` or `appId2`:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loggedInApps",
              "operator": "IN",
              "value": [
                "appId1",
                "appId2"
              ]
            }
          ]
        }
        ```

        Attributes:
            keywords (str): Fuzzy search keyword
            advanced_filter (list): Advanced search
            search_query (dict): Execute search command using ES query statement
            options (dict): Optional
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-public-accounts',
            json={
                'keywords': keywords,
                'advancedFilter': advanced_filter,
                'searchQuery': search_query,
                'options': options,
            },
        )

    def get_public_account(self, user_id, user_id_type=None, with_custom_data=None):
        """Get public account information

        Get public account details by public account user ID, can choose to get custom data, select specific user ID type, etc.

        Attributes:
            user_id (str): Public account user ID
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: User name
- `external_id`: User's ID in the external system, corresponding to the `externalId` field of GenAuth user information

            with_custom_data (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
            },
        )

    def get_public_account_batch(self, user_ids, user_id_type=None, with_custom_data=None):
        """Batch get public account information

        Batch get public account information by public account user ID list, can choose to get custom data, select specific user ID type, etc.

        Attributes:
            userIds (str): Public account user ID array
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: User name
- `external_id`: User's ID in the external system, corresponding to the `externalId` field of GenAuth user information

            with_custom_data (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-account-batch',
            params={
                'userIds': user_ids,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
            },
        )

    def create_public_account(self, status=None, email=None, phone=None, phone_country_code=None, username=None,
                              external_id=None, name=None, nickname=None, photo=None, gender=None, email_verified=None,
                              phone_verified=None, birthdate=None, country=None, province=None, city=None, address=None,
                              street_address=None, postal_code=None, company=None, browser=None, device=None,
                              given_name=None, family_name=None, middle_name=None, profile=None,
                              preferred_username=None, website=None, zoneinfo=None, locale=None, formatted=None,
                              region=None, password=None, salt=None, otp=None, custom_data=None,
                              identity_number=None, options=None):
        """Create public account

        Create public account, email, phone, username must contain at least one, email, phone, username, externalId must be unique within the user pool, this interface will create a public account user as an administrator, so there is no need to perform security checks such as phone number verification.

        Attributes:
            status (str): Current account status
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it is a foreign phone number, please specify the area code in the phoneCountryCode parameter.
            phone_country_code (str): Phone area code, China mainland phone number can be left blank. GenAuth SMS service does not currently support international phone numbers, you need to configure the corresponding international SMS service in the GenAuth console. The complete list of phone area codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
            username (str): Username, unique within the user pool
            external_id (str): Third-party external ID
            name (str): User's real name, not unique
            nickname (str): Nickname
            photo (str): Avatar link
            gender (str): Gender
            email_verified (bool): Whether the email is verified
            phone_verified (bool): Whether the phone number is verified
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            company (str): Company
            browser (str): The browser UA used in the last login
            device (str): The device used in the last login
            given_name (str): Given name
            family_name (str): Family name
            middle_name (str): Middle name
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): User's personal website
            zoneinfo (str): User's time zone information
            locale (str): Locale
            formatted (str): Standard full address
            region (str): User's region
            password (str): User's password, default is plaintext. We use HTTPS protocol to securely transmit the password, which can ensure security to a certain extent. If you need a higher level of security, we also support two ways to encrypt the password, RSA256 and national standard SM2. See the `passwordEncryptType` parameter for details.
            salt (str): Salt for encrypting user passwords
            otp (dict): OTP validator for public accounts
            custom_data (dict): Custom data, the key in the passed-in object must first be defined in the user pool for the relevant custom field
            identity_number (str): User's ID card number
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-public-account',
            json={
                'status': status,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'externalId': external_id,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'gender': gender,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'password': password,
                'salt': salt,
                'otp': otp,
                'customData': custom_data,
                'identityNumber': identity_number,
                'options': options,
            },
        )

    def create_public_accounts_batch(self, list, options=None):
        """Batch create public accounts

        Batch create public accounts, email, phone, username must contain at least one, email, phone, username, externalId must be unique within the user pool, this interface will create a public account user as an administrator, so there is no need to perform security checks such as phone number verification.

        Attributes:
            list (list): List of public accounts
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-public-accounts-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def update_public_account(self, user_id, phone_country_code=None, name=None, nickname=None, photo=None,
                              external_id=None, status=None, email_verified=None, phone_verified=None, birthdate=None,
                              country=None, province=None, city=None, address=None, street_address=None,
                              postal_code=None, gender=None, username=None, email=None, phone=None, password=None,
                              company=None, browser=None, device=None, given_name=None, family_name=None,
                              middle_name=None, profile=None, preferred_username=None, website=None, zoneinfo=None,
                              locale=None, formatted=None, region=None, identity_number=None, custom_data=None,
                              options=None):
        """Modify public account information

        Modify public account information by public account user ID, email, phone, username, externalId must be unique within the user pool, this interface will modify public account information as an administrator, so there is no need to perform security checks such as phone number verification.

        Attributes:
            user_id (str): User unique identifier, can be user ID, username, email, phone, external ID, ID in the external identity source.
            phone_country_code (str): Phone area code, China mainland phone number can be left blank. GenAuth SMS service does not currently support international phone numbers, you need to configure the corresponding international SMS service in the GenAuth console. The complete list of phone area codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
            name (str): User's real name, not unique
            nickname (str): Nickname
            photo (str): Avatar link
            external_id (str): Third-party external ID
            status (str): Current account status
            email_verified (bool): Whether the email is verified
            phone_verified (bool): Whether the phone number is verified
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            gender (str): Gender
            username (str): Username, unique within the user pool
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it is a foreign phone number, please specify the area code in the phoneCountryCode parameter.
            password (str): User's password, default is plaintext. We use HTTPS protocol to securely transmit the password, which can ensure security to a certain extent. If you need a higher level of security, we also support two ways to encrypt the password, RSA256 and national standard SM2. See the `passwordEncryptType` parameter for details.
            company (str): Company
            browser (str): The browser UA used in the last login
            device (str): The device used in the last login
            given_name (str): Given name
            family_name (str): Family name
            middle_name (str): Middle name
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): User's personal website
            zoneinfo (str): User's time zone information
            locale (str): Locale
            formatted (str): Standard full address
            region (str): User's region
            identity_number (str): User's ID card number
            custom_data (dict): Custom data, the key in the passed-in object must first be defined in the user pool for the relevant custom field
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-public-account',
            json={
                'userId': user_id,
                'phoneCountryCode': phone_country_code,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'status': status,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'email': email,
                'phone': phone,
                'password': password,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'identityNumber': identity_number,
                'customData': custom_data,
                'options': options,
            },
        )

    def update_public_account_batch(self, list, options=None):
        """Batch modify public account information

        Batch modify public account information, email, phone, username, externalId must be unique within the user pool, this interface will modify public account information as an administrator, so there is no need to perform security checks such as phone number verification.

        Attributes:
            list (list): List of public accounts
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-public-account-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def delete_public_accounts_batch(self, user_ids, options=None):
        """Batch delete public accounts

        Delete public accounts by public account ID list, support batch deletion, can choose to specify user ID type, etc.

        Attributes:
            user_ids (list): Public account user ID list
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-public-accounts-batch',
            json={
                'userIds': user_ids,
                'options': options,
            },
        )

    def kick_public_accounts(self, app_ids, user_id, options=None):
        """Force logout public accounts

        Force public accounts to log out by public account ID and App ID list, can choose to specify public account ID type, etc.

        Attributes:
            app_ids (list): APP ID list
            user_id (str): Public account ID
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/kick-public-accounts',
            json={
                'appIds': app_ids,
                'userId': user_id,
                'options': options,
            },
        )

    def change_into_public_account(self, user_id):
        """Convert personal account to public account

        Convert personal account to public account by user ID.

        Attributes:
            user_id (str): Public account rowId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/transfer-into-public-account',
            json={
                'userId': user_id,
            },
        )

    def get_public_accounts_of_user(self, user_id):
        """Get the public account list of the user

        Get the public account list of the user by user ID.

        Attributes:
            userId (str): User ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-user',
            params={
                'userId': user_id,
            },
        )

    def get_users_of_public_account(self, public_account_id):
        """User list of public account

        Get the user list by public account ID.

        Attributes:
            publicAccountId (str): Public account ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-users-of-public-account',
            params={
                'publicAccountId': public_account_id,
            },
        )

    def bind_users_public_account(self, public_account_id, user_ids):
        """Bind multiple users with public account

        Bind multiple users with public account

        Attributes:
            public_account_id (str): User unique identifier, can be user ID, username, email, phone, external ID, ID in the external identity source.
            user_ids (list): User ID array
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-users',
            json={
                'publicAccountId': public_account_id,
                'userIds': user_ids,
            },
        )

    def setuser_of_public_account(self, user_id, public_account_ids):
        """Bind multiple public accounts with user

        Bind multiple public accounts with user

        Attributes:
            user_id (str): User unique identifier, can be user ID, username, email, phone, external ID, ID in the external identity source.
            public_account_ids (list): User ID array
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-of-public-accounts',
            json={
                'userId': user_id,
                'publicAccountIds': public_account_ids,
            },
        )

    def unbind_users_public_account(self, user_id, public_account_id):
        """Unbind user from public account

        Unbind user from public account

        Attributes:
            user_id (str): User unique identifier, can be user ID, username, email, phone, external ID, ID in the external identity source.
            public_account_id (str): User unique identifier, can be user ID, username, email, phone, external ID, ID in the external identity source.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-public-account-of-user',
            json={
                'userId': user_id,
                'publicAccountId': public_account_id,
            },
        )

    def get_organization(self, organization_code, with_custom_data=None, with_post=None, tenant_id=None):
        """Get organization details

        Get organization details

        Attributes:
            organizationCode (str): Organization Code (organizationCode)
            withCustomData (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-organization',
            params={
                'organizationCode': organization_code,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
            },
        )

    def get_organizations_batch(self, organization_code_list, with_custom_data=None, with_post=None, tenant_id=None):
        """Batch get organization details

        Batch get organization details

        Attributes:
            organizationCodeList (str): Organization Code (organizationCode) list
            withCustomData (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-organization-batch',
            params={
                'organizationCodeList': organization_code_list,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
            },
        )

    def list_organizations(self, page=None, limit=None, fetch_all=None, with_custom_data=None, with_post=None,
                           tenant_id=None, status=None):
        """Get organization list

        Get organization list, support paging.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, the maximum cannot exceed 50, the default is 10
            fetchAll (bool): Fetch all
            withCustomData (bool): Whether to get custom data
            status (bool): Organization status
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-organizations',
            params={
                'page': page,
                'limit': limit,
                'fetchAll': fetch_all,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
                'status': status,
            },
        )

    def list_users(self, keywords=None, advanced_filter=None, search_query=None, options=None):
        """Get/Search User List

        
This interface is used to get the user list, supporting fuzzy search, as well as filtering users through user basic fields, user custom fields, user departments, user historical login applications, and other dimensions.

### Fuzzy Search Example

Fuzzy search will default to perform fuzzy searches on the `phone`, `email`, `name`, `username`, `nickname` five fields for users. You can also set the `options.fuzzySearchOn` to determine the range of fields for fuzzy matching:

```json
{
  "keywords": "Beijing",
  "options": {
    "fuzzySearchOn": [
      "address"
    ]
  }
}
```

### Advanced Search Example

You can use `advancedFilter` for advanced search, advanced search supports filtering users through user basic information, custom data, departments, user sources, login applications, and external identity source information, etc. **And these filtering conditions can be arbitrarily combined.**

#### Filter users with disabled status

User status (`status`) is a string type, with optional values of `Activated` and `Suspended`: 

```json
{
  "advancedFilter": [
    {
      "field": "status",
      "operator": "EQUAL",
      "value": "Suspended"
    }
  ]
}
```

#### Filter users with email containing `@example.com`

User email (`email`) is a string type, can perform fuzzy search:

```json
{
  "advancedFilter": [
    {
      "field": "email",
      "operator": "CONTAINS",
      "value": "@example.com"
    }
  ]
}
```

#### Search users by any arbitrary extension field

```json
{
  "advancedFilter": [
    {
      "field": "some-custom-key",
      "operator": "EQUAL",
      "value": "some-value"
    }
  ]
}
```

#### Filter users by login count

Filter users with login count greater than 10:

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "GREATER",
      "value": 10
    }
  ]
}
```

Filter users with login count between 10 and 100:

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "BETWEEN",
      "value": [10, 100]
    }
  ]
}
```

#### Filter users by last login time

Filter users who have logged in within the last 7 days:

```json
{
  "advancedFilter": [
    {
      "field": "lastLoginTime",
      "operator": "GREATER",
      "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  ]
}
```

Filter users who have logged in within a certain period of time:

```json
{
  "advancedFilter": [
    {
      "field": "lastLogin",
      "operator": "BETWEEN",
      "value": [
        Date.now() - 14 * 24 * 60 * 60 * 1000,
        Date.now() - 7 * 24 * 60 * 60 * 1000
      ]
    }
  ]
}
```

#### Filter users by the application they have logged in to

Filter out users who have logged in to application `appId1` or `appId2`:

```json
{
  "advancedFilter": [
    {
      "field": "loggedInApps",
      "operator": "IN",
      "value": [
        "appId1",
        "appId2"
      ]
    }
  ]
}
```

Attributes:
            keywords (str): Fuzzy search keyword
            advanced_filter (list): Advanced search
            search_query (dict): Execute search command using ES query statement
            options (dict): Optional
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-users',
            json={
                'keywords': keywords,
                'advancedFilter': advanced_filter,
                'searchQuery': search_query,
                'options': options,
            },
        )

    def list_users_legacy(self, page=None, limit=None, status=None, updated_at_start=None, updated_at_end=None,
                          with_custom_data=None, with_post=None, with_identities=None):
        """Get user list

        Get user list interface, support paging, can choose to get custom data, identities, etc.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, the maximum cannot exceed 50, the default is 10
            status (str): Current account status, such as Disabled, Resigned, Normal, Archived
            updatedAtStart (int): User creation, modification start time, accurate to the second UNIX timestamp; supports getting incremental data after a certain period of time
            updatedAtEnd (int): User creation, modification end time, accurate to the second UNIX timestamp; supports getting incremental data within a certain period of time. The default is the current time
            withCustomData (bool): Whether to get custom data
            withPost (bool): Whether to get department information
            withIdentities (bool): Whether to get identities
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-users',
            params={
                'page': page,
                'limit': limit,
                'status': status,
                'updatedAtStart': updated_at_start,
                'updatedAtEnd': updated_at_end,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'withIdentities': with_identities,
            },
        )

    def get_user(self, user_id, user_id_type=None, flat_custom_data=None, with_custom_data=None, with_post=None,
                 with_identities=None):
        """Get User Information

        Get user details through user ID, can choose to get custom data, identities, and specify user ID type.

        Attributes:
            userId (str): User ID
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in external systems, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, in the format of `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the ID of the GenAuth identity source, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, in the format of `<provier>:<userIdInIdp>`, where `<provier>` is the type of synchronized identity source, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

            flatCustomData (bool): Whether to flatten custom fields
            withCustomData (bool): Whether to get custom data
            withPost (bool): Whether to get department information
            withIdentities (bool): Whether to get identities
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'flatCustomData': flat_custom_data,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'withIdentities': with_identities,
            },
        )

    def get_user_batch(self, user_ids, user_id_type=None, with_custom_data=None, flat_custom_data=None,
                       with_identities=None):
        """Batch Get User Information

        Batch get user information through user ID list, can choose to get custom data, identities, and specify user ID type.

        Attributes:
            userIds (str): User ID array
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in external systems, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, in the format of `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the ID of the GenAuth identity source, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, in the format of `<provier>:<userIdInIdp>`, where `<provier>` is the type of synchronized identity source, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

            withCustomData (bool): Whether to get custom data
            flatCustomData (bool): Whether to flatten custom fields
            withIdentities (bool): Whether to get identities
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-batch',
            params={
                'userIds': user_ids,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
                'withIdentities': with_identities,
            },
        )

    def user_field_decrypt(self, data, private_key):
        """Decrypt User Field

        Interface receives encrypted information and returns decrypted information

        Attributes:
            data (list): List of user attributes to be decrypted
            private_key (str): Private key, obtained through the console security settings-data security-data encryption
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/users/field/decrypt',
            json={
                'data': data,
                'privateKey': private_key,
            },
        )

    def create_user(self, status=None, email=None, phone=None, phone_country_code=None, username=None, external_id=None,
                    name=None, nickname=None, photo=None, gender=None, email_verified=None, phone_verified=None,
                    birthdate=None, country=None, province=None, city=None, address=None, street_address=None,
                    postal_code=None, company=None, browser=None, device=None, given_name=None, family_name=None,
                    middle_name=None, profile=None, preferred_username=None, website=None, zoneinfo=None, locale=None,
                    formatted=None, region=None, password=None, salt=None, tenant_ids=None, otp=None, custom_data=None, metadata_source=None, identities=None, identity_number=None,
                    options=None):
        """Create User

        Create a user, email, phone number, username must include at least one, email, phone number, username, externalId are unique within the user pool, this interface will create a user with administrator privileges, so it does not require phone verification and other security checks.

        Attributes:
            status (str): Current account status
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it's a foreign phone number, please specify the area code in the phoneCountryCode parameter.
            phone_country_code (str): Phone area code, China mainland phone numbers can be omitted. GenAuth SMS service does not natively support international phone numbers, you need to configure the corresponding international SMS service in the GenAuth console. The complete list of phone area codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
            username (str): Username, unique within the user pool
            external_id (str): Third-party external ID
            name (str): User real name, not unique
            nickname (str): Nickname
            photo (str): Profile picture link
            gender (str): Gender
            email_verified (bool): Email verified
            phone_verified (bool): Phone number verified
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            company (str): Company
            browser (str): Browser used in the last login
            device (str): Device used in the last login
            given_name (str): Given name
            family_name (str): Family name
            middle_name (str): Middle name
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): User personal website
            zoneinfo (str): User timezone information
            locale (str): Locale
            formatted (str): Standard complete address
            region (str): User region
            password (str): User password, default is plaintext. We use HTTPS protocol to securely transmit the password, which can ensure security to a certain extent. If you need higher-level security, we also support RSA256 and national encryption standard SM2 two ways to encrypt the password. For details, see the `passwordEncryptType` parameter.
            salt (str): Salt for encrypting user password
            tenant_ids (list): Tenant ID
            otp (dict): User OTP authenticator
            custom_data (dict): Custom data, the key in the object must be defined in the user pool first
            metadata_source (dict): Data object data, the key in the object must be defined in the user pool first
            identities (list): Third-party identity source
            identity_number (str): User ID number
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-user',
            json={
                'status': status,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'externalId': external_id,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'gender': gender,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'password': password,
                'salt': salt,
                'tenantIds': tenant_ids,
                'otp': otp,
                'customData': custom_data,
                'metadataSource': metadata_source,
                'identities': identities,
                'identityNumber': identity_number,
                'options': options,
            },
        )

    def create_users_batch(self, list, options=None):
        """Create Users in Batch

        Batch create users, email, phone number, username must include at least one, email, phone number, username, externalId are unique within the user pool, this interface will create users as an administrator, so it does not require phone verification code checks and other security checks.

        Attributes:
            list (list): User list
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-users-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def update_user(self, user_id, phone_country_code=None, name=None, nickname=None, photo=None, external_id=None,
                    status=None, email_verified=None, phone_verified=None, birthdate=None, country=None, province=None,
                    city=None, address=None, street_address=None, postal_code=None, gender=None, username=None,
                    email=None, phone=None, password=None, company=None, browser=None, device=None, given_name=None,
                    family_name=None, middle_name=None, profile=None, preferred_username=None, website=None,
                    zoneinfo=None, locale=None, formatted=None, region=None, identity_number=None, custom_data=None,
                    options=None):
        """Update User Information

        Update user information by user ID, email, phone number, username, externalId are unique within the user pool, this interface will update user information as an administrator, so it does not require phone verification code checks and other security checks.

        Attributes:
            user_id (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            phone_country_code (str): Phone country code, China mainland phone numbers can be left blank. GenAuth SMS service does not currently support international phone numbers, you need to configure the corresponding international SMS service in the GenAuth console. A complete list of phone country codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
            name (str): Real name, not unique
            nickname (str): Nickname
            photo (str): Profile picture URL
            external_id (str): Third-party external ID
            status (str): Current account status
            email_verified (bool): Email verified
            phone_verified (bool): Phone number verified
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            gender (str): Gender
            username (str): Username, unique within the user pool
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it's an international phone number, please specify the area code in the phoneCountryCode parameter.
            password (str): User password, default is plaintext. We use HTTPS protocol to securely transmit passwords, which can ensure security to a certain extent. If you need higher-level security, we also support RSA256 and national encryption SM2 two ways to encrypt passwords. For details, see the `passwordEncryptType` parameter.
            company (str): Company
            browser (str): Browser UA used in the last login
            device (str): Device used in the last login
            given_name (str): Given name
            family_name (str): Family name
            middle_name (str): Middle name
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): User's personal website
            zoneinfo (str): User's timezone information
            locale (str): Locale
            formatted (str): Standard complete address
            region (str): User's region
            identity_number (str): User's identity card number
            custom_data (dict): Custom data, the key in the object must be defined as a custom field in the user pool
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-user',
            json={
                'userId': user_id,
                'phoneCountryCode': phone_country_code,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'status': status,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'email': email,
                'phone': phone,
                'password': password,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'identityNumber': identity_number,
                'customData': custom_data,
                'options': options,
            },
        )

    def update_user_batch(self, list, options=None):
        """Batch Update User Information

        Batch update user information, email, phone number, username, externalId are unique within the user pool, this interface will update user information as an administrator, so it does not require phone verification code checks and other security checks.

        Attributes:
            list (list): User list
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-user-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def delete_users_batch(self, user_ids, options=None):
        """Batch Delete Users

        Delete users by user ID list, supports batch deletion, and can choose to specify the user ID type.

        Attributes:
            user_ids (list): User ID list
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-users-batch',
            json={
                'userIds': user_ids,
                'options': options,
            },
        )

    def get_user_identities(self, user_id, user_id_type=None):
        """Get User's External Identity Sources

        Get user's external identity sources by user ID, can choose to specify the user ID type.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-identities',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_roles(self, user_id, user_id_type=None, namespace=None):
        """Get User Role List

        Get user role list by user ID, can choose to specify the permission group code, and choose to specify the user ID type.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-roles',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
            },
        )

    def get_user_principal_authentication_info(self, user_id, user_id_type=None):
        """Get user's real-name authentication information

        Get user's real-name authentication information by user ID, you can choose to specify the user ID type.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-principal-authentication-info',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def reset_user_principal_authentication_info(self, user_id, options=None):
        """Delete user's real-name authentication information

        Delete user's real-name authentication information by user ID, you can choose to specify the user ID type.

        Attributes:
            user_id (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-user-principal-authentication-info',
            json={
                'userId': user_id,
                'options': options,
            },
        )

    def get_user_groups(self, user_id, user_id_type=None):
        """Get user's group list

        Get user's group list by user ID, you can choose to specify the user ID type.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-groups',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_mfa_info(self, user_id, user_id_type=None):
        """Get user's MFA binding information

        Get user's MFA binding information by user ID, you can choose to specify the user ID type.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-mfa-info',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def list_archived_users(self, page=None, limit=None, start_at=None):
        """Get the list of archived users

        Get the list of archived users, support paging, can filter start time, etc.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, the maximum cannot exceed 50, the default is 10
            startAt (int): Start time, the exact second UNIX timestamp, default not specified
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-archived-users',
            params={
                'page': page,
                'limit': limit,
                'startAt': start_at,
            },
        )

    def kick_users(self, app_ids, user_id, options=None):
        """Force users to log out

        Force users to log out by user ID and App ID list, you can choose to specify the user ID type, etc.

        Attributes:
            app_ids (list): APP ID list
            user_id (str): User ID
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/kick-users',
            json={
                'appIds': app_ids,
                'userId': user_id,
                'options': options,
            },
        )

    def is_user_exists(self, username=None, email=None, phone=None, external_id=None):
        """Determine whether the user exists

        Determine whether the user exists based on the conditions, you can filter the username, email, phone, third-party external ID, etc.

        Attributes:
            username (str): Username, unique within the user pool
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it is a foreign phone number, please specify the area code in the phoneCountryCode parameter.
            external_id (str): Third-party external ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/is-user-exists',
            json={
                'username': username,
                'email': email,
                'phone': phone,
                'externalId': external_id,
            },
        )

    def get_user_accessible_apps(self, user_id, user_id_type=None):
        """Get the user's accessible applications

        Get the user's accessible applications by user ID, you can choose to specify the user ID type, etc.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-accessible-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_authorized_apps(self, user_id, user_id_type=None):
        """Get the user's authorized applications

        Get the user's authorized applications by user ID, you can choose to specify the user ID type, etc.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-authorized-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def has_any_role(self, roles, user_id, options=None):
        """Determine whether the user has a role

        Determine whether the user has a role by user ID, support passing multiple roles, you can choose to specify the user ID type, etc.

        Attributes:
            roles (list): Role list
            user_id (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/has-any-role',
            json={
                'roles': roles,
                'userId': user_id,
                'options': options,
            },
        )

    def get_user_login_history(self, user_id, user_id_type=None, app_id=None, client_ip=None, start=None, end=None,
                               page=None, limit=None):
        """Get the user's login history

        Get the user's login history by user ID, support paging, you can choose to specify the user ID type, app ID, start and end timestamps, etc.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

            appId (str): App ID
            clientIp (str): Client IP
            start (int): Start timestamp (milliseconds)
            end (int): End timestamp (milliseconds)
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, the maximum cannot exceed 50, the default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-login-history',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'appId': app_id,
                'clientIp': client_ip,
                'start': start,
                'end': end,
                'page': page,
                'limit': limit,
            },
        )

    def get_user_loggedin_apps(self, user_id, user_id_type=None):
        """Get the user's previously logged-in applications

        Get the user's previously logged-in applications by user ID, you can choose to specify the user ID type, etc.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-loggedin-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_loggedin_identities(self, user_id, user_id_type=None):
        """Get the user's previously logged-in identities

        Get the user's previously logged-in identities by user ID, you can choose to specify the user ID type, etc.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-logged-in-identities',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def resign_user(self, user_id, user_id_type=None):
        """Resign a user

        Resign a user. The resignation operation will perform the following operations:

- After the member is resigned, the authorization, department, role, group, and position relationships of the member will be deleted;
- After the member is resigned, the user's basic information will be retained, and the account will be disabled. The application cannot be logged in. If you need to completely delete the account, please call the delete interface.

This operation is not recoverable, please operate with caution!
    

        Attributes:
            user_id (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/resign-user',
            json={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def resign_user_batch(self, user_ids, user_id_type=None):
        """Resign multiple users

        Resign multiple users. The resignation operation will perform the following operations:

- After the member is resigned, the authorization, department, role, group, and position relationships of the member will be deleted;
- After the member is resigned, the user's basic information will be retained, and the account will be disabled. The application cannot be logged in. If you need to completely delete the account, please call the delete interface.

This operation is not recoverable, please operate with caution!
    

        Attributes:
            user_ids (list): User ID array
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/resign-user-batch',
            json={
                'userIds': user_ids,
                'userIdType': user_id_type,
            },
        )

    def get_user_authorized_resources(self, user_id, user_id_type=None, namespace=None, resource_type=None):
        """Get all resources authorized to the user

        Get all resources authorized to the user by user ID, you can choose to specify the user ID type, etc., the resources authorized to the user are a collection of the user's own, inherited through the group, inherited through the role, and inherited through the organizational structure.

        Attributes:
            userId (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

            namespace (str): Code of the permission group (permission space) to which it belongs
            resourceType (str): Resource type, such as data, API, menu, button
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-authorized-resources',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def check_session_status(self, app_id, user_id):
        """Check if a user has a Session login state in an application

        Check if a user has a Session login state in an application

        Attributes:
            app_id (str): App ID
            user_id (str): User's unique identifier, can be user ID, username, email, phone, external ID, user ID in an external identity source.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-session-status',
            json={
                'appId': app_id,
                'userId': user_id,
            },
        )

    def import_otp(self, list):
        """Import a user's OTP

        Import a user's OTP

        Attributes:
            list (list): Parameter list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/import-otp',
            json={
                'list': list,
            },
        )

    def get_otp_secret_by_user(self, user_id, user_id_type=None):
        """Get the OTP secret key bound by the user

        Get the OTP secret key bound by the user by user ID. You can choose to specify the user ID type, etc.

        Attributes:
            userId (str): User ID
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-otp-secret-by-user',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_password_ciphertext(self, user_id, user_id_type=None):
        """Get the user's custom encrypted password

        This function is mainly used to encrypt the user's password based on the key configured in the console, such as RSA, SM2, etc.

        Attributes:
            user_id (str): User ID
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-password-ciphertext',
            json={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def link_identity(self, user_id_in_idp, user_id, ext_idp_id, type=None, is_social=None):
        """Link an identity to a user

        Manually bind the identity information from an external identity source to the user. After the binding is completed, you can use the identity source that has been bound to log in to the corresponding GenAuth user.

        Attributes:
            user_id_in_idp (str): Required, the unique identifier of the user in the external identity source, which needs to be obtained from the authentication return value of the external identity source.
            user_id (str): Required, the GenAuth user ID that performs the binding operation.
            ext_idp_id (str): Required, identity source ID, used to specify which identity the identity belongs to.
            type (str): Non-required, represents the specific type of this identity, which can be obtained from the type field of the user identity information. If not passed, it defaults to generic
            is_social (bool): Deprecated, can be passed arbitrarily, this field will be removed in the future.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/link-identity',
            json={
                'userIdInIdp': user_id_in_idp,
                'userId': user_id,
                'extIdpId': ext_idp_id,
                'type': type,
                'isSocial': is_social,
            },
        )

    def unlink_identity(self, user_id, ext_idp_id, type=None, is_social=None):
        """Unlink all identity information of the user in the identity source

        Unlink all identity information of the user in a certain identity source. After the unlinking, the identity source that has been unlinked will not be able to log in to the corresponding GenAuth user, unless the identity information is re-bound.

        Attributes:
            user_id (str): Required, the GenAuth user ID that performs the binding operation.
            ext_idp_id (str): Required, identity source ID, used to specify which identity the identity belongs to.
            type (str): Non-required, represents the specific type of this identity, which can be obtained from the type field of the user identity information. If not passed, it defaults to generic
            is_social (bool): Deprecated, can be passed arbitrarily, this field will be removed in the future.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unlink-identity',
            json={
                'userId': user_id,
                'extIdpId': ext_idp_id,
                'type': type,
                'isSocial': is_social,
            },
        )

    def set_users_mfa_status(self, mfa_trigger_data, user_id, user_id_type=None):
        """Set User MFA Status

        Set the user's MFA status, that is, the MFA trigger data.

        Attributes:
            mfa_trigger_data (dict): MFA Factor list
            user_id (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronous identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-mfa-status',
            json={
                'mfaTriggerData': mfa_trigger_data,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_mfa_status(self, user_id, user_id_type=None):
        """Get User MFA Status

        Get the user MFA status, that is, the MFA trigger data.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronous identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mfa-status',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_sync_relations(self, user_id, user_id_type=None):
        """Get User Sync Relations

        If the user in GenAuth has performed upstream and downstream synchronization, this interface can be used to query the associated user information in the third party.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronous identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-sync-relations',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def delete_user_sync_relations(self, provider, user_id, user_id_type=None):
        """Delete User Sync Relations

        If the user in GenAuth has performed upstream and downstream synchronization, this interface can be used to delete the association relationship of a user in a specified identity source.

        Attributes:
            provider (str): External identity source type, such as:
- `wechatwork`: Enterprise WeChat
- `dingtalk`: DingTalk
- `lark`: Feishu
- `welink`: Welink
- `ldap`: LDAP
- `active-directory`: Windows AD
- `italent`: North Forest
- `xiaoshouyi`: Sales Easy
- `maycur`: Every Moment Expense
- `scim`: SCIM
- `moka`: Moka HR
    
            user_id (str): User ID
            user_id_type (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronous identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-user-sync-relations',
            json={
                'provider': provider,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_public_account_roles(self, user_id, user_id_type=None, namespace=None):
        """Get Public Account Roles

        Through user ID, get the user role list, can choose the code of the belonging permission group, choose the specified user ID type, etc.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronous identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

            namespace (str): The code of the belonging permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-roles-of-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
            },
        )

    def get_public_accounts_of_role(self, role_id):
        """Get Public Accounts of Role

        Through role ID, get the public account list of the user.

        Attributes:
            roleId (str): Role ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-role',
            params={
                'roleId': role_id,
            },
        )

    def bind_public_account_of_roles(self, role_ids, user_id):
        """Bind Public Account to Roles

        Bind public account to roles in batches

        Attributes:
            role_ids (list): Role IDs
            user_id (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-roles',
            json={
                'roleIds': role_ids,
                'userId': user_id,
            },
        )

    def get_public_accounts_of_group(self, group_id):
        """Get Public Accounts of Group

        Through group ID, get the public account list of the user.

        Attributes:
            groupId (str): Group ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-group',
            params={
                'groupId': group_id,
            },
        )

    def get_groups_of_public_account(self, user_id, user_id_type=None):
        """Get Groups of Public Account

        Through public account ID, get the public account group list, can choose to specify user ID type, etc.

        Attributes:
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: Username
- `external_id`: User's external ID in an external system, corresponding to the `externalId` field in GenAuth user information
- `identity`: User's external identity source information, format is `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the GenAuth identity source ID, `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, format is `<provier>:<userIdInIdp>`, where `<provier>` is the synchronization identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example value: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-groups-of-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_public_account_of_groups(self, group_ids, user_id):
        """Public Account Adds Batch Groups

        Public account adds batch groups through group ID.

        Attributes:
            group_ids (list): Group ID list
            user_id (str): User unique identifier, can be user ID, username, email, phone number, external ID, or ID in an external identity source.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-groups',
            json={
                'groupIds': group_ids,
                'userId': user_id,
            },
        )

    def get_group(self, code, with_custom_data=None):
        """Get Group Details

        Get group details through group code.

        Attributes:
            code (str): Group code
            withCustomData (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-group',
            params={
                'code': code,
                'withCustomData': with_custom_data,
            },
        )

    def list_groups(self, keywords=None, page=None, limit=None, with_metadata=None, with_custom_data=None,
                    flat_custom_data=None):
        """Get Group List

        Get group list, supports pagination.

        Attributes:
            keywords (str): Search group code or group name
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            withMetadata (bool): Whether to display metadata content
            withCustomData (bool): Whether to get custom data
            flatCustomData (bool): Whether to flatten extension fields
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-groups',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
                'withMetadata': with_metadata,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
            },
        )

    def get_all_groups(self, fetch_members=None, with_custom_data=None):
        """Get All Groups

        Get all groups.

        Attributes:
            fetchMembers (bool): Whether to get member list
            withCustomData (bool): Whether to get custom data
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-all-groups',
            params={
                'fetchMembers': fetch_members,
                'withCustomData': with_custom_data,
            },
        )

    def create_group(self, type, description, name, code, custom_data=None):
        """Create Group

        Create a group, a group must include group name and unique identifier code, and must be a valid English identifier, such as developers.

        Attributes:
            type (str): Group type
            description (str): Group description
            name (str): Group name
            code (str): Group code
            custom_data (dict): Custom data, the key in the object passed in must be defined in the user pool for related custom fields
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-group',
            json={
                'type': type,
                'description': description,
                'name': name,
                'code': code,
                'customData': custom_data,
            },
        )

    def create_or_update_group(self, type, description, name, code):
        """Create or Update Group

        If it does not exist, create it; if it exists, update it.

        Attributes:
            type (str): Group type
            description (str): Group description
            name (str): Group name
            code (str): Group code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-or-update-group',
            json={
                'type': type,
                'description': description,
                'name': name,
                'code': code,
            },
        )

    def create_groups_batch(self, list):
        """Create Groups in Batch

        Create groups in batch, each group must include group name and unique identifier code, and must be a valid English identifier, such as developers.

        Attributes:
            list (list): Batch of groups
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-groups-batch',
            json={
                'list': list,
            },
        )

    def update_group(self, description, code, name=None, new_code=None, custom_data=None):
        """Update Group

        Update group by group code, can update this group's code.

        Attributes:
            description (str): Group description
            code (str): Group code
            name (str): Group name
            new_code (str): Group's new code
            custom_data (dict): Custom data, the key in the object passed in must be defined in the user pool for related custom fields
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-group',
            json={
                'description': description,
                'code': code,
                'name': name,
                'newCode': new_code,
                'customData': custom_data,
            },
        )

    def delete_groups_batch(self, code_list):
        """Delete Groups in Batch

        Delete groups in batch by group code.

        Attributes:
            code_list (list): Group code list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-groups-batch',
            json={
                'codeList': code_list,
            },
        )

    def add_group_members(self, user_ids, code):
        """Add Group Members

        Add group members, members are passed in as an array of user IDs.

        Attributes:
            user_ids (list): User ID array
            code (str): Group code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-group-members',
            json={
                'userIds': user_ids,
                'code': code,
            },
        )

    def remove_group_members(self, user_ids, code):
        """Remove Group Members in Batch

        Remove group members in batch, members are passed in as an array of user IDs.

        Attributes:
            user_ids (list): User ID array
            code (str): Group code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-group-members',
            json={
                'userIds': user_ids,
                'code': code,
            },
        )

    def list_group_members(self, code, page=None, limit=None, with_custom_data=None, with_identities=None):
        """List Group Members

        List group members by group code, supports pagination, can get custom data, identities, and department ID list.

        Attributes:
            code (str): Group code
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            withCustomData (bool): Whether to get custom data
            withIdentities (bool): Whether to get identities
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-group-members',
            params={
                'code': code,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
            },
        )

    def get_group_authorized_resources(self, code, namespace=None, resource_type=None):
        """Get Group Authorized Resources

        Get the list of resources authorized by the group by group code, can filter by resource type and permission group code.

        Attributes:
            code (str): Group code
            namespace (str): The code of the permission group (permission space)
            resourceType (str): Resource type
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-group-authorized-resources',
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def get_role(self, code, namespace=None):
        """Get Role Details

        Get role details by role code within the permission group.

        Attributes:
            code (str): The unique identifier of the role within the permission group (permission space)
            namespace (str): The code of the permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-role',
            params={
                'code': code,
                'namespace': namespace,
            },
        )

    def assign_role(self, targets, code, end_time=None, enable_time=None, namespace=None):
        """Assign Role in Batch

        Assign role in batch by role code within the permission group, the assignees can be users or departments.

        Attributes:
            targets (list): Target objects
            code (str): The unique identifier of the role within the permission group
            end_time (int): The expiration time of the subject in milliseconds, null for permanent validity
            enable_time (int): The join time of the subject in milliseconds, null for immediate join
            namespace (str): The code of the permission group
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-role',
            json={
                'targets': targets,
                'code': code,
                'endTime': end_time,
                'enableTime': enable_time,
                'namespace': namespace,
            },
        )

    def assign_role_batch(self, targets, roles):
        """Batch Assign Roles

        Batch assign roles, the assignees can be users, can be departments.

        Attributes:
            targets (list): List of targets to assign roles
            roles (list): List of role information
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-role-batch',
            json={
                'targets': targets,
                'roles': roles,
            },
        )

    def revoke_role(self, targets, code, namespace=None):
        """Revoke Assigned Role

        Revoke assigned role by role code within the permission group, the assignees can be users or departments.

        Attributes:
            targets (list): Targets to revoke role
            code (str): The unique identifier of the role within the permission group
            namespace (str): The code of the permission group
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-role',
            json={
                'targets': targets,
                'code': code,
                'namespace': namespace,
            },
        )

    def revoke_role_batch(self, targets, roles):
        """Batch Revoke Assigned Roles

        Batch revoke assigned roles, the assignees can be users, can be departments.

        Attributes:
            targets (list): List of targets to revoke roles
            roles (list): List of role information
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-role-batch',
            json={
                'targets': targets,
                'roles': roles,
            },
        )

    def get_role_authorized_resources(self, code, namespace=None, resource_type=None):
        """Get Role Authorized Resources

        Get the list of resources authorized by the role by role code within the permission group.

        Attributes:
            code (str): The unique identifier of the role within the permission group
            namespace (str): The code of the permission group
            resourceType (str): Resource type, such as data, API, button, menu
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-role-authorized-resources',
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def list_role_members(self, code, page=None, limit=None, with_custom_data=None, with_identities=None,
                          namespace=None):
        """List Role Members

        List role members by role code within the permission group, supports pagination, can choose to get custom data, identities, etc.

        Attributes:
            code (str): The unique identifier of the role within the permission group
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            withCustomData (bool): Whether to get custom data
            withIdentities (bool): Whether to get identities
            namespace (str): The code of the permission group
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-role-members',
            params={
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'code': code,
                'namespace': namespace,
            },
        )

    def create_role(self, code, name=None, namespace=None, description=None, disable_time=None):
        """Create Role

        Create role by role code within the permission group, can choose permission group, role description, role name, etc.

        Attributes:
            code (str): The unique identifier of the role within the permission group
            name (str): Role name within the permission group
            namespace (str): The code of the permission group (permission space)
            description (str): Role description
            disable_time (str): Role automatic disable time, in milliseconds, if null indicates permanent validity
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-role',
            json={
                'code': code,
                'name': name,
                'namespace': namespace,
                'description': description,
                'disableTime': disable_time,
            },
        )

    def list_roles(self, page=None, limit=None, keywords=None, namespace=None):
        """Get Role List

        Get the role list, support pagination, and filter by permission group (permission space).

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            keywords (str): Used to search by role code or name, optional.
            namespace (str): The code of the permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-roles',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
                'namespace': namespace,
            },
        )

    def delete_roles_batch(self, code_list, namespace=None):
        """Delete Roles in a Single Permission Group (Permission Space)

        Delete roles in a single permission group (permission space), can be deleted in batches.

        Attributes:
            code_list (list): Role code list
            namespace (str): The code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-roles-batch',
            json={
                'codeList': code_list,
                'namespace': namespace,
            },
        )

    def create_roles_batch(self, list):
        """Batch Create Roles

        Batch create roles, can choose permission group, role description, etc.

        Attributes:
            list (list): Role list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-roles-batch',
            json={
                'list': list,
            },
        )

    def update_role(self, name, new_code, code, namespace=None, description=None, status=None, disable_time=None):
        """Modify Role

        Modify the role by the new and old code of the role within the permission group (permission space), can choose the role name, role description, etc.

        Attributes:
            name (str): Role name within the permission group (permission space)
            new_code (str): The unique identifier of the role within the permission group (permission space)
            code (str): The unique identifier of the role within the permission group (permission space)
            namespace (str): The code of the permission group (permission space)
            description (str): Role description
            status (str): Role status, ENABLE-means normal, DISABLE-means prohibited
            disable_time (str): Role automatic disable time, in milliseconds, if null indicates permanent validity
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-role',
            json={
                'name': name,
                'newCode': new_code,
                'code': code,
                'namespace': namespace,
                'description': description,
                'status': status,
                'disableTime': disable_time,
            },
        )

    def delete_roles(self, role_list):
        """Delete Roles Across Permission Groups (Spaces)

        Delete roles across permission groups (spaces), can be deleted in batches.

        Attributes:
            role_list (list): Role code and namespace list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/multiple-namespace-delete-roles-batch',
            json={
                'roleList': role_list,
            },
        )

    def check_params_namespace(self, code, namespace, name=None):
        """Check if the Role Code or Name is Available

        Check if the role code or name is available by the user pool ID, permission space code and role code, or user pool ID, permission space name and role name.

        Attributes:
            code (str): The unique identifier of the role within the permission group (permission space)
            namespace (str): The code of the permission group (permission space)
            name (str): Role name within the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-role-params',
            json={
                'code': code,
                'namespace': namespace,
                'name': name,
            },
        )

    def list_role_assignments(self, role_code, page=None, limit=None, query=None, namespace_code=None,
                              target_type=None):
        """Get Role Assignment List

        Get the role assignment list.

        Attributes:
            roleCode (str): Role code, can only use letters, numbers and -_, up to 50 characters
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Query by role code or role name
            namespaceCode (str): Permission space code
            targetType (str): Target type, accept user, department
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-role-assignments',
            params={
                'page': page,
                'limit': limit,
                'query': query,
                'roleCode': role_code,
                'namespaceCode': namespace_code,
                'targetType': target_type,
            },
        )

    def create_admin_role(self, name, code, description=None):
        """Create Admin Role

        Create an admin role by role code and role name, can choose role description

        Attributes:
            name (str): Admin role name
            code (str): Admin role unique identifier
            description (str): Role description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-admin-role',
            json={
                'name': name,
                'code': code,
                'description': description,
            },
        )

    def delete_admin_roles_batch(self, code_list):
        """Delete Admin Custom Roles

        Delete admin custom roles, support batch deletion.

        Attributes:
            code_list (list): Role code list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-admin-roles',
            json={
                'codeList': code_list,
            },
        )

    def list_ext_idp(self, tenant_id=None, app_id=None):
        """Get Identity Source List

        Get the identity source list, can specify the tenant ID for filtering.

        Attributes:
            tenantId (str): Tenant ID
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
            },
        )

    def get_ext_idp(self, id, tenant_id=None, app_id=None, type=None):
        """Get Identity Source Details

        Get the identity source details by the identity source ID, can specify the tenant ID for filtering.

        Attributes:
            id (str): Identity source ID
            tenantId (str): Tenant ID
            appId (str): Application ID
            type (str): Identity source type
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'id': id,
                'type': type,
            },
        )

    def create_ext_idp(self, name, type, tenant_id=None):
        """Create Identity Source

        Create an identity source, can set the identity source name, connection type, tenant ID, etc.

        Attributes:
            name (str): Identity source name
            type (str): Identity source connection type
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-ext-idp',
            json={
                'name': name,
                'type': type,
                'tenantId': tenant_id,
            },
        )

    def update_ext_idp(self, name, id, tenant_id=None):
        """Update Identity Source Configuration

        Update the identity source configuration, can set the identity source ID and name.

        Attributes:
            name (str): Name
            id (str): Identity source ID
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ext-idp',
            json={
                'name': name,
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def delete_ext_idp(self, id, tenant_id=None):
        """Delete Identity Source

        Delete the identity source by the identity source ID.

        Attributes:
            id (str): Identity source ID
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-ext-idp',
            json={
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def create_ext_idp_conn(self, ext_idp_id, type, identifier, display_name, fields, login_only=None, logo=None,
                            tenant_id=None):
        """Create a New Connection under an Existing Identity Source

        Create a new connection under an existing identity source, can set the identity source icon, whether to support only login, etc.

        Attributes:
            ext_idp_id (str): Identity source connection ID
            type (str): Identity source connection type
            identifier (str): Identity source connection identifier
            display_name (str): Display name of the connection on the login page
            fields (dict): Custom configuration information of the connection
            login_only (bool): Whether to support only login
            logo (str): Identity source icon
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-ext-idp-conn',
            json={
                'extIdpId': ext_idp_id,
                'type': type,
                'identifier': identifier,
                'displayName': display_name,
                'fields': fields,
                'loginOnly': login_only,
                'logo': logo,
                'tenantId': tenant_id,
            },
        )

    def update_ext_idp_conn(self, id, display_name, fields, logo=None, login_only=None, tenant_id=None):
        """Update Identity Source Connection

        Update the identity source connection, can set the identity source icon, whether to support only login, etc.

        Attributes:
            id (str): Identity source connection ID
            display_name (str): Identity source connection display name
            fields (dict): Identity source connection custom parameters (incremental modification)
            logo (str): Identity source connection icon
            login_only (bool): Whether to support only login
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ext-idp-conn',
            json={
                'id': id,
                'displayName': display_name,
                'fields': fields,
                'logo': logo,
                'loginOnly': login_only,
                'tenantId': tenant_id,
            },
        )

    def delete_ext_idp_conn(self, id, tenant_id=None):
        """Delete Identity Source Connection

        Delete the identity source connection by the identity source connection ID.

        Attributes:
            id (str): Identity source connection ID
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-ext-idp-conn',
            json={
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def change_ext_idp_conn_state(self, id, enabled, app_id, tenant_id=None, app_ids=None):
        """Identity Source Connection Switch

        Identity source connection switch, can open or close the identity source connection.

        Attributes:
            id (str): Identity source connection ID
            enabled (bool): Whether to enable the identity source connection
            app_id (str): Application ID
            tenant_id (str): Tenant ID
            app_ids (list): Application ID list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-ext-idp-conn-state',
            json={
                'id': id,
                'enabled': enabled,
                'appId': app_id,
                'tenantId': tenant_id,
                'appIds': app_ids,
            },
        )

    def change_ext_idp_conn_association_state(self, id, association, tenant_id=None):
        """Tenant Association Identity Source

        Tenants can associate or disassociate identity source connections.

        Attributes:
            id (str): Identity source connection ID
            association (bool): Whether to associate the identity source
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-ext-idp-conn-association-state',
            json={
                'id': id,
                'association': association,
                'tenantId': tenant_id,
            },
        )

    def list_tenant_ext_idp(self, tenant_id=None, app_id=None, type=None, page=None, limit=None):
        """Tenant Console Get Identity Source List

        Get the identity source list in the tenant console, can filter by application ID.

        Attributes:
            tenantId (str): Tenant ID
            appId (str): Application ID
            type (str): Identity source type
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'type': type,
                'page': page,
                'limit': limit,
            },
        )

    def ext_idp_conn_state_by_apps(self, id, tenant_id=None, app_id=None, type=None):
        """Connection Details of Applications under Identity Source

        Get the connection status of applications under the identity source details page

        Attributes:
            id (str): Identity source ID
            tenantId (str): Tenant ID
            appId (str): Application ID
            type (str): Identity source type
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/ext-idp-conn-apps',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'id': id,
                'type': type,
            },
        )

    def get_user_base_fields(self, ):
        """Get User Base Fields List

        Get the list of user base fields

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-base-fields',
        )

    def list_user_base_fields(self, target_type, data_type, tenant_id=None, page=None, limit=None, user_visible=None,
                              admin_visible=None, access_control=None, keyword=None, lang=None):
        """List User Base Fields

        List user base fields

        Attributes:
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    ;This interface does not support group (GROUP)
            dataType (str): Field type
            tenantId (str): Tenant ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            userVisible (bool): User visibility
            adminVisible (bool): Administrator visibility
            accessControl (bool): Access control
            keyword (str): Search keyword
            lang (str): Search language
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-user-base-fields',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'dataType': data_type,
                'page': page,
                'limit': limit,
                'userVisible': user_visible,
                'adminVisible': admin_visible,
                'accessControl': access_control,
                'keyword': keyword,
                'lang': lang,
            },
        )

    def set_user_base_fields(self, list):
        """Modify User Base Fields Configuration

        Modify user base fields configuration, base fields do not allow modification of data type, uniqueness.

        Attributes:
            list (list): Custom field list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-base-fields',
            json={
                'list': list,
            },
        )

    def get_custom_fields(self, target_type, tenant_id=None):
        """Get Custom Field List

        Get the custom field list by object type, including user, department, or role.

        Attributes:
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    ;This interface does not support group (GROUP)
            tenantId (str): Tenant ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-custom-fields',
            params={
                'targetType': target_type,
                'tenantId': tenant_id,
            },
        )

    def list_cust_fields(self, target_type, data_type, tenant_id=None, page=None, limit=None, user_visible=None,
                         admin_visible=None, access_control=None, keyword=None, lang=None):
        """List Custom Fields

        List custom fields by object type, including user, department, or role.

        Attributes:
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    ;This interface does not support group (GROUP)
            dataType (str): Field type
            tenantId (str): Tenant ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            userVisible (bool): User visibility
            adminVisible (bool): Administrator visibility
            accessControl (bool): Access control
            keyword (str): Search keyword
            lang (str): Search language
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-custom-fields',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'dataType': data_type,
                'page': page,
                'limit': limit,
                'userVisible': user_visible,
                'adminVisible': admin_visible,
                'accessControl': access_control,
                'keyword': keyword,
                'lang': lang,
            },
        )

    def set_custom_fields(self, list, tenant_id=None):
        """Create/Modify Custom Field Definitions

        Create/modify user, department, or role custom field definitions. If the passed key does not exist, it will be created. If it exists, it will be updated.

        Attributes:
            list (list): Custom field list
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-custom-fields',
            json={
                'list': list,
                'tenantId': tenant_id,
            },
        )

    def delete_custom_fields(self, tenant_id, list):
        """Delete Custom Field Definitions

        Delete user, department, or role custom field definitions.

        Attributes:
            tenant_id (str): Tenant ID
            list (list): Custom field list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-custom-fields',
            json={
                'tenantId': tenant_id,
                'list': list,
            },
        )

    def set_custom_data(self, list, target_identifier, target_type, tenant_id=None, namespace=None):
        """Set Custom Field Values

        Set custom field values for users, roles, or departments. If it exists, it will be updated. If it does not exist, it will be created.

        Attributes:
            list (list): Custom data list
            target_identifier (str): Unique identifier of the target object:
- If it is a user, it is the user's ID, such as `6343b98b7cfxxx9366e9b7c`
- If it is a role, it is the role's code, such as `admin`
- If it is a group, it is the group's code, such as `developer`
- If it is a department, it is the department's ID, such as `6343bafc019xxxx889206c4c`
        
            target_type (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    
            tenant_id (str): Tenant ID
            namespace (str): Code of the permission group to which the role belongs. This is required when the target_type is a role, otherwise it can be ignored.
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-custom-data',
            json={
                'list': list,
                'targetIdentifier': target_identifier,
                'targetType': target_type,
                'tenantId': tenant_id,
                'namespace': namespace,
            },
        )

    def get_custom_data(self, tenant_id, target_type, target_identifier, namespace=None):
        """Get Custom Field Values for Users, Groups, Roles, and Organizational Units

        Get custom field values for users, groups, roles, and organizational units based on filtering conditions.

        Attributes:
            tenantId (str): Tenant ID
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    
            targetIdentifier (str): Unique identifier of the target object:
- If it is a user, it is the user's ID, such as `6343b98b7cfxxx9366e9b7c`
- If it is a role, it is the role's code, such as `admin`
- If it is a group, it is the group's code, such as `developer`
- If it is a department, it is the department's ID, such as `6343bafc019xxxx889206c4c`
        
            namespace (str): Code of the permission group to which the role belongs. This is required when the target_type is a role, otherwise it can be ignored.
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-custom-data',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'namespace': namespace,
            },
        )

    def create_resource(self, type, code, description=None, name=None, actions=None, api_identifier=None,
                        namespace=None):
        """Create Resource

        Create a resource, you can set the resource description, defined operation type, URL identifier, etc.

        Attributes:
            type (str): Resource type, such as data, API, button, menu
            code (str): Resource unique identifier
            description (str): Resource description
            name (str): Resource name
            actions (list): Resource defined operation type
            api_identifier (str): API resource URL identifier
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-resource',
            json={
                'type': type,
                'code': code,
                'description': description,
                'name': name,
                'actions': actions,
                'apiIdentifier': api_identifier,
                'namespace': namespace,
            },
        )

    def create_resources_batch(self, list, namespace=None):
        """Batch Create Resources

        Batch create resources, you can set the resource description, defined operation type, URL identifier, etc.

        Attributes:
            list (list): Resource list
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-resources-batch',
            json={
                'list': list,
                'namespace': namespace,
            },
        )

    def get_resource(self, code, namespace=None):
        """Get Resource Details

        Get resource details based on filtering conditions.

        Attributes:
            code (str): Resource unique identifier
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-resource',
            params={
                'code': code,
                'namespace': namespace,
            },
        )

    def get_resources_batch(self, code_list, namespace=None):
        """Batch Get Resource Details

        Batch get resource details based on filtering conditions.

        Attributes:
            codeList (str): Resource code list, batch can be separated by commas
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-resources-batch',
            params={
                'namespace': namespace,
                'codeList': code_list,
            },
        )

    def list_common_resource(self, page=None, limit=None, keyword=None, namespace_code_list=None):
        """Paging Get Common Resource List

        Get the details of the common resource list based on filtering conditions.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            keyword (str): Query condition
            namespaceCodeList (str): Permission space list
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-common-resource',
            params={
                'page': page,
                'limit': limit,
                'keyword': keyword,
                'namespaceCodeList': namespace_code_list,
            },
        )

    def list_resources(self, namespace=None, type=None, page=None, limit=None):
        """Paging Get Resource List

        Get the details of the resource list based on filtering conditions.

        Attributes:
            namespace (str): Code of the permission group (permission space)
            type (str): Resource type
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-resources',
            params={
                'namespace': namespace,
                'type': type,
                'page': page,
                'limit': limit,
            },
        )

    def update_resource(self, code, description=None, name=None, actions=None, api_identifier=None, namespace=None,
                        type=None):
        """Modify Resource

        Modify a resource, you can set the resource description, defined operation type, URL identifier, etc.

        Attributes:
            code (str): Resource unique identifier
            description (str): Resource description
            name (str): Resource name
            actions (list): Resource defined operation type
            api_identifier (str): API resource URL identifier
            namespace (str): Code of the permission group (permission space)
            type (str): Resource type, such as data, API, button, menu
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-resource',
            json={
                'code': code,
                'description': description,
                'name': name,
                'actions': actions,
                'apiIdentifier': api_identifier,
                'namespace': namespace,
                'type': type,
            },
        )

    def delete_resource(self, code, namespace=None):
        """Delete Resource

        Delete a resource based on the resource unique identifier and the code of the permission group (permission space).

        Attributes:
            code (str): Resource unique identifier
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-resource',
            json={
                'code': code,
                'namespace': namespace,
            },
        )

    def delete_resources_batch(self, namespace=None, code_list=None, ids=None):
        """Batch Delete Resources

        Batch delete resources based on the resource unique identifier and the code of the permission group (permission space).

        Attributes:
            namespace (str): Code of the permission group (permission space)
            code_list (list): Resource code list
            ids (list): Resource Id list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-resources-batch',
            json={
                'namespace': namespace,
                'codeList': code_list,
                'ids': ids,
            },
        )

    def batch_delete_common_resource(self, ids):
        """Batch Delete Resources

        Batch delete resources based on the resource id.

        Attributes:
            ids (list): Resource id list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-common-resources-batch',
            json={
                'ids': ids,
            },
        )

    def associate_tenant_resource(self, code, association, app_id, tenant_id=None):
        """Associate/Disassociate Application Resources to Tenants

        Associate or disassociate resources to tenants based on the resource unique identifier and the permission group.

        Attributes:
            code (str): Resource Code
            association (bool): Whether to associate application resources
            app_id (str): Application ID
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/associate-tenant-resource',
            json={
                'code': code,
                'association': association,
                'appId': app_id,
                'tenantId': tenant_id,
            },
        )

    def create_namespace(self, code, name=None, description=None):
        """Create Permission Group

        Create a permission group, you can set the permission group name, Code, and description.

        Attributes:
            code (str): Permission group unique identifier
            name (str): Permission group name
            description (str): Permission group description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-namespace',
            json={
                'code': code,
                'name': name,
                'description': description,
            },
        )

    def create_namespaces_batch(self, list):
        """Batch Create Permission Groups

        Batch create permission groups, you can set the permission group name, Code, and description separately.

        Attributes:
            list (list): Permission group list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-namespaces-batch',
            json={
                'list': list,
            },
        )

    def get_namespace(self, code):
        """Get Permission Group Details

        Get permission group details based on the permission group unique identifier (Code).

        Attributes:
            code (str): Permission group unique identifier
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-namespace',
            params={
                'code': code,
            },
        )

    def get_namespaces_batch(self, code_list):
        """Batch Get Permission Group Details

        Batch get permission group details based on the permission group unique identifier (Code).

        Attributes:
            codeList (str): Permission group code list, batch can be separated by commas
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-namespaces-batch',
            params={
                'codeList': code_list,
            },
        )

    def update_namespace(self, code, description=None, name=None, new_code=None):
        """Modify Permission Group Information

        Modify permission group information, you can modify the name, description, and new unique identifier (NewCode).

        Attributes:
            code (str): Permission group unique identifier
            description (str): Permission group description
            name (str): Permission group name
            new_code (str): Permission group new unique identifier
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-namespace',
            json={
                'code': code,
                'description': description,
                'name': name,
                'newCode': new_code,
            },
        )

    def delete_namespace(self, code):
        """Delete Permission Group Information

        Delete permission group information based on the permission group unique identifier (Code).

        Attributes:
            code (str): Permission group unique identifier
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-namespace',
            json={
                'code': code,
            },
        )

    def delete_namespaces_batch(self, code_list):
        """Batch Delete Permission Groups

        Batch delete permission groups based on the permission group unique identifier (Code).

        Attributes:
            code_list (list): Permission group code list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-namespaces-batch',
            json={
                'codeList': code_list,
            },
        )

    def list_namespaces(self, page=None, limit=None, keywords=None):
        """Paging Get Permission Group List

        Get the details of the permission group list based on filtering conditions.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            keywords (str): Search permission group Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-namespaces',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
            },
        )

    def list_namespace_roles(self, code, page=None, limit=None, keywords=None):
        """Paging Get All Roles in the Permission Group

        Get the details of all roles in the permission group based on filtering conditions.

        Attributes:
            code (str): Permission group unique identifier
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            keywords (str): Role Code or name
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-namespace-roles',
            params={
                'page': page,
                'limit': limit,
                'code': code,
                'keywords': keywords,
            },
        )

    def authorize_resources(self, list, namespace=None):
        """Authorize Resources

        Authorize one or more resources to users, roles, groups, organizational units, etc., and can specify different operation permissions separately.

        Attributes:
            list (list): Authorized resource list
            namespace (str): Code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-resources',
            json={
                'list': list,
                'namespace': namespace,
            },
        )

    def get_authorized_resources(self, target_type, target_identifier, namespace=None, resource_type=None,
                                 resource_list=None, with_denied=None):
        """Get the list of resources authorized to a subject

        Get the list of resources authorized to a subject based on filtering conditions.

        Attributes:
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    
            targetIdentifier (str): The unique identifier of the target object:
- If it is a user, it is the user's ID, such as `6343b98b7cfxxx9366e9b7c`
- If it is a role, it is the role's code, such as `admin`
- If it is a group, it is the group's code, such as `developer`
- If it is a department, it is the department's ID, such as `6343bafc019xxxx889206c4c`
        
            namespace (str): The code of the permission group (permission space)
            resourceType (str): Limited resource type, such as data, API, button, menu
            resourceList (str): Limited list of resources to be queried. If specified, only the specified list of resources will be returned.

The resourceList parameter supports prefix matching, for example:
- Authorized a resource as `books:123`, you can match it with `books:*`;
- Authorized a resource as `books:fictions_123`, you can match it with `books:fictions_`;

            withDenied (bool): Whether to get denied resources
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-authorized-resources',
            params={
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'namespace': namespace,
                'resourceType': resource_type,
                'resourceList': resource_list,
                'withDenied': with_denied,
            },
        )

    def is_action_allowed(self, user_id, action, resource, namespace=None):
        """Determine if a user has permission to perform a certain action on a resource

        Determine if a user has permission to perform a certain action on a resource.

        Attributes:
            user_id (str): User ID
            action (str): The action corresponding to the resource
            resource (str): Resource identifier
            namespace (str): The code of the permission group (permission space)
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/is-action-allowed',
            json={
                'userId': user_id,
                'action': action,
                'resource': resource,
                'namespace': namespace,
            },
        )

    def get_resource_authorized_targets(self, resource, namespace=None, target_type=None, page=None, limit=None):
        """Get the subjects authorized for a resource

        Get the subjects authorized for a resource

        Attributes:
            resource (str): Resource
            namespace (str): Permission group
            target_type (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-resource-authorized-targets',
            json={
                'resource': resource,
                'namespace': namespace,
                'targetType': target_type,
                'page': page,
                'limit': limit,
            },
        )

    def get_user_action_logs(self, request_id=None, client_ip=None, event_type=None, user_id=None, app_id=None,
                             start=None, end=None, success=None, pagination=None):
        """Get user action logs

        You can choose request ID, client IP, user ID, app ID, start timestamp, whether the request is successful, and pagination parameters to get user action logs

        Attributes:
            request_id (str): Request ID
            client_ip (str): Client IP
            event_type (str): Event type, a series of operations by the user, such as login, logout, register, verifyMfa, etc.
            user_id (str): User ID
            app_id (str): App ID
            start (int): Start timestamp
            end (int): End timestamp
            success (bool): Whether the request is successful
            pagination (dict): Pagination
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-action-logs',
            json={
                'requestId': request_id,
                'clientIp': client_ip,
                'eventType': event_type,
                'userId': user_id,
                'appId': app_id,
                'start': start,
                'end': end,
                'success': success,
                'pagination': pagination,
            },
        )

    def get_admin_audit_logs(self, request_id=None, client_ip=None, operation_type=None, resource_type=None,
                             user_id=None, success=None, start=None, end=None, pagination=None):
        """Get administrator operation logs

        You can choose request ID, client IP, operation type, resource type, administrator user ID, whether the request is successful, start timestamp, end timestamp, and pagination to get the administrator operation log interface

        Attributes:
            request_id (str): Request ID
            client_ip (str): Client IP
            operation_type (str): Operation type, such as create, update, delete, login, etc.
            resource_type (str): Resource type, such as DATA, API, BUTTON, etc.
            user_id (str): Administrator user ID
            success (bool): Whether the request is successful
            start (int): Start timestamp
            end (int): End timestamp
            pagination (dict): Pagination
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-admin-audit-logs',
            json={
                'requestId': request_id,
                'clientIp': client_ip,
                'operationType': operation_type,
                'resourceType': resource_type,
                'userId': user_id,
                'success': success,
                'start': start,
                'end': end,
                'pagination': pagination,
            },
        )

    def get_email_templates(self, ):
        """Get the list of email templates

        Get the list of email templates

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-email-templates',
        )

    def update_email_template(self, content, sender, subject, name, customize_enabled, type, expires_in=None,
                              redirect_to=None, tpl_engine=None):
        """Modify the email template

        Modify the email template

        Attributes:
            content (str): Email content template
            sender (str): Email sender name
            subject (str): Email subject
            name (str): Email template name
            customize_enabled (bool): Whether to enable custom template
            type (str): Template type:
- `WELCOME_EMAIL`: Welcome email
- `FIRST_CREATED_USER`: First create user notification
- `REGISTER_VERIFY_CODE`: Register verification code
- `LOGIN_VERIFY_CODE`: Login verification code
- `MFA_VERIFY_CODE`: MFA verification code
- `INFORMATION_COMPLETION_VERIFY_CODE`: Register information completion verification code
- `FIRST_EMAIL_LOGIN_VERIFY`: First email login verification
- `CONSOLE_CONDUCTED_VERIFY`: Email verification initiated in the console
- `USER_PASSWORD_UPDATE_REMIND`: User expiration reminder
- `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: Administrator reset user password successful notification
- `USER_PASSWORD_RESET_NOTIFICATION`: User password reset successful notification
- `RESET_PASSWORD_VERIFY_CODE`: Reset password verification code
- `SELF_UNLOCKING_VERIFY_CODE`: Self-unlocking verification code
- `EMAIL_BIND_VERIFY_CODE`: Bind email verification code
- `EMAIL_UNBIND_VERIFY_CODE`: Unbind email verification code
    
            expires_in (int): Verification code/email expiration time, only verification class emails have expiration time.
            redirect_to (str): The address to jump to after completing the email verification, only valid for the `FIRST_EMAIL_LOGIN_VERIFY` and `CONSOLE_CONDUCTED_VERIFY` types of templates.
            tpl_engine (str): Template rendering engine. GenAuth email templates currently support two rendering engines:
- `handlebar`: For detailed usage, please see: [handlebars official documentation](https://handlebarsjs.com/)
- `ejs`: For detailed usage, please see: [ejs official documentation](https://ejs.co/)

By default, `handlerbar` will be used as the template rendering engine.
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-email-template',
            json={
                'content': content,
                'sender': sender,
                'subject': subject,
                'name': name,
                'customizeEnabled': customize_enabled,
                'type': type,
                'expiresIn': expires_in,
                'redirectTo': redirect_to,
                'tplEngine': tpl_engine,
            },
        )

    def preview_email_template(self, type, content=None, subject=None, sender=None, expires_in=None, tpl_engine=None):
        """Preview the email template

        Preview the email template

        Attributes:
            type (str): Template type:
- `WELCOME_EMAIL`: Welcome email
- `FIRST_CREATED_USER`: First create user notification
- `REGISTER_VERIFY_CODE`: Register verification code
- `LOGIN_VERIFY_CODE`: Login verification code
- `MFA_VERIFY_CODE`: MFA verification code
- `INFORMATION_COMPLETION_VERIFY_CODE`: Register information completion verification code
- `FIRST_EMAIL_LOGIN_VERIFY`: First email login verification
- `CONSOLE_CONDUCTED_VERIFY`: Email verification initiated in the console
- `USER_PASSWORD_UPDATE_REMIND`: User expiration reminder
- `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: Administrator reset user password successful notification
- `USER_PASSWORD_RESET_NOTIFICATION`: User password reset successful notification
- `RESET_PASSWORD_VERIFY_CODE`: Reset password verification code
- `SELF_UNLOCKING_VERIFY_CODE`: Self-unlocking verification code
- `EMAIL_BIND_VERIFY_CODE`: Bind email verification code
- `EMAIL_UNBIND_VERIFY_CODE`: Unbind email verification code
    
            content (str): Email content template, optional, if not passed, the email template configured in the user pool will be used for rendering.
            subject (str): Email subject, optional, if not passed, the email template configured in the user pool will be used for rendering.
            sender (str): Email sender name, optional, if not passed, the email template configured in the user pool will be used for rendering.
            expires_in (int): Verification code/email expiration time, only verification class emails have expiration time. Optional, if not passed, the email template configured in the user pool will be used for rendering.
            tpl_engine (str): Template rendering engine. GenAuth email templates currently support two rendering engines:
- `handlebar`: For detailed usage, please see: [handlebars official documentation](https://handlebarsjs.com/)
- `ejs`: For detailed usage, please see: [ejs official documentation](https://ejs.co/)

By default, `handlerbar` will be used as the template rendering engine.
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/preview-email-template',
            json={
                'type': type,
                'content': content,
                'subject': subject,
                'sender': sender,
                'expiresIn': expires_in,
                'tplEngine': tpl_engine,
            },
        )

    def get_email_provider(self, ):
        """Get third-party email service configuration

        Get third-party email service configuration

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-email-provider',
        )

    def config_email_provider(self, type, enabled, smtp_config=None, send_grid_config=None, ali_exmail_config=None,
                              tencent_exmail_config=None):
        """Configure third-party email service

        Configure third-party email service

        Attributes:
            type (str): Third-party email service provider type:
- `custom`: Custom SMTP email service
- `ali`: [Ali Enterprise Mail](https://www.ali-exmail.cn/Land/)
- `qq`: [Tencent Enterprise Mail](https://work.weixin.qq.com/mail/)
- `sendgrid`: [SendGrid Email Service](https://sendgrid.com/)
    
            enabled (bool): Whether to enable, if not enabled, the built-in email service of GenAuth will be used by default
            smtp_config (dict): SMTP email service configuration
            send_grid_config (dict): SendGrid email service configuration
            ali_exmail_config (dict): Ali enterprise email service configuration
            tencent_exmail_config (dict): Tencent enterprise email service configuration
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/config-email-provider',
            json={
                'type': type,
                'enabled': enabled,
                'smtpConfig': smtp_config,
                'sendGridConfig': send_grid_config,
                'aliExmailConfig': ali_exmail_config,
                'tencentExmailConfig': tencent_exmail_config,
            },
        )

    def get_application(self, app_id):
        """Get application details

        Get application details by application ID.

        Attributes:
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application',
            params={
                'appId': app_id,
            },
        )

    def detail_auth_subject(self, target_id, target_type, app_id):
        """Subject authorization details

        Subject authorization details

        Attributes:
            targetId (str): Subject id
            targetType (str): Subject type
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-subject-auth-detail',
            params={
                'targetId': target_id,
                'targetType': target_type,
                'appId': app_id,
            },
        )

    def list_auth_subject(self, target_type, target_id, app_name=None, app_type_list=None, effect=None, enabled=None):
        """Subject authorization list

        Subject authorization list

        Attributes:
            target_type (str): Subject type
            target_id (str): Subject id
            app_name (str): Application name
            app_type_list (list): Application type list
            effect (list): Operation type list
            enabled (bool): Switch
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-subject-auth',
            json={
                'targetType': target_type,
                'targetId': target_id,
                'appName': app_name,
                'appTypeList': app_type_list,
                'effect': effect,
                'enabled': enabled,
            },
        )

    def list_auth_application(self, app_id, page=None, limit=None, target_name=None, target_type_list=None, effect=None,
                              enabled=None):
        """Application authorization list

        Application authorization list

        Attributes:
            app_id (str): Application ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            target_name (str): Subject name
            target_type_list (list): Subject type list, USER/ORG/ROLE/GROUP
            effect (str): Operation, ALLOW/DENY
            enabled (bool): Authorization switch,
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-applications-auth',
            json={
                'appId': app_id,
                'page': page,
                'limit': limit,
                'targetName': target_name,
                'targetTypeList': target_type_list,
                'effect': effect,
                'enabled': enabled,
            },
        )

    def enabled_auth(self, enabled, id):
        """Update authorization switch

        Update authorization switch

        Attributes:
            enabled (bool): Authorization switch,
            id (str): Authorization ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-auth-enabled',
            json={
                'enabled': enabled,
                'id': id,
            },
        )

    def delete_auth(self, auth_ids):
        """Batch delete application authorization

        Batch delete application authorization

        Attributes:
            authIds (str): Authorization ID
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/batch-applications-auth',
            params={
                'authIds': auth_ids,
            },
        )

    def list_applications(self, page=None, limit=None, is_integrate_app=None, is_self_built_app=None, sso_enabled=None,
                          keywords=None, all=None):
        """Get application list

        Get application list

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            isIntegrateApp (bool): Whether it is an integrated application
            isSelfBuiltApp (bool): Whether it is a self-built application
            ssoEnabled (bool): Whether single sign-on is enabled
            keywords (str): Fuzzy search string
            all (bool): Search application, true: search all applications, default is false
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-applications',
            params={
                'page': page,
                'limit': limit,
                'isIntegrateApp': is_integrate_app,
                'isSelfBuiltApp': is_self_built_app,
                'ssoEnabled': sso_enabled,
                'keywords': keywords,
                'all': all,
            },
        )

    def get_application_simple_info(self, app_id):
        """Get application simple information

        Get application simple information by application ID.

        Attributes:
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-simple-info',
            params={
                'appId': app_id,
            },
        )

    def list_application_simple_info(self, page=None, limit=None, is_integrate_app=None, is_self_built_app=None,
                                     sso_enabled=None, keywords=None):
        """Get application simple information list

        Get application simple information list

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            isIntegrateApp (bool): Whether it is an integrated application
            isSelfBuiltApp (bool): Whether it is a self-built application
            ssoEnabled (bool): Whether single sign-on is enabled
            keywords (str): Fuzzy search string
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-application-simple-info',
            params={
                'page': page,
                'limit': limit,
                'isIntegrateApp': is_integrate_app,
                'isSelfBuiltApp': is_self_built_app,
                'ssoEnabled': sso_enabled,
                'keywords': keywords,
            },
        )

    def create_application(self, app_name, template=None, template_data=None, app_identifier=None, app_logo=None,
                           app_description=None, app_type=None, default_protocol=None, redirect_uris=None,
                           logout_redirect_uris=None, init_login_uri=None, sso_enabled=None, oidc_config=None,
                           saml_provider_enabled=None, saml_config=None, oauth_provider_enabled=None, oauth_config=None,
                           cas_provider_enabled=None, cas_config=None, login_config=None, register_config=None,
                           branding_config=None):
        """Create application

        Create application

        Attributes:
            app_name (str): Application name
            template (str): Integrated application template type, **required for integrated applications**. Integrated applications only need to fill in the `template` and `templateData` fields, and other fields will be ignored.
            template_data (str): Integrated application configuration information, **required for integrated applications**.
            app_identifier (str): Application unique identifier, **required for self-built applications**.
            app_logo (str): Application Logo link
            app_description (str): Application description information
            app_type (str): Application type
            default_protocol (str): Default application protocol type
            redirect_uris (list): Application login callback address
            logout_redirect_uris (list): Application logout callback address
            init_login_uri (str): Initiate login address: click "Experience Login" in the GenAuth application details or click the application icon in the application panel, will jump to this URL, default is the GenAuth login page.
            sso_enabled (bool): Whether to enable SSO single sign-on
            oidc_config (dict): OIDC protocol configuration
            saml_provider_enabled (bool): Whether to enable SAML identity provider
            saml_config (dict): SAML protocol configuration
            oauth_provider_enabled (bool): Whether to enable OAuth identity provider
            oauth_config (dict): OAuth2.0 protocol configuration. **Important note** It is no longer recommended to use OAuth2.0, it is recommended to switch to OIDC.
            cas_provider_enabled (bool): Whether to enable CAS identity provider
            cas_config (dict): CAS protocol configuration
            login_config (dict): Login configuration
            register_config (dict): Registration configuration
            branding_config (dict): Branding configuration
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-application',
            json={
                'appName': app_name,
                'template': template,
                'templateData': template_data,
                'appIdentifier': app_identifier,
                'appLogo': app_logo,
                'appDescription': app_description,
                'appType': app_type,
                'defaultProtocol': default_protocol,
                'redirectUris': redirect_uris,
                'logoutRedirectUris': logout_redirect_uris,
                'initLoginUri': init_login_uri,
                'ssoEnabled': sso_enabled,
                'oidcConfig': oidc_config,
                'samlProviderEnabled': saml_provider_enabled,
                'samlConfig': saml_config,
                'oauthProviderEnabled': oauth_provider_enabled,
                'oauthConfig': oauth_config,
                'casProviderEnabled': cas_provider_enabled,
                'casConfig': cas_config,
                'loginConfig': login_config,
                'registerConfig': register_config,
                'brandingConfig': branding_config,
            },
        )

    def delete_application(self, app_id):
        """Delete application

        Delete application by application ID.

        Attributes:
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-application',
            json={
                'appId': app_id,
            },
        )

    def get_application_secret(self, app_id):
        """Get application secret

        Get application secret

        Attributes:
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-secret',
            params={
                'appId': app_id,
            },
        )

    def refresh_application_secret(self, app_id):
        """Refresh application secret

        Refresh application secret

        Attributes:
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/refresh-application-secret',
            json={
                'appId': app_id,
            },
        )

    def list_application_active_users(self, app_id, options=None):
        """Get current logged-in users of the application

        Get users who are currently logged in to the application

        Attributes:
            app_id (str): Application ID
            options (dict): Optional
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-application-active-users',
            json={
                'appId': app_id,
                'options': options,
            },
        )

    def get_application_permission_strategy(self, app_id):
        """Get the default access authorization strategy of the application

        Get the default access authorization strategy of the application

        Attributes:
            appId (str): Application ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-permission-strategy',
            params={
                'appId': app_id,
            },
        )

    def update_application_permission_strategy(self, permission_strategy, app_id):
        """Update the default access authorization strategy of the application

        Update the default access authorization strategy of the application

        Attributes:
            permission_strategy (str): Application access authorization strategy
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-application-permission-strategy',
            json={
                'permissionStrategy': permission_strategy,
                'appId': app_id,
            },
        )

    def authorize_application_access(self, app_id, list):
        """Authorize application access

        Authorize application access to users, groups, organizations or roles. If the user, group, organization or role does not exist, skip it and authorize the next step without returning an error.

        Attributes:
            app_id (str): Application ID
            list (list): Authorization subject list, up to 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-application-access',
            json={
                'appId': app_id,
                'list': list,
            },
        )

    def revoke_application_access(self, app_id, list):
        """Delete application access authorization record

        Cancel the application access authorization of users, groups, organizations or roles. If the passed data does not exist, the data is not returned and no error is reported.

        Attributes:
            app_id (str): Application ID
            list (list): Authorization subject list, up to 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-application-access',
            json={
                'appId': app_id,
                'list': list,
            },
        )

    def check_domain_available(self, domain):
        """Check if the domain is available

        Check if the domain is available for creating a new application or updating the application domain

        Attributes:
            domain (str): Domain
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-domain-available',
            json={
                'domain': domain,
            },
        )

    def list_tenant_applications(self, page, limit, keywords, sso_enabled):
        """Get tenant application list

        Get the application list, you can specify the tenant ID for filtering.

        Attributes:
            page (str): Page number to get the application list
            limit (str): Number of applications to get per page
            keywords (str): Search keyword
            sso_enabled (bool): Whether the application is included in single sign-on
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-applications',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
                'sso_enabled': sso_enabled,
            },
        )

    def update_login_page_config(self, update):
        """Update application login page configuration

        Update the login page configuration by application ID.

        Attributes:
            update (dict): Application login configuration update content
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-login-page-config',
            json={
                'update': update,
            },
        )

    def userpoll_tenant_config(self, ):
        """Get user pool tenant configuration information

        Get user pool multi-tenant configuration information based on user pool ID

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/userpool-tenant-config',
        )

    def update_user_pool_tenant_config(self, update):
        """Update user pool tenant configuration information

        Update the login information in the user pool multi-tenant configuration

        Attributes:
            update (dict): Application login configuration update content
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-userpool-tenant-config',
            json={
                'update': update,
            },
        )

    def update_tenant_qr_code_state(self, enabled):
        """Update tenant console QR code login status

        Update tenant console QR code login status

        Attributes:
            enabled (bool): Whether to allow QR code login
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-userpool-tenant-appqrcode-state',
            json={
                'enabled': enabled,
            },
        )

    def change_userpool_tenan_ext_idp_conn_state(self, enabled, conn_ids):
        """Set user pool multi-tenant identity source connection

        Set user pool multi-tenant identity source connection, support setting multiple identity source connections at the same time, support setting and canceling connections

        Attributes:
            enabled (bool): Whether to enable identity source connection
            conn_ids (list): Identity source connection ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-userpool-tenant-ext-idp-conn-state',
            json={
                'enabled': enabled,
                'connIds': conn_ids,
            },
        )

    def update_application_mfa_settings(self, app_id, enabled_factors=None, disabled_factors=None):
        """Update application MFA settings

        Pass in a list of MFA authentication factors to enable or disable

        Attributes:
            app_id (str): Application ID
            enabled_factors (list): List of MFA authentication factors to enable
            disabled_factors (list): List of MFA authentication factors to disable
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-application-mfa-settings',
            json={
                'appId': app_id,
                'enabledFactors': enabled_factors,
                'disabledFactors': disabled_factors,
            },
        )

    def get_mfa_trigger_data(self, app_id, user_id, user_id_type=None):
        """Get MFA trigger data for users under the application

        Get MFA trigger data for users under the application.

        Attributes:
            appId (str): Application ID
            userId (str): User unique identifier, can be user ID, username, email, phone number, external ID, ID in external identity source.
            userIdType (str): User ID type, default value is `user_id`, optional values are:
- `user_id`: GenAuth user ID, such as `6319a1504f3xxxxf214dd5b7`
- `phone`: User phone number
- `email`: User email
- `username`: User name
- `external_id`: User's ID in the external system, corresponding to the `externalId` field of GenAuth user information
- `identity`: User's external identity source information, in the format of `<extIdpId>:<userIdInIdp>`, where `<extIdpId>` is the ID of the GenAuth identity source, and `<userIdInIdp>` is the user's ID in the external identity source.
Example: `62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`.
- `sync_relation`: User's external identity source information, in the format of `<provier>:<userIdInIdp>`, where `<provier>` is the synchronized identity source type, such as wechatwork, lark; `<userIdInIdp>` is the user's ID in the external identity source.
Example: `lark:ou_8bae746eac07cd2564654140d2a9ac61`.

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mfa-trigger-data',
            params={
                'appId': app_id,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def create_asa_account(self, account_info, app_id):
        """Create ASA account

        Create an ASA account under a certain application

        Attributes:
            account_info (dict): Account information, usually a key-value pair containing "account" and "password"
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-asa-account',
            json={
                'accountInfo': account_info,
                'appId': app_id,
            },
        )

    def create_asa_account_batch(self, list, app_id):
        """Batch create ASA accounts

        Batch create ASA accounts under a certain application

        Attributes:
            list (list): Account list
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-asa-accounts-batch',
            json={
                'list': list,
                'appId': app_id,
            },
        )

    def update_asa_account(self, account_info, account_id, app_id):
        """Update ASA account

        Update the information of a certain ASA account

        Attributes:
            account_info (dict): Account information, usually a key-value pair containing "account" and "password"
            account_id (str): ASA account ID
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-asa-account',
            json={
                'accountInfo': account_info,
                'accountId': account_id,
                'appId': app_id,
            },
        )

    def list_asa_account(self, app_id, page=None, limit=None):
        """Get ASA account list

        Paginate to get the ASA account list under a certain application

        Attributes:
            appId (str): Application ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-asa-accounts',
            params={
                'appId': app_id,
                'page': page,
                'limit': limit,
            },
        )

    def get_asa_account(self, app_id, account_id):
        """Get ASA account

        Get detailed information of an ASA account based on the ASA account ID

        Attributes:
            appId (str): Application ID
            accountId (str): ASA account ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-asa-account',
            params={
                'appId': app_id,
                'accountId': account_id,
            },
        )

    def get_asa_account_batch(self, account_ids, app_id):
        """Batch get ASA accounts

        Batch get detailed information of ASA accounts based on a list of ASA account IDs

        Attributes:
            account_ids (list): List of ASA account IDs
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-asa-accounts-batch',
            json={
                'accountIds': account_ids,
                'appId': app_id,
            },
        )

    def delete_asa_account(self, account_id, app_id):
        """Delete ASA account

        Delete an ASA account by ASA account ID

        Attributes:
            account_id (str): ASA account ID
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-asa-account',
            json={
                'accountId': account_id,
                'appId': app_id,
            },
        )

    def delete_asa_account_batch(self, account_ids, app_id):
        """Batch delete ASA accounts

        Batch delete ASA accounts by a list of ASA account IDs

        Attributes:
            account_ids (list): List of ASA account IDs
            app_id (str): Application ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-asa-accounts-batch',
            json={
                'accountIds': account_ids,
                'appId': app_id,
            },
        )

    def assign_asa_account(self, app_id, account_id, targets):
        """Assign ASA account

        Assign an ASA account to a user, organization, group, or role

        Attributes:
            app_id (str): Application ID
            account_id (str): Account ID to be associated
            targets (list): List of associated objects
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-asa-account',
            json={
                'appId': app_id,
                'accountId': account_id,
                'targets': targets,
            },
        )

    def unassign_asa_account(self, app_id, account_id, targets):
        """Unassign ASA account

        Unassign an ASA account assigned to a user, organization, group, or role

        Attributes:
            app_id (str): Application ID
            account_id (str): Account ID to be associated
            targets (list): List of associated objects
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unassign-asa-account',
            json={
                'appId': app_id,
                'accountId': account_id,
                'targets': targets,
            },
        )

    def get_asa_account_assigned_targets(self, app_id, account_id, page=None, limit=None):
        """Get the list of subjects assigned to the ASA account

        Paginate to get the list of subjects to which the account has been assigned

        Attributes:
            appId (str): Application ID
            accountId (str): ASA account ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-asa-account-assigned-targets',
            params={
                'appId': app_id,
                'accountId': account_id,
                'page': page,
                'limit': limit,
            },
        )

    def get_assigned_account(self, app_id, target_type, target_identifier):
        """Get the ASA account assigned to the subject

        Get the ASA account directly assigned to the subject based on the subject type and identifier

        Attributes:
            appId (str): Application ID
            targetType (str): Target object type:
- `USER`: User
- `ROLE`: Role
- `GROUP`: Group
    
            targetIdentifier (str): The unique identifier of the target object:
- If it is a user, it is the user's ID, such as `6343b98b7cfxxx9366e9b7c`
- If it is a role, it is the role's code, such as `admin`
- If it is a group, it is the group's code, such as `developer`
- If it is a department, it is the department's ID, such as `6343bafc019xxxx889206c4c`
        
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-assigned-account',
            params={
                'appId': app_id,
                'targetType': target_type,
                'targetIdentifier': target_identifier,
            },
        )

    def get_security_settings(self, ):
        """Get security settings

        Get security settings without parameters

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-security-settings',
        )

    def update_security_settings(self, allowed_origins=None, genauth_token_expires_in=None, verify_code_length=None,
                                 verify_code_max_attempts=None, change_email_strategy=None, change_phone_strategy=None,
                                 cookie_settings=None, register_disabled=None, register_anomaly_detection=None,
                                 complete_password_after_pass_code_login=None, login_anomaly_detection=None,
                                 login_require_email_verified=None, self_unlock_account=None,
                                 enable_login_account_switch=None, qrcode_login_strategy=None):
        """Update security settings

        Optional security domain, GenAuth Token expiration time (seconds), verification code length, verification code attempt times, user change email security strategy, user change phone security strategy, Cookie expiration time setting, whether to disable user registration, frequent registration detection configuration, whether to require users to set passwords after registering with verification code, whether to prohibit login and send authentication emails when unverified email is used for login, user self-unlock configuration, whether to enable login account selection on the GenAuth login page, and APP scan code login security configuration

        Attributes:
            allowed_origins (list): Security domain (CORS)
            genauth_token_expires_in (int): GenAuth Token expiration time (seconds)
            verify_code_length (int): Verification code length. Includes SMS verification code, email verification code, and graphic verification code.
            verify_code_max_attempts (int): Verification code attempt times. If the user enters the verification code incorrectly more than this threshold within a verification code validity period (default is 60 s), the current verification code will be invalidated and need to be resent.
            change_email_strategy (dict): User change email security strategy
            change_phone_strategy (dict): User change phone security strategy
            cookie_settings (dict): Cookie expiration time setting
            register_disabled (bool): Whether to disable user registration. After enabling, users will not be able to register on their own, and only administrators can create accounts for them. For B2B and B2E type user pools, the default is enabled.
            register_anomaly_detection (dict): Frequent registration detection configuration
            complete_password_after_pass_code_login (bool): Whether to require users to set passwords after registering with verification code (only for GenAuth login page and Guard, not for API calls).
            login_anomaly_detection (dict): Login anti-brute force configuration
            login_require_email_verified (bool): Whether to prohibit login and send authentication emails when unverified email is used for login. After the user receives the email and completes the verification, they can log in.
            self_unlock_account (dict): User self-unlock configuration. Note: Only users with bound phone/email can self-unlock
            enable_login_account_switch (bool): Whether to enable login account selection on the GenAuth login page
            qrcode_login_strategy (dict): APP scan code login security configuration
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-security-settings',
            json={
                'allowedOrigins': allowed_origins,
                'genauthTokenExpiresIn': genauth_token_expires_in,
                'verifyCodeLength': verify_code_length,
                'verifyCodeMaxAttempts': verify_code_max_attempts,
                'changeEmailStrategy': change_email_strategy,
                'changePhoneStrategy': change_phone_strategy,
                'cookieSettings': cookie_settings,
                'registerDisabled': register_disabled,
                'registerAnomalyDetection': register_anomaly_detection,
                'completePasswordAfterPassCodeLogin': complete_password_after_pass_code_login,
                'loginAnomalyDetection': login_anomaly_detection,
                'loginRequireEmailVerified': login_require_email_verified,
                'selfUnlockAccount': self_unlock_account,
                'enableLoginAccountSwitch': enable_login_account_switch,
                'qrcodeLoginStrategy': qrcode_login_strategy,
            },
        )

    def get_global_mfa_settings(self, ):
        """Get global MFA settings

        Get global MFA settings without parameters

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-global-mfa-settings',
        )

    def update_global_mfa_settings(self, enabled_factors):
        """Update global MFA settings

        Pass in a list of MFA authentication factors to enable,

        Attributes:
            enabled_factors (list): List of MFA authentication factors to enable
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-global-mfa-settings',
            json={
                'enabledFactors': enabled_factors,
            },
        )

    def create_tenant(self, name, app_ids, logo=None, description=None, reject_hint=None, source_app_id=None,
                      enterprise_domains=None, expire_time=None, mau_amount=None, member_amount=None,
                      admin_amount=None):
        """Create Tenant

        Create a tenant with the specified parameters.

        Attributes:
            name (str): Tenant name
            app_ids (list): List of app IDs associated with the tenant
            logo (list): Tenant logo
            description (str): Tenant description
            reject_hint (str): Prompt text displayed when a user is rejected from logging in to the tenant
            source_app_id (str): ID of the source app of the tenant, when this value does not exist, it means that the tenant source is the GenAuth console
            enterprise_domains (list): List of enterprise email domains
            expire_time (str): Tenant expiration time
            mau_amount (int): Maximum monthly active users (MAU) for the tenant
            member_amount (int): Maximum number of members for the tenant
            admin_amount (int): Maximum number of administrators for the tenant
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant',
            json={
                'name': name,
                'appIds': app_ids,
                'logo': logo,
                'description': description,
                'rejectHint': reject_hint,
                'sourceAppId': source_app_id,
                'enterpriseDomains': enterprise_domains,
                'expireTime': expire_time,
                'mauAmount': mau_amount,
                'memberAmount': member_amount,
                'adminAmount': admin_amount,
            },
        )

    def update_tenant(self, tenant_id, name=None, app_ids=None, logo=None, description=None, reject_hint=None,
                      source_app_id=None):
        """Update Tenant

        Update the basic information of a tenant.

        Attributes:
            tenant_id (str): Tenant ID
            name (str): Tenant name
            app_ids (list): List of app IDs associated with the tenant
            logo (list): Tenant logo
            description (str): Tenant description
            reject_hint (str): Prompt text displayed when a user is rejected from logging in to the tenant
            source_app_id (str): ID of the source app of the tenant, when this value does not exist, it means that the tenant source is the GenAuth console
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-tenant',
            json={
                'tenantId': tenant_id,
                'name': name,
                'appIds': app_ids,
                'logo': logo,
                'description': description,
                'rejectHint': reject_hint,
                'sourceAppId': source_app_id,
            },
        )

    def delete_tenant(self, tenant_id):
        """Delete Tenant

        Delete a tenant by its ID.

        Attributes:
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant',
            json={
                'tenantId': tenant_id,
            },
        )

    def list_tenants(self, keywords=None, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                     with_source_app_detail=None, page=None, limit=None, source=None):
        """List Tenants

        List all tenants, support fuzzy search.

        Attributes:
            keywords (str): Search keywords
            withMembersCount (bool): Whether to include the number of members in the tenant
            withAppDetail (bool): Whether to include simple information about the apps associated with the tenant
            withCreatorDetail (bool): Whether to include simple information about the creator of the tenant
            withSourceAppDetail (bool): Whether to include simple information about the source app of the tenant
            page (str): Page number
            limit (str): Number of items per page
            source (): Tenant source
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenants',
            params={
                'keywords': keywords,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
                'page': page,
                'limit': limit,
                'source': source,
            },
        )

    def get_tenant_little_info(self, tenant_id, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                               with_source_app_detail=None):
        """Get Tenant Little Info

        Get some basic information about a tenant by its ID.

        Attributes:
            tenantId (str): Tenant ID
            withMembersCount (bool): Whether to include the number of members in the tenant
            withAppDetail (bool): Whether to include simple information about the apps associated with the tenant
            withCreatorDetail (bool): Whether to include simple information about the creator of the tenant
            withSourceAppDetail (bool): Whether to include simple information about the source app of the tenant
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-little-info',
            params={
                'tenantId': tenant_id,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
            },
        )

    def get_tenant(self, tenant_id, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                   with_source_app_detail=None):
        """Get Tenant

        Get detailed information about a tenant by its ID.

        Attributes:
            tenantId (str): Tenant ID
            withMembersCount (bool): Whether to include the number of members in the tenant
            withAppDetail (bool): Whether to include simple information about the apps associated with the tenant
            withCreatorDetail (bool): Whether to include simple information about the creator of the tenant
            withSourceAppDetail (bool): Whether to include simple information about the source app of the tenant
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant',
            params={
                'tenantId': tenant_id,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
            },
        )

    def import_tenant(self, excel_url):
        """Import Tenant

        Import tenants from an Excel file.

        Attributes:
            excel_url (str): URL of the Excel file
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/import-tenant',
            json={
                'excelUrl': excel_url,
            },
        )

    def import_tenant_history(self, page=None, limit=None):
        """Import Tenant History

        Query the import history of tenants from an Excel file.

        Attributes:
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/import-tenant-history',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def import_tenant_notify_user(self, import_id, page=None, limit=None):
        """Import Tenant Notify User

        Query the list of users notified during the tenant import.

        Attributes:
            importId (str): Import record ID
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/import-tenant-notify-user',
            params={
                'importId': import_id,
                'page': page,
                'limit': limit,
            },
        )

    def send_email_batch(self, admin_name, import_id, users):
        """Send Email Batch

        Send batch email notifications.

        Attributes:
            admin_name (str): Administrator name
            import_id (int): Import ID
            users (list): List of users to be notified by email
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-email-batch',
            json={
                'adminName': admin_name,
                'importId': import_id,
                'users': users,
            },
        )

    def send_sms_batch(self, admin_name, import_id, users):
        """Send SMS Batch

        Send batch SMS notifications.

        Attributes:
            admin_name (str): Administrator name
            import_id (int): Import ID
            users (list): List of users to be notified by SMS
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-sms-batch',
            json={
                'adminName': admin_name,
                'importId': import_id,
                'users': users,
            },
        )

    def list_tenant_admin(self, tenant_id, keywords=None, page=None, limit=None):
        """List Tenant Admin

        List all administrators of a tenant, support fuzzy search.

        Attributes:
            tenant_id (str): Tenant ID
            keywords (str): Search keywords
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-tenant-admin',
            json={
                'tenantId': tenant_id,
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def set_tenant_admin(self, tenant_id, link_user_ids=None, member_ids=None):
        """Set Tenant Admin

        Set the administrators of a tenant by user ID or tenant member ID.

        Attributes:
            tenant_id (str): Tenant ID
            link_user_ids (list): List of user IDs associated with the tenant
            member_ids (list): List of tenant member IDs
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-tenant-admin',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def delete_tenant_admin(self, tenant_id, link_user_id=None, member_id=None):
        """Delete Tenant Admin

        Remove the administrator role from a user by user ID or tenant member ID.

        Attributes:
            tenant_id (str): Tenant ID
            link_user_id (str): User ID associated with the tenant
            member_id (str): Tenant member ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant-admin',
            json={
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def delete_tenant_user(self, tenant_id, link_user_ids=None, member_ids=None):
        """Delete Tenant User

        Remove a user from a tenant by user ID or tenant member ID.

        Attributes:
            tenant_id (str): Tenant ID
            link_user_ids (list): List of user IDs associated with the tenant
            member_ids (list): List of tenant member IDs
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant-user',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def generate_invite_tenant_user_link(self, validity_term, emails, app_id, tenant_id=None):
        """Generate Invite Tenant User Link

        Generate a link to invite a user to a tenant.

        Attributes:
            validity_term (str): Link validity period
            emails (list): List of user emails to be invited
            app_id (str): ID of the app to be accessed after the user successfully registers
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/generate-invite-tenant-user-link',
            json={
                'validityTerm': validity_term,
                'emails': emails,
                'appId': app_id,
                'tenantId': tenant_id,
            },
        )

    def list_invite_tennat_user_records(self, keywords, page, limit):
        """List Invite Tenant User Records

        List all the records of users invited to a tenant.

        Attributes:
            keywords (str): Search keywords
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-invite-tenant-user-records',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def list_multiple_tenant_admin(self, keywords=None, page=None, limit=None):
        """List Multiple Tenant Admin

        List all users who have multiple tenant management permissions in a user pool.

        Attributes:
            keywords (str): Search keywords
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-multiple-tenant-admins',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def create_multiple_tenant_admin(self, tenant_ids, user_id, api_authorized=None, send_phone_notification=None,
                                     send_email_notification=None):
        """Create Multiple Tenant Admin

        Create a user pool with multiple tenant management permissions based on user ID

        Attributes:
            tenant_ids (list): Tenant ID
            user_id (str): User ID
            api_authorized (bool): Whether to authorize
            send_phone_notification (bool): SMS notification
            send_email_notification (bool): Email notification
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-multiple-tenant-admin',
            json={
                'tenantIds': tenant_ids,
                'userId': user_id,
                'apiAuthorized': api_authorized,
                'sendPhoneNotification': send_phone_notification,
                'sendEmailNotification': send_email_notification,
            },
        )

    def get_multiple_tenant_admin(self, user_id):
        """Get Multiple Tenant Admin

        Get a list of users with multiple tenant management permissions in a user pool based on user pool ID

        Attributes:
            userId (str): User ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-multiple-tenant-admin',
            params={
                'userId': user_id,
            },
        )

    def list_tenant_cooperators(self, keywords=None, external=None, page=None, limit=None):
        """List Tenant Cooperators

        Get a list of users with cooperator capabilities in a user pool based on user pool ID

        Attributes:
            keywords (str): Search keywords
            external (bool): Whether it is external
            page (str): Page number
            limit (str): Number of items per page
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-cooperators',
            params={
                'keywords': keywords,
                'external': external,
                'page': page,
                'limit': limit,
            },
        )

    def get_tenant_cooperator(self, user_id):
        """Get Tenant Cooperator

        Get a list of cooperator based on user pool ID

        Attributes:
            userId (str): User ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-cooperator',
            params={
                'userId': user_id,
            },
        )

    def get_tenant_cooperator_menu(self, user_id):
        """Get Tenant Cooperator Menu

        Get a list of cooperator based on user pool ID

        Attributes:
            userId (str): User ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-cooperator-menu',
            params={
                'userId': user_id,
            },
        )

    def create_tenant_cooperator(self, policies, user_id, api_authorized=None, send_phone_notification=None,
                                 send_email_notification=None):
        """Create Tenant Cooperator

        Create a cooperator

        Attributes:
            policies (list): Policy
            user_id (str): User ID
            api_authorized (bool): Whether to authorize API
            send_phone_notification (bool): SMS notification
            send_email_notification (bool): Email notification
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant-cooperator',
            json={
                'policies': policies,
                'userId': user_id,
                'apiAuthorized': api_authorized,
                'sendPhoneNotification': send_phone_notification,
                'sendEmailNotification': send_email_notification,
            },
        )

    def get_tenant_by_code(self, code):
        """Get Tenant Details

        Get tenant details based on tenant Code

        Attributes:
            code (str): Tenant Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-by-code',
            params={
                'code': code,
            },
        )

    def send_invite_tenant_user_email(self, ):
        """Send Invite Tenant User Email

        Send an invitation to become a tenant user to multiple email addresses

        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-invite-tenant-user-email',
            json={
            },
        )

    def add_tenant_users(self, link_user_ids, tenant_id):
        """Add Tenant Members

        Batch add tenant members based on user ID

        Attributes:
            link_user_ids (list): Associated user pool level user ID
            tenant_id (str): Tenant ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-tenant-users',
            json={
                'linkUserIds': link_user_ids,
                'tenantId': tenant_id,
            },
        )

    def remove_tenant_users(self, tenant_id, link_user_ids=None, member_ids=None):
        """Batch Remove Tenant Members

        This interface is used to batch remove tenant members based on user ID or tenant member ID.

        Attributes:
            tenant_id (str): Tenant ID
            link_user_ids (list): Associated user pool level user ID
            member_ids (list): Tenant member ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-tenant-users',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def update_tenant_user(self, updates, tenant_id, link_user_id=None, member_id=None):
        """Update Tenant Members

        This interface is used to update tenant members based on user ID or tenant member ID.

        Attributes:
            updates (dict): Information of the tenant member to be updated
            tenant_id (str): Tenant ID
            link_user_id (str): Associated user pool level user ID
            member_id (str): Tenant member ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-tenant-user',
            json={
                'updates': updates,
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def create_tenant_user(self, tenant_id, gender, email=None, phone=None, phone_country_code=None, username=None,
                           name=None, nickname=None, photo=None, birthdate=None, country=None, province=None, city=None,
                           address=None, street_address=None, postal_code=None, given_name=None, family_name=None,
                           middle_name=None, preferred_username=None, password=None, salt=None, options=None):
        """Create Tenant User

        Create a tenant member, the email, phone, and username must contain one of them, the email, phone, username, and externalId are unique within the user pool, this interface will create a user as an administrator, so there is no need to perform security checks such as phone number verification.

        Attributes:
            tenant_id (str): Tenant ID
            gender (str): Gender:
- `M`: Male, `male`
- `F`: Female, `female`
- `U`: Unknown, `unknown`
  
            email (str): Email, case insensitive
            phone (str): Phone number, without area code. If it is a foreign phone number, please specify the area code in the phoneCountryCode parameter.
            phone_country_code (str): Phone area code, the mainland China phone number can be left blank. The GenAuth SMS service does not currently support international phone numbers. You need to configure the corresponding international SMS service in the GenAuth console. The complete list of phone area codes can be found at https://en.wikipedia.org/wiki/List_of_country_calling_codes.
            username (str): Username, unique within the user pool
            name (str): User's real name, not unique
            nickname (str): Nickname
            photo (str): Avatar link
            birthdate (str): Date of birth
            country (str): Country
            province (str): Province
            city (str): City
            address (str): Address
            street_address (str): Street address
            postal_code (str): Postal code
            given_name (str): Given name
            family_name (str): Family name
            middle_name (str): Middle name
            preferred_username (str): Preferred Username
            password (str): User password, default is plaintext. We use HTTPS protocol to securely transmit the password, which can ensure security to a certain extent. If you need higher security, we also support two ways to encrypt the password, RSA256 and national standard SM2. See the `passwordEncryptType` parameter for details.
            salt (str): Salt for encrypting user passwords
            options (dict): Optional parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant-user',
            json={
                'tenantId': tenant_id,
                'gender': gender,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'preferredUsername': preferred_username,
                'password': password,
                'salt': salt,
                'options': options,
            },
        )

    def list_tenant_users(self, tenant_id, keywords=None, options=None):
        """List Tenant Users

        This interface is used to get the user list, support fuzzy search, and filter users based on user basic fields, user custom fields, user department, user historical login applications and other dimensions.

        ### Fuzzy Search Example

        Fuzzy search will default to fuzzy search users from the `phone`, `email`, `name`, `username`, `nickname` five fields, you can also decide the field range of fuzzy matching by setting `options.fuzzySearchOn`:

        ```json
        {
          "keywords": "Beijing",
          "options": {
            "fuzzySearchOn": [
              "address"
            ]
          }
        }
        ```

        ### Advanced Search Example

        You can use `advancedFilter` for advanced search, which supports filtering users based on user's basic information, custom data, department, user source, login application, external identity source information and other dimensions. **And these filtering conditions can be combined arbitrarily.**

        #### Filter users whose email contains `@example.com`

        The user's email (`email`) is a string type and can be fuzzy searched:

        ```json
        {
          "advancedFilter": [
            {
              "field": "email",
              "operator": "CONTAINS",
              "value": "@example.com"
            }
          ]
        }
        ```

        #### Filter based on the number of user logins

        Filter users with more than 10 logins:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "GREATER",
              "value": 10
            }
          ]
        }
        ```

        Filter users with 10 - 100 logins:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "BETWEEN",
              "value": [10, 100]
            }
          ]
        }
        ```

        #### Filter based on the user's last login time

        Filter users who logged in within the last 7 days:

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLoginTime",
              "operator": "GREATER",
              "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
            }
          ]
        }
        ```

        Filter users who logged in during a certain period:

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLoginTime",
              "operator": "BETWEEN",
              "value": [
                Date.now() - 14 * 24 * 60 * 60 * 1000,
                Date.now() - 7 * 24 * 60 * 60 * 1000
              ]
            }
          ]
        }
        ```

        #### Filter based on the user's previously logged in application

        Filter out users who have logged in to application `appId1` or `appId2`:

        ```json
        {
          "advancedFilter": [
            {
              "field": "loggedInApps",
              "operator": "IN",
              "value": [
                "appId1",
                "appId2"
              ]
            }
          ]
        }
        ```

  

        Attributes:
            tenant_id (str): Tenant ID
            keywords (str): Search keywords
            options (dict): Optional items
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-tenant-users',
            json={
                'tenantId': tenant_id,
                'keywords': keywords,
                'options': options,
            },
        )

    def get_tenant_user(self, tenant_id, link_user_id=None, member_id=None):
        """Get a single tenant member

        Get tenant member information based on user ID or tenant member ID

        Attributes:
            tenantId (str): Tenant ID
            linkUserId (str): User ID at the user pool level
            memberId (str): Tenant member ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-user',
            params={
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def create_permission_namespace(self, name, code, description=None):
        """Create a permission namespace

        Create a permission namespace, you can set the permission namespace name, Code and description.

        Attributes:
            name (str): Permission namespace name
            code (str): Permission namespace Code
            description (str): Permission namespace description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-permission-namespace',
            json={
                'name': name,
                'code': code,
                'description': description,
            },
        )

    def create_permission_namespaces_batch(self, list):
        """Batch create permission namespaces

        Batch create permission namespaces, you can set the permission namespace name, Code and description separately.

        Attributes:
            list (list): Permission namespace list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-permission-namespaces-batch',
            json={
                'list': list,
            },
        )

    def get_permission_namespace(self, code):
        """Get permission namespace details

        Get permission namespace details through the unique identifier (Code) of the permission namespace.

        Attributes:
            code (str): Permission namespace Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-permission-namespace',
            params={
                'code': code,
            },
        )

    def get_permission_namespaces_batch(self, codes):
        """Batch get permission namespace details list

        Get permission namespace details separately through the unique identifier (Code) of the permission namespace.

        Attributes:
            codes (str): Permission namespace code list, batch can be separated by commas
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-permission-namespaces-batch',
            params={
                'codes': codes,
            },
        )

    def list_permission_namespaces(self, page=None, limit=None, query=None):
        """Paging get permission namespace list

        Paging get permission namespace list.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Permission namespace name
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-permission-namespaces',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def update_permission_namespace(self, code, name=None, new_code=None, description=None):
        """Modify permission namespace

        Modify the permission namespace, you can modify the permission namespace name, permission namespace description information and the new unique identifier (Code) of the permission namespace.

        Attributes:
            code (str): Old unique identifier Code of the permission group
            name (str): Permission namespace name
            new_code (str): New unique identifier Code of the permission group
            description (str): Permission namespace description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-permission-namespace',
            json={
                'code': code,
                'name': name,
                'newCode': new_code,
                'description': description,
            },
        )

    def delete_permission_namespace(self, code):
        """Delete permission namespace

        Delete the permission namespace information through the unique identifier (Code) of the permission namespace.

        Attributes:
            code (str): Permission namespace Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-permission-namespace',
            json={
                'code': code,
            },
        )

    def delete_permission_namespaces_batch(self, codes):
        """Batch delete permission namespace

        Batch delete permission namespace information through the unique identifier (Code) of the permission namespace.

        Attributes:
            codes (list): Permission group code list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-permission-namespaces-batch',
            json={
                'codes': codes,
            },
        )

    def check_permission_namespace_exists(self, code=None, name=None):
        """Check if the permission namespace Code or name is available

        Check if the permission namespace Code or name is available through the user pool ID and permission namespace Code, or the user pool ID and permission namespace name.

        Attributes:
            code (str): Permission namespace Code
            name (str): Permission namespace name
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-namespace-exists',
            json={
                'code': code,
                'name': name,
            },
        )

    def list_permission_namespace_roles(self, code, page=None, limit=None, query=None):
        """Paging query all role lists under the permission namespace

        Paging query all role lists under the permission namespace, paging get all role lists under the permission namespace.

        Attributes:
            code (str): Unique identifier Code of the permission group
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Role Code or name
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-permission-namespace-roles',
            params={
                'page': page,
                'limit': limit,
                'code': code,
                'query': query,
            },
        )

    def create_data_resource(self, actions, struct, type, resource_code, resource_name, namespace_code,
                             description=None):
        """Create data resources (recommended, focus)

        
  ## Description
  This interface is used to create data resources. When you have data that needs to be set with permissions, create a data resource according to their data type. Currently, we support: string, array, tree three types.
  ## Note
  The `struct` field in the request body needs to be passed in different data structures according to different resource types. Please refer to the example below for details
## Request Example
### Create a string type data resource example
When your data can be represented by a single string, you can use this type, for example: an API, a user ID, etc.
The following is an example of creating a data resource that represents the '/resource/create' API:
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "createResource API",
  "description": "This is createResource API",
  "resourceCode": "createResourceAPI",
  "type": "STRING",
  "struct": "/resource/create",
  "actions": ["access"]
}
```

### Create an array type data resource example
When your data is a group of the same type of data, you can use this type, for example: a group of document links, a group of access card numbers, etc.
The following is an example of creating a data resource that represents a group of access card numbers:
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "A group of access card numbers",
  "description": "This is a group of access card numbers",
  "resourceCode": "accessCardNumber",
  "type": "ARRAY",
  "struct": ["accessCardNumber1", "accessCardNumber2", "accessCardNumber3"],
  "actions": ["get", "update"]
}
```

### Create a tree type data resource example
When your data has a hierarchical relationship, you can use this type, for example: organizational structure, folder structure, etc.
The following is an example of creating a data resource that represents the organizational structure of a company:
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "GenAuth",
  "description": "This is the organizational structure of GenAuth",
  "resourceCode": "genauth",
  "type": "TREE",
  "struct": [
    {
      "name": "Product",
      "code": "product",
      "value": "product",
      "children": [
        {
          "name": "Product Manager",
          "code": "productManager",
          "value": "pm"
        },
        {
          "name": "Design",
          "code": "design",
          "value": "ui"
        }
      ]
    },
    {
      "name": "Research and Development",
      "code": "researchAndDevelopment",
      "value": "rd"
    }
  ],
  "actions": ["get", "update", "delete"]
}
```
  

        Attributes:
            actions (list): Data resource permission operation list
            struct (): Data resource structure, supports string (STRING), tree structure (TREE) and array structure (ARRAY).
            type (str): Data resource type, currently supports tree structure (TREE), string (STRING), array (ARRAY)
            resource_code (str): Data resource Code, unique within the permission space
            resource_name (str): Data resource name, unique within the permission space
            namespace_code (str): Data resource belongs to the permission space Code
            description (str): Data resource description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'type': type,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_string(self, actions, struct, resource_code, resource_name, namespace_code,
                                       description=None):
        """Create a string data resource

        When you only need to create a string type data resource, you can use this API, we have fixed the data resource type, you do not need to pass in the `type` field, note: the `struct` field can only pass in string type data.

        Attributes:
            actions (list): Data resource permission operation list
            struct (str): String data resource node
            resource_code (str): Data resource Code, unique within the permission space
            resource_name (str): Data resource name, unique within the permission space
            namespace_code (str): Data policy belongs to the permission space Code
            description (str): Data resource description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-string-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_array(self, actions, struct, resource_code, resource_name, namespace_code,
                                      description=None):
        """Create an array data resource

        When you only need to create an array type data resource, you can use this API, we have fixed the data resource type, you do not need to pass in the `type` field, note: the `struct` field can only pass in array type data.

        Attributes:
            actions (list): Data resource permission operation list
            struct (list): Array data resource node
            resource_code (str): Data resource Code, unique within the permission space
            resource_name (str): Data resource name, unique within the permission space
            namespace_code (str): Data policy belongs to the permission space Code
            description (str): Data resource description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-array-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_tree(self, actions, struct, resource_code, resource_name, namespace_code,
                                     description=None):
        """Create a tree data resource

        When you only need to create a tree type data resource, you can use this API, we have fixed the data resource type, you do not need to pass in the `type` field, note: the `struct` should be passed in according to the tree type data resource structure, please refer to the example.

        Attributes:
            actions (list): Data resource permission operation list
            struct (list): Tree data resource node
            resource_code (str): Data resource Code, unique within the permission space
            resource_name (str): Data resource name, unique within the permission space
            namespace_code (str): Data policy belongs to the permission space Code
            description (str): Data resource description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tree-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def list_data_resources(self, page=None, limit=None, query=None, namespace_codes=None):
        """Get data resource list

        Get the data resource list, you can specify the filtering through the data resource name, data resource Code and the data resource belongs to the permission space Code list.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Keyword search, can be the data resource name or the data resource Code
            namespaceCodes (str): Permission data belongs to the permission space Code list
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-resources',
            params={
                'page': page,
                'limit': limit,
                'query': query,
                'namespaceCodes': namespace_codes,
            },
        )

    def get_data_resource(self, namespace_code, resource_code):
        """Get data resource details

        Get data resources, query the corresponding data resource information through the data resource ID, including the basic information such as data resource name, data resource Code, data resource type (TREE, STRING, ARRAY), data resource belongs to the permission space ID, data resource belongs to the permission space Code and data resource operation list.

        Attributes:
            namespaceCode (str): Data resource belongs to the permission space Code
            resourceCode (str): Data resource Code, unique within the permission space
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-data-resource',
            params={
                'namespaceCode': namespace_code,
                'resourceCode': resource_code,
            },
        )

    def update_data_resource(self, resource_code, namespace_code, resource_name=None, description=None, struct=None,
                             actions=None):
        """Modify data resources

        Modify data resources, query the original information based on the permission space Code and data resource Code, and only allow modification of data resource name, description and data resource node.

        Attributes:
            resource_code (str): Data resource Code, unique within the permission space
            namespace_code (str): Data resource belongs to the permission space Code
            resource_name (str): Data resource name, unique within the permission space
            description (str): Data resource description
            struct (): Data resource structure, supports string (STRING), tree structure (TREE) and array structure (ARRAY).
            actions (list): Data resource permission operation list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-data-resource',
            json={
                'resourceCode': resource_code,
                'namespaceCode': namespace_code,
                'resourceName': resource_name,
                'description': description,
                'struct': struct,
                'actions': actions,
            },
        )

    def delete_data_resource(self, resource_code, namespace_code):
        """Delete data resources

        Delete data resources, delete the corresponding data resource information based on the data resource ID.

        Attributes:
            resource_code (str): Data resource Code, unique within the permission space
            namespace_code (str): Data resource belongs to the permission space Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-data-resource',
            json={
                'resourceCode': resource_code,
                'namespaceCode': namespace_code,
            },
        )

    def check_data_resource_exists(self, namespace_code, resource_name=None, resource_code=None):
        """Check if the data resource Code or name is available

        Check whether the data resource name or Code is valid in the permission space, judge whether it is available in the specified permission space through the data resource name or data resource Code and the corresponding permission space Code.

### Data resource Code valid example

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceCode": "test"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 0,
  "data": {
      "isValid": "true"
    }
}
```

### Data resource name valid example

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "test"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 0,
  "data": {
      "isValid": "true"
    }
}
```

### Data resource Code invalid example

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceCode": "test"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 0,
  "requestId": "934108e5-9fbf-4d24-8da1-c330328abd6c",
  "data": {
      "isValid": "false",
      "message": "data resource code already exist"
  }
}
```
  

        Attributes:
            namespaceCode (str): Data resource belongs to the permission space Code
            resourceName (str): Data resource name, unique within the permission space
            resourceCode (str): Data resource Code, unique within the permission space
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-data-resource-exists',
            params={
                'namespaceCode': namespace_code,
                'resourceName': resource_name,
                'resourceCode': resource_code,
            },
        )

    def create_data_policy(self, statement_list, policy_name, description=None):
        """Create data policy (focus)

        
  ## Description
  This interface is used to create data policies. Through data policies, you can bind a group of data resources and their specified operations to a subject for joint authorization.
  ## Note
For ease of use, we provide a shortcut writing method for the `permissions` field based on the path, such as:
- Array, string resource: permission space code/data resource code/data resource some action (if it represents all operations, use `*` to replace action)
- Tree type resource: permission space code/data resource code/node code 1/node code 1_1/.../data resource some action

## Request example
Assuming we want to authorize a developer, first create 3 data resources as follows:
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "server",
  "resourceCode": "server_2023",
  "type": "STRING",
  "struct": "server_2023",
  "actions": ["read", "write"]
}
```
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "rd_document",
  "description": "",
  "resourceCode": "rd_document",
  "type": "STRING",
  "struct": "https://www.genauth.ai/rd_document",
  "actions": ["read", "write", "share"]
}
```
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "rd_internal_platform_menu",
  "description": "This is the internal platform menu used by the development team",
  "resourceCode": "rd_internal_platform",
  "type": "TREE",
  "struct": [
    {
      "name": "deploy",
      "code": "deploy",
      "children": [
        {
          "name": "production environment",
          "code": "prod"
        },
        {
          "name": "test environment",
          "code": "test"
        }
      ]
    },
    {
      "name": "database",
      "code": "db"
      "children": [
        {
          "name": "query",
          "code": "query"
        },
        {
          "name": "export",
          "code": "export"
        }
      ]
    }
  ],
  "actions": ["access", "execute"]
}
```
We assign a server: server_2023 to him, he can do any operation on it, and he can also read and edit the development knowledge base, finally he can deploy the test environment in the internal development platform, but he cannot export the database data.
```json
{
  "policyName": "developer policy",
  "description": "This is an example data policy",
  "statementList": [
    {
      "effect": "ALLOW",
      "permissions": [ 
        "examplePermissionNamespaceCode/server_2023/*",
        "examplePermissionNamespaceCode/rd_document/read",
        "examplePermissionNamespaceCode/rd_document/write",
        "examplePermissionNamespaceCode/rd_internal_platform/deploy/test/execute"
       ]
    },
    {
      "effect": "DENY",
      "permissions": [ 
        "examplePermissionNamespaceCode/rd_internal_platform/db/export/execute"
      ]
    }
  ]
}
```


        Attributes:
            statement_list (list): Data permission list, data resource permission list under the policy
            policy_name (str): Data policy name, unique within the user pool
            description (str): Data policy description
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-data-policy',
            json={
                'statementList': statement_list,
                'policyName': policy_name,
                'description': description,
            },
        )

    def list_data_polices(self, page=None, limit=None, query=None):
        """Get data policy list

        Paginate the data policy list, or search for data policy names or data policy Codes through keywords.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Data policy name keyword search
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-policies',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def list_simple_data_polices(self, page=None, limit=None, query=None):
        """Get data policy simple information list

        Paginate the data policy simple information list, and search for data policy ID, data policy name and data policy description information through keywords.

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Data policy name keyword search
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-simple-data-policies',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def get_data_policy(self, policy_id):
        """Get data policy details

        Get data policy details, get the corresponding data policy information through the data policy ID, including the data policy ID, data policy name, data policy description, and all data permission lists under the data policy.

        Attributes:
            policyId (str): Data policy ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-data-policy',
            params={
                'policyId': policy_id,
            },
        )

    def update_data_policy(self, policy_id, policy_name=None, description=None, statement_list=None):
        """Modify data policy

        Modify the data policy, modify the data policy information through the data policy name, data policy description and related data resources.

        Attributes:
            policy_id (str): Data policy ID
            policy_name (str): Data policy name, unique within the user pool
            description (str): Data policy description
            statement_list (list): Data permission list, all data permissions under each policy
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-data-policy',
            json={
                'policyId': policy_id,
                'policyName': policy_name,
                'description': description,
                'statementList': statement_list,
            },
        )

    def delete_data_policy(self, policy_id):
        """Delete Data Policy

        Delete data policy, delete the corresponding policy through the data policy ID, and also delete the relationship data between the data policy and the corresponding data resources.

        Attributes:
            policy_id (str): Data policy ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-data-policy',
            json={
                'policyId': policy_id,
            },
        )

    def check_data_policy_exists(self, policy_name):
        """Check if Data Policy Name is Available

        Check if the data policy name is valid within the user pool.

        Attributes:
            policyName (str): Data policy name, unique within the user pool
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-data-policy-exists',
            params={
                'policyName': policy_name,
            },
        )

    def list_data_policy_targets(self, policy_id, page=None, limit=None, query=None, target_type=None):
        """Get List of Data Policy Authorized Entities

        Get the list of entities authorized by the data policy, find the list of authorized entities by the authorized entity type, data policy ID, and data resource ID.

        Attributes:
            policyId (str): Data policy ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
            query (str): Entity name
            targetType (str): Entity type, including USER, GROUP, ROLE, ORG four types
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-policy-targets',
            params={
                'policyId': policy_id,
                'page': page,
                'limit': limit,
                'query': query,
                'targetType': target_type,
            },
        )

    def authorize_data_policies(self, target_list, policy_ids):
        """Authorize Data Policies

        Authorize data policies, authorize data policies through authorized entities and data policies.

        Attributes:
            target_list (list): Data permission list, all data permissions under each policy
            policy_ids (list): Data policy ID list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-data-policies',
            json={
                'targetList': target_list,
                'policyIds': policy_ids,
            },
        )

    def revoke_data_policy(self, target_type, target_identifier, policy_id):
        """Revoke Data Policy Authorization

        Revoke data policy authorization, revoke through authorized entity ID, authorized entity type, and data policy ID.

        Attributes:
            target_type (str): Entity type, including USER, GROUP, ROLE, ORG four types
            target_identifier (str): Entity ID, including user ID, user group ID, role ID, organization ID
            policy_id (str): Data policy ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-data-policy',
            json={
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'policyId': policy_id,
            },
        )

    def get_user_permission_list(self, user_ids, namespace_codes=None):
        """Get User Permission List

        
  ## Description
  This interface is used to query the permission data of some users in some permission spaces.
Our authorization interface has multiple scenarios, differing in the parameters that can be passed in different scenarios, **when you need to query all permissions of some users** you can use this interface,
## Note
The interface provides two array-type parameters `userIds` and `namespaceCodes` to support batch queries (note: `namespaceCodes` is optional).
## Scenario Example
If your business scenario is that users can see all the resources they can access or perform other operations after logging in, such as documents, personnel information, equipment information, etc., then you can call this interface to query the user's all permissions after logging in.
## Request Example
### Example of Querying a Single User's Permission List
Note: In the return parameters of this interface, the tree-type data resource permission returns are returned in the form of **paths**
- Input
  
```json
{
    "userIds": [
      "6301ceaxxxxxxxxxxx27478"  
    ]
}
```

- Output
  
```json
{
  "statusCode": 200, 
  "message": "Operation successful", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace", 
        "resourceList": [
          {
            "resourceCode": "strCode",
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "Example string resource", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          },
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "Example data resource 1",
                "Example data resource 2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }, 
          {
            "resourceCode": "treeCode", 
            "resourceType": "TREE",
            "treeAuthorize": {
              "authList": [
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode1", 
                  "nodeActions": [
                    "read", 
                    "get"
                  ], 
                  "nodeName": "treeChildrenName1", 
                  "nodeValue": "treeChildrenValue1"
                }, 
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode2", 
                  "nodeActions": [
                    "read", 
                    "get"
                  ], 
                  "nodeName": "treeChildrenName2", 
                  "nodeValue": "treeChildrenValue2"
                }, 
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode3", 
                  "nodeActions": [
                    "read"
                  ], 
                  "nodeName": "treeChildrenName3", 
                  "nodeValue": "treeChildrenValue3"
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

### Example of Querying Multiple Users' Permission Lists

- Input

```json
{
  "userIds": [
    "6301ceaxxxxxxxxxxx27478",
    "6121ceaxxxxxxxxxxx27312"
  ]
}
```

- Output

```json
{
  "statusCode": 200, 
  "message": "Operation successful", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace1", 
        "resourceList": [
          {
            "resourceCode": "strCode",
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "Example string resource", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }, 
      {
        "userId": "6121ceaxxxxxxxxxxx27312", 
        "namespaceCode": "examplePermissionNamespace2", 
        "resourceList": [
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "Example array resource 1", 
                "Example array resource 2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }
    ]
  }
}
```

### Example of Querying Multiple Users' Permission Lists in Multiple Permission Spaces

- Input

```json
{
  "userIds": [
    "6301ceaxxxxxxxxxxx27478",
    "6121ceaxxxxxxxxxxx27312"
  ],
  "namespaceCodes": [
    "examplePermissionNamespace1",
    "examplePermissionNamespace2"
  ]
}
```

- Output

```json
{
  "statusCode": 200, 
  "message": "Operation successful", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace1", 
        "resourceList": [
          {
            "resourceCode": "strCode1", 
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "Example string resource", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }, 
      {
        "userId": "6121ceaxxxxxxxxxxx27312", 
        "namespaceCode": "examplePermissionNamespace2", 
        "resourceList": [
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "Example array resource 1", 
                "Example array resource 2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }
    ]
  }
}
```
  

        Attributes:
            user_ids (list): User ID list
            namespace_codes (list): Permission space Code list
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-permission-list',
            json={
                'userIds': user_ids,
                'namespaceCodes': namespace_codes,
            },
        )

    def check_permission(self, resources, action, user_id, namespace_code, judge_condition_enabled=None,
                         auth_env_params=None):
        """Check User Permissions (Key Point)

        
  ## Description
  When you need to determine whether a user has a specific permission for certain resources, you can use this interface.
  ## Note
  - This interface locates the corresponding data resource by passing the resource code (if it is a tree type, you need to pass the complete code path of the node).
  - If you configure the **environment properties** condition judgment when configuring data policies, you need to set the parameter `judgeConditionEnabled` to `true` (default is false), and pass the environment information (such as IP, device type, system type, etc.) where the request is located through the parameter `authEnvParams`), otherwise the condition judgment will not take effect, causing the data policy to not take effect.

## Scenario Example
When a user needs to determine whether he has the permission to delete a piece of data, you can use this interface.

## Request Example
### Example of Determining User Permissions for String and Array Resources (No Conditional Judgment)

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data": {
      "checkResultList": [
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "strResourceCode1",
              "action": "get",
              "enabled": true
          },
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "arrayResourceCode1",
              "action": "get",
              "enabled": true
          }
      ]
  }
}
```

### Example of Determining User Permissions for String and Array Resources (Enabling Conditional Judgment)

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources": ["strResourceCode1", "arrayResourceCode1"],
  "judgeConditionEnabled": true,
  "authEnvParams":{
      "ip":"110.96.0.0",
      "city":"Beijing",
      "province":"Beijing",
      "country":"China",
      "deviceType":"PC",
      "systemType":"ios",
      "browserType":"IE",
      "requestDate":"2022-12-26 17:40:00"
  }
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data": {
      "checkResultList": [
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "strResourceCode1",
              "action": "get",
              "enabled": false
          },
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "arrayResourceCode1",
              "action": "get",
              "enabled": false
          }
      ]
  }
}
```

### Example of Determining User Permissions for Tree Resources

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "checkResultList": [{
      "namespaceCode": "examplePermissionNamespace",
      "action": "get",
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1",
      "enabled": true     
    },{
      "namespaceCode": "examplePermissionNamespace",
      "action": "get",
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1",
      "enabled": true     
    }]
  }
}
```
  

        Attributes:
            resources (list): List of resource paths, **tree resources must be specific to the tree node**
            action (str): Data resource permission operation, such as read, get, write actions
            user_id (str): User ID
            namespace_code (str): Permission space Code
            judge_condition_enabled (bool): Whether to enable conditional judgment, default false not enabled
            auth_env_params (dict): Conditional environment properties, used if conditional judgment is enabled
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission',
            json={
                'resources': resources,
                'action': action,
                'userId': user_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def check_external_user_permission(self, resources, action, external_id, namespace_code,
                                       judge_condition_enabled=None, auth_env_params=None):
        """Check External User Permission

        
  ## Description
  When your user is an external user, you can use this interface to determine if they have a certain permission for a resource, passing the user's ID through `externalId`.
  

        Attributes:
            resources (list): List of resource paths, **tree resources must be specific to the tree node**
            action (str): Data resource permission operation, such as read, get, write actions
            external_id (str): External user ID
            namespace_code (str): Permission space Code
            judge_condition_enabled (bool): Whether to enable conditional judgment, default true enabled
            auth_env_params (dict): Conditional environment properties, used if conditional judgment is enabled
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-external-user-permission',
            json={
                'resources': resources,
                'action': action,
                'externalId': external_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def get_user_resource_permission_list(self, resources, user_id, namespace_code):
        """Get User Resource Permission List (Recommended)

        
  ## Description
  When you need to query the permissions of a specified resource list for a user, you can use this interface.
  ## Note
  This interface requires you to pass the specified resource code (if it is a tree-type resource, you need to pass the complete code path of the node), this interface has better performance, and it is recommended to use.
  ## Request Example
### Example of Getting User String and Array Resource Permissions

- Parameters
  
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```

- Response

```json
{

  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "permissionList": [{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read","get"],  
      "resource": "strResourceCode1"
    },{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read","update","delete"], 
      "resource": "arrayResourceCode1"
    }]
  }
}
```
  
### Example of Getting User Tree Resource Permissions
  
- Parameters
  
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```

- Response

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "permissionList": [{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read", "update", "delete"],
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1"
    },{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read", "get", "delete"],     
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1"
    }]
  }
}
```
  

        Attributes:
            resources (list): List of resource paths, **tree resources must be specific to the tree node**
            user_id (str): User ID
            namespace_code (str): Permission space Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-resource-permission-list',
            json={
                'resources': resources,
                'userId': user_id,
                'namespaceCode': namespace_code,
            },
        )

    def list_resource_targets(self, resources, actions, namespace_code):
        """Get the list of users with certain resource permissions

        
  ## Description
  When you need to get the list of users with permissions for specific resources, you can use this interface.
  ## Scenario Example
  For example, if your business scenario is: you want to see the list of users who can edit the current document, then you can use this interface.
  ## Request Example
### Example of getting the list of users authorized for string and array resources

- Input
    
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "actions": ["get", "update", "read"],
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```
  
- Output
  
```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "authUserList": [{
      "resource": "strResourceCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "read"
      }]  
    },{
      "resource": "arrayResourceCode1",
      "actionAuthList": [{
      "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "read"
      }] 
    }]
  }
}
```
    
### Example of getting the list of users authorized for tree resources

- Input
    
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "actions": ["get", "update", "delete"],
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```
  
- Output
  
```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "authUserList": [{
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "delete"
      }]  
    },{
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "delete"
      }] 
    }]
  }
}
```
  

        Attributes:
            resources (list): List of data resource paths
            actions (list): List of data resource permission operations
            namespace_code (str): Permission space Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-resource-targets',
            json={
                'resources': resources,
                'actions': actions,
                'namespaceCode': namespace_code,
            },
        )

    def get_user_resource_struct(self, resource_code, user_id, namespace_code):
        """Get user permissions and resource structure information for a specified resource

        
  ## Description
  When you need to get the permissions a user has for a specific resource and also need the structure information of this resource (tree-type resources return tree structure, array-type resources return array, string-type resources return string), then you can use this interface.
  ## Note
  Since other interfaces return tree-type resources in the form of paths, we provide this interface to return in the form of complete tree structure.
  ## Request Example
### Example of getting user authorization for a string data resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleStrResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleStrResourceCode",
    "resourceType": "STRING",
    "strResourceAuthAction":{
      "value": "strTestValue",
      "actions": ["get","delete"]
    }
  }
}
```
# ...

```

-------
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-resource-targets',
            json={
                'resources': resources,
                'actions': actions,
                'namespaceCode': namespace_code,
            },
        )

    def get_user_resource_struct(self, resource_code, user_id, namespace_code):
        """Get the permissions and structure information of the resources owned by the user

        
  ## Description
  When you need to get the permissions and structure information of a resource owned by a user (tree-type resources return tree structure, array-type resources return array, string-type resources return string), you can use this interface.
  ## Note
  Since other interfaces return tree-type resources in the form of paths, we provide this interface to return in the form of complete tree structure.
  ## Request Example
### Example of getting user authorization for a string data resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleStrResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleStrResourceCode",
    "resourceType": "STRING",
    "strResourceAuthAction":{
      "value": "strTestValue",
      "actions": ["get","delete"]
    }
  }
}
```


### Example of getting user authorization for a data array resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleArrResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "ARRAY",
    "arrResourceAuthAction":{
      "values": ["arrTestValue1","arrTestValue2","arrTestValue3"],
      "actions": ["get","delete"]
    }
  }
}
```


### Example of getting user authorization for a tree data resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleTreeResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "TREE",
    "treeResourceAuthAction":{
        "nodeAuthActionList":[{
            "code": "tree11",
            "name": "tree11",
            "value": "test11Value",
            "actions": ["get","delete"],
            "children": [{
              "code": "tree111",
              "name": "tree111",
              "value": "test111Value",
              "actions": ["update","read"],
            }]
        },{
            "code": "tree22",
            "name": "tree22",
            "value": "test22Value",
            "actions": ["get","delete"]
        }]
    }
  }
}
```
  

        Attributes:
            resource_code (str): Data resource Code
            user_id (str): User ID 
            namespace_code (str): Permission space Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-resource-struct',
            json={
                'resourceCode': resource_code,
                'userId': user_id,
                'namespaceCode': namespace_code,
            },
        )

    def get_external_user_resource_struct(self, resource_code, external_id, namespace_code):
        """Get the permission and resource structure information of a specific resource owned by an external user

        
  ## Description
  When you need to get the permission and resource structure information of a specific resource owned by an external user (passed through the `externalId` parameter), you can use this interface.
  ## Request Example
### Example of Getting User Authorization String Data Resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleStrResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleStrResourceCode",
    "resourceType": "STRING",
    "strResourceAuthAction":{
      "value": "strTestValue",
      "actions": ["get","delete"]
    }
  }
}
```


### Example of Getting User Authorization Data Array Resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleArrResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "ARRAY",
    "arrResourceAuthAction":{
      "values": ["arrTestValue1","arrTestValue2","arrTestValue3"],
      "actions": ["get","delete"]
    }
  }
}
```


### Example of Getting User Authorization Tree Data Resource

- Input

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleTreeResourceCode"
}
```

- Output

```json
{
  "statusCode": 200,
  "message": "Operation successful",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "TREE",
    "treeResourceAuthAction":{
        "nodeAuthActionList":[{
            "code": "tree11",
            "name": "tree11",
            "value": "test11Value",
            "actions": ["get","delete"],
            "children": [{
              "code": "tree111",
              "name": "tree111",
              "value": "test111Value",
              "actions": ["update","read"],
            }]
        },{
            "code": "tree22",
            "name": "tree22",
            "value": "test22Value",
            "actions": ["get","delete"]
        }]
    }
  }
}
```
  

        Attributes:
            resource_code (str): Resource Code
            external_id (str): External User ID
            namespace_code (str): Permission Space Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-external-user-resource-struct',
            json={
                'resourceCode': resource_code,
                'externalId': external_id,
                'namespaceCode': namespace_code,
            },
        )

    def check_user_same_level_permission(self, resource_node_codes, resource, action, user_id, namespace_code,
                                         judge_condition_enabled=None, auth_env_params=None):
        """Determine the user's permissions at the same level of tree resources (recommended)

        
  ## Description
  This interface is used to determine whether a user has permission for a certain part of the nodes at the same level of a tree-type resource.
  ## Note
  We use the `resource` parameter to locate a certain level of the tree-type data resource (so the parameter is passed in the format of `resource code/node code path`), and use the `resourceNodeCodes` parameter to locate which nodes are currently at this level.
  ## Scenario Example
For example, if your business scenario is: when a user needs to delete certain files in a file system, you need to determine whether they have the deletion permission for these files, then you can use this interface.
## Request Example
### Example of Determining User Permissions at the Same Level of Tree Resources (No Conditional Judgment)

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"]
}
```

### Example of Determining User Permissions at the Same Level of Tree Resources (With Conditional Judgment)

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"],
  "judgeConditionEnabled": true,
  "authEnvParams":{
      "ip":"110.96.0.0",
      "city":"Beijing",
      "province":"Beijing",
      "country":"China",
# ...

```

-------
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-external-user-resource-struct',
            json={
                'resourceCode': resource_code,
                'externalId': external_id,
                'namespaceCode': namespace_code,
            },
        )

    def check_user_same_level_permission(self, resource_node_codes, resource, action, user_id, namespace_code,
                                         judge_condition_enabled=None, auth_env_params=None):
        """Check User Permissions at the Same Level of Tree Resources (Recommended)

        
  ## Description
  This interface is used to determine whether a user has a certain permission for some nodes at the **same level** of a tree-type resource. Since tree-type resources are quite common, we have added an interface specifically for judging the permissions of tree-type resource nodes based on the business scenario of "judging whether a user has resource permissions".
  ## Note
  We use the `resource` parameter to locate a certain level of the tree-type data resource (so the parameter is passed in the format of `resource code/node code path`), and use the `resourceNodeCodes` parameter to locate which nodes are currently at this level.
  ## Scenario Example
For example, if your business scenario is: when a user needs to delete certain files in a file system, you need to determine whether they have the deletion permission for these files, then you can use this interface.
## Request Example
### Example of Determining User Permissions at the Same Level of Tree Resources (No Conditional Judgment)

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"]
}
```

### Example of Determining User Permissions at the Same Level of Tree Resources (With Conditional Judgment)

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"],
  "judgeConditionEnabled": true,
  "authEnvParams":{
      "ip":"110.96.0.0",
      "city":"Beijing",
      "province":"Beijing",
      "country":"China",
# ...

        Attributes:
            resource_node_codes (list): Tree resource path sub-node Code
            resource (str): Tree resource path, allowing multiple levels of paths, examples are as follows
- treeResourceCode
- treeResourceCode/structCode
- treeResourceCode/structCode/struct1Code
- treeResourceCode/.../structCode
            action (str): Data resource permission operation
            user_id (str): User ID
            namespace_code (str): Permission space Code
            judge_condition_enabled (bool): Whether to enable conditional judgment, default false not enabled
            auth_env_params (dict): Conditional environment properties, used if conditional judgment is enabled
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-user-same-level-permission',
            json={
                'resourceNodeCodes': resource_node_codes,
                'resource': resource,
                'action': action,
                'userId': user_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def list_permission_view(self, page=None, limit=None, keyword=None):
        """Get Permission View Data List

        
  ## Description
  This interface is used to export menus: Permission Management -> Data Permission -> Permission View List Data. If you need to pull our data permission authorization data (all permissions of all resources owned by all users), you can use this interface.
  

        Attributes:
            page (int): The current page number, starting from 1
            limit (int): The number of items per page, cannot exceed 50, default is 10
            keyword (str): Keyword search, supports userName search
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-permission-view/data',
            json={
                'page': page,
                'limit': limit,
                'keyword': keyword,
            },
        )

    def get_current_package_info(self, ):
        """Get Package Details

        Get details of the current user pool package.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-current-package-info',
        )

    def get_usage_info(self, ):
        """Get Usage Details

        Get details of the current user pool usage.

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-usage-info',
        )

    def get_mau_period_usage_history(self, start_time, end_time):
        """Get MAU Usage Record

        Get the MAU usage record of the current user pool

        Attributes:
            startTime (str): Start time (year, month, day)
            endTime (str): End time (year, month, day)
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mau-period-usage-history',
            params={
                'startTime': start_time,
                'endTime': end_time,
            },
        )

    def get_all_rights_item(self, ):
        """Get All Rights

        Get all rights of the current user pool

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-all-rights-items',
        )

    def get_orders(self, page=None, limit=None):
        """Get Order List

        Get the order list of the current user pool

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): The number of items per page, cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-orders',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def get_order_detail(self, order_no):
        """Get Order Details

        Get the order details of the current user pool

        Attributes:
            orderNo (str): Order number
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-order-detail',
            params={
                'orderNo': order_no,
            },
        )

    def get_order_pay_detail(self, order_no):
        """Get Order Payment Details

        Get the order payment details of the current user pool

        Attributes:
            orderNo (str): Order number
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-order-pay-detail',
            params={
                'orderNo': order_no,
            },
        )

    def create_event_app(self, logo, name, identifier):
        """Create Custom Event Application

        Create a custom event application

        Attributes:
            logo (str): Application logo
            name (str): Application name
            identifier (str): Application unique identifier
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-event-app',
            json={
                'logo': logo,
                'name': name,
                'identifier': identifier,
            },
        )

    def list_event_apps(self, ):
        """Get Event Application List

        Get the event application list

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-event-apps',
        )

    def list_events(self, page=None, limit=None, app=None):
        """Get Event List

        Get all event lists supported by GenAuth services

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): The number of items per page, cannot exceed 50, default is 10
            app (str): Application type
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-events',
            params={
                'page': page,
                'limit': limit,
                'app': app,
            },
        )

    def define_event(self, event_description, event_type):
        """Define Custom Event

        Define a custom event in the GenAuth event center

        Attributes:
            event_description (str): Event description
            event_type (str): Event type
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/define-event',
            json={
                'eventDescription': event_description,
                'eventType': event_type,
            },
        )

    def verify_event(self, event_type, event_data):
        """Push Custom Event

        Push a custom event to the GenAuth event center

        Attributes:
            event_type (str): Event type
            event_data (dict): Event body
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pub-event',
            json={
                'eventType': event_type,
                'eventData': event_data,
            },
        )

    def pub_user_event(self, event_type, event_data):
        """Push Custom Event from Authentication End

        Push a custom event to the GenAuth event center from the authentication end

        Attributes:
            event_type (str): Event type
            event_data (dict): Event body
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pub-userEvent',
            json={
                'eventType': event_type,
                'eventData': event_data,
            },
        )

    def add_whitelist(self, type, list=None):
        """Create registration whitelist

        You need to specify the registration whitelist type and data to create

        Attributes:
            type (str): Whitelist type
            list (list): Type parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-whitelist',
            json={
                'type': type,
                'list': list,
            },
        )

    def list_whitelists(self, type):
        """Get registration whitelist list

        Get the registration whitelist list, optional page number, page size to get

        Attributes:
            type (str): Whitelist type
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-whitelist',
            params={
                'type': type,
            },
        )

    def delete_whitelist(self, type, list=None):
        """Delete whitelist

        Delete whitelist by specifying multiple whitelist data in the form of an array

        Attributes:
            type (str): Whitelist type
            list (list): Type parameters
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-whitelist',
            json={
                'type': type,
                'list': list,
            },
        )

    def find_ip_list(self, ip_type, page=None, limit=None):
        """Get ip list

        Get ip list by page

        Attributes:
            ipType (str): IP type
            page (int): Current page number, starting from 1
            limit (int): Number of pages, maximum not exceeding 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/ip-list',
            params={
                'page': page,
                'limit': limit,
                'ipType': ip_type,
            },
        )

    def add(self, expire_at, limit_list, remove_type, add_type, ip_type, ips):
        """Create ip list

        Create ip list

        Attributes:
            expire_at (str): Add time
            limit_list (list): Limit type, FORBID_LOGIN-forbid login, FORBID_REGISTER-forbid register, SKIP_MFA-skip MFA
            remove_type (str): Remove type, MANUAL-manual, SCHEDULE-strategy delete
            add_type (str): Add type, MANUAL-manual, SCHEDULE-strategy add
            ip_type (str): IP type, WHITE-white list, BLACK-black list
            ips (str): ip, multiple IPs separated by commas
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/ip-list',
            json={
                'expireAt': expire_at,
                'limitList': limit_list,
                'removeType': remove_type,
                'addType': add_type,
                'ipType': ip_type,
                'ips': ips,
            },
        )

    def delete_by_id(self, id):
        """Delete ip list

        Delete ip list

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/ip-list/{id}',
        )

    def find_user_list(self, user_list_type, page=None, limit=None):
        """Get user list

        Get user list by page

        Attributes:
            userListType (str): IP type
            page (int): Current page number, starting from 1
            limit (int): Number of pages, maximum not exceeding 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/user-list',
            params={
                'page': page,
                'limit': limit,
                'userListType': user_list_type,
            },
        )

    def add_user(self, expire_at, limit_list, remove_type, add_type, user_list_type, user_ids):
        """Create user list

        Create user list

        Attributes:
            expire_at (int): Expiration time
            limit_list (list): Limit type, FORBID_LOGIN-forbid login, FORBID_REGISTER-forbid register, SKIP_MFA-skip MFA
            remove_type (str): Remove type, MANUAL-manual, SCHEDULE-strategy delete
            add_type (str): Add type, MANUAL-manual, SCHEDULE-strategy add
            user_list_type (str): User list type, WHITE-white list, BLACK-black list
            user_ids (list): userId, multiple userIds separated by commas
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/user-list',
            json={
                'expireAt': expire_at,
                'limitList': limit_list,
                'removeType': remove_type,
                'addType': add_type,
                'userListType': user_list_type,
                'userIds': user_ids,
            },
        )

    def delete_user_list_by_id(self, id):
        """Delete user list

        Delete user list

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/user-list/{id}',
        )

    def find_risk_list_policy(self, opt_object, page=None, limit=None):
        """Get risk list policy

        Get risk list policy by page

        Attributes:
            optObject (str): Policy operation object, currently only ip
            page (int): Current page number, starting from 1
            limit (int): Number of pages, maximum not exceeding 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/risk-list-policy',
            params={
                'page': page,
                'limit': limit,
                'optObject': opt_object,
            },
        )

    def add_risk_list_policy(self, limit_list, action, remove_type, event_state_type, count_thr, time_range, user_cond,
                             ip_cond, user_range, ip_range, opt_object):
        """Create risk list policy

        Create risk list policy

        Attributes:
            limit_list (str): Limit type list, FORBID_LOGIN-forbid login, FORBID_REGISTER-forbid register
            action (str): Policy action, ADD_IP_BLACK_LIST-add IP black list, ADD_USER_BLACK_LIST-add user black list
            remove_type (str): Remove type, MANUAL-manual, SCHEDULE-strategy, currently only manual
            event_state_type (str): Event state type, password_wrong-wrong password, account_wrong-wrong account
            count_thr (int): Number of times threshold
            time_range (int): Time range, how many minutes
            user_cond (str): IP condition, NO_LIMIT-no limit, ONE-single user, one of userCond and ipCond
            ip_cond (str): IP condition, NO_LIMIT-no limit, ONE-single IP, one of userCond and ipCond
            user_range (str): Range of operation USER, ALL-all, NOT_IN_WHITE_LIST-not in white list, one of ipRange and userRange
            ip_range (str): Range of operation IP, ALL-all, NOT_IN_WHITE_LIST-not in white list, one of userRange and ipRange
            opt_object (str): Policy operation object, currently only ip
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/risk-list-policy',
            json={
                'limitList': limit_list,
                'action': action,
                'removeType': remove_type,
                'eventStateType': event_state_type,
                'countThr': count_thr,
                'timeRange': time_range,
                'userCond': user_cond,
                'ipCond': ip_cond,
                'userRange': user_range,
                'ipRange': ip_range,
                'optObject': opt_object,
            },
        )

    def delete_risk_list_policy_by_id(self, id):
        """Delete risk policy

        Delete risk policy

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/risk-list-policy/{id}',
        )

    def create_device(self, device_unique_id, type, custom_data, name=None, version=None, hks=None, fde=None, hor=None,
                      sn=None, producer=None, mod=None, os=None, imei=None, meid=None, description=None, language=None,
                      cookie=None, user_agent=None):
        """Create device

        Create a new device.

        Attributes:
            device_unique_id (str): Device unique identifier
            type (str): Device type
            custom_data (dict): Custom data, the properties of custom data correspond to the custom fields in the metadata
            name (str): Device name
            version (str): System version
            hks (str): Hardware storage key
            fde (str): Disk encryption
            hor (bool): Hardware jailbreak
            sn (str): Device serial number
            producer (str): Manufacturer
            mod (str): Device module
            os (str): Device system
            imei (str): International identification code
            meid (str): Device identification code
            description (str): Device description
            language (str): Device language
            cookie (bool): Whether to enable Cookies
            user_agent (str): User agent
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-device',
            json={
                'deviceUniqueId': device_unique_id,
                'type': type,
                'customData': custom_data,
                'name': name,
                'version': version,
                'hks': hks,
                'fde': fde,
                'hor': hor,
                'sn': sn,
                'producer': producer,
                'mod': mod,
                'os': os,
                'imei': imei,
                'meid': meid,
                'description': description,
                'language': language,
                'cookie': cookie,
                'userAgent': user_agent,
            },
        )

    def find_last_login_apps_by_device_ids(self, device_ids, user_id=None):
        """Recent login apps

        Get a list of recently logged in apps based on the device's unique identifier.

        Attributes:
            device_ids (list): List of device unique identifiers
            user_id (str): User ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-last-login-apps-by-deviceIds',
            json={
                'deviceIds': device_ids,
                'userId': user_id,
            },
        )

    def create_pipeline_function(self, source_code, scene, func_name, func_description=None, is_asynchronous=None,
                                 timeout=None, terminate_on_timeout=None, enabled=None):
        """Create Pipeline function

        Create Pipeline function

        Attributes:
            source_code (str): Function source code
            scene (str): Function trigger scene:
- `PRE_REGISTER`: Before registration
- `POST_REGISTER`: After registration
- `PRE_AUTHENTICATION`: Before authentication
- `POST_AUTHENTICATION`: After authentication
- `PRE_OIDC_ID_TOKEN_ISSUED`: Before OIDC ID Token issued
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: Before OIDC Access Token issued
- `PRE_COMPLETE_USER_INFO`: Before completing user information
    
            func_name (str): Function name
            func_description (str): Function description
            is_asynchronous (bool): Whether to execute asynchronously. Functions set to execute asynchronously will not block the execution of the entire process, suitable for asynchronous notification scenarios, such as Feishu group notification, DingTalk group notification, etc.
            timeout (int): Function execution timeout, must be an integer, minimum is 1 second, maximum is 60 seconds, default is 3 seconds.
            terminate_on_timeout (bool): If the function execution times out, whether to terminate the entire process, default is no.
            enabled (bool): Whether to enable this Pipeline
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-pipeline-function',
            json={
                'sourceCode': source_code,
                'scene': scene,
                'funcName': func_name,
                'funcDescription': func_description,
                'isAsynchronous': is_asynchronous,
                'timeout': timeout,
                'terminateOnTimeout': terminate_on_timeout,
                'enabled': enabled,
            },
        )

    def get_pipeline_function(self, func_id):
        """Get Pipeline function details

        Get Pipeline function details

        Attributes:
            funcId (str): Pipeline function ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-pipeline-function',
            params={
                'funcId': func_id,
            },
        )

    def reupload_pipeline_function(self, func_id):
        """Reupload Pipeline function

        When the Pipeline function upload fails, reupload the Pipeline function

        Attributes:
            func_id (str): Pipeline function ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reupload-pipeline-function',
            json={
                'funcId': func_id,
            },
        )

    def update_pipeline_function(self, func_id, func_name=None, func_description=None, source_code=None,
                                 is_asynchronous=None, timeout=None, terminate_on_timeout=None, enabled=None):
        """Modify Pipeline function

        Modify Pipeline function

        Attributes:
            func_id (str): Pipeline function ID
            func_name (str): Function name
            func_description (str): Function description
            source_code (str): Function source code. If modified, the function will be re-uploaded.
            is_asynchronous (bool): Whether to execute asynchronously. Functions set to execute asynchronously will not block the execution of the entire process, suitable for asynchronous notification scenarios, such as Feishu group notification, DingTalk group notification, etc.
            timeout (int): Function execution timeout, minimum is 1 second, maximum is 60 seconds, default is 3 seconds.
            terminate_on_timeout (bool): If the function execution times out, whether to terminate the entire process, default is no.
            enabled (bool): Whether to enable this Pipeline
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-pipeline-function',
            json={
                'funcId': func_id,
                'funcName': func_name,
                'funcDescription': func_description,
                'sourceCode': source_code,
                'isAsynchronous': is_asynchronous,
                'timeout': timeout,
                'terminateOnTimeout': terminate_on_timeout,
                'enabled': enabled,
            },
        )

    def update_pipeline_order(self, order, scene):
        """Modify Pipeline function order

        Modify Pipeline function order

        Attributes:
            order (list): New sorting method, arranged according to the order of function IDs.
            scene (str): Function trigger scene:
- `PRE_REGISTER`: Before registration
- `POST_REGISTER`: After registration
- `PRE_AUTHENTICATION`: Before authentication
- `POST_AUTHENTICATION`: After authentication
- `PRE_OIDC_ID_TOKEN_ISSUED`: Before OIDC ID Token issued
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: Before OIDC Access Token issued
- `PRE_COMPLETE_USER_INFO`: Before completing user information
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-pipeline-order',
            json={
                'order': order,
                'scene': scene,
            },
        )

    def delete_pipeline_function(self, func_id):
        """Delete Pipeline function

        Delete Pipeline function

        Attributes:
            func_id (str): Pipeline function ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-pipeline-function',
            json={
                'funcId': func_id,
            },
        )

    def list_pipeline_functions(self, scene):
        """Get Pipeline Function List

        Get Pipeline Function List

        Attributes:
            scene (str): Filter by function trigger scene (optional, default returns all):
- `PRE_REGISTER`: Before registration
- `POST_REGISTER`: After registration
- `PRE_AUTHENTICATION`: Before authentication
- `POST_AUTHENTICATION`: After authentication
- `PRE_OIDC_ID_TOKEN_ISSUED`: Before OIDC ID Token issuance
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: Before OIDC Access Token issuance
- `PRE_COMPLETE_USER_INFO`: Before completing user information
    
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-pipeline-functions',
            params={
                'scene': scene,
            },
        )

    def get_pipeline_logs(self, func_id, page=None, limit=None):
        """Get Pipeline Logs

        Get Pipeline Logs

        Attributes:
            funcId (str): Pipeline function ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-pipeline-logs',
            params={
                'funcId': func_id,
                'page': page,
                'limit': limit,
            },
        )

    def create_webhook(self, content_type, events, url, name, enabled=None, secret=None):
        """Create Webhook

        You need to specify the Webhook name, Webhook callback URL, request data format, and user real name to create a Webhook. You can also optionally specify whether to enable and request key for creation.

        Attributes:
            content_type (str): Request data format
            events (list): User real name, not unique. Example value: Zhang San
            url (str): Webhook callback URL
            name (str): Webhook name
            enabled (bool): Whether to enable
            secret (str): Request key
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-webhook',
            json={
                'contentType': content_type,
                'events': events,
                'url': url,
                'name': name,
                'enabled': enabled,
                'secret': secret,
            },
        )

    def list_webhooks(self, page=None, limit=None):
        """Get Webhook List

        Get Webhook List, optional page number and page size to get

        Attributes:
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-webhooks',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def update_webhook(self, webhook_id, name=None, url=None, events=None, content_type=None, enabled=None,
                       secret=None):
        """Update Webhook Configuration

        You need to specify the webhookId, and optionally the Webhook name, Webhook callback URL, request data format, user real name, whether to enable, and request key to update the webhook.

        Attributes:
            webhook_id (str): Webhook ID
            name (str): Webhook name
            url (str): Webhook callback URL
            events (list): User real name, not unique. Example value: Zhang San
            content_type (str): Request data format
            enabled (bool): Whether to enable
            secret (str): Request key
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-webhook',
            json={
                'webhookId': webhook_id,
                'name': name,
                'url': url,
                'events': events,
                'contentType': content_type,
                'enabled': enabled,
                'secret': secret,
            },
        )

    def delete_webhook(self, webhook_ids):
        """Delete Webhook

        Delete webhook by specifying multiple webhookId in the form of an array, if webhookId does not exist, no error is reported

        Attributes:
            webhook_ids (list): webhookId array
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-webhook',
            json={
                'webhookIds': webhook_ids,
            },
        )

    def get_webhook_logs(self, webhook_id, page=None, limit=None):
        """Get Webhook Logs

        Get webhook logs by specifying webhookId, optionally with page and limit, if webhookId does not exist, no error information is returned

        Attributes:
            webhook_id (str): Webhook ID
            page (int): Current page number, starting from 1
            limit (int): Number of items per page, maximum cannot exceed 50, default is 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-webhook-logs',
            json={
                'webhookId': webhook_id,
                'page': page,
                'limit': limit,
            },
        )

    def trigger_webhook(self, webhook_id, request_headers=None, request_body=None):
        """Manually Trigger Webhook Execution

        Manually trigger webhook execution by specifying webhookId, optionally with request headers and request body

        Attributes:
            webhook_id (str): Webhook ID
            request_headers (dict): Request headers
            request_body (dict): Request body
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/trigger-webhook',
            json={
                'webhookId': webhook_id,
                'requestHeaders': request_headers,
                'requestBody': request_body,
            },
        )

    def get_webhook(self, webhook_id):
        """Get Webhook Details

        Get webhook details by specifying webhookId

        Attributes:
            webhookId (str): Webhook ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-webhook',
            params={
                'webhookId': webhook_id,
            },
        )

    def get_webhook_event_list(self, ):
        """Get Webhook Event List

        Returns event list and classification list

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-webhook-event-list',
        )

    def get_bind_pwd(self, ):
        """Generate LDAP Server Administrator Password

        Generate LDAP Server Administrator Password

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-random-pwd',
        )

    def query_ldap_config_info(self, ):
        """Get LDAP Server Configuration Information

        Get LDAP Server Configuration Information

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-config',
        )

    def update_ldap_config_info(self, bind_pwd=None):
        """Update LDAP Server Configuration Information

        Update LDAP Server Configuration Information

        Attributes:
            bind_pwd (str): bindDn password
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ldap-server-config',
            json={
                'bindPwd': bind_pwd,
            },
        )

    def save_ldap_config_info(self, ldap_domain, link_url=None):
        """Initialize/Restart LDAP Server

        Initialize/Restart LDAP Server

        Attributes:
            ldap_domain (str): LDAP domain name
            link_url (str): LDAP host
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enable-ldap-server',
            json={
                'ldapDomain': ldap_domain,
                'linkUrl': link_url,
            },
        )

    def disable_ldap_server(self, enabled):
        """Disable LDAP Server Service, must be initialized before closing

        Disable LDAP Server Service, must be initialized before closing

        Attributes:
            enabled (bool): Whether the switch is turned on
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/disable-ldap-server',
            json={
                'enabled': enabled,
            },
        )

    def query_ldap_log(self, type, page, limit, connection=None, operation_number=None, error_code=None, message=None,
                       start_time=None, end_time=None):
        """LDAP Server Log Query

        LDAP Server Log Query

        Attributes:
            type (int): Type: 1 access log, 2 error log
            page (int): Current page, starting from 1
            limit (int): Number of items per page
            connection (int): Connection identifier
            operationNumber (int): Operation code
            errorCode (int): Error code
            message (str): Message content
            startTime (int): Start time - timestamp
            endTime (int): End time - timestamp
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-log',
            params={
                'type': type,
                'connection': connection,
                'operationNumber': operation_number,
                'errorCode': error_code,
                'message': message,
                'startTime': start_time,
                'endTime': end_time,
                'page': page,
                'limit': limit,
            },
        )

    def query_ldap_sub_entries(self, page, limit, dn=None):
        """LDAP Server Query Next Level by DN

        LDAP Server Query Next Level by DN

        Attributes:
            page (int): Current page, starting from 1
            limit (int): Number of items per page
            dn (str): Current DN
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-sub-entries',
            params={
                'dn': dn,
                'page': page,
                'limit': limit,
            },
        )

    def get_access_key_list(self, user_id=None, tenant_id=None, type=None, status=None):
        """Get Collaborative Administrator AK/SK List

        Get the list of all AK/SK under the collaborative administrator based on the collaborative administrator ID

        Attributes:
            userId (str): User ID of the key
            tenantId (str): Tenant ID of the key
            type (str): Key type
            status (str): AccessKey status, activated: activated, staging: tiered (can be rotated), revoked: revoked
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-access-key',
            params={
                'userId': user_id,
                'tenantId': tenant_id,
                'type': type,
                'status': status,
            },
        )

    def get_access_key(self, user_id, access_key_id):
        """Get Collaborative Administrator AK/SK Details

        Get the details of the collaborative administrator AK/SK, get the details of the corresponding AK/SK based on the collaborative administrator ID and accessKeyId.

        Attributes:
            userId (str): User ID
            accessKeyId (str): accessKeyId
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-access-key',
            params={
                'userId': user_id,
                'accessKeyId': access_key_id,
            },
        )

    def create_access_key(self, type, user_id=None, tenant_id=None):
        """Create AK/SK for Collaborative Administrator

        Create AK/SK for collaborative administrator, generate specified AK/SK based on collaborative administrator ID.

        Attributes:
            type (str): Key type
            user_id (str): User ID of the key
            tenant_id (str): Tenant ID of the key
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-access-key',
            json={
                'type': type,
                'userId': user_id,
                'tenantId': tenant_id,
            },
        )

    def delete_access_key(self, access_key_id):
        """Delete Collaborative Administrator AK/SK

        Delete the collaborative administrator AK/SK, delete the specified AK/SK based on the accessKeyId.

        Attributes:
            access_key_id (str): accessKeyId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-access-key',
            json={
                'accessKeyId': access_key_id,
            },
        )

    def update_access_key(self, enable, access_key_id):
        """Update Administrator AccessKey

        Update an administrator AccessKey based on AccessKeyId, currently only supports updating status, status supports activated / revoked

        Attributes:
            enable (bool): Whether the key is valid
            access_key_id (str): AccessKey ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-access-key',
            json={
                'enable': enable,
                'accessKeyId': access_key_id,
            },
        )

    def get_verify_config_app(self, keywords=None):
        """Get verify-config-app List

        Get verify-config-app List

        Attributes:
            keywords (str): Search keyword
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/verify-config-app',
            params={
                'keywords': keywords,
            },
        )

    def sub_event(self, event_code, callback):
        """Subscribe to Events

        Subscribe to genauth public events or custom events

        Attributes:
            eventCode (str): Event code
            callback (callable): Callback function
        """
        assert event_code, "eventCode cannot be empty"
        assert callable(callback), "callback must be a callable function"
        authorization = getAuthorization(self.access_key_id, self.access_key_secret)
        # print("authorization:"+authorization)
        eventUri = self.websocket_host + self.websocket_endpoint + "?code=" + event_code
        # print("eventUri:"+eventUri)
        handleMessage(eventUri, callback, authorization)

    def put_event(self, event_code, data):
        """Publish Custom Events

        Publish events

        Attributes:
            event_code (str): Event code
            data (json): Event body
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/pub-event",
            json={
                "eventType": event_code,
                "eventData": json.dumps(data)
            },
        )
