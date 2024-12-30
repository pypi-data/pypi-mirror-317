import sys
import base64
import json
from BoschMiniRpa.mini_rpa_manager import MiniRpaManager


def prepare_setting_data_and_run_rpa():
    """ This function is used to prepare the setting data and run the rpa bot

    """
    try:
        input_data = sys.stdin.read()
        decoded_data = base64.b64decode(input_data).decode('utf-8')
        bot_variant_data: dict = json.loads(decoded_data)

        process_cache_data = {}

        (report_module_dict,
         public_folder_dict,
         data_type_dict,
         process_data_dict,
         common_filed_dict) = (bot_variant_data['report_module_dict'],
                               bot_variant_data['public_folder_dict'],
                               bot_variant_data['data_type_dict'],
                               bot_variant_data['process_data_dict'],
                               bot_variant_data['common_filed_dict']
                               )

        (user_name,
         user_password,
         server_name,
         share_name,
         port,
         report_save_path,
         report_process_folder_path,
         ) = (
            public_folder_dict['user_name'],
            public_folder_dict['user_password'],
            public_folder_dict['server_name'],
            public_folder_dict['share_name'],
            public_folder_dict['port'],
            public_folder_dict['report_save_path'],
            public_folder_dict['report_process_folder_path'],
        )

        (
            report_period_type,
            date_format,
            from_period,
            to_period,
            company_code,
            payroll_area,
            employee_subgroup,
            employee_group
        ) = (
            common_filed_dict['report_period_type'],
            common_filed_dict['date_format'],
            common_filed_dict['from_period'],
            common_filed_dict['to_period'],
            common_filed_dict['company_code'],
            common_filed_dict['payroll_area'],
            common_filed_dict['employee_subgroup'],
            common_filed_dict['employee_group']
        )

        download_data, process_data, delivery_data = (report_module_dict['download_data'], report_module_dict['process_data'], report_module_dict['delivery_data'])

        for process_index, process_data_dict in process_data_dict.items():
            for process_type, process_data_list in process_data_dict.items():
                print(f'----------  {process_type} ----------')
                if process_type == 'data_process' and process_data or process_type == 'delivery_process' and delivery_data:
                    for process_dict in process_data_dict:
                        process_number = process_data_dict['process_number']
                        update_file_condition_setting, from_file_condition_setting = (
                            process_dict.get('update_filter_data_list', []), process_dict.get('from_filter_data_list', []))
                        start_mini_rpa = MiniRpaManager(user_name, user_password, server_name, share_name, port, from_period, to_period, report_save_path,
                                                        report_process_folder_path,
                                                        report_period_type, process_cache_data, process_number, process_dict, {}, [], update_file_condition_setting,
                                                        from_file_condition_setting, data_type_dict, download_data, process_data, delivery_data)
                        start_mini_rpa.start_bot()
                elif process_type == 'sap_process' and download_data:
                    start_mini_rpa = MiniRpaManager(user_name, user_password, server_name, share_name, port, from_period, to_period, report_save_path, report_process_folder_path,
                                                    report_period_type, process_cache_data, 0, {}, {}, process_data_list, [], [], data_type_dict,
                                                    download_data, process_data, delivery_data)
                    start_mini_rpa.start_bot()
        print('All tasks have been completed successfully')
        sys.exit(0)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


prepare_setting_data_and_run_rpa()
