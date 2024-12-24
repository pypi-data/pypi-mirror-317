import os

import pandas as pd
from BoschRpaMagicBox.common_functions import *

SE16_TABLE_NAME_INPUT_CSS_SELECTOR = "input[title='Table Name']"
POPUP_WINDOW_OK_BUTTON_CSS_SELECTOR = ".urPWInnerBorder div[title='Continue (Enter)']"
REPORTING_PERIOD_CSS_SELECTOR = "div[title^='Reporting Period:']"
REPORTING_PERIOD_DROPDOWN_CSS_SELECTOR = "input[value='Other Period']"
REPORTING_PERIOD_DROPDOWN_LIST_CSS_SELECTOR = "#DD_DATESAPLHR_QUERY_APPL_AREA-scrl div.lsListbox__values"
QUERY_PARAMETER_TR_CSS_SELECTOR = "table[id$='mrss-cont-none-content'] tr[id*='mrss-cont-none-Row'][id^='C']"
OUTPUT_BUTTON_CSS_SELECTOR = "div[title='Start output (F8)']"
GET_VARIANT_CSS_SELECTOR = "div[title^='Get Variant']"
GET_VARIANT_EXECUTE_CSS_SELECTOR = ".urPWFooterHeight div[title='Execute (F8)']"
PAYROLL_PERIOD_BUTTON_CSS_SELECTOR = "div[lsdata*='Payroll\\\\x20period']"


class MiniRpaSapAutomation:
    def __init__(self, has_save_folder: bool = True, save_folder_path: str = '', has_proxy: bool = False, proxy_area: str = 'hk',
                 is_private: bool = False, is_headless=False, firefox_binary_location: str = '', geckodriver_binary_location: str = '',
                 timeout=1800, auto_get_screenshot=False, time_interval=15, browser_screenshot_tag=''):
        """

        Args:
            auto_get_screenshot(bool): This is the flag whether to auto get browser screenshots
            time_interval(int): This is the time interval to get screenshot
            browser_screenshot_tag(str): Tag in screenshot name
            is_private(bool): Whether to open a private window
            has_save_folder(bool):This is the flag whether to set save folder path
            save_folder_path(str): This is the folder path of save folder
            has_proxy(bool): This is whether to use proxy when open browser
            proxy_area(str): This is the proxy setting for network.proxy.autoconfig_url
            firefox_binary_location(str): This is the path of firefox.exe
            is_headless(bool): This indicates whether to use headless mode to execute automation task
            timeout(int): This is the timeout setting
            geckodriver_binary_location(str): This is the path of geckodriver.exe
        """
        self.web_rpa = get_sap_web_gui_functions()
        self.browser, self.wait = self.web_rpa.initial_browser(has_save_folder, save_folder_path, has_proxy, proxy_area, is_private, is_headless, firefox_binary_location,
                                                               geckodriver_binary_location, timeout, auto_get_screenshot, time_interval, browser_screenshot_tag)

    def login_sap(self, sap_system, sap_user, sap_password):
        """ This function is used to log in SAP system.

        Args:

            sap_system(str): This is the name of SAP system
            sap_user(str): This is the username of SAP system
            sap_password(str): This is the password of SAP system
        """
        self.web_rpa.login_web_sap(sap_system, sap_user, sap_password)

    def input_sap_t_code(self, t_code):
        """ This function is used to input t_code in SAP system.

        Args:

            t_code(str): This is the transaction code of SAP system
        """
        self.web_rpa.input_t_code(t_code)

    def input_se16_table_name(self, table_name):
        """ This function is used to input table name in SE16.

        Args:

            table_name(str): This is the name of table
        """
        sleep(1)
        self.web_rpa.fill_input_filed_with_single_value(table_name, SE16_TABLE_NAME_INPUT_CSS_SELECTOR, is_tab=True)
        self.web_rpa.press_keyboard_shortcut([Keys.ENTER])
        sleep(1)

    def input_filed_single_value(self, field_title, field_index, field_value, is_enter, is_tab, need_click_tip):
        """ This function is used to input single field value in SE16.

        Args:
            field_index(int): This is the index of field. e.g. 1,2
            is_enter(bool): This is the flag whether to press enter
            is_tab(bool): This is the flag whether to press tab
            need_click_tip(bool): This is the flag whether to click tip
            field_title(str): This is the title of field
            field_value(str): This is the value of field
        """
        self.web_rpa.wait_element_presence_by_css_selector(f"input[title='{field_title}']")
        target_input_element = self.web_rpa.find_input_element_by_title(field_title, field_index)
        if target_input_element is not None:
            self.web_rpa.move_to_and_click_element('', target_element=target_input_element)
            sleep(1)
            self.web_rpa.fill_input_filed_with_single_value(field_value, '', is_enter, is_tab, need_click_tip, '', target_input_element)
            sleep(1)
        else:
            raise ValueError(f'Cannot find field: {field_title} with index: {field_index}')

    def input_field_multiple_values(self, field_button_index, tab_index, field_values):
        """ This function is used to input multiple field values in SE16.

        Args:
            field_button_index(int): This is the index of field button. e.g. 1,2
            tab_index(int): This is the index of tab. e.g. 1,2
            field_values(list): This is the list of values
        """
        self.web_rpa.input_multiple_selection_with_index(field_values, field_button_index, tab_index)

    def click_radio_checkbox(self, radio_checkbox_title):
        """ This function is used to click radio or checkbox in SE16.

        Args:
            radio_checkbox_title(str): This is the title of radio or checkbox
        """
        self.web_rpa.click_or_input_by_css_selector(f"span[title='{radio_checkbox_title}']", 'click')

    def click_button(self, button_title):
        """ This function is used to click button in SE16.

        Args:
            button_title(str): This is the title of button
        """
        self.web_rpa.click_or_input_by_css_selector(f"div[title='{button_title}']", 'click')
        sleep(1)

    def click_execute_button(self):
        """ This function is used to click execute button in SE16.
        """
        self.web_rpa.click_execute_button()
        sleep(3)
        self.web_rpa.wait_invisibility_of_loading_window()
        sleep(1)

    def click_output_button(self):
        """ This function is used to click output button.
        """
        self.web_rpa.move_to_and_click_element(OUTPUT_BUTTON_CSS_SELECTOR)
        sleep(3)
        self.web_rpa.wait_invisibility_of_loading_window()
        sleep(1)

    def select_layout_before_download_excel(self, layout_name: str, shortcut_list: list):
        """ This function is used to select layout before downloading excel.

        Args:
            layout_name(str): This is the name of layout
            shortcut_list(list): This is the list of shortcuts
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        self.web_rpa.select_sap_layout(layout_name, shortcut_list)
        sleep(1)

    def context_click_in_table(self, column_name, context_menu_item_name):
        """ This function is used to context click in table.

        Args:
            column_name(str): This is the name of column
            context_menu_item_name(str): This is the name of context menu item
        """
        div_column_css_selector = f"div[title='{column_name}']"
        span_column_css_selector = f"span[title='{column_name}']"

        # column_css_selector = ''
        while True:
            try:
                print(f'try to find {div_column_css_selector}')
                self.web_rpa.browser.find_element(By.CSS_SELECTOR, div_column_css_selector)
                column_css_selector = div_column_css_selector
                break
            except NoSuchElementException:
                try:
                    print(f'try to find {span_column_css_selector}')
                    self.web_rpa.browser.find_element(By.CSS_SELECTOR, span_column_css_selector)
                    column_css_selector = span_column_css_selector
                    break
                except NoSuchElementException:
                    sleep(1)
                    pass

        self.web_rpa.activate_context_click(column_css_selector)
        sleep(2)
        self.web_rpa.click_or_input_by_css_selector(f"tr[aria-label^='{context_menu_item_name}']", 'click')
        sleep(1)

    def download_excel_by_context_click(self, column_name, context_menu_item_name, file_name):
        """ This function is used to download excel by context click.

        Args:
            column_name(str): This is the name of column
            context_menu_item_name(str): This is the name of context menu item
            file_name(str): This is the name of file
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        self.context_click_in_table(column_name, context_menu_item_name)
        sleep(1)
        self.web_rpa.input_download_excel_file_name(file_name)

    def download_excel_by_click_spreadsheet_button(self, spreadsheet_title, file_name):
        """ This function is used to download excel by clicking spreadsheet button.

        Args:
            file_name(str): This is the name of file
            spreadsheet_title(str): This is the title of spreadsheet
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        self.web_rpa.click_or_input_by_css_selector(f"div[title='{spreadsheet_title}']", 'click')
        sleep(1)
        self.web_rpa.input_download_excel_file_name(file_name)
        sleep(1)

    def download_excel_by_click_print_preview(self, print_preview_title, spreadsheet_title, file_name):
        """ This function is used to download excel by clicking print preview.

        Args:
            print_preview_title(str): This is the title of print preview
            spreadsheet_title(str): This is the title of spreadsheet
            file_name(str): This is the name of file
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        self.web_rpa.click_or_input_by_css_selector(f"div[title='{print_preview_title}']", 'click')
        sleep(1)
        self.download_excel_by_click_spreadsheet_button(spreadsheet_title, file_name)

    def download_excel_by_press_short_keys(self, short_keys, file_name):
        """ This function is used to download excel by pressing short keys.

        Args:
            file_name(str): This is the name of file
            short_keys(list): This is the list of short keys
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        self.web_rpa.press_keyboard_shortcut(short_keys)
        sleep(1)
        self.web_rpa.input_download_excel_file_name(file_name)
        sleep(1)

    def save_screenshot(self, screenshot_folder_path, screenshot_file_name_tag='error_info', name_format='time'):
        """ This function is used to save screenshot.

        Args:
            screenshot_file_name_tag(str):This is the first part file name of screenshot
            screenshot_folder_path(str): This is the folder path of screenshot
            name_format(str): This indicates whether user date or datetime to name screenshot
        """
        self.web_rpa.get_screenshot(screenshot_folder_path, screenshot_file_name_tag, name_format)

    def check_button_popup_and_click(self, button_title, try_times=5):
        """ This function is used to check element exist and click.

        Args:
            button_title(str): This is the css selector of button
            try_times(int): This is the times to try
        """
        self.web_rpa.wait_invisibility_of_loading_window()
        button_css_selector = f"div[title='{button_title}']"
        try_time = 1
        while try_time <= try_times:
            print(f'try_time: {try_time}')
            try:
                print(f'try to find {button_css_selector}')
                self.web_rpa.browser.find_element(By.CSS_SELECTOR, button_css_selector)
            except NoSuchElementException:
                sleep(1)
                try_time += 1
            else:
                self.web_rpa.click_or_input_by_css_selector(button_css_selector, 'click')
                sleep(2)
                break

    def press_keyboard_shortcut(self, shortcut_list):
        """ This function is used to press shortcut.

        Args:
            shortcut_list(list): This is the list of shortcuts
        """
        self.web_rpa.press_keyboard_shortcut(shortcut_list)

    def input_reporting_period(self, reporting_period_name, reporting_start_date, reporting_end_date):
        """ This function is used to input reporting period.

        Args:
            reporting_period_name(str): This is the name of reporting period
            reporting_start_date(str): This is the start date
            reporting_end_date(str): This is the end date
        """
        self.web_rpa.click_or_input_by_css_selector(REPORTING_PERIOD_CSS_SELECTOR, 'click')
        sleep(1)
        self.web_rpa.wait_element_presence_by_css_selector(REPORTING_PERIOD_DROPDOWN_CSS_SELECTOR)
        self.web_rpa.click_or_input_by_css_selector(REPORTING_PERIOD_DROPDOWN_CSS_SELECTOR, 'click')
        sleep(1)
        self.web_rpa.wait_element_presence_by_css_selector(REPORTING_PERIOD_DROPDOWN_LIST_CSS_SELECTOR)

        self.web_rpa.click_or_input_by_css_selector(f"div[data-itemvalue2='{reporting_period_name}'", 'click')

        if reporting_period_name in ['Key Date', 'Other Period'] and reporting_start_date:
            self.input_filed_single_value('Start Date', 1, reporting_start_date, is_enter=True, is_tab=False, need_click_tip=False)
            sleep(1)

        if reporting_period_name in ['Other Period'] and reporting_end_date:
            self.input_filed_single_value('End Date', 1, reporting_end_date, is_enter=True, is_tab=False, need_click_tip=False)
            sleep(1)

    def input_query_values(self, query_button_index, query_value_input_method='user_input', query_value_list=None, query_value_columns=None, file_name='', sheet_name='Sheet1',
                           tab_index=1):
        """ This function is used to input query values.

        Args:
            query_button_index(int): This is the index of query button
            query_value_input_method(str): This is the method to input query values. user_input or file
            query_value_list(list): This is the list of query values
            query_value_columns(list): This is the list of query columns
            file_name(str): This is the path of file
            sheet_name(str): This is the name of sheet
            tab_index(int): This is the index of tab
        """
        if query_value_list is None:
            query_value_list = []

        if query_value_columns is None:
            query_value_columns = []

        if query_value_input_method == 'user_input':
            self.web_rpa.input_multiple_selection_with_index(query_value_list, query_button_index, tab_index, clear_section_data=True)
        elif query_value_input_method == 'file':
            file_data = self.load_downloaded_excel_file(file_name, sheet_name)
            if len(query_value_columns) == 2:
                file_data['paste_column'] = file_data[query_value_columns[0]] + '\t' + file_data[query_value_columns[1]]
                query_value_list = file_data['paste_column'].tolist()
            elif len(query_value_columns) == 1:
                query_value_list = file_data[query_value_columns[0]].tolist()
            else:
                raise ValueError('The query_value_columns should be correct values!')
            self.web_rpa.input_multiple_selection_with_index(query_value_list, query_button_index, tab_index, clear_section_data=True)
        sleep(2)

    def load_downloaded_excel_file(self, file_name, sheet_name='Sheet1'):
        """ This function is used to load downloaded Excel file.

        Args:
            file_name(str): This is the name of file
            sheet_name(str): This is the name of sheet
        """
        file_path = self.web_rpa.save_folder_path + os.sep + file_name
        if os.path.exists(file_path):
            file_data = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
        else:
            file_data = pd.DataFrame()

        return file_data

    def find_variant_by_name(self, variant_name):
        """ This function is used to find variant by name.

        Args:
            variant_name(str): This is the name of variant
        """
        self.web_rpa.click_or_input_by_css_selector(GET_VARIANT_CSS_SELECTOR, 'click')
        sleep(2)
        self.input_filed_single_value('Variant Name', 1, variant_name, is_enter=False, is_tab=True, need_click_tip=False)
        self.input_filed_single_value('User Name', 1, '', is_enter=False, is_tab=True, need_click_tip=False)
        self.web_rpa.click_or_input_by_css_selector(GET_VARIANT_EXECUTE_CSS_SELECTOR, 'click')
        sleep(1)
        self.web_rpa.wait_element_invisible_by_css_selector(GET_VARIANT_EXECUTE_CSS_SELECTOR)

    def click_payroll_button(self):
        """ This function is used to click payroll button
        """
        self.web_rpa.click_or_input_by_css_selector(PAYROLL_PERIOD_BUTTON_CSS_SELECTOR, 'click')
        sleep(2)

    def close_browser(self):
        """ This function is used to close browser.
        """
        self.web_rpa.quit_browser()
