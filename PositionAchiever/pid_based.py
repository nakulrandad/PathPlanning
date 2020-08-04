import matplotlib.pyplot as plt 


# Simulation parameters
dt = 0.01
x_pos, y_pos = 0, 0

# Starts interactive mode
plt.ion()


def click(event):  # pragma: no cover
    global x_pos, y_pos
    x_pos = event.xdata
    y_pos = event.ydata


class Dot:
	def __init__(self, x, y, max_vel=2):
		self.x = x
		self.y = y
		self.attain_x = x
		self.attain_y = y
		self.error = [self.attain_x - self.x, self.attain_y - self.y]
		self.prev_error = self.error
		self.tot_error = [0, 0]
		self.max_vel = max_vel

	def plot_dot(self, fig):
		plt.cla()

		plt.scatter(self.attain_x, self.attain_y, marker='x', c='r')
		plt.plot(self.x, self.y, 'go')

		plt.xlim(-1000,1000)
		plt.ylim(-1000,1000)
		plt.gca().set_aspect('equal', adjustable='box')

		plt.show()
		plt.pause(dt)

	def update_pos(self):
		Kp_x = Kp_y = 0.5
		Kd_x = Kd_y = 0.0002
		Ki_x = Ki_y = 0.001

		delta_Vx = (self.error[0]-self.prev_error[0])/dt
		delta_Vy = (self.error[1]-self.prev_error[1])/dt
		delta_X = self.error[0]
		delta_Y = self.error[1]

		self.x += Kp_x*delta_X + Kd_x*delta_Vx + Ki_x*self.tot_error[0]*dt
		self.y += Kp_y*delta_Y + Kd_y*delta_Vy + Ki_y*self.tot_error[1]*dt
		self.prev_error = self.error
		self.error = [self.attain_x - self.x, self.attain_y - self.y]
		self.tot_error[0] += self.error[0]
		self.tot_error[1] += self.error[1]

		if self.tot_error[0] > 100:
			self.tot_error[0] = 100
		elif self.tot_error[0] < -100:
			self.tot_error[0] = -100

		if self.tot_error[1] > 100:
			self.tot_error[1] = 100
		elif self.tot_error[1] < -100:
			self.tot_error[1] = -100


def main():
	fig = plt.figure()
	fig.canvas.mpl_connect("button_press_event", click)
	fig.canvas.mpl_connect('key_release_event',
							lambda event: [exit(0) if event.key == 'escape' else None])
	dot = Dot(0, 0)

	while True:
		global x_pos, y_pos
		dot.attain_x = x_pos
		dot.attain_y = y_pos
		dot.plot_dot(fig)
		dot.update_pos()


if __name__ == "__main__":
	main()

