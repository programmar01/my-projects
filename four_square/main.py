import turtle as t
import colorsys as color
t.bgcolor('black')
t.tracer(10)
h = 0.4
for i in range(2000):
	c = color.hsv_to_rgb(h,1,1)
	h += 0.005
	t.width(5)
	t.color(c)
	t.fillcolor('black')
	t.begin_fill()
	t.fd(i)
	t.circle(120, steps=4)
	t.fd(i)
	t.right(91)
	t.fd(i)
	t.end_fill()
	t.fd(i)
	t.right(1)
t.done()