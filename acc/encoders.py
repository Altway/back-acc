
import json

import numpy as np

from django.core.serializers.json import DjangoJSONEncoder
from strategy.models import RecordHypothesis

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RecordHypothesis):
            return str(obj)
        return super().default(obj)