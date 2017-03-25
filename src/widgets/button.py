#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Dialog_button_edit(wx.Dialog):
	def __init__(self, parent, title):
		super(Dialog_button_edit, self).__init__(parent, title=title,size=(240,120))
		self.parent = parent

		self.texto = wx.TextCtrl( self, wx.ID_ANY, size=(220,30), pos=(10,10))
		
		aceptar = wx.Button( self, wx.ID_ANY, u"Aceptar",pos=(10,50))

		aceptar.Bind(wx.EVT_BUTTON,self.text)

		self.label_content()

	def text(self,evt):
		r = self.texto.GetValue()
		
		self.parent.modify_label(r,10,self.type_shape)
		self.Destroy()

	def label_content(self):
		id_shape = self.parent.shape_selected.GetId()
		self.type_shape = ''
		for data in self.parent.diccionary_shapes_info:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])