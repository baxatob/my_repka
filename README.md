1. Test environment requirements

  - Python 2.7.9
  - Selenium Webdriver package
  
2. Install

  - download and install Python 2.7.9 from https://www.python.org/downloads/ using installer relevant to your OS 
  - download and install the latest Selenium Webdriver package using command line: pip install selenium
  - download and install requests* package using command line: pip install 

                            * this package is required to use Crossbrowsertesting.com REST API  

3. Architecture

  Framework consists of following modules:
  - base_test.py - contains AbstractTestCase class, where we can preset local test environment (browser and implicitly waiting value)
  - Config.py  - storage for all variables used in the test scenarios like urls, user credentials, file directories etc;
  - PageObjects.py  - storage for classes with the page element locators;
  - Methods.py  - storage for all common methods for the project;
  - runner.py - script to execute a couple of tests;
  - cleaner.py - script to remove test artifacts from the application; 
  - /Local  - directory with test-cases to run on local machine;
  - /Cloud - directory with test-cases to run in the cloud - http://www.crossbrowsertesting.com:
  - Crossbrowsertesting_config.py -  module for test environment configuration
  
 For the simple approach the test file contains 3 functions:
  - setUp()  to configure test environment 
  - testCase()  to configure test steps and validations 
  - tearDown()  to exit from the test
 

  One test file can contain several test cases as testCase1(), testCase2() etc. You can simply combine different tests in test suites using copy-paste.
  Do not forget to give a unique name for each test file and class, otherwise you will log improperly. 
 
4. Configuration

  - Setup all necessary variables in Config.py file. 
    The minimum requirements:
    - $logPath - the path to the directory where log files and screenshots will be stored
    - $preconditionPath - the path to the directory where all precondition files will be stored
    - $baseURL - link to the application under test
    Check all credentials as well.
  - Download all testing files from the Files/Test_files directory to your $preconditionPath directory. 

5. Test execution and logging

The best way is to use the Python IDE like PyDev for Eclipse (more info here: www.eclipse.org). 
Download and install IDE.
Download the latest version of automated testing framework from the git repository. 
Import the automated testing framework as Python project (File -> Import -> General -> "Existing Projects into Workspace" -> [select root directory of the framework and click "Finish"])
Select the test and run it as a unit-test (Right click on test module -> Run As -> Python unit-test)

After test execution you will receive one of two messages: 

OK (e.g. "Ran 4 tests in 908.489s - OK") or 
ERROR (e.g. "Ran 1 test in 0.002s - FAILED (errors=1)")

OK does not mean that the test PASSED, it only means that the test was properly executed and all code ran as expected.
ERROR means that the test was interrupted due to the some failure in the whole test (it can be code error or infrastructure failure).

To determine if the test is PASSED or FAILED you should check the test log. If it has no failure records it is PASSED.

All test logs (both for local and cloud tests) are stored in TEST_ID.log files. 
If you launch test locally, each catched failure should have a corresponding screenshot, stored in the file LOG_TIME.jpg.
If you launch test in the cloud you can check screenshots, video and/or additional information about the test results in the appropriate platform section.

The structure of log file:

Usually it's enough to read only the first string [A], which always contains the information about the line of the code, from where was thrown an exception. 
And string [B], which contains the exception message with detailed information about problematic element . All other strings can be omitted. But at the same time they can be useful in more confused cases.

Better first to run Smoke Test. If all smoke tests will pass, then you can run regression tests.
