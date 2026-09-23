import json
from typing import Any
from .models import AboutReportModel, BusinessKpi

class AiResponseError(ValueError): pass

def _ExtractJson(Text: str) -> dict[str, Any]:
  if not isinstance(Text, str) or not Text.strip(): raise AiResponseError("AI response is blank.")
  Candidate=Text.strip()
  if Candidate.startswith("```"):
    Lines=Candidate.splitlines()
    if Lines and Lines[0].strip().casefold() in {"```","```json"}: Lines=Lines[1:]
    if Lines and Lines[-1].strip()=="```": Lines=Lines[:-1]
    Candidate="\n".join(Lines).strip()
  try: Data=json.loads(Candidate)
  except json.JSONDecodeError:
    Decoder=json.JSONDecoder(); Data=None; LastError=None
    for Start,Character in enumerate(Candidate):
      if Character!="{": continue
      try:
        Value,_=Decoder.raw_decode(Candidate[Start:])
        if isinstance(Value,dict): Data=Value; break
      except json.JSONDecodeError as Error: LastError=Error
    if Data is None: raise AiResponseError(f"AI response does not contain valid JSON: {LastError}")
  if not isinstance(Data,dict): raise AiResponseError("AI response root must be a JSON object.")
  return Data

def _Text(Value,Field,Required=False,MaxLength=5000):
  if Value is None: Value=""
  if not isinstance(Value,str): raise AiResponseError(f"{Field} must be text.")
  Value=" ".join(Value.split())
  if Required and not Value: raise AiResponseError(f"{Field} must be nonblank text.")
  if len(Value)>MaxLength: raise AiResponseError(f"{Field} cannot exceed {MaxLength:,} characters.")
  return Value

def _List(Value,Field,MaxItems=20):
  if Value is None: return ()
  if isinstance(Value,str): Value=[Value]
  if not isinstance(Value,list): raise AiResponseError(f"{Field} must be an array of strings.")
  Result=[]; Seen=set()
  for Index,Item in enumerate(Value):
    Text=_Text(Item,f"{Field}[{Index}]"); Key=Text.casefold()
    if Text and Key not in Seen: Result.append(Text); Seen.add(Key)
  if len(Result)>MaxItems: raise AiResponseError(f"{Field} cannot exceed {MaxItems} items.")
  return tuple(Result)

def _Kpis(Value,KnownMeasures,MaxKpis):
  if Value is None: Value=[]
  if not isinstance(Value,list): raise AiResponseError("top_kpis must be an array.")
  Known={Name.casefold():Name for Name in KnownMeasures}; Result=[]; Seen=set()
  for Index,Item in enumerate(Value):
    if isinstance(Item,str): Name=_Text(Item,f"top_kpis[{Index}]",True); Purpose=""
    elif isinstance(Item,dict):
      Name=_Text(Item.get("name"),f"top_kpis[{Index}].name",True)
      Purpose=_Text(Item.get("purpose",""),f"top_kpis[{Index}].purpose",MaxLength=1000)
    else: raise AiResponseError(f"top_kpis[{Index}] must be text or an object.")
    Canonical=Known.get(Name.casefold())
    if not Canonical: raise AiResponseError(f"AI returned unknown measure: {Name}")
    if Canonical.casefold() not in Seen: Result.append(BusinessKpi(Canonical,Purpose)); Seen.add(Canonical.casefold())
  if len(Result)>MaxKpis: raise AiResponseError(f"top_kpis cannot exceed {MaxKpis} items.")
  return tuple(Result)

def ParseAiResponse(Text,KnownSources,KnownMeasures,MaxKpis=5):
  Data=_ExtractJson(Text)
  Summary=_Text(Data.get("report_summary"),"report_summary",True)
  BusinessValue=_Text(Data.get("business_value",""),"business_value")
  Sources=_List(Data.get("data_sources",[]),"data_sources")
  SourceMap={Name.casefold():Name for Name in KnownSources}
  Unknown=[Name for Name in Sources if Name.casefold() not in SourceMap]
  if Unknown: raise AiResponseError("AI returned unknown sources: "+", ".join(Unknown))
  Objectives=_List(Data.get("business_objectives",[]),"business_objectives")
  Decisions=_List(Data.get("key_decisions_supported",[]),"key_decisions_supported")
  Outcomes=_List(Data.get("primary_outcomes",[]),"primary_outcomes")
  if not BusinessValue and not (Objectives or Decisions or Outcomes): raise AiResponseError("business_value is blank and no richer business details were supplied.")
  return AboutReportModel(
    ReportName=_Text(Data.get("report_name",""),"report_name",MaxLength=500),
    ReportSummary=Summary,BusinessValue=BusinessValue,
    Sources=tuple(SourceMap[Name.casefold()] for Name in Sources),
    Kpis=_Kpis(Data.get("top_kpis",[]),KnownMeasures,MaxKpis),
    EvidenceGaps=_List(Data.get("evidence_gaps",[]),"evidence_gaps"),
    Audience=_Text(Data.get("audience",""),"audience",MaxLength=500),
    BusinessObjectives=Objectives,KeyDecisionsSupported=Decisions,PrimaryOutcomes=Outcomes,
    SuccessIndicators=_List(Data.get("success_indicators",[]),"success_indicators"))
