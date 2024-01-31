from turtle import*
import colorsys as cs
bgcolor('black')
tracer(20)
pensize(4)
h=0

def draw(ang,n):
    circle(5+n, 90)
    left(ang)
    circle(5+n, 60)
goto(-10,0)
for i in range(700):
	c = cs.hsv_to_rgb(h,1,1)
	h += 0.005
	color(c)
	up()
	draw(90, i/5)
	draw(180, i/2)
	down()
	fillcolor('black')
	begin_fill()
	draw(1/2, 0)
	draw(180, i/5)
	draw(90, i/2)
	end_fill()
	draw(60, i)
done()