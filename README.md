### Basic implementation of the sponge function (https://en.wikipedia.org/wiki/Sponge_function)

In order to build on top of this implementation, you should pass 3 arguments in Sponge constructor

r - bitrate
c - capacity
f - your pseudorandom transform function (mixer)

In order to execute algorithm, you should call 'operate' method