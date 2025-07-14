import pandas as pd
from openpyxl import load_workbook
from rest_framework.response import Response



def normalize_wbs(value):
    """
    Normalize WBS value by removing trailing '.0' parts.
    E.g., '2.0.0' -> '2', '14.0.0' -> '14'
    """
    try:
        parts = value.split(".")
        while parts and parts[-1] == "0":
            parts.pop()
        return ".".join(parts)
    except Exception:
        return value
    
def validate_wbs_data(df):
# === Validation Checks ===
    try:
        new_df = df[['Description', 'WBS Category', 'WBS Code']]
        new_df = new_df[~new_df['Description'].isin(['Capex', 'Opex','Gain/Loss Account'])]
        new_df['WBS Category'] = new_df['WBS Category'].astype(str)
        new_df['WBS Code'] = new_df['WBS Code'].astype(str)
        same_mask = new_df['WBS Category'] == new_df['WBS Code']  
        invalid_format_mask = ~new_df['WBS Category'].str.match(r'^\d+(\.\d+)*$') | ~new_df['WBS Code'].str.match(r'^\d+(\.\d+)*$')
        errors = []
        
        for _, row in new_df[invalid_format_mask].iterrows():
            errors.append(
                f"WBS values must be integers only. Found invalid WBS category [{row['WBS Category']}] "
                f"or WBS code [{row['WBS Code']}] under sub header [{row['Description']}]."
            )
        
        # for _, row in new_df[same_mask].iterrows():
        for _, row in new_df.iterrows():
            wbs_cat = str(row['WBS Category'])
            wbs_code = str(row['WBS Code'])
        
            if normalize_wbs(wbs_cat) == normalize_wbs(wbs_code) and wbs_cat != wbs_code:
                continue  # Only look different; skip error
        
            if wbs_cat == wbs_code:
                errors.append(
                    f"For the budget sub header [{row['Description']}] the WBS category is "
                    f"[{row['WBS Category']}] and WBS code is [{row['WBS Code']}]."
                    "WBS code and WBS category cannot be same."
                )
        if errors:
            errors.append("File cannot be created due to WBS validation errors.")
            print("\n".join(errors)) 
            raise ValueError(errors)
    
    except Exception as e:
        raise e    

def prepare_final_dataframe(df):   
    # === Prepare Final DataFrame ===
    try:      
        df.columns = ['Header', 'Subheader', 'WBS Code', 'Budget', 'April',
               'May', 'June', 'July', 'August', 'September', 'October', 'November',
               'December', 'January', 'February', 'March']
        
        df['Subheader'] = df['Header']

        capex = df.iloc[1:18,:].copy()
        capex["Header"] =df.loc[0, 'Header']

        
        opex = df.iloc[19:191,:].copy()
        opex["Header"] = df.loc[18, 'Header']
        
        gl_df = df.iloc[192:195,:].copy()
        gl_df["Header"] = df.loc[191, 'Header']

        final_df = pd.concat([capex, opex, gl_df], axis=0, ignore_index=True)
        return final_df

    except Exception as e:
        print(f"Error during DataFrame preparation: {e}")
        return 
    
def export_to_excel(final_df):
    # === Export to Excel ===
        try:
            output_file_path = 'budget.xlsx'
            final_df.to_excel(output_file_path, index=False, engine='openpyxl')
            print(f"Excel file '{output_file_path}' created successfully")
            return output_file_path
        except Exception as e:
            print(f"Error while writing Excel file: {e}")

    
def main(file_obj):
    try:
        # === Load File === 
        df = pd.read_excel(file_obj)
        
        # Validate WBS
        validate_wbs_data(df)

        # Prepare final DataFrame
        final_df = prepare_final_dataframe(df)
        if final_df is None:
            raise ValueError("DataFrame preparation failed.")

        # Export to Excel
        output_path = export_to_excel(final_df)
        return output_path
        
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"[process_excel_and_export] Unexpected error: {e}")
        raise ValueError(["An unexpected error occurred while processing the Excel file."])

