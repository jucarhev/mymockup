#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Tab_dialog(wx.Dialog):
	
	def __init__(self, parent, title):
		super(Tab_dialog, self).__init__(parent, title=title,size=(410,220))
		self.parent = parent
		
		self.nombre = wx.TextCtrl(self,-1, pos=(10,10), size=(200,30),style=wx.TE_PROCESS_ENTER)
		
		wx.StaticText(self,-1,'Activo: ',pos=(10,55))

		self.lbl_selection = wx.StaticText(self,-1,'',(60, 55),(150, -1))

		btn = wx.Button(self,-1,'Aceptar',pos=(10,100))
		
		self.listBox = wx.ListBox(self, -1, (220, 10), (90, 170), [], wx.LB_SINGLE)

		up = wx.Button(self,-1,'Arriba',pos=(320,10))
		down = wx.Button(self,-1,'Abajo',pos=(320,50))
		delete = wx.Button(self,-1,'Eliminar',pos=(320,90))

		btn.Bind(wx.EVT_BUTTON,self.crear_tabs)
		up.Bind(wx.EVT_BUTTON,self.up)
		down.Bind(wx.EVT_BUTTON,self.down)
		delete.Bind(wx.EVT_BUTTON,self.delete)
		self.nombre.Bind(wx.EVT_TEXT_ENTER, self.add_list)

		self.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBox)

	def crear_tabs(self,evt):
		if self.lbl_selection.GetLabel() != '':
			lista = {}
			for i in range(0,self.listBox.GetCount()):
				lista[i] = self.listBox.GetString(i)

			self.parent.draw_tab(None,self.lbl_selection.GetLabel(),lista,False)
			self.Destroy()

		else:
			wx.MessageBox("Seleccione un item", "Message" ,wx.OK | wx.ICON_ERROR)

	def add_list(self,evt):
		n = self.nombre.GetValue()
		self.listBox.Append(n)
		self.nombre.SetValue('')

	def up(self,evt):
		n = self.listBox.GetCount()
		r = 0
		
		for i in range(0,n):
			if self.listBox.GetString(i) == self.listBox.GetStringSelection():
				r = i
				dato = self.listBox.GetStringSelection()
		
		if r != 0:
			r = r - 1
			d = self.listBox.GetString(r)
			self.listBox.SetString(r,dato)
			self.listBox.SetString(r+1,d)

	def down(self,evt):
		try:
			n = self.listBox.GetCount()
			r = 0
			
			for i in range(0,n):
				if self.listBox.GetString(i) == self.listBox.GetStringSelection():
					r = i
					dato = self.listBox.GetStringSelection()
			
			if r <= (n-1):
				r = r + 1
				d = self.listBox.GetString(r)
				self.listBox.SetString(r,dato)
				self.listBox.SetString(r-1,d)
		except Exception as e:
			print(e)
	
	def delete(self,evt):
		n = self.listBox.GetCount()
		r = 0
		for i in range(0,n):
			if self.listBox.GetString(i) == self.listBox.GetStringSelection():
				r = i
		self.listBox.Delete(r)

	def onListBox(self,evt):
		self.lbl_selection.SetLabel(evt.GetEventObject().GetStringSelection())
	
class Tab(ogl.DrawnShape):
	
	def __init__(self,lista,active):
		ogl.DrawnShape.__init__(self)

		n = len(lista)
		self.diccionario = lista

		i = self.buscarElemento(lista,active)

		r = (int(n) * 70 + ((int(n)-1))*4)+50
		self.calculate_size(r)
		self.tabs(n,r,i)
		self.labels(n,r)

		self.CalculateSize()

	def calculate_size(self,r):
		w = r/2
		self.SetDrawnPen(wx.BLACK_PEN)
		self.SetDrawnBrush(wx.WHITE_BRUSH)
		return self.DrawPolygon([(w, 100), (-w,100),(-w,-70),(w,-70),(w,100)])

	def tabs(self,n,r,i):
		w = r / 2
		cp4 = 0
		
		for x in range(0,n):
			sp = 70
			self.SetDrawnPen(wx.BLACK_PEN)
			if x == i:
				self.SetDrawnBrush(wx.Brush(wx.Colour(240, 240, 240)))
			else:
				self.SetDrawnBrush(wx.Brush(wx.Colour(155, 155, 155)))
			self.DrawPolygon([((-w + cp4),-70),((-w + cp4),-100),(((-w+cp4)+sp),-100),(((-w+cp4)+sp),-70)])

			cp4 = cp4 + 74

	def labels(self,items,r):
		w = r / 2
		ran = 0

		for x in xrange(0,items):
			self.SetDrawnTextColour(wx.BLACK)
			self.SetDrawnFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
			
			name = self.diccionario[x]
			self.DrawText(str(name), (-w+ran+10, -90))


			ran = ran + 74

	def buscarElemento(self,lista, elemento):
		for i in range(0,len(lista)):
			if(lista[i] == elemento):
				return i