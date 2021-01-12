from enum import IntEnum

class StrategyTypes(IntEnum):
  MEAN = 1
  EMA = 2
  CAPM = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class MethodTypes(IntEnum):
  COVAR_MAT = 1
  LEDOIT = 2
  ORACLE = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]