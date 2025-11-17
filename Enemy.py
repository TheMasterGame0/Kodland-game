class Enemy:
  def __init__(self, actor, vx, vy):
    self.actor = actor
    self.vy = vy
    self.vx = vx
    self.status = 0
  
  def set_pos(self, x, y):
    self.actor.pos = x, y

  def draw(self):
    self.actor.draw()

  def hit(self):
    self.vx = -self.vx
    self.vy = -self.vy
  
  def change_image(self, img1, img2):
    if self.status == 0:
      self.status = 1
      self.actor.image = img1
    else:
      self.status = 0
      self.actor.image = img2