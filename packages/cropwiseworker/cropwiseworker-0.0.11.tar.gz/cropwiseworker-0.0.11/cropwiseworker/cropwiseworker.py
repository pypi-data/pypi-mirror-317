import requests
import json
import pandas as pd
import simplekml
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from shapely.geometry import Polygon, LineString, MultiPolygon
import numpy as np
import os



def to_auth(login, password):
    response=requests.post('https://operations.cropwise.com/api/v3/sign_in',
                         headers={'Content-Type':'application/json'},
                          json={
                                  "user_login": 
                                        {
                                            "email": login,
                                            "password": password
                                        }
                                }
                         )
    print('Authentication was successful!')
    
    token = json.loads(response.text)['user_api_token']
    company = json.loads(response.text)['company']
    
    return {'company':company,'login':login,'token':token}



def data_downloader(endpoint, token, params=None, data_format=None, version=None):
    print(endpoint.upper(),'DOWNLOADING IS STARTED')
    all_data = []
    base_version='v3'
    if version is not None:
        base_version=version
    base_url = 'https://operations.cropwise.com/api/'+str(base_version)+'/'
    headers = {
        "Content-Type": "application/json",
        "X-User-Api-Token": token
    }

    base_params = {'sort_by': 'id_asc'}
    if params is not None:
        base_params.update(params)

    get = requests.get(f'{base_url}{endpoint}', headers=headers, params=base_params)
    try:
        record_id = json.loads(get.text)['data'][0]['id']
        iter_num = 0
        
        while True:
            try:
                iter_params = {'from_id': record_id}
                iter_params.update(base_params)

                get = requests.get(f'{base_url}{endpoint}', headers=headers, params=iter_params)
                data = json.loads(get.text)['data']

                all_data.extend(data)
                record_id = data[-1]['id'] + 1
                iter_num += 1
                print('Iteration num:', iter_num, 'Last added record id:', record_id - 1)
            except (IndexError, KeyError):
                print('The work is done...')
                break
                
        if data_format == 'json':
            return all_data
        else:
            return pd.DataFrame(all_data)
    except IndexError:
        print('DATA IS MISSING')
    


def agrimatrix_dataset(enterprise, token, season):
    fields=data_downloader('fields',token)
    
    def calculate_centroid_as_string(geojson_str):
        try:
            geom = shape(json.loads(geojson_str))
            centroid = geom.centroid
            return f"{centroid.y}, {centroid.x}"
        except Exception as e:
            return None
    
    fields['centroid'] = fields['shape_simplified_geojson'].apply(calculate_centroid_as_string)
    fields_reworked=fields[['id', 'centroid','calculated_area', 'legal_area', 'tillable_area']].rename(columns={'id':'field_id'})

    crops=data_downloader('crops',token)
    crops=crops[['id', 'name']].rename(columns={'id':'crop_id'})

    params={'year':season-1}
    history_items_previous=data_downloader('history_items',token,params=params)
    history_items_previous=history_items_previous[['field_id','crop_id','variety']]
    history_items_previous=history_items_previous.merge(crops,how='left',on='crop_id').drop(columns='crop_id').rename(columns={'name':'ancestor','variety':'ancestor_variety'})
    history_items_previous=history_items_previous[['field_id','ancestor','ancestor_variety']]

    params={'year':season}
    history_items_current=data_downloader('history_items',token,params=params)
    history_items_current=history_items_current[['field_id','crop_id','variety','sowing_date','harvesting_date','harvested_weight']]
    history_items_current=history_items_current.merge(crops,how='left',on='crop_id').drop(columns='crop_id').rename(columns={'name':'crop','variety':'crop_variety'})
    history_items_current=history_items_current[['field_id','crop','crop_variety','sowing_date','harvesting_date','harvested_weight']]

    crop_rotation=fields_reworked.merge(history_items_previous,how='left',on='field_id').merge(history_items_current,how='left',on='field_id')

    soil_tests=data_downloader('soil_tests',token)

    soil_tests_reworked=soil_tests.join(pd.json_normalize(soil_tests['elements'])).drop(columns=['elements']).sort_values(by=['field_id', 'made_at'], ascending=[True, False]).drop_duplicates(subset='field_id')
    ph_columns = [col for col in soil_tests_reworked.columns if 'pH' in col]
    soil_tests_reworked['pH_combined'] = soil_tests_reworked[ph_columns].bfill(axis=1).iloc[:, 0]
    soil_tests_reworked=soil_tests_reworked[['field_id','pH_combined','organic_matter','P','K','S','made_at']]

    yield_and_soil_params=crop_rotation.merge(soil_tests_reworked,how='left',on='field_id')

    chemicals=data_downloader('chemicals',token)
    chemicals=chemicals[['id','chemical_type','name']].rename(columns={'id':'applicable_id','name':'applicable_name','chemical_type':'applicable_feature'})

    seeds=data_downloader('seeds',token)
    seeds=seeds[['id','name']].rename(columns={'id':'applicable_id','name':'applicable_name'})

    fertilizers=data_downloader('fertilizers',token)
    fertilizers=fertilizers[['id','fertilizer_type','name']].rename(columns={'id':'applicable_id','name':'applicable_name','fertilizer_type':'applicable_feature'})

    applicable=pd.concat([chemicals,seeds,fertilizers])

    work_types=data_downloader('work_types',token)
    work_types=work_types[['id','name']].rename(columns={'id':'work_type_id','name':'work_type_name'})

    application_mix_items=data_downloader('application_mix_items',token,params=params)

    application_mix_items_reworked=application_mix_items[['id','agro_operation_id','applicable_type','applicable_id','fact_amount','fact_rate','planned_amount','planned_rate']]

    mix_items_applicable=application_mix_items_reworked.merge(applicable,how='left',on='applicable_id').drop_duplicates(subset=['id'])

    params={'season':season}
    agro_operations=data_downloader('agro_operations',token,params=params)

    agro_operations_work_types=agro_operations.merge(work_types,how='left',on='work_type_id')
    agro_operations_reworked=agro_operations_work_types[['id','season','field_id','operation_type', 'operation_subtype','work_type_name','status','actual_start_datetime','completed_date','fact_water_rate','humidity','protein_content','planned_water_rate']].dropna(subset=['completed_date']).rename(columns={'id':'agro_operation_id'})

    ao_with_ami=agro_operations_reworked.merge(mix_items_applicable,how='left',on='agro_operation_id').drop(columns=['id'])

    first_half=ao_with_ami[['field_id','agro_operation_id', 'season', 'operation_type',
           'operation_subtype', 'work_type_name','applicable_type','applicable_feature', 'applicable_name',
           'actual_start_datetime', 'completed_date', 'fact_amount', 'fact_rate', 'planned_amount',
           'planned_rate','fact_water_rate','humidity', 'protein_content', 'planned_water_rate']]

    def transform_dataframe(df):
        df['operation_count'] = df.groupby('field_id').cumcount() + 1
        new_column_names = []
        for i in range(1, df['operation_count'].max() + 1):
            for col in df.columns.drop(['field_id', 'operation_count']):
                new_column_names.append(f"{col}_{i}")
        pivot_data_grouped = pd.DataFrame(index=df['field_id'].unique(), columns=new_column_names)
        for index, row in df.iterrows():
            count = row['operation_count']
            for col in df.columns.drop(['field_id', 'operation_count']):
                pivot_data_grouped.at[row['field_id'], f"{col}_{count}"] = row[col]
        pivot_data_grouped.reset_index(inplace=True)
        pivot_data_grouped.rename(columns={"index": "field_id"}, inplace=True)
        return pivot_data_grouped

    transform_half=transform_dataframe(first_half)

    pre_final_part1=yield_and_soil_params.merge(transform_half,how='left',on='field_id')

    for_deleting=[]
    for x in pre_final_part1.columns.to_list():
        if x.startswith('season') or x.startswith('agro_operation_id'):
            for_deleting.append(x)

    pre_final_part2=pre_final_part1.drop(columns=for_deleting)
    columns=pre_final_part2.columns.to_list()
    pre_final_part2['season']=season
    pre_final_part2['eterprise']=enterprise
    final=pre_final_part2[['season','eterprise']+columns]
    return final



def create_orchard_rows(file_path, quarter_name, number_of_rows, start_side='right', crop=None, download_directory=None, start_row_number=1):
    tree = ET.parse(file_path)
    root = tree.getroot()

    crop_name = crop

    # Извлечение пространственных данных из KML
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = root.findall('.//kml:Placemark', namespaces)

    quarter_polygons = []
    direction_line = None

    # Получение координат для заданного квартала и направляющей линии
    for placemark in placemarks:
        name = placemark.find('kml:name', namespaces).text
        if name == quarter_name:
            multigeometry = placemark.find('.//kml:MultiGeometry', namespaces)
            if multigeometry is not None:
                # Обработка MultiGeometry
                for polygon in multigeometry.findall('.//kml:Polygon', namespaces):
                    coordinates = polygon.find('.//kml:coordinates', namespaces).text.strip()
                    coords = [
                        (float(coord.split(',')[0]), float(coord.split(',')[1]))
                        for coord in coordinates.split()
                    ]
                    quarter_polygons.append(Polygon(coords))
            else:
                # Обработка обычных полигонов
                coordinates = placemark.find('.//kml:coordinates', namespaces).text.strip()
                coords = [
                    (float(coord.split(',')[0]), float(coord.split(',')[1]))
                    for coord in coordinates.split()
                ]
                quarter_polygons.append(Polygon(coords))
        elif name == f"row_direction_{quarter_name}":
            coordinates = placemark.find('.//kml:coordinates', namespaces).text.strip()
            coords = [
                (float(coord.split(',')[0]), float(coord.split(',')[1]))
                for coord in coordinates.split()
            ]
            direction_line = LineString(coords)

    if not quarter_polygons or direction_line is None:
        raise ValueError("Quarter polygon or direction line not found in the KML file.")

    # Создание KML
    kml = simplekml.Kml()

    # Определение направления ряда
    start_point = np.array(direction_line.coords[0])
    end_point = np.array(direction_line.coords[1])
    direction_vector = end_point - start_point
    direction_vector = direction_vector / np.linalg.norm(direction_vector)

    # Поворот вектора на 90 градусов для создания параллельных рядов
    perp_vector = np.array([-direction_vector[1], direction_vector[0]])

    # Инициализация переменных для вычисления границ
    min_perp_distance = float('inf')
    max_perp_distance = float('-inf')

    # Вычисляем минимальные и максимальные расстояния по перпендикуляру для всех полигонов
    for polygon in quarter_polygons:
        for coord in polygon.exterior.coords:
            perp_distance = np.dot(np.array(coord) - start_point, perp_vector)
            min_perp_distance = min(min_perp_distance, perp_distance)
            max_perp_distance = max(max_perp_distance, perp_distance)

    total_perp_distance = max_perp_distance - min_perp_distance
    row_width = total_perp_distance / number_of_rows

    print(f"Quarter: {quarter_name}, Number of Rows: {number_of_rows}, Row Width: {row_width}")

    # Определяем начальную сторону для нумерации рядов
    if start_side == 'right':
        row_indices = range(start_row_number, start_row_number + number_of_rows)
    else:
        row_indices = reversed(range(start_row_number, start_row_number + number_of_rows))

    # Создание рядов по обе стороны от направляющей линии
    row_geometries = {}
    for i, row_index in enumerate(row_indices):
        offset_distance = min_perp_distance + i * row_width
        offset_vector = perp_vector * offset_distance
        base_point1 = start_point + offset_vector - direction_vector * 100
        base_point2 = start_point + offset_vector + direction_vector * 100

        row_poly = Polygon([
            base_point1,
            base_point1 + perp_vector * row_width,
            base_point2 + perp_vector * row_width,
            base_point2
        ])

        for polygon in quarter_polygons:
            intersection = row_poly.intersection(polygon)

            if not intersection.is_empty:
                row_name = f"{quarter_name}.{row_index}"
                if row_name not in row_geometries:
                    row_geometries[row_name] = []
                if intersection.geom_type == 'Polygon':
                    row_geometries[row_name].append(intersection)
                elif intersection.geom_type == 'MultiPolygon':
                    row_geometries[row_name].extend(intersection.geoms)

    # Добавляем ряды в KML
    for row_name, geometries in row_geometries.items():
        multigeometry = kml.newmultigeometry(name=row_name, description=crop_name)
        for geom in geometries:
            pol = multigeometry.newpolygon()
            pol.outerboundaryis = [(point[0], point[1]) for point in geom.exterior.coords]

    # Определение пути для сохранения KML-файла
    if download_directory is None:
        download_directory = os.getcwd()
    
    kml_file_path = os.path.join(download_directory, f"{quarter_name}_Rows.kml")
    kml.save(kml_file_path)



def fetch_changes(endpoint, token, start_date, end_date, step_days=3, output_format='dataframe'):
    url = f'https://operations.cropwise.com/api/v3/{endpoint}/changes'
    headers = {
        "X-User-Api-Token": token,
        "Content-Type": "application/json"
    }
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    all_changes = []

    while current_date < end_date:
        next_date = current_date + timedelta(days=step_days)
        params = {
            'from_time': current_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'to_time': next_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            changes = json.loads(response.text).get('data', [])
            if changes:
                all_changes.extend(changes)
            print(f'Successfully fetched changes from {current_date} to {next_date}')
        else:
            print(f'Failed to fetch changes from {current_date} to {next_date}: {response.text}')
        
        current_date = next_date

    if output_format == 'json':
        return json.loads(json.dumps(all_changes))
    else:
        valid_changes = [change for change in all_changes if isinstance(change, dict)]
        if valid_changes:
            return pd.concat([pd.DataFrame([change]) for change in valid_changes], ignore_index=True)
        else:
            return pd.DataFrame()
