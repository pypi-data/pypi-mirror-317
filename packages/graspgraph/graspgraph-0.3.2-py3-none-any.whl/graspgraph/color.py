class Color:
  def __init__(self, r = 0, g = 0, b = 0):
    self.R = r
    self.G = g
    self.B = b

  @property
  def R(self):
    return self.__R

  @R.setter
  def R(self, value):
    self.__R = min(max(value, 0), 255)

  @property
  def G(self):
    return self.__G

  @G.setter
  def G(self, value):
    self.__G = min(max(value, 0), 255)

  @property
  def B(self):
    return self.__B

  @B.setter
  def B(self, value):
    self.__B = min(max(value, 0), 255)

  def to_string(self, format = "#{R:02X}{G:02X}{B:02X}"):
    return format.format(R = self.__R, G = self.__G, B = self.__B)

  def __str__(self):
    return self.to_string()

  @classmethod
  def from_hex_code(cls, hexCode):
    return Color(*[int(hexCode[i: i + 2], 16) for i in range(1, 7, 2)])
