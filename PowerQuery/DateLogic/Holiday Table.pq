// Holiday Table
// Builds a table of US holidays for a range of years, with the actual date and the
// observed date (moved off weekends). No source data needed.
//
// Use it to:
//   - flag working days on the date table (Functions/fxAddWorkdayFlag)
//   - count working days between dates  (Functions/fxNetworkDays)
//   - merge a holiday name onto the date table
//
// Edit HolidayRules to match the holidays your organization observes.
let
    // ----------------------------
    // Settings
    // ----------------------------
    YearsBack          = 2,           // years before the current year
    YearsForward       = 1,           // years after the current year
    SaturdayMovesTo    = "Friday",    // "Friday" (US federal rule) or "Monday"
    ExcludeFutureDates = false,       // true = only holidays up to today

    Today = Date.From(DateTime.LocalNow()),
    Years = List.Numbers(Date.Year(Today) - YearsBack, YearsBack + YearsForward + 1),

    // ----------------------------
    // Date helpers
    // ----------------------------
    // Nth weekday of a month, e.g. NthWeekday(2025, 11, Day.Thursday, 4) = Thanksgiving
    NthWeekday = (y as number, m as number, weekday as number, n as number) as date =>
        let
            FirstOfMonth = #date(y, m, 1),
            Offset       = Number.Mod(weekday - Date.DayOfWeek(FirstOfMonth, Day.Sunday) + 7, 7)
        in
            Date.AddDays(FirstOfMonth, Offset + 7 * (n - 1)),

    // Last weekday of a month, e.g. LastWeekday(2025, 5, Day.Monday) = Memorial Day
    LastWeekday = (y as number, m as number, weekday as number) as date =>
        let
            MonthEnd = Date.EndOfMonth(#date(y, m, 1)),
            Back     = Number.Mod(Date.DayOfWeek(MonthEnd, Day.Sunday) - weekday + 7, 7)
        in
            Date.AddDays(MonthEnd, -Back),

    // ----------------------------
    // Holiday rules: {Name, (year) => date}
    // Uncomment or add the ones you observe.
    // ----------------------------
    HolidayRules = {
        {"New Year's Day",                  (y) => #date(y, 1, 1)},
        // {"Martin Luther King Jr. Day",   (y) => NthWeekday(y, 1, Day.Monday, 3)},
        // {"Presidents' Day",              (y) => NthWeekday(y, 2, Day.Monday, 3)},
        {"Memorial Day",                    (y) => LastWeekday(y, 5, Day.Monday)},
        // {"Juneteenth",                   (y) => #date(y, 6, 19)},
        {"Independence Day",                (y) => #date(y, 7, 4)},
        {"Labor Day",                       (y) => NthWeekday(y, 9, Day.Monday, 1)},
        // {"Columbus Day",                 (y) => NthWeekday(y, 10, Day.Monday, 2)},
        // {"Veterans Day",                 (y) => #date(y, 11, 11)},
        {"Thanksgiving Day",                (y) => NthWeekday(y, 11, Day.Thursday, 4)},
        // {"Day After Thanksgiving",       (y) => Date.AddDays(NthWeekday(y, 11, Day.Thursday, 4), 1)},
        // {"Christmas Eve",                (y) => #date(y, 12, 24)},
        {"Christmas Day",                   (y) => #date(y, 12, 25)}
    },

    // One row per year x holiday
    Rows = List.TransformMany(
        Years,
        (y) => HolidayRules,
        (y, rule) => {y, rule{0}, rule{1}(y)}
    ),

    Holidays = #table(
        type table [Year = Int64.Type, Holiday = text, Holiday Date = date],
        Rows
    ),

    // Weekend holidays move to the nearest weekday
    AddObservedDate = Table.AddColumn(
        Holidays,
        "Observed Date",
        each
            let
                DayIndex = Date.DayOfWeek([Holiday Date], Day.Monday)    // Mon = 0 ... Sat = 5, Sun = 6
            in
                if DayIndex = 5 then Date.AddDays([Holiday Date], if SaturdayMovesTo = "Monday" then 2 else -1)
                else if DayIndex = 6 then Date.AddDays([Holiday Date], 1)
                else [Holiday Date],
        type date
    ),

    // 1 = holiday; handy after merging onto a date table (null elsewhere -> replace with 0)
    AddHolidayFlag = Table.AddColumn(AddObservedDate, "Is Holiday", each 1, Int64.Type),

    Result =
        if ExcludeFutureDates
        then Table.SelectRows(AddHolidayFlag, each [Observed Date] <= Today)
        else AddHolidayFlag
in
    Result
