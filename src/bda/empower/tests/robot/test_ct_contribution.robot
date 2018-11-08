# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s bda.empower -t test_contribution.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src bda.empower.testing.BDA_EMPOWER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/bda/empower/tests/robot/test_contribution.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Contribution
  Given a logged-in site administrator
    and an add Contribution form
   When I type 'My Contribution' into the title field
    and I submit the form
   Then a Contribution with the title 'My Contribution' has been created

Scenario: As a site administrator I can view a Contribution
  Given a logged-in site administrator
    and a Contribution 'My Contribution'
   When I go to the Contribution view
   Then I can see the Contribution title 'My Contribution'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Contribution form
  Go To  ${PLONE_URL}/++add++Contribution

a Contribution 'My Contribution'
  Create content  type=Contribution  id=my-contribution  title=My Contribution

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Contribution view
  Go To  ${PLONE_URL}/my-contribution
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Contribution with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Contribution title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
