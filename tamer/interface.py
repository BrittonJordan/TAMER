import os
import pygame


class Interface:
    """ Pygame interface for training TAMER """

    def __init__(self, action_map):
        self.action_map = action_map
        pygame.init()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self._last_action = None
        self._owns_window = pygame.display.get_surface() is None

        if self._owns_window:
            # set position of pygame window (so it doesn't overlap with gym)
            os.environ["SDL_VIDEO_WINDOW_POS"] = "1000,100"
            os.environ["SDL_VIDEO_CENTERED"] = "0"
            self.screen = pygame.display.set_mode((200, 100))
            area = self.screen.fill((0, 0, 0))
            pygame.display.update(area)
        else:
            # Reuse Gym's pygame window to avoid replacing it with another display.
            self.screen = pygame.display.get_surface()

    def get_scalar_feedback(self):
        """
        Get human input. 'W' key for positive, 'A' key for negative.
        Returns: scalar reward (1 for positive, -1 for negative)
        """
        reward = 0
        area = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self._owns_window:
                        area = self.screen.fill((0, 255, 0))
                    reward = 1
                    break
                elif event.key == pygame.K_a:
                    if self._owns_window:
                        area = self.screen.fill((255, 0, 0))
                    reward = -1
                    break
        if self._owns_window:
            pygame.display.update(area)
        return reward

    def show_action(self, action):
        """
        Show agent's action on pygame screen
        Args:
            action: numerical action (for MountainCar environment only currently)
        """
        if self._owns_window:
            area = self.screen.fill((0, 0, 0))
            pygame.display.update(area)
            text = self.font.render(self.action_map[action], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (100, 50)
            area = self.screen.blit(text, text_rect)
            pygame.display.update(area)
        elif self._last_action != action:
            # In single-window mode, expose the current action in the title bar.
            pygame.display.set_caption(f'TAMER action: {self.action_map[action]}')
            self._last_action = action
