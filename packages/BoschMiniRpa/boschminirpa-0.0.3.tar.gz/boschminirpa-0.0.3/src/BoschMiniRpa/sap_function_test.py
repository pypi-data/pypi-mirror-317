from mini_rpa_sap_automation import *
import pandas as pd

firefox_driver_path = r'C:\Python_Work\OBR RPA\geckodriver.exe'
test_file_path = r'C:\Users\LZV2SZH\Desktop\MiniRpa\web_sap_test.xlsx'
test_folder_path = r'C:\Users\LZV2SZH\Desktop\MiniRpa'
test_data = pd.read_excel(test_file_path, sheet_name='Sheet4', dtype=str)
test_data = test_data.fillna('')
test_data = test_data.to_dict(orient='records')

sap_automation = MiniRpaSapAutomation(True, test_folder_path, False, 'hk', False,
                                      False, '', firefox_driver_path, 1800,
                                      False, 15, '')

for data in test_data:
    function_name = data['function_name']
    print(function_name)
    layout_name = data['layout_name']
    field_values = data['field_values'].split(',')
    is_enter = True if data['is_enter'] == '1' else False
    is_tab = True if data['is_tab'] == '1' else False
    need_click_tip = True if data['need_click_tip'] == '1' else False
    shortcut_list = [shortcut for shortcut in data['shortcut_list'].split(',') if shortcut]
    if shortcut_list:
        shortcut_list = [getattr(Keys, shortcut) for shortcut in shortcut_list]
        # print('shortcut_list: ', shortcut_list)

    if function_name == 'login_sap':
        sap_automation.login_sap(data['sap_system'], data['sap_user'], data['sap_password'])
    elif function_name == 'input_sap_t_code':
        sap_automation.input_sap_t_code(data['t_code'])
    elif function_name == 'input_se16_table_name':
        sap_automation.input_se16_table_name(data['table_name'])
    elif function_name == 'input_field_multiple_values':
        sap_automation.input_field_multiple_values(int(data['field_button_index']), int(data['tab_index']), field_values)
    elif function_name == 'input_filed_single_value':
        sap_automation.input_filed_single_value(data['field_title'], int(data['field_index']), data['field_value'], is_enter, is_tab, need_click_tip)
    elif function_name == 'click_execute_button':
        sap_automation.click_execute_button()
    elif function_name == 'click_output_button':
        sap_automation.click_output_button()
    elif function_name == 'click_payroll_button':
        sap_automation.click_payroll_button()
    elif function_name == 'check_button_popup_and_click':
        sap_automation.check_button_popup_and_click(data['button_title'], int(data['try_times']))
    elif function_name == 'download_excel_by_click_print_preview':
        sap_automation.download_excel_by_click_print_preview(data['print_preview_title'], data['spreadsheet_title'], data['file_name'])
    elif function_name == 'download_excel_by_click_spreadsheet_button':
        sap_automation.download_excel_by_click_spreadsheet_button(data['spreadsheet_title'], data['file_name'])
    elif function_name == 'download_excel_by_press_short_keys':
        sap_automation.download_excel_by_press_short_keys(shortcut_list, data['file_name'])
    elif function_name == 'save_screenshot':
        sap_automation.save_screenshot(data['screenshot_folder_path'], data['screenshot_file_name_tag'], data['name_format'])
    elif function_name == 'download_excel_by_context_click':
        sap_automation.download_excel_by_context_click(data['column_name'], data['context_menu_item_name'], data['file_name'])
    elif function_name == 'select_layout_before_download_excel':
        sap_automation.select_layout_before_download_excel(layout_name, shortcut_list)
    elif function_name == 'click_button':
        sap_automation.click_button(data['button_title'])
    elif function_name == 'click_radio_checkbox':
        sap_automation.click_radio_checkbox(data['radio_checkbox_title'])
    elif function_name == 'input_reporting_period':
        sap_automation.input_reporting_period(data['reporting_period_name'], data['reporting_start_date'],
                                              data['reporting_end_date'])
    elif function_name == 'input_query_values':
        (query_button_index,
         query_value_input_method,
         query_value_list,
         query_value_columns,
         file_name,
         sheet_name,
         tab_index) = (int(data['field_button_index']),
                       data['query_value_input_method'],
                       data['query_value_list'],
                       data['query_value_columns'],
                       data['file_name'],
                       data['sheet_name'],
                       int(data['tab_index']))
        query_value_list = query_value_list.split(',') if query_value_list else None
        query_value_columns = query_value_columns.split(',') if query_value_columns else None
        sap_automation.input_query_values(query_button_index, query_value_input_method, query_value_list, query_value_columns, file_name, sheet_name, tab_index)
    elif function_name == 'find_variant_by_name':
        sap_automation.find_variant_by_name(data['variant_name'])
