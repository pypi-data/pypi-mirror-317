import pandas as pd
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

# List of file paths
file_paths = [
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/maize_1.xlsx',
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/maize_2.xlsx',
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/rice_1.xlsx',
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/winter_wheat_1.xlsx',
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/spring_wheat_1.xlsx',
    r'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/soybean_1.xlsx'
]


# Function to reshape data dynamically
def reshape_data_dynamic(data, value_name):
    id_vars_possible = ['ADM0_NAME', 'ADM1_NAME', 'ADM2_NAME', 'Season', 'Data Source', 'num_ID']
    id_vars_present = [col for col in id_vars_possible if col in data.columns]
    return data.melt(
        id_vars=id_vars_present,
        value_vars=[year for year in range(1990, 2024) if year in data.columns],
        var_name='year',
        value_name=value_name
    )


# Function to process individual files
def process_file_dynamic(file_path):
    file_name = os.path.basename(file_path)
    growing_season = int(file_name.split('_')[-1].split('.')[0])  # Extract growing season from filename
    crop = file_name.split('_')[0]  # Extract crop name from filename

    # Load the Excel file and read the sheets
    excel_data = pd.ExcelFile(file_path)
    area_data = pd.read_excel(excel_data, sheet_name='Area (ha)')
    production_data = pd.read_excel(excel_data, sheet_name='Production (tn)')
    yield_data = pd.read_excel(excel_data, sheet_name='Yield (tn per ha)')

    # Reshape each sheet dynamically
    area_long = reshape_data_dynamic(area_data, 'area')
    production_long = reshape_data_dynamic(production_data, 'production')
    yield_long = reshape_data_dynamic(yield_data, 'yield')

    # Merge reshaped data
    merged_data = pd.merge(area_long, production_long, on=['ADM0_NAME', 'ADM1_NAME', 'year'], how='outer',
                           suffixes=('_area', '_prod'))
    merged_data = pd.merge(merged_data, yield_long, on=['ADM0_NAME', 'ADM1_NAME', 'year'], how='outer')

    # Drop unwanted columns
    merged_data.drop(columns=['ADM2_NAME_prod', 'Season_prod'], errors='ignore', inplace=True)

    # Keep one 'Data Source' and 'num_ID'
    merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

    # Add growing season and crop
    merged_data['growing_season'] = growing_season
    merged_data['crop'] = crop

    # Rename columns
    merged_data.rename(columns={
        'ADM0_NAME': 'country',
        'ADM1_NAME': 'admin_1',
        'ADM2_NAME': 'admin_2',
    }, inplace=True)

    # if admin_2 columns is not present then add it
    if 'admin_2' not in merged_data.columns:
        merged_data['admin_2'] = None

    # Add placeholders for missing columns
    merged_data['calendar_region'] = None
    merged_data['category'] = None

    # Ensure 'year' is integer
    merged_data['year'] = merged_data['year'].astype(int)

    return merged_data

# Clean and finalize the combined data
def clean_combined_data(data):
    # Drop unnecessary columns
    data = data.drop(columns=[
        'ADM2_NAME_area', 'ADM2_NAME_prod', 'Season_area', 'Season_prod',
        'Data Source_area', 'Data Source_prod', 'num_ID_area', 'num_ID_prod'
    ], errors='ignore')

    # Keep one `Data Source` and `num_ID` column
    data = data.loc[:, ~data.columns.duplicated()]

    # Rename remaining columns for consistency
    data.rename(columns={
        'Data Source': 'data_source',
        'num_ID': 'num_id'
    }, inplace=True)

    # Drop rows where yield, area and production are all missing
    data = data.dropna(subset=['yield', 'area', 'production'], how='all')

    return data


# Process each file in parallel
def process_and_return(file_path):
    return process_file_dynamic(file_path)


if __name__ == "__main__":
    # read in lookup table
    df_lookup = pd.read_csv("lookup_table.csv")
    df_lookup = df_lookup[df_lookup['percentage_intersection'] > 10]

    for path in file_paths:
        df_crop = process_file_dynamic(path)

        crop = df_crop['crop'].unique()[0]
        growing_season = df_crop['growing_season'].unique()[0]

        df_crop = clean_combined_data(df_crop)
        breakpoint()
        # merge df_lookup and merged_data on ADM0_NAME and dominant_state columns in the former
        # and country and admin_1 columns in the latter
        for country in df_crop['country'].unique():
            df_crop_country = df_crop[df_crop['country'] == country]
            df_lookup_country = df_lookup[df_lookup['ADM0_NAME'] == country]

            for admin_1 in df_crop_country['admin_1'].unique():
                if admin_1:
                    df_crop_admin_1 = df_crop_country[df_crop_country['admin_1'] == admin_1]
                    df_lookup_admin_1 = df_lookup_country[df_lookup_country['dominant_state'] == admin_1]

                    df_crop_admin_1 = pd.merge(df_crop_admin_1, df_lookup_admin_1, how='outer',
                                               left_on=['country', 'admin_1'], right_on=['ADM0_NAME', 'dominant_state'])
                else:
                    df_crop_admin_1 = pd.merge(df_crop_country, df_lookup_country, how='outer',
                                               left_on=['country'], right_on=['ADM0_NAME'])



        df_crop = pd.merge(df_crop, df_lookup, how='outer', left_on=['country', 'admin_1'],
                               right_on=['ADM0_NAME', 'dominant_state'])

        try:
            df_crop = df_crop.sort_values(
                by=['country', 'growing_season', 'crop', 'admin_1', 'admin_2', 'year'])
        except:
            breakpoint()

        final_output_path_dynamic = rf'D:\Users\ritvik\projects\GEOGLAM\Input\crop_condition\yield/statistics_{crop}_{growing_season}.csv'
        df_crop.to_csv(final_output_path_dynamic, index=False)
