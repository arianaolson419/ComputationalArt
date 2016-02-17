""" TODO: Put your header comment here """

from random import randint
from math import *
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    #using a dictionary/tuple combination allows for easy additions to the functions if I want to later
    #keys are number of arguments required and values are the elementary functions
    functions = {0:('x', 'y'), 1:('cos_pi', 'sin_pi', 'square'), 2:('prod', 'avg', 'prod_squared')} #sum(a,b) = a+b; square(a) = a**2 
    f = []
    #base case for depth of 1. The function cannot have any arguments.
    depth = randint(min_depth, max_depth)
    if depth == 1:
        arguments = 0
        elementary = functions[arguments][randint(0, len(functions[arguments])-1)]
        f.append(elementary)
        return f
    #base case for depth of 2. These functions can only take one argument
    elif depth == 2:
        arguments = 1
        #I chose to use arguments as my max_depth below instead of 1 for readability
        argument1 = build_random_function(1,arguments)  #chooses a random function that takes no arguments
        #can chose a random elementary function from the functions that take one argument
        elementary = functions[arguments][randint(0, len(functions[arguments])-1)]
        chunk = [elementary, argument1]
        f.append(chunk)
        return f[0]
    #random functions with a depth greater than 2 can have either 1 or two arguments
    else:
        #randomly choses the number of arguments
        arguments = randint(1,2)
        #by using depth-1 as the max_depth below, this allows the randomly built function to be limited to the
        #original max_depth 
        argument1 = build_random_function(1,depth-1)
        argument2 = build_random_function(1, depth-1)
        #choses a function that takes the number of arguments specified
        elementary = functions[arguments][randint(0, len(functions[arguments])-1)]
    
        if arguments == 2:
            chunk = [elementary, argument1, argument2]
    
        else:
            chunk = [elementary, argument1]
        f.append(chunk)
        return f[0]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['prod', ['sin_pi', ['x']], ['cos_pi', ['y']]], 0, 0)
        0.0
        >>> evaluate_random_function(['z'], 3.5, 1.2)
        z is not in the list of defined functions
    
    """
    #by using recursion, evaluating each depth of the function becomes easy
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'sin_pi':
        return sin(evaluate_random_function(f[1], x, y)*pi)
    elif f[0] == 'cos_pi':
        return cos(evaluate_random_function(f[1], x, y)*pi)
    elif f[0] == 'square':
        return evaluate_random_function(f[1], x, y)**2
    elif f[0] == 'avg':
        return 0.5*(evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))
    elif f[0] == 'prod': 
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == 'prod_squared':
        return (evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y))**2
    #I wanted the option to not include colors 
    elif f[0] == '0':
        return 0
    else: 
        print f[0], "is not in the list of defined functions"
        return None



def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    #the floats below ensure we avoid weird integer math mistakes
    a = float(val- input_interval_start)
    b = float(input_interval_end - input_interval_start)
    c = float(output_interval_end - output_interval_start)
    ratio = c*(a/b)
    return ratio + output_interval_start



def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(10,20)
    green_function = build_random_function(1,1)
    blue_function = build_random_function(20,25)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(evaluate_random_function, globals())

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png", 400, 450)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
