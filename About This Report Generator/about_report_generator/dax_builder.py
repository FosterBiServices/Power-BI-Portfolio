def BuildDaxMeasure(Html, Config):
  EscapedHtml = Html.replace('"', '""')
  EscapedName = Config.MeasureName.replace("'", "''")
  return "createOrReplace\n\n" + f"  ref table {Config.MeasureTable}\n\n" + f"    measure '{EscapedName}' =\n" + f'      "{EscapedHtml}"\n'
