import json

class AiResponseError(ValueError): pass

def ParseAiResponse(Text,KnownSources,KnownMeasures,MaxKpis=5):
  try: Data=json.loads(Text)
  except json.JSONDecodeError as Error: raise AiResponseError(f"AI response is not valid JSON: {Error}") from Error
  Required=("report_summary","business_value","data_sources","top_kpis","evidence_gaps")
  Missing=[Key for Key in Required if Key not in Data]
  if Missing: raise AiResponseError("AI response is missing: "+", ".join(Missing))
  if not isinstance(Data["report_summary"],str) or not Data["report_summary"].strip(): raise AiResponseError("report_summary must be nonblank text.")
  if not isinstance(Data["business_value"],str) or not Data["business_value"].strip(): raise AiResponseError("business_value must be nonblank text.")
  for Key in ("data_sources","top_kpis","evidence_gaps"):
    if not isinstance(Data[Key],list) or not all(isinstance(Item,str) for Item in Data[Key]): raise AiResponseError(f"{Key} must be an array of strings.")
  UnknownSources=[Item for Item in Data["data_sources"] if Item.casefold() not in {Value.casefold() for Value in KnownSources}]
  UnknownKpis=[Item for Item in Data["top_kpis"] if Item.casefold() not in {Value.casefold() for Value in KnownMeasures}]
  if UnknownSources: raise AiResponseError("AI returned unknown sources: "+", ".join(UnknownSources))
  if UnknownKpis: raise AiResponseError("AI returned unknown measures: "+", ".join(UnknownKpis))
  if len(Data["top_kpis"])>MaxKpis: raise AiResponseError(f"top_kpis cannot exceed {MaxKpis} items.")
  return Data
