# Built-in workflows register themselves via workflow_registry at import time
# Import the modules to trigger registration
from workflows.builtin import investigation
from workflows.builtin import case_analysis
from workflows.builtin import suspect_profile
from workflows.builtin import crime_briefing
