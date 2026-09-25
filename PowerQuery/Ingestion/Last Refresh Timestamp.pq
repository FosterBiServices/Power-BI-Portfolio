// Last Refresh Timestamp
// A one-row table holding the time the model last refreshed, shown on report
// pages as "Data Last Refreshed: ...".
//
// The Power BI service refreshes in UTC, so DateTime.LocalNow() would show UTC
// time after publishing. This converts to US Eastern with Functions/fxUtcToEastern
// (which handles daylight saving time). Swap in another zone's function if needed.


// =====================================================================
// Query: Last Refresh   (requires fxUtcToEastern)
// =====================================================================
let
    Source = #table(
        type table [Last Refreshed = datetime],
        {
            { fxUtcToEastern(DateTimeZone.UtcNow()) }
        }
    )
in
    Source


// =====================================================================
// DAX measure for a card or text box
// =====================================================================
// Last Refresh Label =
//     "Data Last Refreshed: "
//         & FORMAT ( MAX ( 'Last Refresh'[Last Refreshed] ), "m/d/yyyy h:mm AM/PM" )
