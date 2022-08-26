### Basic implementation of sponge function (https://en.wikipedia.org/wiki/Sponge_function)

In order to build on top of this class, you should pass 3 arguments in Sponge constructor

r - bitrate
c - capacity
f - your pseudorandom transform function (mixer)