The `cropwiseworker` module is designed to work with the [Cropwise Operations](https://www.cropwise.com/operations) digital agricultural enterprise management platform. The module allows you to interact with various platform data, facilitating the integration and automation of tasks.

## Installing
Install module using pip:

```bash
pip install cropwiseworker
```

## Module functions

### Get dict with Cropwise Operations user account API token

```python
to_auth(login, password):
```

- **login (required)** – enter your [Cropwise Operations](https://www.cropwise.com/operations) user account login using `str` data type
- **password (required)** – enter your [Cropwise Operations](https://www.cropwise.com/operations) user account password using `str` data type

### Mass download of data from the Cropwise Operations account

```python
data_downloader(endpoint, token, params=None, data_format=None, version=None)
```

- **endpoint (required)** – enter your endpoint from [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/) documentation using `str` data type
- **token (required)** – enter your TOKEN from Cropwise Operations account using `str` data type
- **params** – enter your endpoint parameters using array format (default = None)
- **data_format** – enter suggested data format (default = pd.DataFrame(), also could be 'json')
- **version** – enter your [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/) version using `str` data type (default = 'v3')

### Create a massive dataset with soil test, crop rotation, agro operation and yield data for analysis named Agrimatrix

```python
agrimatrix_dataset(enterprise, token, season)
```

- **enterprise (required)** – enter a name of your enterprise using `str` data type
- **token (required)** – enter your TOKEN from Cropwise Operations account using `str` data type
- **season (required)** – enter an interested value of season using `int` data type

### Create a kml-file with several orchard rows inside of quarter kml-file

```python
create_orchard_rows(file_path, quarter_name, number_of_rows, start_side='right', crop=None, download_directory=None, start_row_number=1)
```

- **file_path (required)** – enter a directory of your quarter with row direction line in KML format using `str` data type. The row direction line should have a name 'row_direction_{quarter name}'
- **quarter_name (required)** – enter a name of your quarter. This argument allows to create rows for KML-file with several quarters with different row directions 
- **number_of_rows (required)** – enter the relevant number of orchard rows to create using `int` data type
- **start_side** – select the side from which you want to start numbering rows relative to the direction line (default = 'right', also could be 'left')
- **crop** – enter a name of crop which grows in your quarter using `str` data type (default = None)
- **download_directory** – enter a directory to download result file using `str` data type (default = None)
- **start_row_number** – enter a number of a first row in the quarter using `int` data type (default = 1)

### Get a data with last changed objects within certain period
```python
fetch_changes(endpoint, token, start_date, end_date, step_days=3, output_format='dataframe')
```

- **endpoint (required)** – enter your endpoint from [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/) documentation using `str` data type
- **token (required)** – enter your TOKEN from Cropwise Operations account using `str` data type
- **start_date (required)** – enter a date which from the data should start downloading in format 'YYYY-MM-DD'
- **end_date (required)** – enter a date which till the data should start downloading in format 'YYYY-MM-DD'
- **step_days** – enter a number of days between start_date and every next date 
- **output_format** – enter a format name for output data (default = pd.DataFrame, also could be 'json')

## Workflow examples

```python
import cropwiseworker as cw

token = to_auth('test@cropwise.com', 'pass')['token']

params = {'created_at_gt_eq':'2023-01-01'}

fields = cw.data_downloader('fields', token=token, params=params)
print(fields)

my_2023_analysis = cw.agrimatrix_dataset('YOUR_ENTERPRISE_NAME', token=token, season=2023)
print(my_2023_analysis)

cw.create_orchard_rows('path/to/your/file.kml', 'Quarter1', 50, 'left', 'Apple', 'path/to/download/directory', 10)

field_changes = cw.fetch_changes('fields', token, '2024-01-01', '2024-01-07', step_days=1, output_format='json')
print(field_changes)
```

## License
This package is distributed under the Apache License 2.0.