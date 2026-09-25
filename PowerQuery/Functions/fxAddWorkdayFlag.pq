// fxAddWorkdayFlag
// Adds a 1/0 "is working day" column to a date table: 0 for Saturdays, Sundays and
// holidays, 1 otherwise. Sum the flag in DAX to count working days in any period.
//
// Parameters:
//   DateTable      the date table
//   DateColumn     name of its date column, e.g. "<DATE_COLUMN>"
//   Holidays       optional; list of holiday dates. Pass the date column from a holiday
//                  table (see DateLogic/Holiday Table.pq), or leave null for weekends only.
//   FlagColumn     optional; name of the new column (default "Is Workday")
//
// Examples:
//   fxAddWorkdayFlag(<DATE_TABLE>, "<DATE_COLUMN>", <HOLIDAY_TABLE>[<DATE_COLUMN>])
//
//   // Holiday flag already on the date table (1 = holiday):
//   fxAddWorkdayFlag(<DATE_TABLE>, "<DATE_COLUMN>",
//       Table.SelectRows(<DATE_TABLE>, each [<HOLIDAY_FLAG_COLUMN>] = 1)[<DATE_COLUMN>])
(DateTable as table, DateColumn as text, optional Holidays as nullable list, optional FlagColumn as nullable text) as table =>
let
    HolidayList = List.Buffer(if Holidays = null then {} else List.Transform(Holidays, Date.From)),
    NewColumn   = if FlagColumn = null then "Is Workday" else FlagColumn,

    AddFlag = Table.AddColumn(
        DateTable,
        NewColumn,
        (row) =>
            let
                CurrentDate = Date.From(Record.Field(row, DateColumn)),
                IsWeekend   = Date.DayOfWeek(CurrentDate, Day.Monday) >= 5,
                IsHoliday   = List.Contains(HolidayList, CurrentDate)
            in
                if IsWeekend or IsHoliday then 0 else 1,
        Int64.Type
    )
in
    AddFlag
