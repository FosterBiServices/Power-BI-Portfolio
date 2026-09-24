def BuildRelationshipStrategy(Inventory):
  Items = Inventory.Relationships
  if not Items: return "Evidence Gap: No relationship metadata was available in the supplied documentation."
  Inactive = sum(not Item.IsActive for Item in Items)
  DateTargets = {Item.ToTable for Item in Items if "date" in Item.ToTable.casefold() or "date" in Item.ToColumn.casefold()}
  ManyToMany = any("many : many" in Item.Cardinality.casefold() or "many:many" in Item.Cardinality.casefold() for Item in Items)
  Bidirectional = any("both" in Item.Direction.casefold() or "bi" in Item.Direction.casefold() for Item in Items)
  if DateTargets and Inactive: Text = "The model uses a centralized date table with inactive date relationships that measures can activate for different business dates."
  elif DateTargets: Text = "The model uses a centralized date table to support time-based reporting."
  else: Text = "The model connects reporting tables through defined semantic-model relationships."
  if ManyToMany: Text += " The model also contains many-to-many relationships."
  if Bidirectional: Text += " Bidirectional filtering is present."
  return Text
