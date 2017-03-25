#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Accordion_dialog(wx.Dialog):
	
	def __init__(self, parent, title):
		super(Accordion_dialog, self).__init__(parent, title=title,size=(410,220))
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

			self.parent.draw_accordeon(None,self.lbl_selection.GetLabel(),lista,False)
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

class Accordion(ogl.DividedShape):
	
	def __init__(self, width, height, canvas, lista, active):
		ogl.DividedShape.__init__(self, width, height)

		n = len(lista)
		self.diccionario = lista

		for i in range(0,n):
			region = ogl.ShapeRegion()
			region.SetText(self.diccionario[i])
			region.SetProportions(0.0, 0.2)
			region.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ|ogl.FORMAT_CENTRE_VERT)
			self.AddRegion(region)

			if active == self.diccionario[i]:
				region = ogl.ShapeRegion()
				region.SetProportions(0.0, 0.4)
				region.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ|ogl.FORMAT_CENTRE_VERT)
				self.AddRegion(region)

		self.SetRegionSizes()
		self.ReformatRegions(canvas)


	def ReformatRegions(self, canvas=None):
		rnum = 0

		if canvas is None:
			canvas = self.GetCanvas()

		dc = wx.ClientDC(canvas)

		for region in self.GetRegions():
			text = region.GetText()
			self.FormatText(dc, text, rnum)
			rnum += 1

	def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
		ogl.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
		self.SetRegionSizes()
		self.ReformatRegions()
		self.GetCanvas().Refresh()