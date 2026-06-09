# Example Report 1: Student Performance Dashboard

**Domain**: Education / ADA Compliance | **Author**: hturbano

## Overview

An executive-facing dashboard showing key student performance and ADA (Average Daily Attendance) metrics for a school district.

## Pages

### Page 1: Executive Summary
- **KPI Cards** (top row):
  - Total Enrollment
  - ADA Rate (conditional: green >= 96%, amber 94-96%, red < 94%)
  - Attendance Rate
  - YoY Enrollment Change

- **Charts** (two-column):
  - Monthly Attendance Trend (line chart, current vs prior year)
  - Campus Breakdown (bar chart, ADA rate by campus)

### Page 2: Campus Detail [Drill-Through]
- Campus selector slicer
- Demographic breakdown (matrix)
- Trend by grade level (line chart)
- Student-level detail table

## Data Sources
- Student Information System (SIS)
- Campus master reference
- Date dimension table

## Key DAX Patterns
- Total Enrollment, ADA Rate, Attendance Rate, YoY Change
- All from `design-system/dax-patterns/time-intelligence.json`

## Design Notes
- Corporate theme (district brand colors)
- ADA threshold indicators
- Campus drill-through
- School year date slicer
