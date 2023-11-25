import pygame

#button class
class Button():
	mouse_holding=False
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#kiểm tra xem chuột đang có hover trên button và đang click hay không
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			if  pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.__class__.mouse_holding == False :
				self.clicked = True	
				self.__class__.mouse_holding=True
			if  pygame.mouse.get_pressed()[0] == 0 and self.clicked == True :
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
			self.__class__.mouse_holding=False
		#hiển thị button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
