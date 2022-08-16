from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urljoin


class SansaLiverServerTestCase(LiveServerTestCase):
    """
    Generic SANSA LiveServerTestCase
    """

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        # maximum time to wait for page load
        cls.browser.implicitly_wait(2)
        super(SansaLiverServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SansaLiverServerTestCase, cls).tearDownClass()


class Menu():
    """
    Menu PageObject

    * menu interactions
    * checks menu items availability
    """

    ANONYMOUS_MENU = [
        ' Home', ' Login', ' Register', ' Reset Password', ' About',
        ' Contact']

    STAFF_MENU = [
        ' Home', ' Search', ' My Cart', ' Order Now!', ' Popular Links',
        ' Staff', ' Account', ' About', ' Contact']

    REGULAR_MENU = [
        ' Home', ' Search', ' My Cart', ' Order Now!', ' Popular Links',
        ' Account', ' About', ' Contact']

    def __init__(self, theWebDriver):
        self.browser = theWebDriver
        # check if menu is available (also inits menu)
        self.is_available()

    def _get_menu(self):
        try:
            self.menu.is_enabled()
            return self.menu
        except:
            self.menu = self.browser.find_element_by_id("menu")
            return self.menu

    def is_available(self):
        try:
            self._get_menu()
            return True
        except NoSuchElementException:
            return False

    def get_menu_items(self):
        # store all links by using css selector
        myMenu = self._get_menu()
        self.menu_items = myMenu.find_elements_by_css_selector('a, span')

    def for_anonymous_user(self):
        return self.check_menu_items('ANONYMOUS')

    def for_staff_user(self):
        return self.check_menu_items('STAFF')

    def for_regular_user(self):
        return self.check_menu_items('REGULAR')

    def check_menu_items(self, theMenuType):
        self.get_menu_items()
        # get menu titles (text)
        self.menu_item_titles = [
            ele.text for ele in self.menu_items if ele.is_displayed()]

        if theMenuType == 'ANONYMOUS':
            if self.menu_item_titles == self.ANONYMOUS_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.ANONYMOUS_MENU, self.menu_item_titles))

        elif theMenuType == 'STAFF':
            if self.menu_item_titles == self.STAFF_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.STAFF_MENU, self.menu_item_titles))

        elif theMenuType == 'REGULAR':
            if self.menu_item_titles == self.REGULAR_MENU:
                return True
            else:
                raise Exception('Expected %s, got %s' % (
                    self.REGULAR_MENU, self.menu_item_titles))
        else:
            raise Exception('Unknown menu type')

    def click_home(self):
        myMenu = self._get_menu()
        myMenu.find_element_by_partial_link_text('Home').click()

    def click_login(self):
        myMenu = self._get_menu()
        myMenu.find_element_by_partial_link_text('Login').click()

    def click_logout(self):
        myMenu = self._get_menu()
        myMenu.find_element_by_partial_link_text('Logout').click()

    def click_search(self):
        myMenu = self._get_menu()
        myMenu.find_element_by_partial_link_text('Search').click()


class Login():
    """
    Login PageObject, abstracting login
    """
    def __init__(self, theWebDriver, theUser, thePassword):
        self.browser = theWebDriver
        # find login menu option
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys(theUser)
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys(thePassword)

        # find login button and click it
        self.browser.find_element_by_xpath('//input[@value="Login"]').click()


class Search():
    """
    Search PageObject, abstracts search
    """

    def __init__(self, theWebDriver):
        self.browser = theWebDriver
        # check if search is available
        self.is_available()

    def _get_search_panel(self):
        try:
            self.search_panel.is_enabled()
            return self.search_panel
        except:
            self.search_panel = self.browser.find_element_by_id("search-panel")
            return self.search_panel

    def _get_sensor_list(self):
        try:
            self.sensor_list.is_enabled()
            return self.sensor_list
        except:
            self.sensor_list = Select(
                self.browser.find_element_by_id('id_sensors'))
            return self.sensor_list

    def is_available(self):
        try:
            self._get_search_panel()
            return True
        except NoSuchElementException:
            return False

    def listed_sensors(self):
        mySensorSelect = self._get_sensor_list()
        return [opt.name for opt in mySensorSelect.options]

    def selected_sensors(self):
        mySensorSelect = self._get_sensor_list()
        return [opt.name for opt in mySensorSelect.all_selected_options]

    def select_sensor(self, theSensor):
        mySensorSelect = self._get_sensor_list()
        mySensorSelect.select_by_visible_text(theSensor)

    def click_search(self):
        mySearch = self._get_search_panel()
        mySearch.find_element_by_xpath('.//input[@name="_search"]').click()


class DatePickerWidget():
    """
    DatePicker PageObject, abstracts DatePicker Widget
    """

    def __init__(self, theWebDriver, theWidgetID):
        self.browser = theWebDriver
        self.widgetID = theWidgetID
        # check if datepickerwidget is available
        self.is_available()

    def _get_datepicker(self):
        try:
            self.datepicker.is_enabled()
            return self.datepicker
        except:
            self.datepicker = self.browser.find_element_by_id(self.widgetID)
            return self.datepicker

    def is_available(self):
        try:
            self._get_datepicker()
            return True
        except NoSuchElementException:
            return False

    def select_month(self, theMonth):
        myDatepicker = self._get_datepicker()
        myMonthSelect = Select(myDatepicker.find_element_by_css_selector(
            '.ui-datepicker-month'))
        myMonthSelect.select_by_visible_text(theMonth)

    def select_year(self, theYear):
        myDatepicker = self._get_datepicker()
        myYearSelect = Select(myDatepicker.find_element_by_css_selector(
            '.ui-datepicker-year'))
        myYearSelect.select_by_visible_text(theYear)

    def select_day(self, theDay):
        myDatepicker = self._get_datepicker()
        myDaySelect = myDatepicker.find_element_by_css_selector(
            '.ui-datepicker-calendar')
        myDaySelect.find_element_by_link_text(theDay).click()

    def set_date(self, theDate):
        # split carefully formatted date
        myDay, myMonth, myYear = theDate.split('/')

        self.select_year(myYear)
        self.select_month(myMonth)
        self.select_day(myDay)


class DateRangeWidget():
    """
    DateRange PageObject, abstracts DateRange Widget
    """

    def __init__(self, theWebDriver):
        self.browser = theWebDriver
        # check if daterangewidget is available
        self.is_available()

    def _get_daterange(self):
        try:
            self.daterange_add.is_enabled()
            self.daterange_del.is_enabled()
            return (self.daterange_add, self.daterange_del)
        except:
            self.daterange_add = self.browser.find_element_by_id('dr_add')
            self.daterange_del = self.browser.find_element_by_id('dr_del')
            return (self.daterange_add, self.daterange_del)

    def is_available(self):
        try:
            self._get_daterange()
            return True
        except NoSuchElementException:
            return False

    def add_daterange(self):
        myDRAdd, myDRDel = self._get_daterange()
        myDRAdd.click()

    def del_daterange(self):
        """
        Deleting DateRanges is not simple, TODO
        """
        pass


class MapContainerWidget():
    """
    MapContainer PageObject, abstracts MapContainer Widget
    """

    def __init__(self, theWebDriver):
        self.browser = theWebDriver
        # check if daterangewidget is available
        self.is_available()

    def _get_mapcontainer(self):
        try:
            self.mapcontainer.is_enabled()
            return self.mapcontainer
        except:
            self.mapcontainer = self.browser.find_element_by_id(
                'map-container')
            return self.mapcontainer

    def is_available(self):
        try:
            self._get_mapcontainer()
            return True
        except NoSuchElementException:
            return False

    def _get_mapnavigation(self):
        try:
            self.mapnavigation.is_enabled()
            return self.mapnavigation
        except:
            self.mapnavigation = self.browser.find_element_by_id(
                'map-navigation-panel')
            return self.mapnavigation

    def _get_map(self):
        try:
            self.map.is_enabled()
            return self.map
        except:
            self.map = self.browser.find_element_by_id(
                'map')
            return self.map

    def activate_capture_polygon(self):
        myMapNav = self._get_mapnavigation()
        myMapNav.find_element_by_css_selector(
            '.olControlDrawFeaturePolygonItemInactive').click()

    def activate_pan_map(self):
        myMapNav = self._get_mapnavigation()
        myMapNav.find_element_by_css_selector(
            '.olControlNavigationItemInactive').click()

    def draw_polygon(self, thePolygonData):
        """
        Preform complex actionchain to draw a polygon

        Polygon is actually hardcoded, as this is only shows how to use
        action chains.

        In theory, we could use real geographic data for polygon, but then we
        must get current map extent and translate geo to image coordinates
        """
        self.activate_capture_polygon()
        myAc = ActionChains(self.browser)
        myMap = self._get_map()

        # simply move to the center of a map, click
        # move by 200px to the left and click
        # move by 200px to the bottom and double click to finish capturing a
        # polygon
        (myAc.move_to_element(myMap)
            .click()
            .move_by_offset(-200, 0)
            .click()
            .move_by_offset(0, 200)
            .double_click()
            .perform())


class SeleniumLogin(SansaLiverServerTestCase):
    fixtures = ['test_user.json']

    def Xtest_login_staff(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())
        # check if menu is for anonymous user
        self.assertTrue(myMenu.for_anonymous_user())

        # click login menu item
        myMenu.click_login()

        # login staff user
        Login(self.browser, 'timlinux', 'password')

        self.assertTrue(myMenu.for_staff_user())

    def Xtest_login_user(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())

        # click login menu item
        myMenu.click_login()

        # login staff user
        Login(self.browser, 'pompies', 'password')

        self.assertTrue(myMenu.for_regular_user())


class SeleniumSearch(SansaLiverServerTestCase):
    fixtures = [
        'test_user.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
    ]

    def Xtest_search_staff(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())

        # click login menu item
        myMenu.click_login()

        # login staff user
        Login(self.browser, 'timlinux', 'password')

        myMenu.click_search()

        mySearch = Search(self.browser)

        self.assertTrue(mySearch.is_available())

        mySearch.select_sensor('SPOT 3 HRV')

        myDatePickerStart = DatePickerWidget(
            self.browser, 'id_start_datepicker_widget')
        myDatePickerStart.set_date('10/Apr/1980')

        myDatePickerEnd = DatePickerWidget(
            self.browser, 'id_end_datepicker_widget')
        myDatePickerEnd.set_date('30/Sep/1995')

        myDateRangeWidget = DateRangeWidget(self.browser)
        myDateRangeWidget.add_daterange()

        mySearch.click_search()

        # check if we got redirected to searchresult page
        myUrlParts = self.browser.current_url.split('/')
        self.assertTrue(myUrlParts[3], 'searchresult')

        # check number of returned results
        mySearchResults = self.browser.find_element_by_id('search-messages')
        self.assertEqual(
            mySearchResults.find_element_by_tag_name('b').text, '2')

    def Xtest_search_polygon(self):
        # we use 'urljoin' to prepare URL
        self.browser.get(urljoin(self.live_server_url, reverse('index')))

        # for this test we need menu PageObject
        myMenu = Menu(self.browser)

        # check if we have menu
        self.assertTrue(myMenu.is_available())

        # click login menu item
        myMenu.click_login()

        # login staff user
        Login(self.browser, 'timlinux', 'password')

        myMenu.click_search()

        mySearch = Search(self.browser)

        self.assertTrue(mySearch.is_available())

        mySearch.select_sensor('Landsat 5 TM')

        myDatePickerStart = DatePickerWidget(
            self.browser, 'id_start_datepicker_widget')
        myDatePickerStart.set_date('1/Jan/1972')

        myDatePickerEnd = DatePickerWidget(
            self.browser, 'id_end_datepicker_widget')
        myDatePickerEnd.set_date('31/Dec/2012')

        myDateRangeWidget = DateRangeWidget(self.browser)
        myDateRangeWidget.add_daterange()

        myMap = MapContainerWidget(self.browser)
        myMap.draw_polygon([])

        mySearch.click_search()

        # check if we got redirected to searchresult page
        myUrlParts = self.browser.current_url.split('/')
        self.assertTrue(myUrlParts[3], 'searchresult')

        # check number of returned results
        mySearchResults = self.browser.find_element_by_id('search-messages')
        self.assertEqual(
            mySearchResults.find_element_by_tag_name('b').text, '1')
