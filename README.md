### Game Class 

Encapsulates the game's state, simplifies the main loop, and ensures that resources like images and fonts are handled systematically.

- **Initialization Control**: Putting pygame.init() and pygame.display.set_mode() in the __init__ method ensures the engine is ready before any other part of the game tries to use it.

- **Dependency Management**: By creating an Assets attribute with the Game class, we ensure that all images and fonts are loaded once and are accessible to every game object that needs them.

- **Cleanliness**: Avoid global variables, making the code easier to debug and test.

### Assets Class 

**Why use convert_alpha()?** 

In Pygame, calling convert_alpha() is a critical optimization step when loading images that contain transparency (like PNGs). Two main reasons for its use:

1. Massive Performance Boost 

When you load an image using pygame.image.load(), it keeps the image in its original file format (e.g., 24-bit or 32-bit PNG). Every time you "blit" (draw) that image to your game window, Pygame has to convert its pixels on-the-fly to match the  display's format.

- Without it: Your game might lag or drop frames because it's recalculating pixel data 60 times a second.
- With it: The conversion happens once at the start of the game. This makes the drawing process significantly faster, sometimes increasing FPS by up to 5 times.

2. Preserves Transparency 

There are tow "convert" methods, and choosing the right one depends on whether your image is transparent:

- convert(): Optimized for speed but removes transparency. Transparent areas will often turn black or white. Use this for backgrounds or images without any see-through parts.
- convert_alpha(): Optimized for speed while keeping the alpha channel (transparency). Use this for sprites, UI elements, or anything wiht rounded edges or "empty" space.

Always call these methods **after** you have initialized your display with pygame.display.set_mode(), as they need the window's format to know what to convert the images into.