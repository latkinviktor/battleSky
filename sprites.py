class Sprites:#collection of sprites
  __jetRight = [
    -CELL//4  , -CELL//20 ,
    -CELL//5  , -CELL//20 ,
    -CELL//3  , -CELL//20 ,
    -CELL//3  , -CELL//10 ,
    -CELL//5  , -CELL//10 ,
    -CELL//4  , -CELL//10 ,
    -CELL//4  , -CELL//4  ,
          0   , -CELL//10 ,
    CELL//4   , -CELL//20 ,
    CELL//2   ,        0  ,
    CELL//4   , CELL//20  ,
    0         , CELL//10  ,
    -CELL//4  ,  CELL//4  ,
    -CELL//4  , CELL//10  ,
    -CELL//5  , CELL//10  ,
    -CELL//3  , CELL//10  ,
    -CELL//3  , CELL//20  ,
    -CELL//5  , CELL//20  ,
    -CELL//4  , CELL//20  ,
    ]
  __jetLeft  = [-1*elem for elem in __jetRight]
  __jetDown = list()
  for i in range(0,len(__jetRight),2):
    __jetDown.append(__jetRight[i+1])
    __jetDown.append(__jetRight[i])

  __jetUp = [-1*elem for elem in __jetDown]

  __jets = {
    "right": __jetRight,
    "left" : __jetLeft,
    "up"   : __jetUp,
    "down" : __jetDown
    }
  def jet(self, direction):
    return self.__jets[direction]



  __markerRight = [
                  -CELL//3, -CELL//10,
                  -CELL//3, CELL//10,
                  -CELL//2, CELL//20,
                  -CELL//3,       0,
                  -CELL//2, -CELL//20,
                ]
  __markerLeft = [-elem for elem in __markerRight]
  __markerDown = list()
  for i in range(0, len(__markerRight), 2):
    __markerDown.append(__markerRight[i+1])
    __markerDown.append(__markerRight[i])
  __markerUp = [-elem for elem in __markerDown]
  __markers = {
          "right" : __markerRight,
          "left"  : __markerLeft,
          "up"    : __markerUp,
          "down"  : __markerDown
    }
  def marker(self, direction):
    return self.__markers[direction]
