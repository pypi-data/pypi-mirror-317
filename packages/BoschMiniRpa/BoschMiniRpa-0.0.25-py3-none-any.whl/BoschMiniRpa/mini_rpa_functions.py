from email.utils import formataddr
from mini_rpa_core import *
from mini_rpa_hrs_customized_functions import *
from BoschRpaMagicBox.remote_excel_functions import *
from BoschRpaMagicBox.helper_functions import *
from mini_rpa_sap_automation import *


class MiniRpaFunction(MiniRPACore):
    """This class is used to process single RPA task"""

    def __init__(self, user_name: str, user_password: str, server_name: str, share_name: str, port: int,
                 from_period: str, to_period: str, report_save_path: str, report_process_folder_path: str, report_period_type: str, process_cache_data: dict,
                 process_number: int,process_dict: dict, delivery_dict: dict, sap_operation_list: list, update_file_condition_setting: list,
                 from_file_condition_setting: list, data_type_dict: dict, download_data=False, process_data: bool = False, delivery_data: bool = False):
        """This function is used to initial parameters

        Args:
            user_name(str): This is the username
            user_password(str): This is the password
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            port(int): This is the port number of the server name
            from_period(str):This is the start month
            to_period(str): This is the end month
            report_process_folder_path(str): This is the file path for process Excel
            report_period_type(str): This is the report period type. e.g. period, current_date
            report_save_path(str): This is the folder path for original data
            delivery_data(bool): This is the indicator whether to delivery files to folders, receivers or api
            download_data(bool): This is the indicator whether to do sap operation
            process_data(bool): This is the indicator whether to process data
            process_cache_data(dict): This is the dict that save the process data
            data_type_dict(dict): This is the dict that save the data type
            sap_operation_list: This is the list of sap operation
            process_number(int): This is the number of process
            process_dict(dict): This is the dict that save the process logic data
            delivery_dict(dict): This is the dict that save the delivery logic data
            update_file_condition_setting(list): This is the list of update file condition setting
            from_file_condition_setting(list): This is the list of from file condition setting
        """
        super().__init__(user_name, user_password, server_name, share_name, port, from_period, to_period, report_save_path,
                         report_process_folder_path, report_period_type, process_cache_data, process_number, process_dict, delivery_dict,
                         sap_operation_list, update_file_condition_setting, from_file_condition_setting, data_type_dict, download_data, process_data, delivery_data)

        self.has_from_relevant_process = False
        self.relevant_from_process_number = 0
        self.relevant_from_flag = 'from_file'
        self.has_update_relevant_process = False
        self.relevant_update_process_number = 0
        self.relevant_update_flag = 'update_file'

    def keep(self, from_file_path: str, from_file_name: str, from_sheet_name: str, process_number: int, is_save: bool, has_from_file_condition: bool) \
            -> Union[pd.DataFrame, None]:
        """This function is used to remove data from loaded file

        Args:
            from_file_path(str): This is the file path of target Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            process_number(int): This is the process number
            is_save(bool): This is indicator whether to save processed data
            from_file_name(str): This is the file name of current file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
        """
        keep_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                keep_data, keep_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition, self.relevant_from_flag)
            else:
                keep_data, keep_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')
            self.process_cache_data[process_number]['from_file'] = keep_data.copy()
            self.save_file(process_number, from_file_name, keep_dtype_dict, keep_data, 'keep', from_sheet_name, is_save)
            print(f'---------------keep result of process no {process_number}---------------')
            print(keep_data.head())
            print('\n')
        return keep_data

    def vlookup(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_column_by: str, update_file_path: str,
                update_file_name: str, update_sheet_name: str, update_column_name: str, update_column_by: str, has_from_file_condition: bool, has_update_file_condition: bool,
                is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to vlookup data between two Excel sheets

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target excel file that is vlookuped
            from_file_name(str): This is the file name of excel file that is vlookuped
            from_sheet_name(str): This is the sheet name of excel file that is vlookuped
            from_column_name(str): This is the column name to be vlookuped of from file
            from_column_by(str): This is the by column of from file
            update_file_path(str): This is the file path of target excel file that vlookup
            update_file_name(str): This is the file name of excel file that vlookup
            update_sheet_name(str): This is the sheet name of excel file that vlookup
            update_column_name(str): This is the column name to be created in update file
            update_column_by(str): This is the by column of update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            has_update_file_condition(bool): This is the syntax dict for update file
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        is_update_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port)

        vlookup_data = None
        if is_from_file_exist and is_update_file_exist:
            if self.has_update_relevant_process:
                update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, self.relevant_update_process_number,
                                                                              has_update_file_condition, self.relevant_update_flag)
            else:
                update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, process_number, has_update_file_condition,
                                                                              'update_file')

            if self.has_from_relevant_process:
                from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition, self.relevant_from_flag)
            else:
                from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                          'from_file')

            self.process_cache_data[process_number]['from_file'] = from_data.copy()

            from_column_list = from_column_name.split(',')
            update_column_list = update_column_name.split(',')
            if from_column_by != update_column_by and from_column_by in update_data.columns:
                from_data = from_data.rename(columns={from_column_by: f'From_{from_column_by}'})
                from_column_by = f'From_{from_column_by}'
            column_rename_dict = dict(zip(from_column_list, update_column_list))
            from_data = from_data.loc[:, [from_column_by, *from_column_list]]
            from_data = from_data.rename(columns=column_rename_dict)
            vlookup_data = pd.merge(update_data, from_data, how='left', left_on=update_column_by, right_on=from_column_by)
            if update_column_by != from_column_by:
                vlookup_data.drop([from_column_by], axis=1, inplace=True)
            self.process_cache_data[process_number]['update_file'] = vlookup_data.copy()
            self.save_file(process_number, update_file_name, update_dtype_dict, vlookup_data, 'vlookup', update_sheet_name, is_save)
            print(f'---------------vlookup result of process no {process_number}---------------')
            print(vlookup_data.head())
            print('\n')
        elif is_update_file_exist:
            if self.has_update_relevant_process:
                update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, self.relevant_update_process_number,
                                                                              has_update_file_condition, self.relevant_update_flag)
            else:
                update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, process_number, has_update_file_condition,
                                                                              'update_file')
            vlookup_data = update_data
            update_column_list = update_column_name.split(',')
            for column in update_column_list:
                vlookup_data[column] = ''

            self.process_cache_data[process_number]['update_file'] = vlookup_data.copy()
            self.save_file(process_number, update_file_name, update_dtype_dict, vlookup_data, 'vlookup', update_sheet_name, is_save)
            print(f'---------------vlookup result of process no {process_number}---------------')
            print(vlookup_data.head())
            print('\n')
        return vlookup_data

    def copy_to_new(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, update_file_name: str,
                    update_sheet_name: str, update_column_name: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to copy data and paste to new created file

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file that is copied
            from_file_name(str): This is the file name of Excel file that is copied
            from_sheet_name(str): This is the sheet name of Excel file that is copied
            from_column_name(str): This is the column name to be copied of from file
            update_file_name(str): This is the file name of Excel file that need copied data
            update_sheet_name(str): This is the sheet name of excel file that vlookup
            update_column_name(str): This is the column name to be created in update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        copy_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                copy_data, copy_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition, self.relevant_from_flag)
            else:
                copy_data, copy_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')
            update_column_list = update_column_name.split(',')
            from_column_list = from_column_name.split(',')
            column_dict = dict(zip(from_column_list, update_column_list))
            copy_data = copy_data.loc[:, from_column_list]
            copy_data.rename(columns=column_dict, inplace=True)
            self.process_cache_data[process_number]['from_file'] = copy_data.copy()
            self.save_file(process_number, update_file_name, copy_dtype_dict, copy_data, 'copy to new', update_sheet_name, is_save)
            print(f'---------------copy to new result of process no {process_number}---------------')
            print(copy_data.head())
            print('\n')
        return copy_data

    def replace(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, original_value: str,
                replace_value: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to replace values with new values in specific columns

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file
            from_file_name(str): This is the file name of Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            from_column_name(str): This is the column name of from file whose value will be replaced
            original_value(str): This is the value or regular expression
            replace_value(str): This is the value to replace original value
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        replace_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                has_from_file_condition, self.relevant_from_flag)
            else:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                'from_file')
            from_column_list = from_column_name.split(',')
            for column in from_column_list:
                replace_data[column] = replace_data[column].str.replace(original_value, replace_value)

            self.process_cache_data[process_number]['from_file'] = replace_data.copy()
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'replace', from_sheet_name, is_save)
            print(f'---------------replace result of process no {process_number}---------------')
            print(replace_data.head())
            print('\n')
        return replace_data

    def replace_empty_value(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                            replace_value: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to replace empty values with new values in specific columns

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file
            from_file_name(str): This is the file name of Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            from_column_name(str): This is the column name of from file whose empty values will be replaced
            replace_value(str): This is the value to replace original value
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        replace_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                has_from_file_condition, self.relevant_from_flag)
            else:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                'from_file')
            from_column_list = from_column_name.split(',')

            for column in from_column_list:
                replace_data[column].fillna(replace_value, inplace=True)
                empty_value_data_flag = replace_data[column] == ''
                replace_data.loc[empty_value_data_flag, column] = replace_value

            self.process_cache_data[process_number]['from_file'] = replace_data.copy()
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'replace empty value', from_sheet_name, is_save)
            print(f'---------------replace empty value result of process no {process_number}---------------')
            print(replace_data.head())
            print('\n')
        return replace_data

    def combine_new_column(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                           new_column_name: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to create a new column by combine target column or columns

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be combined into new_column
            new_column_name: This is the new column that is combined from from_column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data
        """
        combine_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                has_from_file_condition, self.relevant_from_flag)
            else:
                combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                'from_file')
            from_column_list = from_column_name.split(',')
            combine_data[new_column_name] = ''
            for column in from_column_list:
                combine_data[new_column_name] = combine_data[new_column_name] + combine_data[column]

            self.process_cache_data[process_number]['from_file'] = combine_data.copy()
            self.save_file(process_number, from_file_name, combine_dtype_dict, combine_data, 'combine new column', from_sheet_name, is_save)

            print(f'---------------combine new column result of process no {process_number}---------------')
            print(combine_data)
            print('\n')
        return combine_data

    def split_to_new_file(self, from_file_path: str, from_file_name: str, from_sheet_name: str, from_group_by_column: str, process_number: int,
                          from_file_condition: bool) -> Union[pd.DataFrame, None]:
        """This function is used to split data into different files according to key columns

        Args:
           from_file_path: This is the file path of target Excel file
           from_file_name: This is the file name of Excel file
           from_sheet_name: This is the sheet name of Excel file
           from_group_by_column: This is the column name to be used as group by key
           process_number: This is the process number
           from_file_condition: This indicates whether current process has additional condition settings

        """
        split_column_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                split_data, split_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number, from_file_condition,
                                                                            self.relevant_from_flag)
            else:
                split_data, split_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, from_file_condition, 'from_file')

            self.process_cache_data[process_number]['from_file'] = split_data.copy()

            split_data[from_group_by_column].fillna('', inplace=True)
            split_data = split_data.groupby(by=[from_group_by_column])
            for split_column, split_column_data in split_data:
                split_file_name = from_file_name.split('.')[0] + f'_{split_column}.xlsx'
                split_file_path = from_file_path.split('.')[0] + f'_{split_column}.xlsx'
                smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, split_file_path, self.port)

                self.save_file(process_number, split_file_name, split_dtype_dict, split_column_data, 'split to new file', from_sheet_name, True)

                # file_obj = BytesIO()
                # with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
                #     split_column_data.to_excel(writer, index=False, float_format='%.2f')
                # file_obj.seek(0)
                # smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, split_file_path, file_obj, self.port)
                print(f'---------------split to new result of process no {process_number}---------------')
                print(split_column_data.head())
                print('\n')
        return split_column_data

    def column_calculate(self, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, new_column_name: str, process_number: int,
                         has_from_file_condition: bool, is_save: bool, function_type: str, calculate_value: str = '') -> Union[pd.DataFrame, None]:
        """This function is used to process values of different columns and create a new column to save result

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name of from file whose values will be calculated into new_column
            new_column_name: This is the new column that is combined by from_column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: whether to save file
            function_type: This is the function type, e.g. add, minus
            calculate_value(str): This is the value to be + - * /
        """
        combine_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                has_from_file_condition, self.relevant_from_flag)
            else:
                combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                'from_file')
            from_column_list = from_column_name.split(',')
            combine_data[new_column_name] = combine_data[from_column_list[0]]
            calculate_value_list = [value.strip() for value in calculate_value.split(',') if value.strip()]

            # calculation among columns
            for column in from_column_list[1:]:
                if function_type == 'column addition':
                    combine_data[new_column_name] = combine_data[new_column_name].add(combine_data[column], fill_value=0)
                if function_type == 'column deduction':
                    combine_data[new_column_name] = combine_data[new_column_name].sub(combine_data[column], fill_value=0)
                if function_type == 'column multiply':
                    combine_data[new_column_name] = combine_data[new_column_name].multiply(combine_data[column], fill_value=1)
                if function_type == 'column divide':
                    combine_data[new_column_name] = combine_data[new_column_name].divide(combine_data[column], fill_value=1)

            # calculation with fixed value
            if calculate_value_list:
                for str_calculate_value in calculate_value_list:
                    try:
                        float_calculate_value = round(float(str_calculate_value), 2)
                        if function_type == 'column addition':
                            combine_data[new_column_name] = combine_data[new_column_name] + float_calculate_value
                        if function_type == 'column deduction':
                            combine_data[new_column_name] = combine_data[new_column_name] - float_calculate_value
                        if function_type == 'column multiply':
                            combine_data[new_column_name] = combine_data[new_column_name] * float_calculate_value
                        if function_type == 'column divide':
                            float_calculate_value = float_calculate_value if float_calculate_value else 1
                            combine_data[new_column_name] = combine_data[new_column_name] / float_calculate_value
                    except ValueError:
                        pass

            self.process_cache_data[process_number]['from_file'] = combine_data.copy()
            self.save_file(process_number, from_file_name, combine_dtype_dict, combine_data, function_type, from_sheet_name, is_save)
            print(f'---------------create new column result of process no {process_number}---------------')
            print(combine_data.head())
            print('\n')
        return combine_data

    def copy_to_exist(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, update_file_path: str,
                      update_sheet_name: str, update_column_name: str, has_from_file_condition: bool):
        """This function is used to copy target column to existed Excel file

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file path that is copied
            from_file_name(str): This is the file name of Excel file that is copied
            from_sheet_name(str): This is the sheet name of Excel file that is copied
            from_column_name(str): This is the column name to be copied of from file
            update_column_name(str): This is the column name to be located in update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            update_file_path(str):This is the file path of  Excel file path that save copy columns
            update_sheet_name(str): This is the sheet name of Excel file that save copy data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        is_update_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port)

        if is_from_file_exist and is_update_file_exist:
            if self.has_from_relevant_process:
                from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition,
                                                                          self.relevant_from_flag)
            else:
                from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')
            from_column_list = [column.strip() for column in from_column_name.split(',')]
            update_column_list = [column.strip() for column in update_column_name.split(',')]
            print(f'---------------copy to exist result of process no {process_number}---------------')

            from_data_columns = set(list(from_data.columns))
            for column_name, column_type in from_dtype_dict.items():
                if column_name in from_data_columns:
                    from_data[column_name] = from_data[column_name].astype(column_type)
                    if column_type == str:
                        from_data[column_name] = "'" + from_data[column_name]

            self.process_cache_data[process_number]['from_file'] = from_data.copy()

            column_name_dict = dict(zip(from_column_list, update_column_list))
            append_flexible_dataframe_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path,
                                                 update_sheet_name, from_data, column_name_dict, self.port, True, True)

    def date_transfer(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                      has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to transfer date format


        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be transferred into date format
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data

        """
        date_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                date_data, date_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition, self.relevant_from_flag)
            else:
                date_data, date_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')

            if date_data is not None and not date_data.empty:
                from_column_list = from_column_name.split(',')
                for column in from_column_list:
                    date_data[column].fillna('', inplace=True)
                    date_data[column] = date_data[column].astype(str).str.strip()
                    date_data[column] = pd.to_datetime(date_data[column], errors='coerce').dt.strftime('%Y-%m-%d').fillna('')

                self.process_cache_data[process_number]['from_file'] = date_data.copy()
                self.save_file(process_number, from_file_name, date_dtype_dict, date_data, 'date_transfer', from_sheet_name, is_save)

                print(f'---------------date transfer result of process no {process_number}---------------')
                print(date_data.head())
                print('\n')
        return date_data

    def remove_duplicates(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                          has_from_file_condition: bool, keep_config: Union[str, bool], is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to remove duplicate values

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose values will be removed duplicates
            has_from_file_condition(bool):This indicates whether current process has additional condition settings
            is_save:This is indicator whether to save processed data
            keep_config(Union[str, False]): first, last or False
        """
        duplicate_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                duplicate_data, duplicate_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                    has_from_file_condition,
                                                                                    self.relevant_from_flag)
            else:
                duplicate_data, duplicate_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                    'from_file')
            from_column_list = from_column_name.split(',')
            duplicate_data.drop_duplicates(subset=from_column_list, keep=keep_config, inplace=True)
            self.process_cache_data[process_number]['from_file'] = duplicate_data.copy()
            self.save_file(process_number, from_file_name, duplicate_dtype_dict, duplicate_data, 'remove_duplicates', from_sheet_name, is_save)

            print(f'---------------remove duplicate result of process no {process_number}---------------')
            print(duplicate_data.head())
            print('\n')
        return duplicate_data

    def sort_values(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                    has_from_file_condition: bool, is_ascending: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to sort values

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose value will be sorted
            has_from_file_condition(bool):This indicates whether current process has additional condition settings
            is_save:This is indicator whether to save processed data
            is_ascending(bool): This is the indicator whether to sort values in ascending order
        """
        sort_values_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                sort_values_data, sort_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                 has_from_file_condition, self.relevant_from_flag)
            else:
                sort_values_data, sort_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                 'from_file')
            from_column_list = from_column_name.split(',')
            sort_values_data.sort_values(by=from_column_list, ascending=is_ascending, inplace=True)

            self.process_cache_data[process_number]['from_file'] = sort_values_data.copy()
            self.save_file(process_number, from_file_name, sort_dtype_dict, sort_values_data, 'sort_values', from_sheet_name, is_save)

            print(f'---------------sort values result of process no {process_number}---------------')
            print(sort_values_data.head())
            print('\n')
        return sort_values_data

    def contain_condition_replace(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_contain_column: str,
                                  original_value: str, replace_value: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to replace values with new values in specific columns after filtering data by using string contain function

        Args:
             process_number: This is the process number
             from_file_path: This is the file path of target Excel file path that is processed
             from_file_name: This is the file name of Excel file that is processed
             from_sheet_name: This is the sheet name of Excel file that is processed
             from_column_name: This is the column name to be processed of from file
             from_contain_column: This is the column name to be used for filtering
             original_value: This is the value or regular expression
             replace_value: This is the value to replace original value
             has_from_file_condition: This indicates whether current process has additional condition settings
             is_save: This is indicator whether to save processed data
        """
        replace_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                has_from_file_condition, self.relevant_from_flag)
            else:
                replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                'from_file')
            replace_data_status = replace_data[from_contain_column].str.contains(original_value, na=False, regex=False)
            replace_data.loc[replace_data_status, from_column_name] = replace_value

            self.process_cache_data[process_number]['from_file'] = replace_data.copy()
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'condition replace', from_sheet_name, is_save)

            print(f'---------------condition replace result of process no {process_number}---------------')
            print(replace_data.head())
            print('\n')
        return replace_data

    def group_by(self, process_number: int, from_file_path: str, from_file_name: str, update_file_name: str, from_sheet_name: str, update_sheet_name: str,
                 from_column_name: str, from_group_by_column: str, group_by_config: str, has_from_file_condition: bool, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to aggregate data according to condition

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            update_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            update_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name to be vlookuped of from file
            from_group_by_column: This is the column name to be used fill in from column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data
            group_by_config(str): sum or count
        """
        group_by_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                group_by_data, group_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                               has_from_file_condition,
                                                                               self.relevant_from_flag)
            else:
                group_by_data, group_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                               'from_file')
            from_column_list = from_column_name.split(',')
            from_column_by_list = from_group_by_column.split(',')
            group_by_data = group_by_data.loc[:, from_column_by_list + from_column_list]
            if group_by_config == 'sum':
                group_by_data = group_by_data.groupby(by=from_column_by_list, as_index=False, dropna=False).sum()
            elif group_by_config == 'count':
                group_by_data = group_by_data.groupby(by=from_column_by_list, as_index=False, dropna=False).count()

            for from_column_name in from_column_list:
                if from_column_name not in group_by_data.columns:
                    group_by_data[from_column_name] = ''
            self.process_cache_data[process_number]['from_file'] = group_by_data.copy()
            self.save_file(process_number, update_file_name, group_dtype_dict, group_by_data, 'group_by', update_sheet_name, is_save)

            print(f'---------------group by result of process no {process_number}---------------')
            print(group_by_data.head())
            print('\n')
        return group_by_data

    def column_compare(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_compare_column: str,
                       has_from_file_condition: bool, new_column_name: str, compare_result_value: str, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to compare values of two different columns and create new column to record compare result

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose value will be compared with from_compare_column
            has_from_file_condition:This indicates whether current process has additional condition settings
            new_column_name: This is the new column that will record compare result
            is_save:This is indicator whether to save processed data
            from_compare_column: This is the column name to be compared
            compare_result_value: This is the value to be updated in new_column
        """
        column_compare_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                column_compare_data, column_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                                      has_from_file_condition, self.relevant_from_flag)
            else:
                column_compare_data, column_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition,
                                                                                      'from_file')
            positive_result = compare_result_value.split(',')[0]
            negative_result = compare_result_value.split(',')[1]
            positive_compare_flag = column_compare_data[from_compare_column] == column_compare_data[from_column_name]
            negative_compare_flag = column_compare_data[from_compare_column] != column_compare_data[from_column_name]
            column_compare_data.loc[positive_compare_flag, new_column_name] = positive_result
            column_compare_data.loc[negative_compare_flag, new_column_name] = negative_result

            self.process_cache_data[process_number]['from_file'] = column_compare_data.copy()
            self.save_file(process_number, from_file_name, column_dtype_dict, column_compare_data, 'column_compare', from_sheet_name, is_save)

            print(f'---------------column compare result of process no {process_number}---------------')
            print(column_compare_data)
            print('\n')
        return column_compare_data

    def calculate_anniversary_duration(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                                       has_from_file_condition: bool, new_column_name: str, is_save: bool) -> Union[pd.DataFrame, None]:
        """This function is used to calculate time difference between values of from column and today (anniversary duration)

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name
            has_from_file_condition:This indicates whether current process has additional condition settings
            new_column_name: This is the new column that will record compare result
            is_save:This is indicator whether to save processed data
        """
        time_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                time_data, time_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                          has_from_file_condition, self.relevant_from_flag)
            else:
                time_data, time_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')
            time_data = hrs_calculate_duration(time_data, from_column_name, self.from_period, new_column_name)

            self.process_cache_data[process_number]['from_file'] = time_data.copy()
            self.save_file(process_number, from_file_name, time_dtype_dict, time_data, 'calculate_anniversary_duration', from_sheet_name, is_save)

            print(f'---------------calculate time duration result of process no {process_number}---------------')
            print(time_data)
            print('\n')
        return time_data

    def copy_excel_files(self, from_folder_path: str, from_file_name: str, update_folder_path: str):
        """This function is used to copy files from from_folder or sub_folder of from folder to update folder

        Args:
            from_folder_path: This is the from_folder_path
            from_file_name: This is the file name that contains common file name fragment
            update_folder_path: This is the target folder path

        """
        traverse_result_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, from_folder_path, self.port)
        sub_folder_list = [folder_item for folder_item in traverse_result_list if folder_item['is_folder']]

        sub_folder_list.sort(key=lambda folder_item: folder_item['creation_time'])
        sub_folder_list = [folder_item['name'] for folder_item in sub_folder_list]

        print(f'--------------- copy files ---------------')
        if sub_folder_list:
            if self.from_period:
                target_folder_path = from_folder_path + os.sep + f'{self.from_period[:4]}.{self.from_period[4:]}'
            else:
                target_folder_path = from_folder_path + os.sep + sub_folder_list[-1]
            file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, target_folder_path, self.port)
            target_file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]
            for file_name in target_file_name_list:
                upper_file_name = file_name.upper()
                if from_file_name.upper() in upper_file_name and '.XLS' in upper_file_name:
                    print(f'--------------- copy file for {target_folder_path + os.sep + file_name} ---------------')
                    from_file_path = target_folder_path + os.sep + file_name
                    update_file_path = update_folder_path + os.sep + file_name
                    from_file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
                    smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, from_file_obj, self.port)
        else:
            print('Target folder is not found！')

    def combine_excel_files(self, from_folder_path: str, from_file_name: str, from_sheet_name: str, update_folder_path: str, update_file_name: str, update_sheet_name: str,
                            process_number: int, function_name: str):
        """This function is used to combine files from from_folder or sub_folder of from folder ,then save to update folder

        Args:
            from_folder_path: This is the from_folder_path
            from_file_name: This is the file name that contains common file name fragment
            update_folder_path: This is the target folder path
            from_sheet_name: This is the sheet name of from_file
            update_file_name: This is the file name of update file
            update_sheet_name:This is the sheet name to be saved
            process_number: This is the process number
            function_name: This is the function name
        """
        file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, from_folder_path, self.port)
        target_file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]
        combine_data_list = []
        from_sheet_list = from_sheet_name.split(',')
        for file_name in target_file_name_list:
            upper_file_name = file_name.upper()
            if from_file_name.upper() in upper_file_name and '.XLS' in upper_file_name:
                file_path = from_folder_path + os.sep + file_name
                for from_sheet_name in from_sheet_list:
                    try:
                        file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
                        from_file_data = pd.read_excel(file_obj, sheet_name=from_sheet_name, dtype=str)
                    except ValueError:
                        pass
                    else:
                        combine_data_list.append(from_file_data)
                        break
        print(f'--------------- combine files ---------------')
        if combine_data_list:
            combine_data = pd.concat(combine_data_list, ignore_index=True)
            combine_data_save_path = update_folder_path + os.sep + f'{process_number}_{function_name}_{update_file_name}'

            file_obj = BytesIO()
            with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
                combine_data.to_excel(writer, index=False, float_format='%.2f', sheet_name=update_sheet_name)
            file_obj.seek(0)
            smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, combine_data_save_path, file_obj, self.port)

    def copy_value_to_range(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, has_from_file_condition: bool,
                            update_folder_path: str, update_file_name: str, update_file_sheet: str, update_range: str) -> Union[pd.DataFrame, None]:
        """This function is used to copy dataframe value to range/ranges of Excel file

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            update_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name to be saved in update_file_sheet
            has_from_file_condition: This indicates whether current process has additional condition settings
            update_folder_path: This is the folder path where update file is located
            update_file_name: This is the file name of update file
            update_file_sheet: This is the sheet name of update file
            update_range: This is the range name in the update sheet. e.g. A1, B1

        """
        new_target_data = None
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            if self.has_from_relevant_process:
                target_data, target_data_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, self.relevant_from_process_number,
                                                                             has_from_file_condition, self.relevant_from_flag)
            else:
                target_data, target_data_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, process_number, has_from_file_condition, 'from_file')

            from_column_list = from_column_name.split(',')
            new_target_data = target_data.loc[:, from_column_list]
            for column_name, column_type in target_data_dict.items():
                if column_name in new_target_data.columns and column_type == str:
                    new_target_data[column_name] = "'" + new_target_data[column_name]

            self.process_cache_data[process_number]['from_file'] = new_target_data.copy()
            update_file_path = update_folder_path + os.sep + update_file_name
            save_dataframe_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, update_file_sheet, new_target_data,
                                      update_range, False, self.port)

            print(f'---------------copy_value_to_range result of process no {process_number}---------------')
            print(new_target_data)
            print('\n')
        return new_target_data

    def delete_files(self, all_from_file_name):
        """This function is used to delete file

        Args:
            all_from_file_name(str): This is the file name who will be deleted.It is seperated by ','
        """
        file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, self.report_save_path, self.port)
        file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]

        for from_file_name in all_from_file_name.split(','):
            from_file_name = from_file_name.strip()
            if from_file_name:
                for existed_file_name in file_name_list:
                    if from_file_name in existed_file_name:
                        file_path = self.report_save_path + os.sep + existed_file_name
                        try:
                            smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
                            print(f'-----{file_path} is deleted successfully!-----')
                        except:
                            print(f'Failed to delete： {file_path}')

    def send_email(self, email_account: str, email_password: str, email_address: str, email_body: str, email_header: str, email_subject: str, email_to: list, email_cc: list,
                   attachment_name: str, error_log_folder_path: str):
        """This function is used to send emails

        Args:
            email_account(str): This is the email account
            email_password(str): This is the email password for nt account
            email_address(str): This is the email address of nt account
            email_body(str): This is the email content
            email_header(str): This is the customized sender name instead of actual user nt
            email_subject(str): This is the email subject
            email_to(list): This is the list of to emails
            email_cc(list): This is the list of cc emails
            attachment_name(str): This is the name of attachment.
            error_log_folder_path(str): This is the folder path for saving error log. This is the path on the server rather than the remote folder path.
        """
        mail_host = 'rb-smtp-auth.rbesz01.com'
        mail_user = f'APAC\\{email_account}'
        mail_pass = f'{email_password}'
        sender = email_address

        try:
            smtpObj = smtplib.SMTP(mail_host, 25)
            smtpObj.starttls()
            smtpObj.login(mail_user, mail_pass)
            receivers = ','.join(email_to)
            ccs = ','.join(email_cc)

            message = MIMEMultipart()
            message['From'] = formataddr((str(Header(email_header, 'utf-8')), sender))
            message['To'] = receivers
            message['Cc'] = ccs

            message['Subject'] = email_subject
            content = MIMEText(email_body, 'html', 'utf-8')
            message.attach(content)

            # add attachment
            attachment_file_path = self.report_save_path + os.sep + attachment_name
            is_attachment_exist, attachment_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, attachment_file_path,
                                                                       self.port)
            if is_attachment_exist:
                email_attachment = MIMEApplication(attachment_obj)
                email_attachment.add_header('Content-Disposition', 'attachment', filename=attachment_name)  # 为附件命名
                message.attach(email_attachment)

            smtpObj.sendmail(from_addr=sender, to_addrs=email_to + email_cc, msg=message.as_string())
            smtpObj.quit()
            print(f'-----email is sent successfully!-----')
        except:
            print('Mail sent failed.')
            create_error_log(error_log_folder_path, traceback.format_exc())

    def upload_file_by_api(self, file_path: str, api: str, api_add_token: bool, api_token: str, api_bearer: str, error_log_folder_path: str):
        """This function is used to upload file by api

        Args:
            file_path(str): This is the file path that need to be uploaded
            api(str): This is the api that is used to upload file
            api_add_token(bool): This is the indicator  whether to use token
            api_token(str): This is the token value
            api_bearer(str): This is the bearer value
            error_log_folder_path(str): This is the folder path for saving error log. This is the path on the server rather than the remote folder path.
        """
        new_api_token = ''
        new_api_bearer = ''

        is_file_exist, file_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
        if is_file_exist:
            files = {'file': file_obj}
            headers = {}
            if api_add_token:
                headers = {
                    'Bearer': api_bearer,
                    'Token': api_token
                }
            res = requests.post(api, files=files, headers=headers, verify=False)
            if int(res.status_code) == 200:
                res_json = res.json()
                if res_json['isSuccess']:
                    print(f'-----{file_path} is uploaded successfully!-----')
                    new_api_token = res.headers['Token']
                    new_api_bearer = res.headers['Bearer']
                else:
                    print(f'{file_path} is failed to upload!')
            else:
                print(f'There is un error to upload {file_path}!')
                create_error_log(error_log_folder_path, res.text)

        return new_api_token, new_api_bearer

    # def start_bot(self):
    #     """This function is used to collect all function and start to run bot
    #
    #     """
    #     time_start = perf_counter()
    #
    #     if self.download_data:
    #         sap_automation = MiniRpaSapAutomation(**self.sap_config_dict)
    #
    #         for sap_operation_dict in self.sap_operation_list:
    #             function_name = sap_operation_dict['function_name']
    #             print(f'---------- current sap function is {function_name} ----------')
    #
    #             layout_name = sap_operation_dict['layout_name']
    #             field_values = sap_operation_dict['field_values'].split(',')
    #             is_enter = sap_operation_dict['is_enter']
    #             is_tab = sap_operation_dict['is_tab']
    #             need_click_tip = sap_operation_dict['need_click_tip']
    #             shortcut_list = [shortcut for shortcut in sap_operation_dict['shortcut_list'].split(',') if shortcut]
    #             if shortcut_list:
    #                 shortcut_list = [getattr(Keys, shortcut) for shortcut in shortcut_list]
    #
    #             if function_name == 'login_sap':
    #                 sap_automation.login_sap(sap_operation_dict['sap_system'], sap_operation_dict['sap_user'], sap_operation_dict['sap_password'])
    #             elif function_name == 'input_sap_t_code':
    #                 sap_automation.input_sap_t_code(sap_operation_dict['t_code'])
    #             elif function_name == 'input_se16_table_name':
    #                 sap_automation.input_se16_table_name(sap_operation_dict['table_name'])
    #             elif function_name == 'input_field_multiple_values':
    #                 sap_automation.input_field_multiple_values(int(sap_operation_dict['field_button_index']), int(sap_operation_dict['tab_index']), field_values)
    #             elif function_name == 'input_filed_single_value':
    #                 sap_automation.input_filed_single_value(sap_operation_dict['field_title'], int(sap_operation_dict['field_index']), sap_operation_dict['field_value'], is_enter,
    #                                                         is_tab, need_click_tip)
    #             elif function_name == 'click_execute_button':
    #                 sap_automation.click_execute_button()
    #             elif function_name == 'check_button_popup_and_click':
    #                 sap_automation.check_button_popup_and_click(sap_operation_dict['button_title'], int(sap_operation_dict['try_times']))
    #             elif function_name == 'download_excel_by_click_spreadsheet_button':
    #                 sap_automation.download_excel_by_click_spreadsheet_button(sap_operation_dict['spreadsheet_title'], sap_operation_dict['file_name'])
    #             elif function_name == 'download_excel_by_press_short_keys':
    #                 sap_automation.download_excel_by_press_short_keys(shortcut_list, sap_operation_dict['file_name'])
    #             elif function_name == 'save_screenshot':
    #                 sap_automation.save_screenshot(sap_operation_dict['screenshot_folder_path'], sap_operation_dict['screenshot_file_name_tag'], sap_operation_dict['name_format'])
    #             elif function_name == 'download_excel_by_context_click':
    #                 sap_automation.download_excel_by_context_click(sap_operation_dict['column_name'], sap_operation_dict['context_menu_item_name'], sap_operation_dict['file_name'])
    #             elif function_name == 'select_layout_before_download_excel':
    #                 sap_automation.select_layout_before_download_excel(layout_name, shortcut_list)
    #             elif function_name == 'click_button':
    #                 sap_automation.click_button(sap_operation_dict['button_title'])
    #             elif function_name == 'click_radio_checkbox':
    #                 sap_automation.click_radio_checkbox(sap_operation_dict['radio_checkbox_title'])
    #
    #     if self.process_data:
    #         self.prepare_data_type()
    #         self.initial_process_cache_data()
    #
    #         self.has_from_relevant_process = self.process_dict['has_from_relevant_process']
    #         self.relevant_from_process_number = self.process_dict['relevant_from_process_number']
    #         self.relevant_from_flag = self.process_dict['relevant_from_flag']  # from_file or update_file
    #         self.has_update_relevant_process = self.process_dict['has_update_relevant_process']
    #         self.relevant_update_process_number = self.process_dict['relevant_update_process_number']
    #         self.relevant_update_flag = self.process_dict['relevant_update_flag']  # from_file or update_file
    #
    #         process_number = self.process_number
    #         function_name = self.process_dict['function_name']
    #         is_save = self.process_dict['is_save']
    #
    #         from_file_path = self.process_dict['from_file_path']
    #         from_file_name = self.process_dict['from_file_name']
    #         from_sheet_name = self.process_dict['from_sheet_name']
    #         from_folder_path = self.process_dict['from_folder_path']
    #         from_column_name = self.process_dict['from_column']
    #         from_column_by = self.process_dict['from_column_by']
    #         from_compare_column = self.process_dict['from_compare_column']
    #         from_group_by_column = self.process_dict['from_group_by_column']
    #         from_contain_column = self.process_dict['from_contain_column']
    #         from_group_by_column = self.process_dict['from_group_by_column']
    #         has_from_file_condition = self.process_dict['has_from_file_condition']
    #         all_from_delete_file_name = self.process_dict['all_from_delete_file_name']
    #
    #         update_file_path = self.process_dict['update_file_path']
    #         update_file_name = self.process_dict['update_file_name']
    #         update_sheet_name = self.process_dict['update_sheet_name']
    #         update_folder_path = self.process_dict['update_folder_path']
    #         update_column_name = self.process_dict['update_column']
    #         update_column_by = self.process_dict['update_column_by']
    #         has_update_file_condition = self.process_dict['has_update_file_condition']
    #         update_range = self.process_dict['update_range']
    #
    #         original_value = self.process_dict['original_value']
    #         replace_value = self.process_dict['replace_value']
    #         new_column_name = self.process_dict['new_column']
    #         compare_result_value = self.process_dict['compare_result_value']
    #         calculate_value = self.process_dict['calculate_value']
    #         keep_config = self.process_dict['keep_config']
    #         group_by_config = self.process_dict['group_by_config']
    #         is_ascending = self.process_dict['is_ascending']
    #
    #         if function_name == 'keep':
    #             self.keep(self.from_file_path, self.from_file_name, self.from_sheet_name, process_number, is_save, has_from_file_condition)
    #         elif function_name == 'vlookup':
    #             self.vlookup(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_column_by,
    #                          self.update_file_path, self.update_file_name, self.update_sheet_name, update_column_name, update_column_by, has_from_file_condition,
    #                          has_update_file_condition, is_save)
    #         elif function_name == 'copy as new file':
    #             copy_as_new_file(from_folder_path, self.from_file_name, update_folder_path, update_file_name, self.from_period, self.user_name, self.user_password,
    #                              self.server_name, self.share_name, self.port)
    #         elif function_name == 'copy to new':
    #             self.copy_to_new(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, self.update_file_name,
    #                              update_column_name, has_from_file_condition, is_save)
    #         elif function_name == 'replace':
    #             self.replace(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, original_value, replace_value,
    #                          has_from_file_condition, is_save)
    #         elif function_name == 'replace empty value':
    #             self.replace_empty_value(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, replace_value,
    #                                      has_from_file_condition, is_save)
    #         elif function_name == 'combine new column':
    #             self.combine_new_column(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name,
    #                                     has_from_file_condition, is_save)
    #
    #         elif function_name == 'split to new':
    #             self.split_to_new_file(self.from_file_path, self.from_file_name, self.from_sheet_name, from_group_by_column, process_number,
    #                                    has_from_file_condition)
    #
    #         elif function_name == 'column addition':
    #             self.column_calculate(self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name, process_number,
    #                                   has_from_file_condition, is_save, 'column addition', calculate_value)
    #         elif function_name == 'column deduction':
    #             self.column_calculate(self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name, process_number,
    #                                   has_from_file_condition, is_save, 'column deduction', calculate_value)
    #         elif function_name == 'column multiply':
    #             self.column_calculate(self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name, process_number,
    #                                   has_from_file_condition, is_save, 'column multiply', calculate_value)
    #         elif function_name == 'column divide':
    #             self.column_calculate(self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name, process_number,
    #                                   has_from_file_condition, is_save, 'column divide', calculate_value)
    #         elif function_name == 'copy to exist':
    #             self.copy_to_exist(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, self.update_file_path,
    #                                self.update_sheet_name, update_column_name, has_from_file_condition)
    #         elif function_name == 'date transfer':
    #             self.date_transfer(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
    #                                is_save)
    #         elif function_name == 'remove duplicates':
    #             self.remove_duplicates(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
    #                                    keep_config, is_save)
    #         elif function_name == 'sort values':
    #             self.sort_values(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
    #                              is_ascending, is_save)
    #
    #         elif function_name == 'contain condition replace':
    #             self.contain_condition_replace(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_contain_column,
    #                                            original_value, replace_value, has_from_file_condition, is_save)
    #
    #         elif function_name == 'group by':
    #             self.group_by(process_number, self.from_file_path, self.from_file_name, self.update_file_name, self.from_sheet_name, self.update_sheet_name, from_column_name,
    #                           from_group_by_column, group_by_config, has_from_file_condition, is_save)
    #
    #         elif function_name == 'column compare':
    #             self.column_compare(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_compare_column,
    #                                 has_from_file_condition, new_column_name, compare_result_value, is_save)
    #         elif function_name == 'calculate anniversary duration':
    #             self.calculate_anniversary_duration(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
    #                                                 new_column_name, is_save)
    #         elif function_name == 'copy excel files':
    #             self.copy_excel_files(from_folder_path, from_file_name, update_folder_path)
    #         elif function_name == 'combine excel files':
    #             self.combine_excel_files(from_folder_path, from_file_name, self.from_sheet_name, update_folder_path, self.update_file_name,
    #                                      self.update_sheet_name, process_number, function_name)
    #         elif function_name == 'copy value to range':
    #             self.copy_value_to_range(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
    #                                      update_folder_path,
    #                                      self.update_file_name, self.update_sheet_name, update_range)
    #         elif function_name == 'delete files':
    #             self.delete_files(all_from_delete_file_name)
    #
    #     if self.delivery_data:
    #         self.prepare_file_name_suffix()
    #         delivery_type = self.delivery_dict['delivery_type']
    #         if delivery_type == 'send email':
    #             # error_log_folder_path is teh path on the server rather than the remote folder path
    #             email_fields = ['email_account', 'email_password', 'email_address', 'email_body', 'email_header', 'email_subject', 'email_to', 'email_cc', 'attachment_name',
    #                             'error_log_folder_path']
    #             email_values = {field: self.delivery_dict.get(field, [] if field in ['email_to', 'email_cc'] else '') for field in email_fields}
    #
    #             email_account = email_values['email_account']
    #             email_password = email_values['email_password']
    #             email_address = email_values['email_address']
    #             email_body = email_values['email_body']
    #             email_header = email_values['email_header']
    #             email_subject = email_values['email_subject']
    #             email_to = email_values['email_to']
    #             email_cc = email_values['email_cc']
    #             attachment_name = self.delivery_dict['file_name'] + f'{self.file_name_suffix}.xlsx'
    #             error_log_folder_path = email_values['error_log_folder_path']
    #             self.send_email(email_account, email_password, email_address, email_body, email_header, email_subject, email_to, email_cc, attachment_name, error_log_folder_path)
    #         elif delivery_type == 'fixed folder':
    #             delivery_file_name = self.delivery_dict.get('file_name', '') + f'{self.file_name_suffix}.xlsx'
    #             delivery_file_path = self.delivery_dict.get('delivery_file_path', '')
    #             original_file_path = self.report_save_path + os.sep + delivery_file_name
    #
    #             smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, delivery_file_path, self.port)
    #             file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, original_file_path, self.port)
    #             smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, delivery_file_path, file_obj, self.port)
    #             print(f'-----{original_file_path} is copied successfully!-----')
    #         elif delivery_type == 'api':
    #             # error_log_folder_path is teh path on the server rather than the remote folder path
    #             api_fields = ['api', 'api_add_token', 'api_token', 'api_bearer', 'error_log_folder_path', 'file_name']
    #             api_values = {field: self.delivery_dict.get(field, False if field == 'api_add_token' else '') for field in api_fields}
    #
    #             api = api_values['api']
    #             api_add_token = api_values['api_add_token']
    #             api_token = api_values['api_token']
    #             api_bearer = api_values['api_bearer']
    #             error_log_folder_path = api_values['error_log_folder_path']
    #             api_file_name = api_values['file_name'] + f'{self.file_name_suffix}.xlsx'
    #             api_file_path = self.report_save_path + os.sep + api_file_name
    #             new_api_token, new_api_bearer = self.upload_file_by_api(api_file_path, api, api_add_token, api_token, api_bearer, error_log_folder_path)
    #
    #     time_end = perf_counter()
    #     total_time_in_minutes = round((time_end - time_start) / 60, 2)
    #     print(f'Congratulations, all work has been completed successfully!\nTotal Time: {total_time_in_minutes} minutes.')
