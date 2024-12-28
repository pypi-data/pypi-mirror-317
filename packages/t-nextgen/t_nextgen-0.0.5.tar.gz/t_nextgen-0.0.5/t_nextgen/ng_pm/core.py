"""NextGenCore Module."""

import time
from typing import Optional
from t_desktop.config import IS_WINDOWS_OS

if IS_WINDOWS_OS:
    from pywinauto import keyboard
    from pywinauto.findwindows import ElementNotFoundError

from t_desktop.decorators import retry_if_pywin_error
from t_desktop.decorators import capture_screenshot_if_pywin_error
from t_desktop.exceptions import AppCrashException
from t_ocr import Textract
from t_nextgen.exceptions import WrongDatabaseSelectedError, MultipleSessionsError
from t_nextgen.config import Config
from t_nextgen.ng_app_manager import NGAppManager
from t_nextgen.ng_pm.windows.batch_maitenance import BatchMaintenanceWindow
from t_nextgen.ng_pm.windows.batch_posting import BatchPostingWindow
from t_nextgen.ng_pm.windows.cob import COBWindow
from t_nextgen.ng_pm.windows.encounter_insurance import EncounterInsuranceWindow
from t_nextgen.ng_pm.windows.import_file import ImportFileWindow
from t_nextgen.ng_pm.windows.payment_entry import PaymentEntryWindow
from t_nextgen.ng_pm.windows.transaction_ledger import TransactionLedgerWindow
from t_nextgen.utils.logger import logger


class NextGenPMCore:
    """NextGenPMCore Class.

    This class is used to access all the windows of NextGen PM.
    """

    def __init__(
        self,
        username: str,
        password: str,
        textract: Optional[Textract] = None,
        app_path: str = Config.DIRECTORIES.ENTERPRISE_PM,
    ):
        """This method is used to initialize the NextGenPMCore class.

        Args:
            username (str): username of the user.
            password (str): password of the user.
            textract (Optional[Textract], optional): Textract object. Defaults to None.
            app_path (str, optional): path of nextgen PM application. Defaults to Config.DIRECTORIES.ENTERPRISE_PM.

        """
        self.desktop_app = NGAppManager(app_path)
        self.username = username
        self.password = password
        self.app_path = app_path
        self.textract = textract
        self._batch_posting_window = None
        self._batch_maintenance_window = None
        self._cob_window = None
        self._encounter_insurance_window = None
        self._import_file_window = None
        self._payment_entry_window = None
        self._transaction_legder_window = None

    @property
    def batch_posting_window(self):
        """This property is used to access BatchPostingWindow class."""
        if self._batch_posting_window is None:
            self._batch_posting_window = BatchPostingWindow(self.app_path)
        return self._batch_posting_window

    @property
    def batch_maintenance_window(self):
        """This property is used to access BatchMaintenanceWindow class."""
        if self._batch_maintenance_window is None:
            self._batch_maintenance_window = BatchMaintenanceWindow(self.app_path)
        return self._batch_maintenance_window

    @property
    def cob_window(self):
        """This property is used to access COBWindow class."""
        if self._cob_window is None:
            self._cob_window = COBWindow(self.app_path)
        return self._cob_window

    @property
    def encounter_insurance_window(self):
        """This property is used to access EncounterInsuranteWindow class."""
        if self._encounter_insurance_window is None:
            self._encounter_insurance_window = EncounterInsuranceWindow(self.app_path)
        return self._encounter_insurance_window

    @property
    def import_file_window(self):
        """This property is used to access ImportFileWindow class."""
        if self._import_file_window is None:
            self._import_file_window = ImportFileWindow(self.app_path)
        return self._import_file_window

    @property
    def payment_entry_window(self):
        """This property is used to access PaymentEntryWindow class."""
        if self._payment_entry_window is None:
            self._payment_entry_window = PaymentEntryWindow(self.app_path, self.textract)
        return self._payment_entry_window

    @property
    def transaction_ledger_window(self):
        """This property is used to access TransactionLedgerWiundow class."""
        if self._transaction_legder_window is None:
            self._transaction_legder_window = TransactionLedgerWindow(self.app_path)
        return self._transaction_legder_window

    @retry_if_pywin_error(retries=2, delay=5)
    @capture_screenshot_if_pywin_error()
    def login(
        self,
        practice: Optional[str] = None,
        database: str = Config.DATABASES.TEST,
        app_folder: str = Config.DIRECTORIES.BASE_DIR,
    ) -> None:
        """Login to the app."""
        if process := self.desktop_app.get_app_session_if_running(self.app_path):
            self.close_session(process)  # Close a NextGen Session if it exists
        try:
            self.desktop_app.start_app(app_path=self.app_path, app_folder=app_folder)
            self.desktop_app.wait_until_element_visible(auto_id="txtUserName", control_type="Edit")
            self._check_database_name(db_name_flag=database)
            self.desktop_app.set_input_text(auto_id="txtUserName", text=self.username)
            self.desktop_app.set_input_text(auto_id="txtPassword", text=self.password)
            if practice:
                self.desktop_app.select_dropdown_item("cboPractice", practice)
            self.desktop_app.invoke_button(auto_id="btnLogon")
            self.desktop_app.app = self.desktop_app.connect_to_app(title="MainForm", timeout=20)
            logger.info("Logged into NextGen")
        except Exception as e:
            try:
                if app := self.desktop_app.connect_to_app(title="MainForm", timeout=20):
                    logger.info("Logged into NextGen")
                    self.desktop_app.app = app
                    return
            except Exception as inner_e:
                self.handle_multiple_sessions_popup()
                raise inner_e
            logger.error(f"Login failed: {e}")
            raise e

    @retry_if_pywin_error(retries=3, delay=5, exceptions=(ElementNotFoundError))  # type: ignore[misc]
    def _check_database_name(self, db_name_flag: str = Config.DATABASES.PROD) -> None:
        """Validates if the name received is part of the database selected.

        Args:
            db_name_flag (str): The database name to be validated.

        Returns:
            Raises WrongDatabaseSelected: if the database doesn't match.
        """
        database_name = self.desktop_app.dialog.child_window(auto_id="lblDatabase").window_text()
        logger.info(f"App is connected to '{database_name}' database")
        if db_name_flag.lower() not in database_name.lower():
            raise WrongDatabaseSelectedError(f"'{database_name}' selected, wrong database selected.")

    def handle_multiple_sessions_popup(self) -> None:
        """Close multiple sessions pop-up that comes immediately after login.

        Raises:
            MultipleSessionsError: if the modal exists
        """
        if self.desktop_app.dialog.child_window(title="Multiple station logon error", control_type="Window").exists(
            timeout=3, retry_interval=1
        ):
            logger.warning("Multiple sessions detected. Closing the popup.")
            if next_gen_process := self.desktop_app.get_app_session_if_running(self.app_path):
                self.close_session(next_gen_process)
            raise MultipleSessionsError("Process failed with multiple sessions issue")

    @capture_screenshot_if_pywin_error()
    def close_session(self, process: str) -> None:
        """Close the session using keyboard shortcuts.

        Args:
            process (str): The name of the process to kill if necessary.

        Returns:
            None
        """
        logger.info("Running close_session method.")
        self.desktop_app.connect_to_main_form()
        self.desktop_app.close_modal(modal_title="NextGen", button_to_click="NO")
        self.desktop_app.open_file_menu()
        logout_key = "l"
        keyboard.send_keys(logout_key)

        # This kind of .exe needs to kill the app after logout

        self.desktop_app.close_modal(button_to_click="YES")
        time.sleep(20)
        try:
            self.desktop_app.wait_to_disappear(auto_id="cmdToolApptlist", control_type="Button", max_attempts=12)
        except AssertionError:
            raise AppCrashException("Session not closed successfully")
        logger.info("Session closed, killing the process for EnterprisePM.exe")
        time.sleep(5)
        self.desktop_app.kill_app(process=process, app_path=self.app_path)
