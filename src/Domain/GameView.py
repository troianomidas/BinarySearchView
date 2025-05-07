import pygame
import random
import time

class BinarySearchVisualizer:
    # Constants
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 650
    ARRAY_SIZE = 151
    COLORS = {
        'default': (0, 204, 102),
        'search': (255, 0, 0),
        'found': (0, 0, 153),
        'highlight': (255, 102, 0),
        'background': (255, 255, 255),
        'text': (0, 0, 0)
    }

    def __init__(self):
        pygame.font.init()
        self.small_font = pygame.font.SysFont("comicsan", 20)
        self.medium_font = pygame.font.SysFont("comicsans", 30)
        self.large_font = pygame.font.SysFont("comicsans", 70)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("BINARY SEARCH VISUALIZER")
        
        self.array = [0] * self.ARRAY_SIZE
        self.array_colors = [self.COLORS['default']] * self.ARRAY_SIZE
        self.search_key = 0
        self.key_found = False
        self.start_time = time.time()
        self.generate_array()

    def generate_array(self):
        for i in range(1, self.ARRAY_SIZE):
            self.array_colors[i] = self.COLORS['default']
            self.array[i] = random.randrange(1, 100)
        self.heap_sort()

    def heap_sort(self):
        n = len(self.array)

        for i in range(n // 2 - 1, -1, -1):
            self._heapify(i, n)
        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            self._heapify(0, i)

    def _heapify(self, root, size):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and self.array[left] > self.array[largest]:
            largest = left
        if right < size and self.array[right] > self.array[largest]:
            largest = right

        if largest != root:
            self.array[root], self.array[largest] = self.array[largest], self.array[root]
            self._heapify(largest, size)

    def binary_search(self):
        left, right = 0, len(self.array) - 1
        
        while left < right:
            self.array_colors[left] = self.array_colors[right] = self.COLORS['search']
            self.refresh_display()

            mid = left + (right - left) // 2

            if self.array[mid] == self.search_key:
                self.array_colors[mid] = self.COLORS['found']
                return True
            
            if self.array[mid] < self.search_key:
                self.array_colors[left] = self.COLORS['default']
                left = mid + 1
            else:
                self.array_colors[right] = self.COLORS['default']
                right = mid - 1
                
            self.refresh_display()
            
        return False

    def handle_keypress(self, event):
        if event.key == pygame.K_r:
            self.reset_search()
            self.generate_array()
        elif event.key == pygame.K_n:
            self.reset_search()
        elif event.key == pygame.K_RETURN and self.search_key != 0:
            self.key_found = self.binary_search()
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            digit = event.key - pygame.K_0
            self.search_key = self.search_key * 10 + digit

    def reset_search(self):
        self.search_key = 0
        self.key_found = False
        self.array_colors = [self.COLORS['default']] * self.ARRAY_SIZE

    def draw(self):
        self.screen.fill(self.COLORS['background'])
        self._draw_interface()
        self._draw_array()
        pygame.display.update()

    def _draw_interface(self):
        texts = [
            (self.medium_font, "SEARCH: PRESS 'ENTER'", (20, 20)),
            (self.medium_font, "NEW ARRAY: PRESS 'R'", (20, 40)),
            (self.small_font, f"ENTER NUMBER TO SEARCH: {self.search_key}", (600, 60)),
            (self.small_font, f"Running Time(sec): {int(time.time() - self.start_time)}", (600, 20))
        ]
        
        for font, text, pos in texts:
            self.screen.blit(font.render(text, True, self.COLORS['text']), pos)

    def _draw_array(self):
        element_width = (self.WINDOW_WIDTH - 150) // 150
        x_scale = self.WINDOW_WIDTH / 150
        y_scale = 550 / 100

        pygame.draw.line(self.screen, self.COLORS['text'], (0, 95),
                        (self.WINDOW_WIDTH, 95), 6)

        for i in range(1, self.ARRAY_SIZE):
            pygame.draw.line(self.screen, self.array_colors[i],
                           (x_scale * i - 3, 100),
                           (x_scale * i - 3, self.array[i] * y_scale + 100),
                           element_width)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event)
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    visualizer = BinarySearchVisualizer()
    visualizer.run()