// Workday Calculations
// Inline patterns for counting weekdays in a column. For reusable versions see
// Functions/fxNetworkDays (count between two dates) and Functions/fxAddWorkdayFlag
// (1/0 flag on a date table), plus DateLogic/Holiday Table.pq for the holiday list.
// Paste into an existing query; <PREVIOUS_STEP> is the step before.


// =====================================================================
// 1) Weekdays between two date columns (inclusive), no function needed
// =====================================================================
    AddWeekdays = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Weekdays",
        each
            let
                StartDate = Date.From([<START_DATE_COLUMN>]),
                EndDate   = Date.From([<END_DATE_COLUMN>]),
                DayCount  = Duration.Days(EndDate - StartDate) + 1,
                AllDates  = if StartDate = null or EndDate = null or DayCount <= 0
                            then {}
                            else List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0))
            in
                // Day.Monday makes Mon = 0 ... Fri = 4, Sat = 5, Sun = 6
                List.Count(List.Select(AllDates, each Date.DayOfWeek(_, Day.Monday) < 5)),
        Int64.Type
    ),


// =====================================================================
// 2) Same, excluding holidays
// ---------------------------------------------------------------------
// Buffer the holiday list once in its own step so it isn't re-read for every row.
// =====================================================================
    HolidayList = List.Buffer(<HOLIDAY_TABLE>[<DATE_COLUMN>]),

    AddWorkdays = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Workdays",
        each fxNetworkDays(Date.From([<START_DATE_COLUMN>]), Date.From([<END_DATE_COLUMN>]), HolidayList),
        Int64.Type
    ),


// =====================================================================
// 3) Prorated working days in a period for rows that end mid-period
// ---------------------------------------------------------------------
// Example: a person/contract/asset that ends inside the reporting period only
// counts the weekdays from PeriodStart up to its end date; everyone else gets the
// full period value from [<DAYS_IN_PERIOD_COLUMN>].
// PeriodStart / PeriodEnd are parameters or earlier steps.
// =====================================================================
    AddProratedDays = Table.AddColumn(
        <PREVIOUS_STEP>,
        "Prorated Workdays",
        each
            let
                EndDate = if [<END_DATE_COLUMN>] = null then null else Date.From([<END_DATE_COLUMN>])
            in
                if EndDate <> null and EndDate > PeriodStart and EndDate <= PeriodEnd
                then fxNetworkDays(PeriodStart, EndDate)
                else [<DAYS_IN_PERIOD_COLUMN>],
        type number
    ),
