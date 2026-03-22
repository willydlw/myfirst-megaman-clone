### Learning Journey 

What new things did I learn?

#### __init__.py 

- Package Recognition: Adding an __init__.py file to a directory marks the directory as a regular python package. This makes the modules in this directory explicitly importable. 

- Initialization Code: Any code in the __init__.py file is executed once, the first time the package (or any module within it) is imported. This is a good place to 
    - Define package-level variables and constants.
    - Set up configurations
    - Perform setup tasks

- Simplified Imports/Defining the Public API: The file can be used to control the package's namespace and simplify access for users. By importing specfic functions or classes into the __init__.py's namespace, users can access them directly form the package name, rather than needing to navigate the internal module structure.
    - Example: Instead of ```from mypackage.mymodule import my_function```, you can add from ```.mymodule import my_function``` to ```mypackage/__init__.py```, allowing users to simply use ```from mypackage import my_function``` 

- Controlling from package import * behavior. By defining the special ```__all__``` variable in ```__init__.py```, you can explicitly specify which modules or names should be imported when a wildcard import(*) is used.


#### Fallback Images and Font

If an image fails to load, a brigh magenta surface is created as fallback. Helpful because (1) draw loops won't fail because self.image[name] will always contain a valid pygame surface. (2) Visual debugging: If you see a bright pink box while testing, you instantly know which asset has a broken path.

If a font fails to load, the fallback is a system font.


#### Scaling Images 

Megaman Images

megaman-left.png and megaman-right.png are 210 x 240 pixels. Ratio is 7:8 

megaman-left-jump.png and megaman-right-jump.png are 260 x 300 pixels. Ratio is 13:15

The player standing and jumping images are different sizes. This can cause collision issues when switching from jumping to standing. The player hitbox constant is the smaller of the two sizes: 42 x 48.

Floor tiles: floor-tile.png is 160 x 160 pixels. Ratio is 1:1





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