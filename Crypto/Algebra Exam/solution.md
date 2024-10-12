# Algebra Exam

In this challenge, we are given a list of equations in a .txt file. The first step in solving the challenge is knowing that equations correspond to lines/curves in a 2D plane and hence the next logical step would be to plot the equations. There are primarily two different ways to solve this:

## Approach 1

This is one of the easiest ways to solve the challenge if you are not comfortable with coding. Basically, plot the equations in a graphing calculator preferably Desmos and you would be able to see some letters on the graph. This is what the output should look like. Now the question is about what these letters mean. If you notice carefully, the equations are given in a particular order and a set of equations correspond to a letter. The order of the equations given is the order of the characters.

![alt text](image.png)

## Approach 2

For all the programming enthusiasts,

You can write a simple solve script using python and plot the equations using matplotlib. The script would look something like this:

```import numpy
import matplotlib.pyplot

fig, ax = matplotlib.pyplot.subplots()

#M
yvalue = numpy.linspace(-6, -4, 100)
ax.plot([-3]*len(yvalue), yvalue)
yvalue = numpy.linspace(-6, -4, 100)
ax.plot([-1]*len(yvalue), yvalue)
xvalue = numpy.linspace(-3, -2, 100)
yvalue = -xvalue - 7
ax.plot(xvalue, yvalue)
xvalue = numpy.linspace(-2, -1, 100)
yvalue = xvalue - 3
ax.plot(xvalue, yvalue)

#A
xvalue = numpy.linspace(-5, -4, 100)
yvalue = 2 * xvalue + 10
ax.plot(xvalue, yvalue)
xvalue = numpy.linspace(-4, -3, 100)
yvalue = -2 * xvalue - 6
ax.plot(xvalue, yvalue)
xvalue = numpy.linspace(-4.5, -3.5, 100)
ax.plot(xvalue, [1]*len(xvalue))

#T
xvalue = numpy.linspace(2, 4, 100)
ax.plot(xvalue, [-7]*len(xvalue))
yvalue = numpy.linspace(-9, -7, 100)
ax.plot([3]*len(yvalue), yvalue)

#H
yvalue = numpy.linspace(-3, -1, 100)
ax.plot([-1]*len(yvalue), yvalue)
yvalue = numpy.linspace(-3, -1, 100)
ax.plot([0]*len(yvalue), yvalue)
xvalue = numpy.linspace(-1, 0, 100)
ax.plot(xvalue, [-2]*len(xvalue))

#I
xvalue = numpy.linspace(1, 2, 100)
ax.plot(xvalue, [-1]*len(xvalue))
xvalue = numpy.linspace(1, 2, 100)
ax.plot(xvalue, [-3]*len(xvalue))
yvalue = numpy.linspace(-3, -1, 100)
ax.plot([1.5]*len(yvalue), yvalue)

#S
theta = numpy.linspace(0, 2 * numpy.pi, 100)
x_circle = 0.5 + 0.5 * numpy.cos(theta)
y_circle = -7.5 + 0.5 * numpy.sin(theta)
ax.plot(x_circle[y_circle > -7.5], y_circle[y_circle > -7.5])
theta = numpy.linspace(0, 2 * numpy.pi, 100)
x_circle = 0.5 + 0.5 * numpy.cos(theta)
y_circle = -7.5 + 0.5 * numpy.sin(theta)
ax.plot(x_circle[x_circle < 0.5], y_circle[x_circle < 0.5])
theta = numpy.linspace(-numpy.pi / 2, numpy.pi / 2, 100)
x_circle = 0.5 + 0.5 * numpy.cos(theta)
y_circle = -8.5 + 0.5 * numpy.sin(theta)
ax.plot(x_circle, y_circle)

#F
xvalue = numpy.linspace(-5, -4, 100)
ax.plot(xvalue, [-1]*len(xvalue))
xvalue = numpy.linspace(-5, -4.25, 100)
ax.plot(xvalue, [-2]*len(xvalue))
yvalue = numpy.linspace(-3, -1, 100)
ax.plot([-5]*len(yvalue), yvalue)

#U
yvalue = numpy.linspace(-8.5, -7, 100)
ax.plot([5]*len(yvalue), yvalue)
yvalue = numpy.linspace(-8.5, -7, 100)
ax.plot([6]*len(yvalue), yvalue)
theta = numpy.linspace(0, 2 * numpy.pi, 100)
x_circle = 5.5 + 0.5 * numpy.cos(theta)
y_circle = -8.5 + 0.5 * numpy.sin(theta)
ax.plot(x_circle[y_circle < -8.5], y_circle[y_circle < -8.5])

#N
yvalue = numpy.linspace(-6, -4, 100)
ax.plot([0]*len(yvalue), yvalue)
xvalue = numpy.linspace(0, 1.5, 100)
yvalue = (-4/3) * xvalue - 4
ax.plot(xvalue, yvalue)
yvalue = numpy.linspace(-6, -4, 100)
ax.plot([1.5]*len(yvalue), yvalue)

matplotlib.pyplot.show()
```

The comments in the code indicates which letter the set of equations corresponds to and spells out: M-A-T-H-I-S-F-U-N

FLAG: ironCTF{MATHISFUN}
