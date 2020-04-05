class SuburbStatisticCaller:

	def __init__(self, state, suburb_id, property_category, chronological_span, t_plus_from, t_plus_to, bedrooms=None):
		self.state = state
		self.suburb_id = suburb_id
		self.property_category = property_category
		self.chronological_span = chronological_span
		self.t_plus_from = t_plus_from
		self.t_plus_to = t_plus_to
		if bedrooms is None:
			self.bedrooms = None
		else:
			self.bedrooms = bedrooms