import pygame
import math

def getRotatedImage(image, rect, angle):
    rotatedImage = pygame.transform.rotate(image, angle)
    new_rect = rotatedImage.get_rect(center=rect.center)
    return rotatedImage, new_rect

def angleBetweenPoints(x1, y1, x2, y2):
    x_difference = x2 -x1
    y_difference = y2 -y1
    angle = math.degrees(math.atan2(-y_difference, x_difference))
    return angle

def findMiddle(image, screen):
    new_x = int(screen.get_width() / 2) - int(image.get_width() / 2)
    new_y = int(screen.get_height() / 2) - int(image.get_height() / 2)
    return new_x, new_y
