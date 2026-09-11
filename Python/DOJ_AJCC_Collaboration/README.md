# DOJ AJCC Collaboration

## Overview

This project contains Python notebooks used to prepare, validate, and structure DOJ AJCC Collaboration data for Power BI reporting.

The primary purpose of these scripts is to transform source data into a format that is suitable for Power BI ingestion, reporting, analysis, and dashboard development.

These notebooks were developed to support specific reporting initiatives and may be executed on an as-needed basis when source data structures change or additional historical data preparation is required.

---

## Project Structure

```text
│   DOJ AJCC_Step1_Regions_HardCodedValues.ipynb
│   DOR AJCC_Step 2_GrantParticipants.ipynb
│   DOR AJCC_Step 3_ServicesProvided.ipynb
│   DOR AJCC_VALIDATIONS -- FILES READY FOR REFRESH.ipynb
│
├───.ipynb_checkpoints
│       DOJ AJCC_Step1_Regions_HardCodedValues-checkpoint.ipynb
│       DOR AJCC_Step 2_GrantParticipants-checkpoint.ipynb
│       DOR AJCC_Step 3_ServicesProvided-checkpoint.ipynb
│       DOR AJCC_VALIDATIONS -- FILES READY FOR REFRESH-checkpoint.ipynb
│
├───Executable Scripts
│   │   DOJ AJCC_Step1_Regions_HardCodedValues.py
│   │   DOR AJCC_Step 2_GrantParticipants.py
│   │   DOR AJCC_Step 3_ServicesProvided.py
│   │   DOR AJCC_VALIDATIONS -- FILES READY FOR REFRESH.py
│   │
│   └───.ipynb_checkpoints
│           DOJ AJCC_Step1_Regions_HardCodedValues-checkpoint.py
│
└───One Time Scripts
    │   DOR AJCC_ActivityCodes.ipynb
    │   DOR AJCC_EnrollmentTargets.ipynb
    │   DOR AJCC_NeedsAssessmentResponses.ipynb
    │   DOR AJCC_ProjectReadiness.ipynb
    │   DOR Staff Survey.ipynb
    │   DOR-AJCC Collab Data Validations.ipynb
    │
    └───.ipynb_checkpoints
            DOR AJCC_ActivityCodes-checkpoint.ipynb
            DOR AJCC_EnrollmentTargets-checkpoint.ipynb
            DOR AJCC_NeedsAssessmentResponses-checkpoint.ipynb
            DOR AJCC_ProjectReadiness-checkpoint.ipynb
            DOR Staff Survey-checkpoint.ipynb
            DOR-AJCC Collab Data Validations-checkpoint.ipynb