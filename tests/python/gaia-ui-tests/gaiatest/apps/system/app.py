# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class System(Base):

    # status bar
    _status_bar_locator = (By.ID, 'statusbar')
    _status_bar_notification_locator = (By.ID, 'statusbar-notification')
    _geoloc_statusbar_locator = (By.ID, 'statusbar-geolocation')
    _airplane_mode_statusbar_locator = (By.ID, 'statusbar-flight-mode')

    _notification_toaster_locator = (By.ID, 'notification-toaster')
    _update_manager_toaster_locator = (By.ID, 'update-manager-toaster')
    _banner_locator = (By.CSS_SELECTOR, '.banner.generic-dialog')

    def wait_for_status_bar_displayed(self):
        self.wait_for_element_displayed(*self._status_bar_locator)

    def wait_for_notification_toaster_displayed(self, timeout=10):
        # TODO Re-enable this when Bug 861874
        # self.wait_for_element_displayed(*self._notification_toaster_locator)
        self.wait_for_condition(lambda m: m.find_element(*self._notification_toaster_locator).location['y'] == 0, timeout=timeout)

    def wait_for_notification_toaster_not_displayed(self, timeout=10):
        # TODO Re-enable this when Bug 861874
        # self.wait_for_element_not_displayed(*self._notification_toaster_locator)
        self.wait_for_condition(lambda m: m.find_element(*self._notification_toaster_locator).location['y'] == -50, timeout=timeout)

    def open_utility_tray(self):
        # TODO Use actions for this
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")

        from gaiatest.apps.system.regions.utility_tray import UtilityTray
        return UtilityTray(self.marionette)

    # As we have trouble disabling the app update toaster these methods
    # may be used to wait for it when we know it may interfere
    @property
    def is_app_update_notification_displayed(self):
        update_manager_toaster = self.marionette.find_element(*self._update_manager_toaster_locator)
        return update_manager_toaster.location['y'] > (0 - update_manager_toaster.size['height'])

    def wait_for_app_update_to_clear(self):
        update_manager_toaster = self.marionette.find_element(*self._update_manager_toaster_locator)
        self.wait_for_condition(lambda m: update_manager_toaster.location['y'] == (0 - update_manager_toaster.size['height']))

    @property
    def geolocation_icon_displayed(self):
        return self.marionette.find_element(*self._geoloc_statusbar_locator).is_displayed()

    @property
    def is_airplane_mode_statusbar_displayed(self):
        return self.marionette.find_element(*self._airplane_mode_statusbar_locator).is_displayed()

    def wait_for_banner(self):
        """Waits for the banner to appear and then disappear"""
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._banner_locator)
        self.wait_for_element_not_displayed(*self._banner_locator)
        self.apps.switch_to_displayed_app()
