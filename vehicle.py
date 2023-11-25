import pygame
# doi tuong xe luu thong
class vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # scale img
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
class vehicleAlert(vehicle):
    def __init__(self, image, x, y, starting_tick):
        self.starting_tick=starting_tick
        super().__init__(image, x, y)