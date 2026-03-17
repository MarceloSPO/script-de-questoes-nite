from enums.platform_types import PlatformType

def get_delimiter(platform_type:PlatformType):
  if platform_type == PlatformType.AVA:
    return ","
  elif platform_type == PlatformType.PLATAFORMA_A:
    return ";"    