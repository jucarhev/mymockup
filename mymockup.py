#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl
import random
import wx.lib.imagebrowser as imagebrowser
import sys, glob, os
import cPickle, os.path


class MyMockup ( wx.Frame ):
	list_shape = []
	list_image_shape = {}
	shape_selected = None

	# Example
	diccionario = []

	select = False
	list_shape_selected = []

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent,size = wx.Size( 790,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		favicon = wx.Icon('icons/logo.png',wx.BITMAP_TYPE_ICO, 16,16)
		self.SetIcon(favicon)
		self.Centre( wx.BOTH )
		self.Show()
		self.SetTitle('MyMockup')
		self.menu()
		self.toolbar()
		self.gui()

	def menu(self):
		"""
		Genera los menus que se necesitan en la pantalla
		"""
		menuBar = wx.MenuBar()

		# Menu de archivo
		archivo = wx.Menu()
		guardar		= archivo.Append(wx.ID_SAVE,'Guardar')
		abrir 		= archivo.Append(wx.ID_OPEN,'Abrir')
		exportar 	= archivo.Append(-1,'Exportar')
		salir 		= archivo.Append(wx.ID_EXIT,'Salir')

		# Menu de Editar
		editar = wx.Menu()
		grid		= editar.AppendCheckItem(-1,'Grid')
		lista_shape = editar.Append(-1,'Lista de shapes')

		# Menu de componentes
		componentes = wx.Menu()
		label		= componentes.Append(-1,'Label')
		text 		= componentes.Append(-1,'TextField')
		password 	= componentes.Append(-1,'PasswordField')
		checkbox 	= componentes.Append(-1,'CheckBox')
		radiobox 	= componentes.Append(-1,'RadioButton')
		button		= componentes.Append(-1,'Button')
		tree 		= componentes.Append(-1,'Tree')
		image 		= componentes.Append(-1,'Image')
		window 		= componentes.Append(-1,'Window')
		tab 		= componentes.Append(-1,'Tab')

		# Menu de shapes
		shapes = wx.Menu()
		circle 		= shapes.Append(-1, "Circulo")
		rectangle 	= shapes.Append(-1, "Rectangulo")
		linea 		= shapes.Append(-1, "Lineas")

		# Menu de ayuda
		ayuda 		= wx.Menu()
		ayudam 		= ayuda.Append(wx.ID_HELP,'Ayuda')
		about 		= ayuda.Append(-1,'Acerca de')
		
		#Agregar los menus a la barra de menu
		menuBar.Append(archivo, "Archivo")
		menuBar.Append(editar, "Editar")
		menuBar.Append(componentes, "Componentes")
		menuBar.Append(shapes, "Shapes")
		menuBar.Append(ayuda, "Ayuda")
		
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.guardar, guardar)
		self.Bind(wx.EVT_MENU, self.abrir, abrir)
		self.Bind(wx.EVT_MENU, self.exportar, exportar)
		self.Bind(wx.EVT_MENU, self.salir, salir)
		self.Bind(wx.EVT_MENU, self.grid, grid)

		self.Bind(wx.EVT_MENU, self.circle, circle)
		self.Bind(wx.EVT_MENU, self.rectangle, rectangle)
		self.Bind(wx.EVT_MENU, self.linea, linea)
		self.Bind(wx.EVT_MENU, self.ayudam, ayudam)
		self.Bind(wx.EVT_MENU, self.about, about)

	def gui(self):
		p = wx.Panel(self)

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		fgSizer3 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		w_select = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_select.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_select, 0, wx.ALL, 5 )
		
		w_texto = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_text.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_texto, 0, wx.ALL, 5 )
		
		w_label = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_label.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_label, 0, wx.ALL, 5 )
		
		w_link = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_link.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_link, 0, wx.ALL, 5 )

		w_button = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_button.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_button, 0, wx.ALL, 5 )
		
		w_icon_checkbox_checked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_checkbox_checked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_icon_checkbox_checked, 0, wx.ALL, 5 )
		
		w_icon_checkbox_unchecked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_checkbox_unchecked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_icon_checkbox_unchecked, 0, wx.ALL, 5 )
		
		w_radio_checked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_radio_checked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_radio_checked, 0, wx.ALL, 5 )
		
		w_radio_unchecked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_radio_unchecked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_radio_unchecked, 0, wx.ALL, 5 )
		
		w_textfield = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_textfield.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_textfield, 0, wx.ALL, 5 )
		
		w_combobox = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_combobox.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_combobox, 0, wx.ALL, 5 )
		
		w_spinner = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_spinner.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_spinner, 0, wx.ALL, 5 )
		
		w_password_field = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_passwordfield.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_password_field, 0, wx.ALL, 5 )
		
		w_scale = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_scale.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_scale, 0, wx.ALL, 5 )
		
		w_listbox = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_listbox.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_listbox, 0, wx.ALL, 5 )
		
		w_image = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_image.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_image, 0, wx.ALL, 5 )
		
		w_windows = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_window.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		fgSizer3.Add( w_windows, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer3, 0, wx.EXPAND, 5 )


		# --------------------------------------------------------
		self.canvas = Canvas( p )
		bSizer1.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )

		

		self.diagram = ogl.Diagram()
		self.canvas.SetDiagram( self.diagram )
		self.diagram.SetCanvas( self.canvas )



		# --------------------------------------------------------
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		lblposition = wx.StaticText( p, wx.ID_ANY, u"Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		lblposition.Wrap( -1 )
		fgSizer1.Add( lblposition, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.position_shape_x = wx.SpinCtrl( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,30 ), wx.SP_ARROW_KEYS, 0, 1000, 0 )
		fgSizer1.Add( self.position_shape_x, 0, wx.ALL, 5 )
		
		self.position_shape_y = wx.SpinCtrl( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,30 ), wx.SP_ARROW_KEYS, 0, 1000, 0 )
		fgSizer1.Add( self.position_shape_y, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( p, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( p, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( p, wx.ID_ANY, u"Tamanio", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.size_shape_x = wx.SpinCtrl( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,30 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		fgSizer1.Add( self.size_shape_x, 0, wx.ALL, 5 )
		
		self.size_shape_y = wx.SpinCtrl( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,30 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		fgSizer1.Add( self.size_shape_y, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( p, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( p, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer1.Add( self.m_staticText7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( p, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer1.Add( self.m_staticText8, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer2.Add( fgSizer1, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline1 = wx.StaticLine( p, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( p, wx.ID_ANY, u"Capa", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer4.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bring_to_front = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/front_to_back2.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( bring_to_front, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bring_forward = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/back_to_front.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( bring_forward, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		send_backward = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/front_to_back.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( send_backward, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		send_to_back = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/front_to_back3.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( send_to_back, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		# -------------------------------------------------
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( p, wx.ID_ANY, u"Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer5.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.position_mouse_x = wx.StaticText( p, wx.ID_ANY, u"X: 0", size=(50,30))
		self.position_mouse_x.Wrap( -1 )
		bSizer5.Add( self.position_mouse_x, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.position_mouse_y = wx.StaticText( p, wx.ID_ANY, u"Y: 0", size=(50,30))
		self.position_mouse_y.Wrap( -1 )
		bSizer5.Add( self.position_mouse_y, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer5, 0, wx.EXPAND | wx.ALL, 5 )

		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

		# -------------------------------------------------
		
		
		
		p.SetSizer( bSizer1 )

		w_select.Bind(wx.EVT_BUTTON,self.select_shapes)
		w_texto.Bind(wx.EVT_BUTTON,self.draw_w_text)
		w_link.Bind(wx.EVT_BUTTON,self.draw_w_link)
		w_label.Bind(wx.EVT_BUTTON,self.draw_w_label)
		w_button.Bind(wx.EVT_BUTTON,self.draw_w_button)
		w_textfield.Bind(wx.EVT_BUTTON,self.draw_w_textfield)
		w_icon_checkbox_checked.Bind(wx.EVT_BUTTON,self.drawn_checkbox_checked)
		w_icon_checkbox_unchecked.Bind(wx.EVT_BUTTON,self.drawn_checkbox_unchecked)
		w_radio_checked.Bind(wx.EVT_BUTTON,self.draw_radiobuttonchecked)
		w_radio_unchecked.Bind(wx.EVT_BUTTON,self.draw_radiobuttonunchecked)
		w_combobox.Bind(wx.EVT_BUTTON,self.draw_combobox)
		w_spinner.Bind(wx.EVT_BUTTON,self.draw_spinner)
		w_password_field.Bind(wx.EVT_BUTTON,self.draw_password_field)
		w_scale.Bind(wx.EVT_BUTTON,self.draw_scale)
		w_listbox.Bind(wx.EVT_BUTTON,self.draw_listbox)
		w_image.Bind(wx.EVT_BUTTON,self.draw_image)
		w_windows.Bind(wx.EVT_BUTTON,self.draw_windows)

		self.position_shape_x.Bind(wx.EVT_SPINCTRL, self.function_position_shape_x)
		self.position_shape_y.Bind(wx.EVT_SPINCTRL, self.function_position_shape_y)
		self.size_shape_x.Bind(wx.EVT_SPINCTRL, self.function_size_shape_x)
		self.size_shape_y.Bind(wx.EVT_SPINCTRL, self.function_size_shape_y)

		bring_to_front.Bind(wx.EVT_BUTTON,self.bring_to_front)
		bring_forward.Bind(wx.EVT_BUTTON,self.bring_forward)
		send_backward.Bind(wx.EVT_BUTTON,self.send_backward)
		send_to_back.Bind(wx.EVT_BUTTON,self.send_to_back)

		#self.canvas.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)

		#self.Bind(wx.EVT_CLOSE, self.doClose)
		#self.Bind(wx.EVT_CHAR_HOOK, self.onKeyEvent)

	def onKeyEvent(self,evt):
		if evt.GetKeyCode() ==  wx.WXK_ESCAPE:
			print('scape')
		elif evt.GetKeyCode() ==  wx.WXK_DELETE:
			if self.shape_selected != None:
				self.delete_shape()
		self.Skip()

	def toolbar(self):
		self.toolbar = self.CreateToolBar()
		tool_delete = self.toolbar.AddLabelTool(5, '', wx.Bitmap('icons/trash.png'))
		tool_duplicate = self.toolbar.AddLabelTool(6, '', wx.Bitmap('icons/tabs-outline.png'))
		tool_image = self.toolbar.AddLabelTool(7, '', wx.Bitmap('icons/image.png'))
		self.toolbar.Realize()

		self.Bind(wx.EVT_TOOL,self.duplicate_shape,tool_duplicate)
		self.Bind(wx.EVT_TOOL,self.delete_shape,tool_delete)
		self.Bind(wx.EVT_TOOL,self.image_collection,tool_image)

	#===============================#
	#		Eventos del menu		#
	#===============================#
	def guardar(self,evt):
		curDir = os.getcwd()

		fileName = wx.FileSelector("Save File As", "Saving",
			default_filename='default',
			default_extension="mmp",
			wildcard="*.mmp",
			flags = wx.SAVE | wx.OVERWRITE_PROMPT)
		
		if fileName != "":
			fileName = os.path.join(os.getcwd(), fileName)
			os.chdir(curDir)

			title = os.path.basename(fileName)
			self.SetTitle(title)
	
	def abrir(self,evt):pass
	
	def exportar(self,evt):
		curDir = os.getcwd()

		fileName = wx.FileSelector("Export", "Export",
			default_filename='mockup',
			default_extension="png",
			wildcard="*.png",
			flags = wx.SAVE | wx.OVERWRITE_PROMPT)
		
		if fileName != "":
			fileName = os.path.join(os.getcwd(), fileName)
			os.chdir(curDir)
			self._export_image(fileName)

	def salir(self,evt):pass

	def grid(self,evt):
		if evt.IsChecked() == True:
			shape = DrawGrid()
			shape.SetId(1)
			self.canvas.AddShape( shape )
			self.diagram.ShowAll( 1 )
			dc = wx.ClientDC(self)
			shape.Move(dc, 0, 0,False)
			shape.SetDraggable(False)
			shape.GetCanvas().Refresh(True)
	
	# Figuras basicas -----------
	
	def circle(self,evt):
		shape = ogl.CircleShape( 20.0 )
		shape.SetX( 25.0 )
		shape.SetY( 25.0 )
		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		shape.GetCanvas().Refresh(True)

		self.list_shape.append(shape)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)
	
	def rectangle(self,evt):
		shape = ogl.RectangleShape(100, 100)
		shape.SetX( random.randint(50,190) )
		shape.SetY( random.randint(50,190) )
		shape.SetId(random.randint(10000,90000))

		shape.SetPen(wx.BLACK_PEN)

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		shape.GetCanvas().Refresh(True)

		self.list_shape.append(shape)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def linea(self,evt):pass

	# Ayuda ---------------------
	def ayudam(self,evt):pass
	def about(self,evt):pass

	#===============================#
	#		Eventos de botones		#
	#===============================#
	def select_shapes(self,evt):
		self.select = True
		self.shape_selected = None

	def draw_w_text(self,evt):
		text = 'Lorem ipsum dolor sit amet,\nconsectetur adipisicing.\nIllum ad expedita repudiandae.'

		shape = ogl.TextShape(210, 55)
		shape.AddText(text)
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
		shape.SetId(random.randint(10000,90000))
		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )
		dc = wx.ClientDC(self)
		shape.Move(dc, 150, 150)
		shape.SetCentreResize(False)

		shape.GetCanvas().Refresh(True)
		self.list_shape.append(shape)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),'Text',text)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def draw_w_link(self,evt):
		text = 'Link'
		self.shape_selected = None

		shape = ogl.TextShape(60, 30)
		shape.AddText('Link')
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
		shape.SetId(random.randint(10000,90000))
		shape.SetTextColour('BLUE')
		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )
		dc = wx.ClientDC(self)
		shape.Move(dc, 100, 100)
		shape.Recentre(dc)
		shape.SetCentreResize(False)
		self.list_shape.append(shape)

		shape.GetCanvas().Refresh(True)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),'Link',text)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def draw_w_label(self,evt):
		text = 'Label'
		shape = ogl.TextShape(60, 30)
		shape.AddText('Label')
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
		shape.SetId(random.randint(10000,90000))
		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )
		dc = wx.ClientDC(self)
		shape.Move(dc, 100, 100)
		shape.SetCentreResize(False)

		shape.GetCanvas().Refresh(True)
		self.list_shape.append(shape)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),'Label',text)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def draw_w_button(self,evt):
		text = 'Button'
		shape = ogl.RectangleShape(100, 30)
		shape.SetX( random.randint(50,190) )
		shape.SetY( random.randint(50,190) )
		shape.SetId(random.randint(10000,90000))
		shape.AddText(text)
		shape.SetCornerRadius(5)
		shape.SetCentreResize(False)

		shape.SetPen(wx.BLACK_PEN)

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		self.list_shape.append(shape)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),'Button',text)

		shape.GetCanvas().Refresh(True)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def draw_w_textfield(self,evt):
		shape = ogl.RectangleShape(100, 30)
		shape.SetX( random.randint(50,190) )
		shape.SetY( random.randint(50,190) )
		shape.SetId(random.randint(10000,90000))
		shape.SetCornerRadius(5)
		shape.SetFixedSize(False,30)
		shape.SetCentreResize(False)

		shape.SetPen(wx.BLACK_PEN)

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		self.list_shape.append(shape)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),'textfield','')

		shape.GetCanvas().Refresh(True)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def drawn_checkbox_checked(self,evt):
		self.draw_radio_and_check('CheckBox','icons/checkboxchecked.png','CheckBox')

	def drawn_checkbox_unchecked(self,evt):
		self.draw_radio_and_check('CheckBox','icons/checkboxunchecked.png','CheckBox')

	def draw_radiobuttonchecked(self,evt):
		self.draw_radio_and_check('RadioButton','icons/radiobuttonchecked.png','RadioButton')

	def draw_radiobuttonunchecked(self,evt):
		self.draw_radio_and_check('RadioButton','icons/radiobuttonunchecked.png','RadioButton')

	def draw_combobox(self,evt):
		self.ShapeComboSpin('ComboBox','icons/combo.png')

	def draw_spinner(self,evt):
		self.ShapeComboSpin('Spinner','icons/spinner.png')

	def ShapeComboSpin(self,type_shape,img):
		shape = CompositeShapeComboSpin(self.canvas,img)
		shape.SetId(random.randint(10000,90000))

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		dc = wx.ClientDC(self)
		shape.Move(dc, random.randint(10,400), random.randint(10,400))
		shape.SetDraggable(True)

		shape.SetFixedSize(False,30)
		shape.SetCentreResize(False)

		self.list_shape.append(shape)

		shape.GetCanvas().Refresh(True)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),type_shape,'')

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def draw_password_field(self,evt):pass
	def draw_scale(self,evt):pass
	def draw_listbox(self,evt):pass
	
	def draw_image(self,evt):
		dialog = imagebrowser.ImageDialog(None)   
		if dialog.ShowModal() == wx.ID_OK: 
			shape = ogl.BitmapShape()
			img = str(dialog.GetFile())
			shape.SetBitmap(wx.Bitmap(img,wx.BITMAP_TYPE_ANY))
			shape.SetId(random.randint(10000,90000))

			self.canvas.AddShape( shape )
			self.diagram.ShowAll( 1 )

			dc = wx.ClientDC(self)
			shape.Move(dc, random.randint(10,200), random.randint(10,200))

			self.list_shape.append(shape)
			self.list_image_shape[shape.GetId()] = img

			shape.GetCanvas().Refresh(True)

			evthandler = MyEvtHandler(self)
			evthandler.SetShape(shape)
			evthandler.SetPreviousHandler(shape.GetEventHandler())
			shape.SetEventHandler(evthandler)
		dialog.Destroy()
	
	def draw_windows(self,evt):pass

	def draw_radio_and_check(self,text,img,type_shape):
		shape = CompositeShape(self.canvas,img)
		shape.SetId(random.randint(10000,90000))

		shape.ClearText()
		shape.AddText(text)
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		dc = wx.ClientDC(self)
		shape.Move(dc, 120, 130)
		shape.SetDraggable(True)

		self.list_shape.append(shape)

		shape.GetCanvas().Refresh(True)

		# Diccionario
		self._add_shape_to_diccionary(shape,shape.GetId(),type_shape,text)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	#=======================================#
	#	Posicion y tamaño de una figura 	#
	#=======================================#
	
	def function_position_shape_x(self,evt):
		self.shape_selected.SetX(self.position_shape_x.GetValue())
		self.canvas.Refresh(True)

	def function_position_shape_y(self,evt):
		self.shape_selected.SetY(self.position_shape_y.GetValue())
		self.canvas.Refresh(True)
	
	def function_size_shape_x(self,evt):
		self.shape_selected.SetWidth(self.size_shape_x.GetValue())
		self.canvas.Refresh(True)

	def function_size_shape_y(self,evt):
		self.shape_selected.SetHeight(self.size_shape_y.GetValue())
		self.canvas.Refresh(True)

	#===============================#
	#	Posicion de las figuras		#
	#===============================#
	
	def bring_to_front(self,evt):
		"""
		Traer al frente cualquier figura o imagen 
		superponiendose a las demas
		"""
		if self.shape_selected != None:
			array_id = []

			for e in self.list_shape:
				array_id.append(e.GetId())

			position = array_id.index(self.shape_selected.GetId())
			self.list_shape.pop(position)
			self.list_shape.append(self.shape_selected)

			self._redraw()

	def bring_forward(self,evt):
		"""
		Adelanta una figura o image una posicion 
		recpecto a la figura anterior
		"""
		if self.shape_selected != None:
			array_id = []

			for e in self.list_shape:
				array_id.append(e.GetId())

			position = array_id.index(self.shape_selected.GetId())

			self.list_shape.pop(position)
			self.list_shape.insert(position + 1, self.shape_selected)

			self._redraw()

	def send_backward(self,evt):
		"""
		Enviar atras una figura con respecto a la que esta
		detras de esta
		"""
		if self.shape_selected != None:
			array_id = []

			if len(self.list_shape) > 1:
				array_id = []

				for e in self.list_shape:
					array_id.append(e.GetId())

				position = array_id.index(self.shape_selected.GetId())

				if self.list_shape[0].GetId() == 1:
					if position-1 != 1:
						self.list_shape.pop(position)
						self.list_shape.insert(position - 1, self.shape_selected)
				else:
					self.list_shape.pop(position)
					self.list_shape.insert(position - 1, self.shape_selected)

				self._redraw()

	def send_to_back(self,evt):
		"""
		Enviar al fondo cualquier imagen o figura
		"""
		if self.shape_selected != None:
			array_id = []
			shape = self.shape_selected

			if self.list_shape[0].GetId() == 1:
				for i in self.list_shape:
					array_id.append(i.GetId())

				if len(array_id) >= 3:
					id_pos = array_id.index(shape.GetId())
					self.list_shape.pop(id_pos)
					self.list_shape.insert(1, self.shape_selected)

			else:
				for i in self.list_shape:
					array_id.append(i.GetId())

				if len(array_id) >= 2:
					id_pos = array_id.index(shape.GetId())
					self.list_shape.pop(id_pos)
					self.list_shape.insert(0, self.shape_selected)

			self._redraw()

	#
	
	def doClose(self, event):
		if len(self.list_shape) != 0:
			self.dirty = True

		if self.dirty == True:
			if not self.askIfUserWantsToSave("closing"): return

		self.Destroy()

	def askIfUserWantsToSave(self, action):
		response = wx.MessageBox("Save changes before " + action + "?","Confirm", wx.YES_NO | wx.CANCEL, self)
		if response == wx.YES:
			pass
		elif response == wx.NO:
			self.Destroy()
		elif response == wx.CANCEL:
			pass
	
	def image_collection(self,evt):
		self.image_selected=[]
		dialog = Dialog_image_collection(self,'Image collection')
		result = dialog.ShowModal()
		if self.image_selected != '':
			for x in self.image_selected:
			 	self.image_duplicate(x)
	
	def image_duplicate(self,img):
		shape = ogl.BitmapShape()
		shape.SetBitmap(wx.Bitmap(img,wx.BITMAP_TYPE_ANY))
		shape.SetId(random.randint(10000,90000))

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		dc = wx.ClientDC(self)
		shape.Move(dc, random.randint(100,200), random.randint(100,200))

		self.list_shape.append(shape)
		self.list_image_shape[shape.GetId()] = img

		shape.GetCanvas().Refresh(True)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)
	
	def duplicate_shape(self,evt):
		if self.shape_selected != None:
			id_shape = self.shape_selected.GetId()
			if str(self.shape_selected).count('BitmapShape') > 0:
				shape = self.shape_selected
				img = self.list_image_shape.get(shape.GetId())
				self.image_duplicate(img)
			elif str(self.shape_selected).count('RectangleShape') > 0:
				self.rectangule_duplicate(self.shape_selected.GetX(),
					self.shape_selected.GetY(),
					self.shape_selected.GetWidth(),
					self.shape_selected.GetHeight())
	
	def rotate_shape(self,evt):pass

	def delete_shape(self,evt = None):
		if self.shape_selected != None:
			self.canvas.RemoveShape(self.shape_selected)
			self.canvas.Refresh(True)
			self.list_shape.remove(self.shape_selected)
		
			dc = wx.ClientDC(self.canvas)
			self.canvas.PrepareDC(dc)
			self.shape_selected.Select(False, dc)

			self.shape_selected = None
		
			self._redraw()
			self.canvas.Refresh(True)
	
	def scale_bitmap(self,bitmap, width, height):
		image = wx.ImageFromBitmap(bitmap)
		image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
		result = wx.BitmapFromImage(image)
		return result

	def shape_propierties(self,shape,x,y):
		self.shape_selected = shape
		self.position_shape_x.SetValue(x)
		self.position_shape_y.SetValue(y)
		self.size_shape_x.SetValue(shape.GetWidth())
		self.size_shape_y.SetValue(shape.GetHeight())

	def double_click(self,shape):
		if str(shape).count("BitmapShape") == True:
			if self.list_image_shape.has_key(shape.GetId()) != 0:
				img = self.list_image_shape[shape.GetId()]
				dialog = Dialog_icon_resize(self,'size',img)
				result = dialog.ShowModal()
		elif str(shape).count("TextShape") == True:
			if self.get_content_diccionary(shape,'type') == 'Label':
				dialog = Dialog_label_edit(self,'LabelEdit')
				result = dialog.ShowModal()
			elif self.get_content_diccionary(shape,'type') == 'Link':
				dialog = Dialog_link_edit(self,'LinkEdit')
				result = dialog.ShowModal()
			elif self.get_content_diccionary(shape,'type') == 'Text':
				dialog = Dialog_text_edit(self,'TextEdit')
				result = dialog.ShowModal()
		elif str(shape).count("RectangleShape") == True:
			if self.get_content_diccionary(shape,'type') == 'Button':
				dialog = Dialog_button_edit(self,'ButtonEdit')
				result = dialog.ShowModal()
		elif str(shape).count("CompositeShape") == True:
			if self.get_content_diccionary(shape,'type') == 'CheckBox':
				dialog = Dialog_widget_edit(self,'CheckBoxEdit')
				result = dialog.ShowModal()
			if self.get_content_diccionary(shape,'type') == 'RadioButton':
				dialog = Dialog_widget_edit(self,'RadioButtonEdit')
				result = dialog.ShowModal()

	def modify_size_bitmap(self,img,size):
		bitmap = wx.Bitmap(img)
		img = self.scale_bitmap(bitmap,int(size),int(size))
		self.shape_selected.SetBitmap(self.scale_bitmap(bitmap,int(size),int(size)))
		self.shape_selected.SetWidth(int(size))
		self.shape_selected.SetHeight(int(size))
		self.shape_selected.GetCanvas().Refresh(True)

	def modify_label(self,texto,h,type_shape):
		self.shape_selected.ClearText()
		self.shape_selected.AddText(texto)
		if h == 10:
			self.shape_selected.SetFont(wx.Font(h, wx.FONTFAMILY_DEFAULT,
				wx.FONTSTYLE_NORMAL,
				wx.FONTWEIGHT_NORMAL))
		else:
			self.shape_selected.SetFont(wx.Font(h, wx.FONTFAMILY_DEFAULT, 
				wx.FONTSTYLE_NORMAL, 
				wx.FONTWEIGHT_BOLD))
		dc = wx.ClientDC(self)
		self.shape_selected.Recentre(dc)
		self.canvas.Refresh(True)
	
		self._search_and_modifi_diccionary(self.shape_selected,'content',texto)

	#===============================#
	#		Eventos de privados		#
	#===============================#
	def _redraw(self):
		x = 0
		
		for i in self.list_shape:
			self.canvas.RemoveShape(i)
		
		for e in self.list_shape:
			self.canvas.AddShape( e )
			self.diagram.ShowAll( 1 )
			
			if x > 0:
				e.SetDraggable(True)
			
			e.GetCanvas().Refresh(True)
			x = x + 1
	
	def _list_shapes(self,evt):
		pass
	
	def _shape_propierties(self,evt):
		pass

	def _data_list_all_shape(self,evt):
		pass
	
	def _search_and_modifi_diccionary(self,shape,atributo,contenido):
		i = 0
		for row in self.diccionario:
			if row[1] == shape.GetId():
				if atributo == 'content':
					row[3] = contenido
			i = i + 1

		self.print_diccionary_content()

	def print_diccionary_content(self):
		for row in self.diccionario:
			print(row)

	def get_content_diccionary(self,shape,data):
		dato = None
		n = 0
		if data == 'shape':
			n = 0
		elif data == 'id':
			n = 1
		elif data == 'type':
			n = 2
		elif data == 'content':
			n = 3

		for row in self.diccionario:
			if row[1] == shape.GetId():
				dato = row[n]
		return dato
	
	def _add_shape_to_diccionary(self,shape,id_shape,type_shape,content):
		array = [shape,id_shape,type_shape,content]
		self.diccionario.append(array)

	def _export_image(self,ruta):
		self.statbmp = wx.StaticBitmap(self)

		w, h = 500, 500
		draw_bmp = wx.EmptyBitmap(w, h)
		dc = wx.MemoryDC(draw_bmp)
		dc.Clear()
		
		self.canvas.GetDiagram().Redraw(dc)
		self.statbmp.SetBitmap(draw_bmp)
		finished_image = self.statbmp.GetBitmap()
		finished_image.SaveFile(ruta, wx.BITMAP_TYPE_PNG)

# Class Grid -----------------------------------------------------------------------
class DrawGrid(ogl.DrawnShape):
	
	def __init__(self):
		ogl.DrawnShape.__init__(self)

		self.SetDrawnPen(wx.Pen("#BABABA"))
		for i in xrange(0,400):
			self.DrawLine((10*i, 0), (10*i, 2020))

		for i in xrange(0,400):
			self.DrawLine((0, 10*i), (2020, 10*i))

		self.SetDrawnPen(wx.Pen("#848484"))
		for i in xrange(0,200):
			self.DrawLine((50*i, 0), (50*i, 2020))

		for i in xrange(0,200):
			self.DrawLine((0, 50*i), (2020, 50*i))

		# Make sure to call CalculateSize when all drawing is done
		self.CalculateSize()

class CompositeShape(ogl.CompositeShape):
	
	def __init__(self, canvas,img):
		ogl.CompositeShape.__init__(self)

		self.SetCanvas(canvas)

		constraining_shape = ogl.BitmapShape()
		constraining_shape.SetBitmap(wx.Bitmap( img, wx.BITMAP_TYPE_ANY ))
		constrained_shape1 = ogl.TextShape(100,30)

		self.AddChild(constraining_shape)
		self.AddChild(constrained_shape1)

		constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF, constraining_shape, [constrained_shape1])
		self.AddConstraint(constraint)

		self.Recompute()

		# If we don't do this, the shapes will be able to move on their
		# own, instead of moving the composite
		constraining_shape.SetDraggable(True)
		constrained_shape1.SetDraggable(True)

		# If we don't do this the shape will take all left-clicks for itself
		constraining_shape.SetSensitivityFilter(0)

class CompositeShapeComboSpin(ogl.CompositeShape):
	
	def __init__(self, canvas,img):
		ogl.CompositeShape.__init__(self)

		self.SetCanvas(canvas)

		constraining_shape = ogl.BitmapShape()
		constraining_shape.SetBitmap(wx.Bitmap( img, wx.BITMAP_TYPE_ANY ))
		constrained_shape1 = ogl.RectangleShape(100, 30)

		self.AddChild(constraining_shape)
		self.AddChild(constrained_shape1)

		constraint = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF, constraining_shape, [constrained_shape1])
		self.AddConstraint(constraint)

		self.Recompute()

		# If we don't do this, the shapes will be able to move on their
		# own, instead of moving the composite
		constraining_shape.SetDraggable(False)
		constrained_shape1.SetDraggable(False)

		# If we don't do this the shape will take all left-clicks for itself
		constraining_shape.SetSensitivityFilter(0)

# Event handler --------------------------------------------------------------------
class MyEvtHandler(ogl.ShapeEvtHandler):
	def __init__(self,parent):
		ogl.ShapeEvtHandler.__init__(self)
		self.parent = parent

	def UpdateStatusBar(self, shape):
		x, y = shape.GetX(), shape.GetY()
		width, height = shape.GetBoundingBoxMax()

	def OnLeftClick(self, x, y, keys=0, attachment=0):
		shape = self.GetShape()
		self.shape_selected = shape
		self.parent.shape_propierties(shape,x,y)
		canvas = shape.GetCanvas()
		dc = wx.ClientDC(canvas)
		canvas.PrepareDC(dc)

		if shape.Selected():
			shape.Select(False, dc)
			#canvas.Redraw(dc)
			canvas.Refresh(False)
		else:
			redraw = False
			shapeList = canvas.GetDiagram().GetShapeList()
			toUnselect = []

			for s in shapeList:
				if s.Selected():
					# If we unselect it now then some of the objects in
					# shapeList will become invalid (the control points are
					# shapes too!) and bad things will happen...
					toUnselect.append(s)

			shape.Select(True, dc)

			if toUnselect:
				for s in toUnselect:
					s.Select(False, dc)

				##canvas.Redraw(dc)
				canvas.Refresh(False)

		self.UpdateStatusBar(shape)

	def OnEndDragLeft(self, x, y, keys=0, attachment=0):
		shape = self.GetShape()
		ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

		if not shape.Selected():
			self.OnLeftClick(x, y, keys, attachment)

		self.UpdateStatusBar(shape)

	def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
		ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
		self.UpdateStatusBar(self.GetShape())

	def OnMovePost(self, dc, x, y, oldX, oldY, display):
		shape = self.GetShape()
		self.shape_selected = shape
		self.parent.shape_propierties(shape,x,y)
		#-----
		shape = self.GetShape()
		ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
		self.UpdateStatusBar(shape)
		if "wxMac" in wx.PlatformInfo:
			shape.GetCanvas().Refresh(False)

	def OnRightClick(self, *dontcare):#  print("%s\n" % self.GetShape())
		shape = self.GetShape()
		self.parent.double_click(shape)

	def OnLeftDoubleClick(self, *dontcare):
		shape = self.GetShape()
		self.parent.double_click(shape)

# ---------------
class Canvas(ogl.ShapeCanvas):
	def __init__(self,parent):
		ogl.ShapeCanvas.__init__(self, parent)
		self.parent = parent

		self.gridsize = 20

		self.SetBackgroundColour( "WHITE" )
		self.SetScrollbars(20, 20, 2000/20, 2000/20)

		self.coordenadas = []


	def OnLeftClick(self, x, y, keys = 0):
		array = [x,y]
		self.coordenadas.append(array)

	def OnRightClick(self, x, y, keys = 0):
		print(self.coordenadas)

# Class dialog -----------------------------------------------------------------
class Dialog_image_collection(wx.Dialog):
	def __init__(self, parent, title):
		super(Dialog_image_collection, self).__init__(parent, title=title,size=(500,500))
		        # load some images into an image list
		il = wx.ImageList(24,24, True)
		self.parent = parent

		self.images_l=['icons_mockup/adjust-brightness.png','icons_mockup/adjust-contrast.png','icons_mockup/anchor-outline.png','icons_mockup/anchor.png','icons_mockup/archive.png','icons_mockup/arrow-back-outline.png',
		'icons_mockup/arrow-back.png','icons_mockup/arrow-down-outline.png','icons_mockup/arrow-down.png','icons_mockup/arrow-down-thick.png','icons_mockup/arrow-forward-outline.png',
		'icons_mockup/arrow-forward.png','icons_mockup/arrow-left-outline.png','icons_mockup/arrow-left.png','icons_mockup/arrow-left-thick.png','icons_mockup/arrow-loop-outline.png',
		'icons_mockup/arrow-loop.png','icons_mockup/arrow-maximise-outline.png','icons_mockup/arrow-maximise.png','icons_mockup/arrow-minimise-outline.png','icons_mockup/arrow-minimise.png',
		'icons_mockup/arrow-move-outline.png','icons_mockup/arrow-move.png','icons_mockup/arrow-repeat-outline.png','icons_mockup/arrow-repeat.png','icons_mockup/arrow-right-outline.png',
		'icons_mockup/arrow-right.png','icons_mockup/arrow-right-thick.png','icons_mockup/arrow-shuffle.png','icons_mockup/arrow-sync-outline.png','icons_mockup/arrow-sync.png',
		'icons_mockup/arrow-up-outline.png','icons_mockup/arrow-up.png','icons_mockup/arrow-up-thick.png','icons_mockup/at.png','icons_mockup/attachment-outline.png','icons_mockup/attachment.png',
		'icons_mockup/backspace-outline.png','icons_mockup/backspace.png','icons_mockup/battery-charge.png','icons_mockup/battery-full.png','icons_mockup/battery-high.png','icons_mockup/battery-low.png',
		'icons_mockup/battery-mid.png','icons_mockup/beaker.png','icons_mockup/beer.png','icons_mockup/bell.png','icons_mockup/bookmark.png','icons_mockup/book.png','icons_mockup/briefcase.png','icons_mockup/brush.png',
		'icons_mockup/business-card.png','icons_mockup/calculator.png','icons_mockup/calender-outline.png','icons_mockup/calender.png','icons_mockup/camera-outline.png','icons_mockup/camera.png','icons_mockup/cancel-outline.png','icons_mockup/cancel.png',
		'icons_mockup/chart-area-outline.png','icons_mockup/chart-area.png','icons_mockup/chart-bar-outline.png','icons_mockup/chart-bar.png','icons_mockup/chart-line-outline.png','icons_mockup/chart-line.png','icons_mockup/chart-pie-outline.png','icons_mockup/chart-pie.png',
		'icons_mockup/chevron-left-outline.png','icons_mockup/chevron-left.png','icons_mockup/chevron-right-outline.png','icons_mockup/chevron-right.png','icons_mockup/clipboard.png','icons_mockup/cloud-storage.png','icons_mockup/code-outline.png','icons_mockup/code.png',
		'icons_mockup/coffee.png','icons_mockup/cog-outline.png','icons_mockup/cog.png','icons_mockup/compass.png','icons_mockup/contacts.png','icons_mockup/credit-card.png','icons_mockup/cross.png','icons_mockup/database.png',
		'icons_mockup/delete-outline.png','icons_mockup/delete.png','icons_mockup/device-desktop.png','icons_mockup/device-laptop.png','icons_mockup/device-phone.png','icons_mockup/device-tablet.png','icons_mockup/directions.png','icons_mockup/divide-outline.png',
		'icons_mockup/divide.png','icons_mockup/document-add.png','icons_mockup/document-delete.png','icons_mockup/document.png','icons_mockup/document-text.png','icons_mockup/download-outline.png','icons_mockup/download.png','icons_mockup/edit.png',
		'icons_mockup/eject-outline.png','icons_mockup/eject.png','icons_mockup/equals-outline.png','icons_mockup/equals.png','icons_mockup/export-outline.png','icons_mockup/export.png','icons_mockup/eye-outline.png',
		'icons_mockup/eye.png','icons_mockup/feather.png','icons_mockup/film.png','icons_mockup/flag-outline.png','icons_mockup/flag.png','icons_mockup/flash-outline.png','icons_mockup/flash.png','icons_mockup/flow-children.png',
		'icons_mockup/flow-merge.png','icons_mockup/flow-parallel.png','icons_mockup/flow-switch.png','icons_mockup/folder-add.png','icons_mockup/folder-delete.png','icons_mockup/folder.png','icons_mockup/gift.png','icons_mockup/globe-outline.png',
		'icons_mockup/globe.png','icons_mockup/group-outline.png','icons_mockup/group.png','icons_mockup/headphones.png','icons_mockup/heart-outline.png','icons_mockup/heart.png','icons_mockup/home-outline.png','icons_mockup/home.png',
		'icons_mockup/image-outline.png','icons_mockup/image.png','icons_mockup/infinity-outline.png','icons_mockup/infinity.png','icons_mockup/info-large-outline.png','icons_mockup/info-large.png','icons_mockup/info-outline.png',
		'icons_mockup/info.png','icons_mockup/input-checked-outline.png','icons_mockup/input-checked.png','icons_mockup/key-outline.png','icons_mockup/key.png','icons_mockup/leaf.png','icons_mockup/lightbulb.png',
		'icons_mockup/link-outline.png','icons_mockup/link.png','icons_mockup/location-arrow-outline.png','icons_mockup/location-arrow.png','icons_mockup/location-outline.png','icons_mockup/location.png',
		'icons_mockup/lock-closed-outline.png','icons_mockup/lock-closed.png','icons_mockup/lock-open-outline.png','icons_mockup/lock-open.png','icons_mockup/mail.png','icons_mockup/map.png','icons_mockup/media-eject-outline.png',
		'icons_mockup/media-eject.png','icons_mockup/media-fast-forward-outline.png','icons_mockup/media-fast-forward.png','icons_mockup/media-pause-outline.png','icons_mockup/media-pause.png',
		'icons_mockup/media-play-outline.png','icons_mockup/media-play.png','icons_mockup/media-record-outline.png','icons_mockup/media-record.png','icons_mockup/media-rewind-outline.png','icons_mockup/media-rewind.png',
		'icons_mockup/media-stop-outline.png','icons_mockup/media-stop.png','icons_mockup/message.png','icons_mockup/messages.png','icons_mockup/message-typing.png','icons_mockup/microphone-outline.png',
		'icons_mockup/microphone.png','icons_mockup/minus-outline.png','icons_mockup/minus.png','icons_mockup/news.png','icons_mockup/notes-outline.png','icons_mockup/notes.png','icons_mockup/pencil.png','icons_mockup/pen.png',
		'icons_mockup/phone-outline.png','icons_mockup/phone.png','icons_mockup/pin-outline.png','icons_mockup/pin.png','icons_mockup/pi-outline.png','icons_mockup/pipette.png','icons_mockup/pi.png','icons_mockup/plane-outline.png','icons_mockup/plane.png',
		'icons_mockup/plug.png','icons_mockup/plus-outline.png','icons_mockup/plus.png','icons_mockup/point-of-interest-outline.png','icons_mockup/point-of-interest.png','icons_mockup/power-outline.png',
		'icons_mockup/power.png','icons_mockup/printer.png','icons_mockup/puzzle-outline.png','icons_mockup/puzzle.png','icons_mockup/radar-outline.png','icons_mockup/radar.png','icons_mockup/refresh-outline.png',
		'icons_mockup/refresh.png','icons_mockup/rss-outline.png','icons_mockup/rss.png','icons_mockup/scissors-outline.png','icons_mockup/scissors.png','icons_mockup/shopping-bag.png','icons_mockup/shopping-cart.png',
		'icons_mockup/social-at-circular.png','icons_mockup/social-dribbble-circular.png','icons_mockup/social-dribbble.png','icons_mockup/social-facebook-circular.png','icons_mockup/social-facebook.png',
		'icons_mockup/social-flickr-circular.png','icons_mockup/social-flickr.png','icons_mockup/social-github-circular.png','icons_mockup/social-github.png','icons_mockup/social-last-fm-circular.png',
		'icons_mockup/social-last-fm.png','icons_mockup/social-linkedin-circular.png','icons_mockup/social-linkedin.png','icons_mockup/social-pinterest-circular.png','icons_mockup/social-pinterest.png',
		'icons_mockup/social-skype-outline.png','icons_mockup/social-skype.png','icons_mockup/social-tumbler-circular.png','icons_mockup/social-tumbler.png','icons_mockup/social-twitter-circular.png','icons_mockup/social-twitter.png',
		'icons_mockup/social-vimeo-circular.png','icons_mockup/social-vimeo.png','icons_mockup/sort-alphabetically-outline.png','icons_mockup/sort-alphabetically.png','icons_mockup/sort-numerically-outline.png',
		'icons_mockup/sort-numerically.png','icons_mockup/spanner-outline.png','icons_mockup/spanner.png','icons_mockup/starburst-outline.png','icons_mockup/starburst.png','icons_mockup/star-outline.png',
		'icons_mockup/star.png','icons_mockup/stopwatch.png','icons_mockup/support.png','icons_mockup/tabs-outline.png','icons_mockup/tag.png','icons_mockup/tags.png','icons_mockup/thermometer.png','icons_mockup/th-large-outline.png',
		'icons_mockup/th-large.png','icons_mockup/th-list-outline.png','icons_mockup/th-list.png','icons_mockup/th-menu-outline.png','icons_mockup/th-menu.png','icons_mockup/th-small-outline.png','icons_mockup/th-small.png',
		'icons_mockup/thumbs-down.png','icons_mockup/thumbs-up.png','icons_mockup/ticket.png','icons_mockup/tick-outline.png','icons_mockup/tick.png','icons_mockup/time.png','icons_mockup/times-outline.png','icons_mockup/times.png',
		'icons_mockup/trash.png','icons_mockup/tree.png','icons_mockup/upload-outline.png','icons_mockup/upload.png','icons_mockup/user-add-outline.png','icons_mockup/user-add.png','icons_mockup/user-delete-outline.png',
		'icons_mockup/user-delete.png','icons_mockup/user-outline.png','icons_mockup/user.png','icons_mockup/video-outline.png','icons_mockup/video.png','icons_mockup/volume-down.png','icons_mockup/volume-mute.png','icons_mockup/volume.png',
		'icons_mockup/volume-up.png','icons_mockup/warning-outline.png','icons_mockup/warning.png','icons_mockup/watch.png','icons_mockup/waves-outline.png','icons_mockup/waves.png','icons_mockup/weather-cloudy.png',
		'icons_mockup/weather-downpour.png','icons_mockup/weather-night.png','icons_mockup/weather-partly-sunny.png','icons_mockup/weather-shower.png','icons_mockup/weather-snow.png','icons_mockup/weather-stormy.png',
		'icons_mockup/weather-sunny.png','icons_mockup/weather-windy-cloudy.png','icons_mockup/weather-windy.png','icons_mockup/wi-fi-outline.png','icons_mockup/wi-fi.png','icons_mockup/wine.png','icons_mockup/world-outline.png',
		'icons_mockup/world.png','icons_mockup/zoom-in-outline.png','icons_mockup/zoom-in.png','icons_mockup/zoom-outline.png','icons_mockup/zoom-out-outline.png','icons_mockup/zoom-out.png','icons_mockup/zoom.png']
		for name in self.images_l:
			bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
			il_max = il.Add(bmp)

		# create the list control
		self.list = wx.ListCtrl(self, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE)

		# assign the image list to it
		self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

		# create some items for the list
		for x in range(308):
			img = x % (il_max+1)
			self.list.InsertImageStringItem(x, "Image " + str(x), img)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListBox, self.list)

		self.lista_imagenes = []

	def onListBox(self,evt):
		item = evt.GetItem()
		i = int(str(item.GetText()).replace("Image ",""))
		self.lista_imagenes.append(self.images_l[i])
		self.parent.image_selected = self.lista_imagenes

class Dialog_icon_resize(wx.Dialog):
	
	def __init__(self, parent, title, img):
		super(Dialog_icon_resize, self).__init__(parent, title=title,size=(180,100))
		self.parent = parent
		self.img = img
		wx.StaticText(self,-1,'Size:',pos=(10,10),size=(50,30))
		
		tam = ['24','48','96','196']

		self.size_cbo_img = wx.ComboBox(self, -1, value="24", pos=(60,5),size=(100,30), choices=tam)

		btn = wx.Button(self,-1,'Aceptar',pos=(60,40))

		btn.Bind(wx.EVT_BUTTON,self.size)

	def size(self,evt):
		s = self.size_cbo_img.GetValue()
		self.parent.modify_size_bitmap(self.img,s)
		self.Destroy()

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
		for data in self.parent.diccionario:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])

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
		for data in self.parent.diccionario:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])

class Dialog_text_edit(wx.Dialog):
	
	def __init__(self, parent, title):
		super(Dialog_text_edit, self).__init__(parent, title=title,size=(240,200))
		self.parent = parent

		self.texto = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_MULTILINE , size=(220,120), pos=(10,10))
		
		aceptar = wx.Button( self, wx.ID_ANY, u"Aceptar",pos=(10,140))

		aceptar.Bind(wx.EVT_BUTTON,self.text)

		self.label_content()

	def text(self,evt):
		r = self.texto.GetValue()
		
		self.parent.modify_label(r,10,self.type_shape)
		self.Destroy()

	def label_content(self):
		id_shape = self.parent.shape_selected.GetId()
		self.type_shape = ''
		for data in self.parent.diccionario:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])

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
		for data in self.parent.diccionario:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])

class Dialog_widget_edit(wx.Dialog):
	def __init__(self, parent, title):
		super(Dialog_widget_edit, self).__init__(parent, title=title,size=(240,120))
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
		for data in self.parent.diccionario:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[3]))
				type_shape = str(data[2])

app = wx.App()
ogl.OGLInitialize()
MyMockup(None)
app.MainLoop()