"""Module for BatchMaintenance class."""
import contextlib
import re

from t_nextgen.nextgen_window import NextGenWindow

import _ctypes
from decimal import Decimal
from t_desktop.config import IS_WINDOWS_OS

if IS_WINDOWS_OS:
    from pywinauto.controls.uia_controls import ComboBoxWrapper
    from pywinauto.findwindows import ElementNotFoundError
from t_nextgen.utils.logger import logger


class BatchMaintenanceWindow(NextGenWindow):
    """Batch Maintenance class with methods to interact with batch maintenance window."""

    @property
    def window(self):
        """Return the AMBatches window element."""
        return self.desktop_app.dialog.child_window(title="AMBatches", control_type="Window")

    def click_cancel(self) -> None:
        """Clicks the cancel button on the maintenance window and confirms by clicking 'No'."""
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="cmdCancel", control_type="Button").click()
        self.click_no_on_popup_if_exist()

    def click_no_on_popup_if_exist(self) -> None:
        """Clicks the 'No' button on the maintenance window pop-up if it appears."""
        try:
            self.desktop_app.wait_until_element_visible(title="NextGen", control_type="Window")
            next_gen_popup = self.desktop_app.dialog.child_window(title="NextGen", control_type="Window")
            no_button = next_gen_popup.child_window(auto_id="7", control_type="Button")
            with contextlib.suppress(_ctypes.COMError):
                no_button.click()
            no_button.wait_not("visible", timeout=10)
        except (ElementNotFoundError, TimeoutError):
            logger.debug("Save confirmation pop-up not found; proceeding without further action.")

    def click_ok(self) -> None:
        """Clicks the OK button and waits for it to disappear."""
        ok_button = self.window.child_window(auto_id="cmdOK", control_type="Button")
        with contextlib.suppress(_ctypes.COMError):
            ok_button.click()
        ok_button.wait_not("visible", timeout=10)

    def get_desc_amount(self) -> str:
        """Fetch Batch Desc Amount from Batch Maintenance Window.

        Returns:
            str: desc amount
        """
        amt = self.window.child_window(auto_id="txtDesc", control_type="Edit").get_value()
        return re.search(r"(-?\$-?[0-9]+\.?[0-9]*)", amt).group().replace("$", "")

    def update_total_billed_header(self, ledger_billed: str) -> None:
        """Update Billed Amount Header in the Batch Header Window.

        Args:
            ledger_billed (str): The amount billed to be updated in the batch header.
        """
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="txtTotBilled").set_text(str(ledger_billed))

    def update_total_allowed_header(self, ledger_allowed: str) -> None:
        """Update Allowed Amount Header in the Batch Header Window.

        Args:
            ledger_allowed (str): The allowed amount to be updated in the batch header.
        """
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="txtTotApproved").set_text(str(ledger_allowed))

    def update_total_paid_header(self, ledger_payment: str) -> None:
        """Update Paid Amount Header in the Batch Header Window.

        Args:
            ledger_payment (str): The paid amount to be updated in the batch header.
        """
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="txtTotPaid").set_text(str(ledger_payment))

    def set_user_in_secured_to(self, username: str) -> None:
        """Update comboboxe for user in the Batch Maintenace window."""
        cbo_secured = self.window.child_window(auto_id="cboSecured", control_type="Pane")
        combobox_user = cbo_secured.child_window(auto_id="mcbo", control_type="ComboBox", found_index=0)
        self.desktop_app.select_value_from_combobox(combobox_user, username)

    def set_doc_mgmt(self, payment_trn: str, payment_amt: Decimal) -> None:
        """Update comboboxe for image batch in the Batch Maintenace window."""
        cbo_image_batch = self.window.child_window(auto_id="cboImageBatch", control_type="Pane")
        combobox_image_batch = cbo_image_batch.child_window(auto_id="mcbo", control_type="ComboBox", found_index=0)
        normalized_payment_amt = str(payment_amt).replace(".", "_")
        self.select_combobox_doc_mgmt(combobox_image_batch, f"{payment_trn}_{normalized_payment_amt}.pdf")

    def select_combobox_doc_mgmt(
        self, combobox: ComboBoxWrapper, value: str, use_type_keys: bool = False, click_combobox: bool = True
    ) -> None:
        """Selects a value from a ComboBox by simulating a click and searching for the matching option.

        Args:
            combobox (ComboBoxWrapper): The ComboBox control in which to search for the value.
            value (str): The value to search for and select within the ComboBox.
            use_type_keys (bool, optional): If True, uses type_keys instead of set_text. Defaults to False.
            click_combobox (bool, optional): If True, clicks the combobox before selecting the value. Defaults to True.
        """
        current_value = combobox.legacy_properties().get("Value", "")
        if current_value:
            return
        if click_combobox:
            self.desktop_app.click_on_combobox(combobox)
        option_to_select = self.desktop_app.get_option_to_select_from_combobox(combobox, value)
        if option_to_select:
            self.desktop_app.select_option_in_combobox(combobox, use_type_keys, option_to_select)
        else:
            raise ValueError(f"Value '{value}' not found in ComboBox.")

    def update_default_tracking(self, trn: str) -> None:
        """Updates the txtDefTracking field in the AMBatches window with the trn.

        Args:
            trn (str): TRN
        """
        self.desktop_app.wait_until_element_visible(control_type="Window", auto_id="AMBatches")
        self.window.child_window(title="txtDefTracking", control_type="Edit").set_text(f"ERA Check {trn}")
