#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Dialog_link_edit(wx.Dialog):
	
	def __init__(self, parent, title):
		super(Dialog_link_edit, self).__init__(parent, title=title,size=(240,150))
		self.parent = parent

		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.texto = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.texto, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		aceptar = wx.Button( self, wx.ID_ANY, u"Aceptar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( aceptar, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.SetSizer(bSizer2)

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