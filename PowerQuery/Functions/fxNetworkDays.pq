// fxNetworkDays
// Counts working days (Mon-Fri) between two dates, optionally excluding holidays.
// Equivalent to Excel's NETWORKDAYS.
//
// Parameters:
//   StartDate   first date
//   EndDate     last date
//   Holidays    optional; list of dates to exclude (e.g. <HOLIDAY_TABLE>[<DATE_COLUMN>])
//   Inclusive   optional; true (default) counts EndDate too, false stops the day before EndDate
//
// Examples:
//   fxNetworkDays(#date(2025, 1, 1), #date(2025, 1, 31))
//   Table.AddColumn(<TABLE>, "Working Days",
//       each fxNetworkDays([<COLUMN_1>], [<COLUMN_2>], List.Buffer(<HOLIDAY_TABLE>[<DATE_COLUMN>])),
//       Int64.Type)
//
// Tip: when calling this from Table.AddColumn, buffer the holiday list once in its own
// step (HolidayList = List.Buffer(...)) and pass that step, so it isn't re-read per row.
(StartDate as date, EndDate as date, optional Holidays as nullable list, optional Inclusive as nullable logical) as number =>
let
    IncludeEnd = if Inclusive = null then true else Inclusive,
    DayCount   = Duration.Days(EndDate - StartDate) + (if IncludeEnd then 1 else 0),

    // Every date in the range (empty if EndDate is before StartDate)
    ListOfDates = if DayCount <= 0 then {} else List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),

    // Drop holidays when a list is supplied
    WithoutHolidays = if Holidays = null then ListOfDates else List.Difference(ListOfDates, Holidays),

    // Keep Monday-Friday (Day.Monday makes Monday = 0, so weekdays are 0-4)
    WeekdaysOnly = List.Select(WithoutHolidays, each Date.DayOfWeek(_, Day.Monday) < 5),

    CountDays = List.Count(WeekdaysOnly)
in
    CountDays
