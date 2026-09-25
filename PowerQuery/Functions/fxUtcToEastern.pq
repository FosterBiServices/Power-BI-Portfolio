// fxUtcToEastern
// Converts a UTC timestamp to US Eastern time, applying US DST rules (2007+):
//   DST starts: 2nd Sunday in March    @ 02:00 local (07:00 UTC)
//   DST ends:   1st Sunday in November @ 02:00 local (06:00 UTC)
//
// Parameters:
//   DateTimeValue  datetime, datetimezone, or text. Values without a zone are treated as UTC.
//   KeepZone       optional; true returns datetimezone (-04:00/-05:00), false/null returns datetime.
//
// Examples:
//   fxUtcToEastern(DateTimeZone.UtcNow(), true)          // "now" in Eastern, e.g. for a Last Refreshed table
//   Table.TransformColumns(<TABLE>, {{"<COLUMN>", each fxUtcToEastern(_), type datetime}})
//   For several columns at once, see fxConvertColumnsUtcToEastern.
//
// For other US zones change the two offsets (Central -5/-6, Mountain -6/-7, Pacific -7/-8)
// and the UTC switch-over hours (local 02:00 + standard offset).
(DateTimeValue as any, optional KeepZone as nullable logical) as any =>
let
    // Normalize the input to a UTC datetimezone value
    UtcZoned =
        if DateTimeValue = null then
            null
        else if Value.Is(DateTimeValue, type datetimezone) then
            DateTimeZone.ToUtc(DateTimeValue)
        else
            // Treat naive values as UTC by attaching +00:00 (no clock change)
            DateTime.AddZone(DateTime.From(DateTimeValue), 0),

    Result =
        if UtcZoned = null then
            null
        else
            let
                y = Date.Year(DateTimeZone.RemoveZone(UtcZoned)),

                // First Sunday on or after a given date
                FirstSundayOnOrAfter = (d as date) as date =>
                    Date.StartOfWeek(Date.AddDays(d, 6), Day.Sunday),

                // DST start: 2nd Sunday in March = first Sunday on or after March 8
                DstStartDay = FirstSundayOnOrAfter(#date(y, 3, 8)),
                DstStartUtc = DateTime.AddZone(DateTime.From(DstStartDay) + #duration(0, 7, 0, 0), 0),

                // DST end: 1st Sunday in November
                DstEndDay = FirstSundayOnOrAfter(#date(y, 11, 1)),
                DstEndUtc = DateTime.AddZone(DateTime.From(DstEndDay) + #duration(0, 6, 0, 0), 0),

                IsDst       = UtcZoned >= DstStartUtc and UtcZoned < DstEndUtc,
                OffsetHours = if IsDst then -4 else -5,

                // Shift the zone while preserving the instant
                EasternZoned = DateTimeZone.SwitchZone(UtcZoned, OffsetHours, 0),

                Keep   = if KeepZone = null then false else KeepZone,
                Output = if Keep then EasternZoned else DateTimeZone.RemoveZone(EasternZoned)
            in
                Output
in
    Result
