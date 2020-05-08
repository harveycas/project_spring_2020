import pytest
from tetrad_analysis import dataframe_functions as ddf
import os
import pandas as pd
import numpy as np
from pathlib import Path
from pandas import DataFrame


#create sample excel document for performing tests
SAMPLE_XLSX = Path(__file__).parent/ "data"/"python_test_list.xlsx"
SAMPLE_DF_TAIL = pd.DataFrame(
    data={
             "Plate": [1,1,1],
             "Tetrad":[12,12,12],
             "spore":["12B","12C","12D"],
             "viability":[1,1,1],
             "NAT": [0,1,0],
             "HYG": [0,1,0],
             "URA": [0,1,0],
             }
     )
COL = "URA"   

#test read_excel_file() to see if it reads the input correctly
def test_read_excel_file():
    
    expected_tail = SAMPLE_DF_TAIL.set_index("Plate") 
    result = ddf.read_excel_file(SAMPLE_XLSX)  
    
    assert result.tail(3) == expected_tail
    

    
    
#test sort_and_filter_by_col() to make sure it sorts input data by correct col and positive values 
def test_sort_and_filter_by_col():
   
    expected_df = SAMPLE_DF_TAIL.set_index("Plate")


    expected_df_sorted = expected_df.sort_values(["URA"], ascending = False)
    
    #test for isolating positive values:
    
    expected_pos_vals = expected_df_sorted[expected_df_sorted[COL]>0]
    expected_df_filtered = pd.DataFrame(expected_pos_vals)

    
    result = ddf.sort_and_filter_by_col(expected_df,expected_df["URA"])
    
    assert result == expected_df_filtered
    
    
    
    
                  

#test combine_antibiotics() to see if it combines all positive values of col into one dictionary
def test_combine_antibiotics():
    
    expected_df = ddf.read_excel_file(SAMPLE_XLSX)
    markers = ['NAT','HYG','URA']
  
    
    expected_all_positive = {}
    for marker in markers:
        expected_marker = ddf.sort_and_filter_by_col(expected_df,marker)
        expected_all_positive[marker + '_plus'] = expected_marker
    return expected_all_positive
    
    result = ddf.combine_antibiotics(expected_df,markers)
    
    assert result == expected_all_positive
    
    
    
    
#tests write_marker_dict_to_disk() to see if it creates a new excel doucment for the newly created library
def test_write_marker_dict_to_disk():
   

    file_out = "test.xlsx"
    marker = "URA"
    
    writer = pd.ExcelWriter(file_out, engine='xlsxwriter')
    anti_bs = {"a": pd.DataFrame({"Plate": [1,1,1], "Tetrad":[12,12,12],})}
    for sheet_name in anti_bs.keys():
        anti_bs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    expected_result = writer.save
    
    result = ddf.write_marker_dict_to_disk(marker=[anti_bs,file_out])
    
    assert result == expected_result

    
    
    
#tests test_antibiotic_analysis() to see if it sorts the data within the new excel document before the document is sent out
def test_antibiotic_analysis():
    
    file_out = "test.xlsx"
    markers = ['NAT','HYG','URA']
    expected_df = ddf.read_excel_file(SAMPLE_XLSX)
    
    expected_df_tetrad = ddf.read_excel_file(SAMPLE_XLSX)
    expected_output_dict = ddf.combine_antibiotics(expected_df_tetrad, markers)
    expected_result = ddf.writer_marker_dict_to_disk(expected_output_dict,file_out)
    
    result = ddf.antibiotic_analysis(SAMPLE_XLSX,file_out="Antibiotic_markers.xlsx",markers=markers)
    
    assert result == expected_result
    

    
#for testing
if __name__=='__main__':
    test_read_excel_file()
    test_sort_and_filter_by_col()
    test_combine_antibiotics()
    test_write_marker_dict_to_disk()
    test_antibiotic_analysis()