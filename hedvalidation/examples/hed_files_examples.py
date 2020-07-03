import os

from hed.validator.hed_input_reader import HedInputReader

if __name__ == '__main__':
    local_hed_file = '../tests/data/HED.xml'   # path HED v7.1.1 stored locally
    example_data_path = '../tests/data'   # path to example data
    valid_tsv_file = os.path.join(example_data_path, 'ValidTwoColumnHED7_1_1.tsv')

    bcit_guard_duty_path = os.path.join(example_data_path, 'BCIT_GuardDuty_HED_tag_spec_v27.tsv')
    tx_14_path = os.path.join(example_data_path, 'TX14 HED Tags v9.87.csv')
    tx_16_path = os.path.join(example_data_path, 'TX16 HED Tags v5.9.xlsx')
    bcit_rsvp = os.path.join(example_data_path, 'BCIT RSVP HED Tags v46.0.xlsx')
    bcit_driving = os.path.join(example_data_path, 'BCIT Driving HED Tags v46.0.xlsx')
    ncturwn = os.path.join(example_data_path, 'ExcelMultipleSheets.xlsx')
    ncturwn_lkt_worksheet = 'LKT Events'
    ncturwn_pvt_worksheet = 'PVT Events'
    ncturwn_das_worksheet = 'DAS Events'


    # Example 1c: Valid TSV file
    print(valid_tsv_file)
    hed_input_reader = HedInputReader(valid_tsv_file, tag_columns=[2])
    issues = hed_input_reader.get_validation_issues()
    print(hed_input_reader.get_printable_issue_string('Example 1 should have no issues'))

    print(valid_tsv_file)
    hed_input_reader = HedInputReader(valid_tsv_file, tag_columns=[2], hed_xml_file=local_hed_file)
    issues = hed_input_reader.get_validation_issues()
    print(hed_input_reader.get_printable_issue_string('Example 1 should have no issues'))

    # Example 2: Valid CSV file
    prefixed_needed_tag_columns = {3: 'Description', 4: 'Label', 5: 'Category'}
    hed_input_reader = HedInputReader(tx_14_path, tag_columns=[6],
                                      required_tag_columns=prefixed_needed_tag_columns)
    print(hed_input_reader.get_printable_issue_string('X14 HED Tags v9.87.csv abc issues'))

    # Example 3: Valid XLSX file
    prefixed_needed_tag_columns = {3: 'Description', 4: 'Label', 5: 'Category'}
    hed_input_reader = HedInputReader(bcit_rsvp, tag_columns=[6],
                                      required_tag_columns=prefixed_needed_tag_columns)
    print(hed_input_reader.get_printable_issue_string('BCIT RSVP HED Tags v46.0.xlsx abc issues'))


    # Example 4: Valid XLSX file
    prefixed_needed_tag_columns = {3: 'Description', 4: 'Label', 5: 'Category'}
    hed_input_reader = HedInputReader(tx_16_path, tag_columns=[6],
                                      required_tag_columns=prefixed_needed_tag_columns)
    print(hed_input_reader.get_printable_issue_string('TX16 HED Tags v5.9.xlsx abc issues'))

    # Example 5: Valid XLSX file
    prefixed_needed_tag_columns = {2: 'Label', 3: 'Description'}
    hed_input_reader = HedInputReader(ncturwn, tag_columns=[4], required_tag_columns=prefixed_needed_tag_columns,
                                      worksheet_name=ncturwn_lkt_worksheet)
    print(hed_input_reader.get_printable_issue_string('ExcelMultipleSheets.xlsx abc LKT Events worksheet issues'))

    # Example 6: Invalid XLSX file
    hed_input_reader = HedInputReader(ncturwn, tag_columns=[4], worksheet_name=ncturwn_pvt_worksheet)
    print(hed_input_reader.get_printable_issue_string('EventCodesNCTURWN_Revised.xlsx abc PVT Events worksheet issues'))

    # Example 7: Invalid XLSX file
    hed_input_reader = HedInputReader(ncturwn, tag_columns=[4], worksheet_name=ncturwn_das_worksheet)
    print(hed_input_reader.get_printable_issue_string('EventCodesNCTURWN_Revised.xlsx abc PVT Events worksheet issues'))
