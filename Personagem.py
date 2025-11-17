# from pgzero import clock

class Personagem:
  def __init__(self, actor, stay, hurt, right, right2, left, left2):
    self.actor = actor
    self.vy = -2
    self.vx = 0
    self.status = 0

    self.stay = stay
    self.hurt = hurt
    self.right = right
    self.right1 = right2
    self.left = left
    self.left1 = left2
  
  def set_pos(self, x, y):
    self.actor.pos = x, y

  def draw(self):
    self.actor.draw()

  def hit(self, pos):
    if self.actor.collidepoint(pos):
      self.set_actor_hurt()
      return True

  def set_actor_hurt(self):
    self.actor.image = self.hurt
    # clock.schedule_unique(self.set_actor_normal, 0.2)

  def set_actor_normal(self):
    self.actor.image = self.stay

  def animate_left(self):
    if self.status == 0:
      self.status = 1
      self.actor.image = self.left
    else:
      self.status = 0
      self.actor.image = self.left1

  def animate_right(self):
    if self.status == 0:
      self.status = 1
      self.actor.image = self.right
    else:
      self.status = 0
      self.actor.image = self.right1