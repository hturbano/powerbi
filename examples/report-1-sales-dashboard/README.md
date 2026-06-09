# Example Report 1: Student Performance Dashboard

**Domain**: Education / ADA Compliance
**Layout**: dashboard-2col
**Theme**: corporate

## Overview

A executive-facing dashboard showing key student performance and ADA (Average Daily Attendance) metrics for a school district.

## Pages

### Page 1: Executive Summary
- **KPI Cards** (top row, full width):
  - Total Enrollment (card)
  - ADA Rate % (card, conditional formatting: green >= 96%, amber 94-96%, red < 94%)
  - Attendance Rate % (card)
  - Year-over-Year Enrollment Change (card, trend indicator)

- **Charts** (two-column layout):
  - Left: Monthly Attendance Trend (line chart, current year vs prior year)
  - Right: Campus Breakdown (bar chart, ADA rate by campus)

### Page 2: Campus Detail [Drill-Through]
- Campus selector slicer
- Student demographic breakdown (matrix/heat map)
- Trend by grade level (line chart)
- Detail table with student-level data (table visual, alternating rows)

## Data Sources
- Student Information System (SIS) export
- Campus master reference table
- Date dimension table

## Key DAX Measures
- `Total Enrollment = COUNT(StudentID)`
- `ADA Rate = DIVIDE(Sum(DaysPresent), Sum(SchoolDays), 0)`
- `YoY Enrollment Change = [Current Year Enrollment] - [Prior Year Enrollment]`
- `Attendance Rate = DIVIDE(Sum(DaysPresent), Sum(EnrolledDays), 0)`

## Design Notes
- Uses corporate theme (brand colors from district)
- ADA threshold indicators (green >= 96%, amber 94-96%, red < 94%)
- Campus drill-through from summary to detail
- Date slicer for school year filtering

## Files
To be populated after design system extraction from .pbip:
- `definition/report.json` — report layout and visuals
- `design-system/themes/corporate.json` — theme extracted to this location
