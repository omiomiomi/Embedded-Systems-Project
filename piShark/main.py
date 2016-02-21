from kivy.uix.textinput import TextInput
from kivy.app import App 
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget 
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
protocol = '0'
cls = '0'
import os
import posix_ipc
class ScreenManagement(ScreenManager):
	pass
writePipe = "/tmp/pipe"
messageQueue = "/msg_que"
mq = posix_ipc.MessageQueue(messageQueue)

try:
	os.mkfifo(writePipe)
except OSError:
	pass
class TriggeredCapture(Screen):	
	my_data1 = ListProperty([])
	my_data2 = ListProperty([])
	my_data3 = ListProperty([])
	my_data4 = ListProperty([])
	my_data5 = ListProperty([])
	my_data6 = ListProperty([])
	my_data7 = ListProperty([])

	def change2(self):
		self.selected_value = 'Selected: {}'.format(change.text)
	def protocol1(self):
		global protocol
		protocol = '1'
	def protocol2(self):
		global protocol
		protocol = '2'
	def protocol3(self):
		global protocol
		protocol = '3'
	def protocol4(self):
		global protocol
		protocol = '4'
	def receive(self, *args):
		global count
		try:
			f, _ = mq.receive(10)
			f_string = str(f)
			f_list = f_string.split(',')
			self.ids.noti.text = 'Running'
			self.my_data1.append(f_list[0])
			self.my_data3.append(f_list[2])
			self.my_data4.append(f_list[3])
			self.my_data5.append(f_list[4])
			self.my_data6.append(f_list[5])
			self.my_data7.append(f_list[6])
		except:
			self.ids.noti.text = 'Nothing received'
			pass
	def send_parameters(self, params):
		p = open(writePipe, 'w')
		params_send = str(params)
		p.write(params_send)
		p.close()
	def start(self):
		global cls
		cls = '0'
		self.ids.start.text = 'Started capture with filter'
		self.ids.noti.text = 'Starting capture'
		src = self.ids.src.text
		dst = self.ids.dst.text
		amount=self.ids.amount.text
		if self.ids.amount.text=="":
			amount="0"
		global protocol
		params = protocol+","+src+","+dst+","+amount
		self.send_parameters(params)
		print params
		Clock.schedule_interval(self.receive, 1/1000.)

	def stop(self):
		global cls
		global count
		if cls == '0':
			cls = '1'
			self.ids.noti.text = 'Click Start to Continue or Stop to Clear'
			self.ids.start.text = 'Start'
			Clock.unschedule(self.receive)
		elif cls == '1':
			del self.my_data1[:]
			del self.my_data2[:]
			del self.my_data3[:]
			del self.my_data4[:]
			del self.my_data5[:]
			del self.my_data6[:]
			del self.my_data7[:]
			self.ids.noti.text = 'Cleared'
			cls = '0'




class TrackingLog(Screen):
	my_data3 = ListProperty([])
class BasicCapture(Screen):
	my_data1 = ListProperty([])
	my_data2 = ListProperty([])
	my_data3 = ListProperty([])
	my_data4 = ListProperty([])
	my_data5 = ListProperty([])
	my_data6 = ListProperty([])
	my_data7 = ListProperty([]) 
	selected_value = StringProperty('Select a packet')
	def change(self,change):
		self.selected_value = 'Selected: {}'.format(change.text)
	def protocol1(self):
		global protocol
		protocol = '1'
	def protocol2(self):
		global protocol
		protocol = '2'
	def protocol3(self):
		global protocol
		protocol = '3'
        def protocol4(self):
                global protocol
                protocol = '4'
	def receive(self, *args):
		global count
		try:
			f, _ = mq.receive(10)
			self.ids.noti.text = 'Running'
			f_string = str(f)
			f_list = f_string.split(',')
			self.my_data1.append(f_list[0])
			self.my_data3.append(f_list[2])
			self.my_data4.append(f_list[3])
			self.my_data5.append(f_list[4])
			self.my_data6.append(f_list[5])
			self.my_data7.append(f_list[6])
		except:
			self.ids.noti.text = 'Nothing received'
			pass		
	def send_parameters(self, params):
		p = open(writePipe, 'w')
		params_send = str(params)
		p.write(params_send)
		p.close()
		
	def start(self):
		global cls
		cls = '0'
		self.ids.start.text = 'Started capture with filter'
		self.ids.noti.text = 'Starting capture'
		src = self.ids.src.text
		dst = self.ids.dst.text
		amount = "0"
		global protocol
		params = protocol+","+src+","+dst+","+amount
		self.send_parameters(params)
		print params
		Clock.schedule_interval(self.receive, 1/1000.)		
	def stop(self):
		global cls
		global count	
		if cls == '0':
			cls = '1'
			self.ids.noti.text = 'Click Start to Continue or Stop to Clear'
			self.ids.start.text = 'Start'
			Clock.unschedule(self.receive)					
		elif cls == '1':			
			del self.my_data1[:]
			del self.my_data2[:]
			del self.my_data3[:]
			del self.my_data4[:]
			del self.my_data5[:]
			del self.my_data6[:]
			del self.my_data7[:]
			self.ids.noti.text = 'Cleared'
			cls = '0'
presentation = Builder.load_file("pishark.kv")						
class PiSharkApp(App):
		def build(self):
			return presentation

if __name__ == '__main__':
	PiSharkApp().run()


