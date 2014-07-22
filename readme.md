# GOAPy
### Written by flags, 2014 (https://github.com/flags)

## About GOAP

Goal-Oriented Action Planning is a generic architecture for autonomous AI.

Created by Jeff Orkin, GOAP is employed by a variety of AAA game titles, known for its high level of flexibility and ease-of-use. Those interested in learning more should check out [Jeff's website.](http://alumni.media.mit.edu/~jorkin/goap.html)

## Warning

This library is currently in development.

## Example

See `example.py`.

By taking the current state of the AI (e.g.: Hungry? Tired?) and their desired state (e.g.: Not tired) a "plan" is generated to take the AI from their current state to their goal state by considering a list of actions. By attaching weights to these actions, GOAP is capable of producing highly dynamic results. In this case, the AI will discover that in order to sleep, they must first find and consume food, potentially leading to a complex course of action that involves going shopping, cooking, ordering pizza, taking a shower, etc.

## License

The MIT License (MIT)

Copyright (c) 2014 Luke Martin (flags)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
