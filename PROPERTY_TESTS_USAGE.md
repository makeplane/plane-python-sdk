# Work Item Types and Properties Test Scripts

This guide explains how to use the test scripts for testing work item types, custom properties, and property values in the Plane Python SDK.

## Overview

The test scripts demonstrate comprehensive testing of:

1. **Work Item Types** - Creating and managing different types of work items
2. **Custom Properties** - Creating various property types (text, boolean, decimal, datetime, option, URL, email, relation)
3. **Property Options** - Creating selectable options for option-type properties
4. **Property Values** - Assigning, updating, and retrieving property values for work items

## Test Scripts

### 1. `test_work_item_types_and_properties.py`

**Basic comprehensive test covering all core functionality**

**What it tests:**

- Creating work item types (Bug, Feature, Epic)
- Creating custom properties (Text, Option, Boolean, Decimal)
- Creating property options for select lists
- Creating work items with specific types
- Assigning property values to work items
- Retrieving and verifying property values

**Usage:**

```bash
python test_work_item_types_and_properties.py
```

### 2. `test_advanced_properties.py`

**Advanced test covering complex property scenarios**

**What it tests:**

- All property types including URL, Email, DateTime, Relation
- Multi-select option properties
- Property validation
- Complex property value assignments
- Property value updates
- Relations between work items

**Usage:**

```bash
python test_advanced_properties.py
```

### 3. `test_property_values.py`

**Focused test for property value operations**

**What it tests:**

- Creating property values for all property types
- Retrieving individual and bulk property values
- Updating property values
- Deleting property values
- Property values across multiple work items

**Usage:**

```bash
python test_property_values.py
```

## Setup

### 1. Environment Variables

Set the following environment variables:

```bash
export BASE_URL="https://api.plane.so"  # Your Plane instance URL
export WORKSPACE_SLUG="your-workspace"   # Your workspace slug
export API_KEY="your_api_key"            # Your API key (or use ACCESS_TOKEN)
# OR
export ACCESS_TOKEN="your_token"         # Your access token (alternative to API_KEY)
```

### 2. Install Dependencies

```bash
cd plane-python-sdk
pip install -r requirements.txt
```

## Property Types Tested

### Basic Property Types

- **TEXT** - Free-form text input
- **BOOLEAN** - True/false values
- **DECIMAL** - Numeric values with decimals
- **DATETIME** - Date and time values
- **OPTION** - Single-select from predefined options

### Advanced Property Types

- **URL** - URL validation and formatting
- **EMAIL** - Email validation and formatting
- **RELATION** - Links to other work items
- **FILE** - File attachments (if supported)

### Property Features Tested

- **Required vs Optional** - Properties can be marked as required
- **Multi-select** - Option properties can allow multiple selections
- **Default values** - Properties can have default values
- **Validation rules** - Properties can have custom validation
- **Sort order** - Properties can be ordered
- **Active/Inactive** - Properties can be enabled/disabled

## Expected Output

Each test script provides detailed step-by-step output:

```
Starting Work Item Types and Properties Test
Base URL: https://api.plane.so
Workspace: my-workspace
Authentication: API Key

======================================================================
Step 1: Initializing Plane Client
======================================================================
✓ Client initialized successfully

======================================================================
Step 2: Creating a new project
======================================================================
✓ Project created: Types & Properties Test 20250109_143025 (ID: abc-123-def)
  Identifier: TYPES143025
  Emoji: 🔧

======================================================================
Step 3: Creating work item types
======================================================================
✓ Work item type created: Bug (ID: type-1)
✓ Work item type created: Feature (ID: type-2)
✓ Work item type created: Epic (ID: type-3)

======================================================================
Step 4: Creating custom properties for Bug type
======================================================================
✓ Property created: Severity (ID: prop-1)
✓ Property created: Priority (ID: prop-2)
✓ Property created: Is Critical (ID: prop-3)
✓ Property created: Estimated Hours (ID: prop-4)

======================================================================
Step 5: Creating property options for Priority
======================================================================
✓ Option created: Critical (ID: opt-1)
✓ Option created: High (ID: opt-2)
✓ Option created: Medium (ID: opt-3)
✓ Option created: Low (ID: opt-4)

======================================================================
Step 6: Creating a work item with Bug type and custom properties
======================================================================
✓ Work item created: Test Bug with Custom Properties (ID: work-item-1)
  Type: Bug
  Priority: high

======================================================================
Step 7: Assigning custom property values to work item
======================================================================
✓ Severity value set: High
✓ Priority value set: High
✓ Critical value set: True
✓ Estimated hours value set: 4.5

======================================================================
Step 8: Verifying work item and property values
======================================================================
✓ Work item retrieved: Test Bug with Custom Properties
✓ Retrieved 4 property values

======================================================================
Step 9: Creating a work item with Feature type
======================================================================
✓ Feature work item created: Test Feature with Custom Properties (ID: work-item-2)
  Type: Feature

======================================================================
Step 10: Test Summary
======================================================================
✓ Project created: Types & Properties Test 20250109_143025
✓ Work item types created: 3
✓ Custom properties created: 4
✓ Property options created: 4
✓ Work items created: 2
✓ Property values assigned: 4

All tests completed successfully!

View your project at: https://api.plane.so/w/my-workspace/p/abc-123-def
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**

   - Verify your API key or access token is correct
   - Check that you have the necessary permissions in the workspace

2. **Property Type Errors**

   - Ensure you're using the correct property type enum values
   - Check that the property type matches the value type being assigned

3. **Validation Errors**

   - Some property types have built-in validation (e.g., email format)
   - Check that your values match the expected format

4. **Missing Dependencies**
   - Ensure all required models are imported
   - Check that the SDK is properly installed

### Debug Tips

1. **Enable Verbose Logging**

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check API Responses**

   - The scripts print detailed success/error messages
   - Look for specific error details in the traceback

3. **Verify Data Types**
   - Ensure property values match the expected types
   - Check that UUIDs are properly formatted

## Customization

### Adding New Property Types

To test additional property types, modify the test scripts:

```python
# Add new property type
new_prop_data = CreateWorkItemProperty(
    display_name="Custom Field",
    description="Your custom property",
    property_type=PropertyTypeEnum.YOUR_TYPE,
    is_required=False,
    is_active=True,
)
```

### Testing Different Scenarios

1. **Required Properties** - Set `is_required=True`
2. **Multi-select Options** - Set `is_multi=True` for option properties
3. **Validation Rules** - Add custom validation in the `validation_rules` field
4. **Default Values** - Set `default_value` for properties

### Performance Testing

For performance testing, modify the scripts to:

- Create many work items with properties
- Test bulk property value operations
- Measure response times for large datasets

## Cleanup

The test scripts create timestamped resources that can be easily identified and cleaned up:

- **Projects**: Names like "Types & Properties Test 20250109_143025"
- **Work Item Types**: Names like "Bug", "Feature", "Epic"
- **Work Items**: Names like "Test Bug with Custom Properties"

You can manually delete these resources from your workspace if needed.

## Integration with CI/CD

These test scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Test Work Item Properties
  run: |
    export BASE_URL="${{ secrets.PLANE_BASE_URL }}"
    export API_KEY="${{ secrets.PLANE_API_KEY }}"
    export WORKSPACE_SLUG="${{ secrets.PLANE_WORKSPACE }}"
    python test_work_item_types_and_properties.py
```

The scripts return appropriate exit codes (0 for success, 1 for failure) for CI/CD integration.
