import wx

class Dialog_label_edit(wx.Dialog):
	
	def __init__(self, parent, title):
		super(Dialog_label_edit, self).__init__(parent, title=title,size=(240,150))
		self.parent = parent

		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.texto = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.texto, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.none = wx.RadioButton( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.none, 0, wx.ALL, 5 )
		
		self.h1 = wx.RadioButton( self, wx.ID_ANY, u"H1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.h1, 0, wx.ALL, 5 )
		
		self.h2 = wx.RadioButton( self, wx.ID_ANY, u"H2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.h2, 0, wx.ALL, 5 )
		
		self.h3 = wx.RadioButton( self, wx.ID_ANY, u"H3", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.h3, 0, wx.ALL, 5 )
		
		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		aceptar = wx.Button( self, wx.ID_ANY, u"Aceptar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( aceptar, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.SetSizer(bSizer2)

		aceptar.Bind(wx.EVT_BUTTON,self.text)

		self.label_content()

	def text(self,evt):
		opcion = 10
		if self.h1.GetValue() == True:
			opcion = 16
		elif self.h2.GetValue() == True:
			opcion = 14
		elif self.h3.GetValue() == True:
			opcion = 12

		r = self.texto.GetValue()
		
		self.parent.modify_label(r,opcion,self.type_shape)
		self.Destroy()

	def label_content(self):
		id_shape = self.parent.shape_selected.GetId()
		self.type_shape = ''
		for data in self.parent.diccionary_shapes_info:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])