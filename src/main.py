#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl
import random
import wx.lib.imagebrowser as imagebrowser
import sys, glob, os
import os.path
from subprocess import PIPE, Popen
import json

from canvas import Canvas
from handler import MyEvtHandler

from widgets.label import *
from widgets.link import *
from widgets.text import *
from widgets.button import *
from widgets.radiocheck import *
from widgets.combospin import *
from widgets.frame import *
from widgets.search import *
from widgets.slider import *
from widgets.accordion import *
from widgets.progressbar import *
from widgets.tooltip import *
from widgets.scrollbar import *
from widgets.tab import *

class MyMockup(wx.Frame):

	# list all shapes
	list_shape = []

	# shape selected now
	shape_selected = None

	# List data shapes
	diccionary_shapes_info = []

	# Filename export, if '' not export
	file_name_export = ''

	# id shape selected now
	_id_shape = None

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent,size = wx.Size( 790,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		favicon = wx.Icon('icons/logo.png',wx.BITMAP_TYPE_ICO, 16,16)
		self.SetIcon(favicon)
		self.Centre( wx.BOTH )
		self.Show()
		self.SetTitle('MyMockup')
		self.toolbar()
		self.menu()
		self.gui()
		
	def toolbar(self):
		self.toolbar = self.CreateToolBar()

		new_d = self.toolbar.AddLabelTool(-1, "tool", wx.Bitmap( u"icons/document.png"), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"New document")
		open_d = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/folder.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Open project")
		save_d = self.toolbar.AddLabelTool(-1, "tool", wx.Bitmap( u"icons/save.png"), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Save project")
		export = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/export.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Export to image")
		self.toolbar.AddSeparator()
		
		bring_to_front = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/bring_to_front.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"bring to front")
		bring_forward = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/bring_forward.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"bring forward")
		send_backward = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/send_backward.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"send backward")
		send_to_back = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/send_to_back.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"send to back")
		self.toolbar.AddSeparator()

		duplicate = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/popup.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Duplicate")
		image = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/image.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Image collection")
		trash = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/trash.png'), 
			wx.NullBitmap, wx.ITEM_NORMAL, u"Delete")
		self.toolbar.AddSeparator()
		
		label_x = wx.StaticText( self.toolbar, wx.ID_ANY, u"  X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.toolbar.AddControl( label_x )
		self.pos_X = wx.SpinCtrl( self.toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		self.toolbar.AddControl( self.pos_X )
		label_Y = wx.StaticText( self.toolbar, wx.ID_ANY, u"  Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.toolbar.AddControl( label_Y )
		self.pos_Y = wx.SpinCtrl( self.toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		self.toolbar.AddControl( self.pos_Y )
		self.toolbar.AddSeparator()

		lblw = wx.StaticText( self.toolbar, wx.ID_ANY, u"  Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.toolbar.AddControl( lblw )
		self.width_shape = wx.SpinCtrl( self.toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		self.toolbar.AddControl( self.width_shape )
		lblh = wx.StaticText( self.toolbar, wx.ID_ANY, u"  Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.toolbar.AddControl( lblh )
		self.height_shape = wx.SpinCtrl( self.toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 500, 0 )
		self.toolbar.AddControl( self.height_shape )

		self.toolbar.Realize()

		self.Bind(wx.EVT_TOOL, self.new_document, new_d)
		self.Bind(wx.EVT_TOOL, self.open_document, open_d)
		self.Bind(wx.EVT_TOOL, self.save_document, save_d)
		self.Bind(wx.EVT_TOOL, self.export, export)

		self.Bind(wx.EVT_TOOL,self.bring_to_front,bring_to_front)
		self.Bind(wx.EVT_TOOL,self.bring_forward,bring_forward)
		self.Bind(wx.EVT_TOOL,self.send_backward,send_backward)
		self.Bind(wx.EVT_TOOL,self.send_to_back,send_to_back)

		self.Bind(wx.EVT_TOOL,self.image_collection,image)
		self.Bind(wx.EVT_TOOL,self.delete_shape,trash)

		self.pos_X.Bind(wx.EVT_SPINCTRL, self.function_position_shape_x)
		self.pos_Y.Bind(wx.EVT_SPINCTRL, self.function_position_shape_y)
		self.width_shape.Bind(wx.EVT_SPINCTRL, self.function_size_shape_x)
		self.height_shape.Bind(wx.EVT_SPINCTRL, self.function_size_shape_y)

	def menu(self):
		"""
		Genera los menus que se necesitan en la pantalla
		"""
		menuBar = wx.MenuBar()

		# Menu de archivo
		archivo = wx.Menu()
		guardar		= archivo.Append(wx.ID_SAVE,'Guardar')
		new			= archivo.Append(wx.ID_NEW,'New')
		abrir 		= archivo.Append(wx.ID_OPEN,'Abrir')
		exportar 	= archivo.Append(-1,'Exportar')
		salir 		= archivo.Append(wx.ID_EXIT,'Salir')

		# Menu de Editar
		ver = wx.Menu()
		lista_shape = ver.Append(-1,'Lista de shapes')

		# Menu de shapes
		shapes = wx.Menu()
		circle 		= shapes.Append(-1, "Circulo")
		rectangle 	= shapes.Append(-1, "Rectangulo")

		# Menu de ayuda
		ayuda 		= wx.Menu()
		#helpm 		= ayuda.Append(wx.ID_HELP,'Ayuda')
		about 		= ayuda.Append(-1,'Acerca de')
		
		#Agregar los menus a la barra de menu
		menuBar.Append(archivo, "Archivo")
		menuBar.Append(ver, "Ver")
		menuBar.Append(shapes, "Shapes")
		menuBar.Append(ayuda, "Ayuda")
		
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.circle, circle)
		self.Bind(wx.EVT_MENU, self.rectangle, rectangle)

		self.Bind(wx.EVT_MENU, self.shapes_view, lista_shape)
		self.Bind(wx.EVT_MENU, self.OnAboutBox, about)

	def gui(self):
		p = wx.Panel(self)
		hsizer = wx.BoxSizer( wx.HORIZONTAL )
		
		flexigrid = wx.FlexGridSizer( 0, 3, 0, 0 )
		flexigrid.SetFlexibleDirection( wx.BOTH )
		flexigrid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		w_texto = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_text.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_texto, 0, wx.ALL, 1 )
		
		w_label = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_label.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_label, 0, wx.ALL, 1 )
		
		w_link = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_link.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_link, 0, wx.ALL, 1 )

		w_button = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_button.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_button, 0, wx.ALL, 1 )

		w_icon_checkbox_checked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_checkbox_checked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_icon_checkbox_checked, 0, wx.ALL, 1 )
		
		w_icon_checkbox_unchecked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_checkbox_unchecked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_icon_checkbox_unchecked, 0, wx.ALL, 1 )
		
		w_radio_checked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_radio_checked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_radio_checked, 0, wx.ALL, 1 )
		
		w_radio_unchecked = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_radio_unchecked.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_radio_unchecked, 0, wx.ALL, 1 )

		w_textfield = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_textfield.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_textfield, 0, wx.ALL, 1 )

		w_combobox = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_combobox.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_combobox, 0, wx.ALL, 1 )

		w_spinner = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_spinner.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_spinner, 0, wx.ALL, 1 )

		w_windows = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_window.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_windows, 0, wx.ALL, 1 )

		w_image = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_image.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_image, 0, wx.ALL, 1 )

		w_search = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_search.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_search, 0, wx.ALL, 1 )

		w_scale = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_scale.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_scale, 0, wx.ALL, 1 )

		w_accordeon = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_accordion.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_accordeon, 0, wx.ALL, 1 )

		w_tab = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_tab.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_tab, 0, wx.ALL, 1 )

		w_popup = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_popup.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_popup, 0, wx.ALL, 1 )

		w_progress = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_progress.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_progress, 0, wx.ALL, 1 )

		w_scroll = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_scrollbar.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_scroll, 0, wx.ALL, 1 )

		w_three = wx.BitmapButton( p, wx.ID_ANY, wx.Bitmap( u"icons/icon_three.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		flexigrid.Add( w_three, 0, wx.ALL, 1 )
		
		
		hsizer.Add( flexigrid, 0, wx.EXPAND, 5 )

		# --------------------------------------------------------
		self.canvas = Canvas( p )
		hsizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )

		self.diagram = ogl.Diagram()
		self.canvas.SetDiagram( self.diagram )
		self.diagram.SetCanvas( self.canvas )

		# --------------------------------------------------------
		p.SetSizer( hsizer )

		# --------------------------------------------------------
		# Binds
		w_texto.Bind(wx.EVT_BUTTON,self.draw_w_text)
		w_label.Bind(wx.EVT_BUTTON,self.draw_w_label)
		w_link.Bind(wx.EVT_BUTTON,self.draw_w_link)
		w_button.Bind(wx.EVT_BUTTON,self.draw_w_button)
		w_textfield.Bind(wx.EVT_BUTTON,self.draw_w_textfield)
		w_icon_checkbox_checked.Bind(wx.EVT_BUTTON,self.drawn_checkbox_checked)
		w_icon_checkbox_unchecked.Bind(wx.EVT_BUTTON,self.drawn_checkbox_unchecked)
		w_radio_checked.Bind(wx.EVT_BUTTON,self.draw_radiobuttonchecked)
		w_radio_unchecked.Bind(wx.EVT_BUTTON,self.draw_radiobuttonunchecked)
		w_combobox.Bind(wx.EVT_BUTTON,self.draw_combobox)
		w_spinner.Bind(wx.EVT_BUTTON,self.draw_spinner)
		w_windows.Bind(wx.EVT_BUTTON,self.draw_w_frame)
		w_image.Bind(wx.EVT_BUTTON,self.draw_image)
		w_search.Bind(wx.EVT_BUTTON,self.draw_search)
		w_scale.Bind(wx.EVT_BUTTON,self.draw_slider)
		w_accordeon.Bind(wx.EVT_BUTTON,self.draw_accordeon)
		w_three.Bind(wx.EVT_BUTTON,self.draw_three)
		w_popup.Bind(wx.EVT_BUTTON,self.draw_tooltip)
		w_progress.Bind(wx.EVT_BUTTON,self.draw_progress)
		w_scroll.Bind(wx.EVT_BUTTON,self.draw_scrollbar)
		w_tab.Bind(wx.EVT_BUTTON,self.draw_tab)

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyEvent)

	def onKeyEvent(self,evt):
		if evt.GetKeyCode() ==  wx.WXK_ESCAPE:
			print('scape')
		elif evt.GetKeyCode() ==  wx.WXK_DELETE:
			if self.shape_selected != None:
				self.delete_shape()
		evt.Skip()

	#===============================#
	#			Files				#
	#===============================#

	def file_content(self,filename):
		self.print_diccionary_contents()
		
		data_json = {}
		data_list = []

		for row in self.diccionary_shapes_info:
			data = {}
			shape = row[0]
			data['Type'] 	= row[2]
			data['Id'] 		= row[1]
			data['Y'] 		= shape.GetX()
			data['X'] 		= shape.GetX()
			data['Heigth'] 	= shape.GetHeight()
			data['Width'] 	= shape.GetWidth()
			data['Content']	= row[3]
			data['extra'] 	= row[4]
			
			data_list.append(data)

		json_data = json.dumps(data_list)
		data_json['shape'] = json.loads(json_data)

		try:
			json_data = json.dumps(data_json)
			decoded = json.loads(json_data)

			with open(filename, 'w') as outfile:
				json.dump(decoded, outfile)
		except Exception as e:
			print(e)

	def read_content(self,filename):
		with open(filename, "r+") as archivo:
			contenido = archivo.read()

		#encoded
		data_string = json.dumps(contenido)

		#Decoded
		decoded = json.loads(data_string)

		self._create_shapes_since_file(decoded)
	
	def export_image(self,ruta,w,h):#Mejorar
		self.statbmp = wx.StaticBitmap(self)

		draw_bmp = wx.EmptyBitmap(w, h)
		dc = wx.MemoryDC(draw_bmp)
		dc.Clear()
		
		self.canvas.GetDiagram().Redraw(dc)
		self.statbmp.SetBitmap(draw_bmp)
		finished_image = self.statbmp.GetBitmap()
		finished_image.SaveFile(ruta, wx.BITMAP_TYPE_PNG)

	def _create_shapes_since_file(self,data):
		item_dict = json.loads(data)
		n = len(item_dict['shape'])

		for i in range(0,n):
			height  	= item_dict['shape'][i]['Heigth']
			width 		= item_dict['shape'][i]['Width']
			x 			= item_dict['shape'][i]['X']
			y 			= item_dict['shape'][i]['Y']
			typeshape 	= item_dict['shape'][i]['Type']
			idshape 	= item_dict['shape'][i]['Id']
			extra 		= item_dict['shape'][i]['extra']
			content 	= item_dict['shape'][i]['Content']

			if typeshape == 'Acordeon' or typeshape == 'Tab':
				array = content.values()
			else:
				array = content

			self._create_shape(idshape,height,width,x,y,typeshape,array,extra)

	def _create_shape(self,Id,Height,Width,X,Y,type_s,content,extra=None):
		if type_s == 'Link':
			shape = ogl.TextShape(float(Width), float(Height))
			shape.SetTextColour('BLUE')
		elif type_s == 'Label':
			shape = ogl.TextShape(float(Width), float(Height))
		elif type_s == 'Text' or type_s == 'Tree':
			shape = ogl.TextShape(float(Width), float(Height))
		elif type_s == 'Circle':
			shape = ogl.CircleShape( float(Width) )
			shape.SetPen(wx.BLACK_PEN)
		elif type_s == 'Rectangle':
			shape = ogl.RectangleShape(float(Width), float(Height))
			shape.SetPen(wx.BLACK_PEN)
		elif type_s == 'Button':
			shape = ogl.RectangleShape(float(Width), float(Height))
			shape.SetPen(wx.BLACK_PEN)
			shape.AddText(content)
			shape.SetCornerRadius(5)
		elif type_s == 'CheckBox' or type_s == 'RadioButton':
			shape = RadioCheck(self.canvas,content)
			shape.ClearText()
			shape.AddText(extra)
			shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.Recentre(dc)
		elif type_s == 'ComboBox' or type_s == 'Spinner':
			shape = ComboSpin(self.canvas,content)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Frame':
			shape = Frame(self.canvas)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Search':
			shape = ShapeSearch(self.canvas)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Progress':
			shape = ProgressBar(self.canvas)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Scroolbar':
			shape = ScrollBar(self.canvas)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Tooltip':
			shape = Tooltip()
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Acordeon':
			shape = Accordion(100,220,self.canvas,content,extra)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Tab':
			shape = Tab(content,extra)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Scroolbar':
			shape = ScrollBar(self.canvas)
			shape.SetFixedSize(False,20)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Progress':
			shape = ProgressBar(self.canvas)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.SetDraggable(True)
		elif type_s == 'Image':
			if os.path.exists(content) == False:
				wx.MessageBox('La imagen: '+content+' No existe','Error',wx.OK | wx.ICON_ERROR)
				content = 'icons/noimage.png'
			shape = ogl.BitmapShape()
			shape.SetBitmap(wx.Bitmap(content,wx.BITMAP_TYPE_ANY))
		elif type_s == 'TextField':
			shape = ogl.RectangleShape(float(Width), float(Height))
			shape.SetPen(wx.BLACK_PEN)
			shape.SetCornerRadius(5)
			
		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		if type_s == 'Label' or type_s == 'Link' or type_s == 'Text':
			shape.AddText(content)
			shape.SetFont(wx.Font(int(extra), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
			
			shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
			dc = wx.ClientDC(self)
			shape.Move(dc, float(X), float(Y))
			shape.Recentre(dc)
		else:
			shape.SetX( float(X) )
			shape.SetY( float(Y) )

		shape.SetId(int(Id))
		shape.SetCentreResize(False)

		shape.GetCanvas().Refresh(True)

		# Add shape to list
		self.list_shape.append(shape)

		# Add shape to diccionary
		self._add_shape_to_diccionary(shape,int(Id),type_s,content,extra,None)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	#===============================#
	#			Menus				#
	#===============================#
	
	def new_document(self,evt):
		response = wx.MessageBox("Save changes before?","Confirm", wx.YES_NO | wx.CANCEL, self)
		if response == wx.YES:
			self.save_document()
		elif response == wx.NO:
			self.diagram.RemoveAllShapes()
			self.canvas.Refresh(True)
			self.diccionary_shapes_info = []
			self.list_shape = []
		elif response == wx.CANCEL:
			pass
	
	def open_document(self,evt):#Mejorar
		curDir = os.getcwd()

		fileName = wx.FileSelector("Open file", "Open",
			default_filename='',
			default_extension="mmp",
			wildcard="*.mmp",
			flags = wx.OPEN | wx.OVERWRITE_PROMPT)

		if fileName != "":
			fileName = os.path.join(os.getcwd(), fileName)
			os.chdir(curDir)
			self.read_content(fileName)

			title = os.path.basename(fileName)
			self.SetTitle(title)

	def save_document(self,evt=None):#Mejorar
		curDir = os.getcwd()

		fileName = wx.FileSelector("Save File As", "Saving",
			default_filename='default',
			default_extension="mmp",
			wildcard="*.mmp",
			flags = wx.SAVE | wx.OVERWRITE_PROMPT)

		if fileName != "":
			self.file_content(fileName)
			fileName = os.path.join(os.getcwd(), fileName)
			os.chdir(curDir)

			title = os.path.basename(fileName)
			self.SetTitle(title)
	
	def export(self,evt):
		dialog = Dialog_export_image(self,'Export')
		result = dialog.ShowModal()
        	
	#===============================#
	#		Draw elements			#
	#===============================#
	
	def draw_w_label(self,evt):
		text = 'Label'
		shape = ogl.TextShape(60, 30)
		shape.AddText('Label')
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
		shape.SetFixedSize(False,30)

		self._shape_to_handler(shape,'Label','Label',10,'-')

	def draw_w_link(self,evt):
		text = 'Link'
		shape = ogl.TextShape(60, 30)
		shape.AddText('Link')
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)
		shape.SetTextColour('BLUE')

		self._shape_to_handler(shape,'Link','Link',10,'')

	def draw_w_text(self,evt):
		text = 'Lorem ipsum dolor sit amet,\nconsectetur adipisicing.\nIllum ad expedita repudiandae.'
		shape = ogl.TextShape(210, 55)
		shape.AddText(text)
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)

		self._shape_to_handler(shape,'Text',text,10,'')

	def draw_w_button(self,evt):
		text = 'Button'
		shape = ogl.RectangleShape(100, 30)
		shape.AddText(text)
		shape.SetCornerRadius(5)
		shape.SetPen(wx.BLACK_PEN)

		self._shape_to_handler(shape,'Button','Button',10,'')

	def drawn_checkbox_checked(self,evt):
		self.draw_radio_and_check('CheckBox','icons/checkboxchecked.png','CheckBox')

	def drawn_checkbox_unchecked(self,evt):
		self.draw_radio_and_check('CheckBox','icons/checkboxunchecked.png','CheckBox')

	def draw_radiobuttonchecked(self,evt):
		self.draw_radio_and_check('RadioButton','icons/radiobuttonchecked.png','RadioButton')

	def draw_radiobuttonunchecked(self,evt):
		self.draw_radio_and_check('RadioButton','icons/radiobuttonunchecked.png','RadioButton')

	def draw_w_textfield(self,evt):
		shape = ogl.RectangleShape(100, 30)
		shape.SetCornerRadius(5)
		shape.SetFixedSize(False,30)
		shape.SetPen(wx.BLACK_PEN)

		self._shape_to_handler(shape,'TextField','','','')

	def draw_combobox(self,evt):
		self.ShapeComboSpin('ComboBox','icons/combo.png')

	def draw_spinner(self,evt):
		self.ShapeComboSpin('Spinner','icons/spinner.png')

	def ShapeComboSpin(self,type_shape,img):
		shape = ComboSpin(self.canvas,img)
		shape.SetFixedSize(False,30)

		self._shape_to_handler(shape,type_shape,img,'','-')

	def draw_radio_and_check(self,text,img,type_shape):
		shape = RadioCheck(self.canvas,img)
		shape.ClearText()
		shape.AddText(text)
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self._shape_to_handler(shape,type_shape,img,text,'-')

	def draw_w_frame(self,evt):
		shape = Frame(self.canvas)
		shape.SetFixedSize(False,30)
		self._shape_to_handler(shape,'Frame','','','-')

	def draw_image(self,evt):
		dialog = imagebrowser.ImageDialog(None)   
		if dialog.ShowModal() == wx.ID_OK: 
			shape = ogl.BitmapShape()
			img = str(dialog.GetFile())
			shape.SetBitmap(wx.Bitmap(img,wx.BITMAP_TYPE_ANY))

			self._shape_to_handler(shape,'Image',img,'','')
		dialog.Destroy()

	def draw_search(self,evt):
		shape = ShapeSearch(self.canvas)
		self._shape_to_handler(shape,'Search','-','-','-')

	def draw_slider(self,evt):
		shape = Slider(self.canvas,'icons/circle.png')
		self._shape_to_handler(shape,'Search','-','-','-')

	def draw_accordeon(self,evt=None,item = '', lista = None,recursive=True):
		if recursive != False:
			dialog = Accordion_dialog(self,'Acordeon').ShowModal()
		else:
			shape = Accordion(100,220,self.canvas,lista,item)
			self._shape_to_handler(shape,'Acordeon',lista,item,'-')

	def draw_progress(self,evt):
		shape = ProgressBar(self.canvas)
		self._shape_to_handler(shape,'Progress','-','-','-')

	def draw_three(self,evt):
		text = '|-Item 1\n|----Item 1.1\n|----Item 1.2\n|-Item 2\n|----Item 2.1\n|----Item 3.2\n|------Item 3.2.1\n|------Item 3.2.2\n|-Item 3'

		shape = ogl.TextShape(110, 120)
		shape.AddText(text)
		shape.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		shape.SetFormatMode(ogl.FORMAT_SIZE_TO_CONTENTS)

		self._shape_to_handler(shape,'Tree',text,10,'-')

	def draw_tooltip(self,evt):
		shape = Tooltip()
		self._shape_to_handler(shape,'Tooltip','-','-','-')

	def draw_scrollbar(self,evt):
		shape = ScrollBar(self.canvas)
		shape.SetFixedSize(False,20)
		
		self._shape_to_handler(shape,'Scroolbar','-','-','-')

	def draw_tab(self,evt=None,item = '', lista = None,recursive=True):
		if recursive != False:
			dialog = Tab_dialog(self,'Tab').ShowModal()
		else:
			shape = Tab(lista,item)
			self._shape_to_handler(shape,'Tab',lista,item,'-')

	#===============================#
	#		Basic shapes			#
	#===============================#
	
	def circle(self,evt):
		shape = ogl.CircleShape( 20.0 )
		self._shape_to_handler(shape,'Circle','-','-','-')

	def rectangle(self,evt):
		shape = ogl.RectangleShape(100, 100)
		self._shape_to_handler(shape,'Rectangle','-','-','-')

	#===============================#
	#		Other functions			#
	#===============================#
	
	def delete_shape(self,evt = None):#mejorar
		if self.shape_selected != None:
			self.canvas.RemoveShape(self.shape_selected)
			self.canvas.Refresh(True)
			self.list_shape.remove(self.shape_selected)
		
			dc = wx.ClientDC(self.canvas)
			self.canvas.PrepareDC(dc)
			self.shape_selected.Select(False, dc)

			i = 0
			for row in self.diccionary_shapes_info:
				if row[1] == self.shape_selected.GetId():
					self.diccionary_shapes_info.pop(i)
			
			self.shape_selected = None
		
			self._redraw()
			self.canvas.Refresh(True)

	def image_collection(self,evt=None, recursive = False, data = None):
		if recursive == False:
			r = Dialog_image_collection(self).ShowModal()
		else:
			for x in data:
				self.image_duplicate(str(x))
			
	def double_click(self,shape):
		print(shape)
		if str(shape).count("BitmapShape") == True:
			img = self.get_content_diccionary(self.shape_selected,'content')
			dialog = Dialog_icon_resize(self,'size',img)
			result = dialog.ShowModal()
		elif str(shape).count("TextShape") == True:
			if self.get_content_diccionary(shape,'type') == 'Label':
				dialog = Dialog_label_edit(self,'LabelEdit')
				result = dialog.ShowModal()
			elif self.get_content_diccionary(shape,'type') == 'Link':
				dialog = Dialog_link_edit(self,'LinkEdit')
				result = dialog.ShowModal()
			elif self.get_content_diccionary(shape,'type') == 'Text' or self.get_content_diccionary(shape,'type') == 'Tree':
				dialog = Dialog_text_edit(self,'TextEdit')
				result = dialog.ShowModal()
		elif str(shape).count("RectangleShape") == True:
			if self.get_content_diccionary(shape,'type') == 'Button':
				dialog = Dialog_button_edit(self,'ButtonEdit')
				result = dialog.ShowModal()
		elif str(shape).count("RadioCheck") == True:
			img = self.get_content_diccionary(shape,'content')
			dialog = Dialog_widget_edit(self,'Edit',img)
			result = dialog.ShowModal()
	
	def update_shape_selected(self,id_f):
		for row in self.list_shape:
			id_shape = row.GetId()
			if row.GetId() == int(id_f):
				dc = wx.ClientDC(self)
				self.canvas.PrepareDC(dc)
				self.shape_selected.Select(False, dc)
				self.shape_selected = row
				self.shape_selected.Select(True, dc)
				self.shape_selected.SetDraggable(True)

				evthandler = MyEvtHandler(self)
				evthandler.SetShape(self.shape_selected)
				evthandler.SetPreviousHandler(self.shape_selected.GetEventHandler())
				self.shape_selected.SetEventHandler(evthandler)

	def image_duplicate(self,img):
		shape = ogl.BitmapShape()
		shape.SetBitmap(wx.Bitmap(img,wx.BITMAP_TYPE_ANY))

		self._shape_to_handler(shape,'Image',img,'','')

	def modify_size_bitmap(self,img,size):
		bitmap = wx.Bitmap(img)
		img = self.scale_bitmap(bitmap,int(size),int(size))
		self.shape_selected.SetBitmap(self.scale_bitmap(bitmap,int(size),int(size)))
		self.shape_selected.SetWidth(int(size))
		self.shape_selected.SetHeight(int(size))
		self.shape_selected.GetCanvas().Refresh(True)

	def scale_bitmap(self,bitmap, width, height):
		image = wx.ImageFromBitmap(bitmap)
		image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
		result = wx.BitmapFromImage(image)
		return result
	
	def OnAboutBox(self,evt):
		description = "MyMockup\n Diseñador de mockups experimental, no apto para\n"
		description = description + "Produccion, por su pobre rendimiento, y errores menores.\n"
		description = description + "Fue escrito en wxpython y la libreria OGL, por lo que no es\n"
		description = description + "muy estable, presenta ciertos errores para mover objetos.\n"
		description = description + "No selecciona multiples elementos, defecto grave."

		licence = "Esta biblioteca es software libre; puede redistribuirla\ny/o modificarla bajo los términos de la\n"
		licence = licence + "Licencia Pública General Reducida de GNU tal como la publica la\n"
		licence = licence + "Free SoftwareFoundation; ya sea la versión 2.1 de la licencia o \n"
		licence = licence + "(según su criterio) cualquier versión posterior."

		info = wx.AboutDialogInfo()

		info.SetIcon(wx.Icon('icons/logo_64x64.png', wx.BITMAP_TYPE_PNG))
		info.SetName('MyMockup')
		info.SetVersion('0.2')
		info.SetDescription(description)
		info.SetCopyright('(C) 2006 - 2016 JC')
		info.SetWebSite('http://www.pacpac1992.github.io')
		info.SetLicence(licence)
		info.AddDeveloper('JC')
		info.AddDocWriter('JC')
		info.AddArtist('Iconos de flaticons')
		info.AddTranslator('-----')

		wx.AboutBox(info)

	#===============================#
	#		Order shapes			#
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
					if position != 0:
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

	#=======================================#
	#			Position and size 			#
	#=======================================#
	
	def function_position_shape_x(self,evt):
		h, w = 0, 0
		if self.shape_selected != None:
			h = self.shape_selected.GetHeight() / 2
			w = self.shape_selected.GetWidth() / 2

		if str(self.shape_selected).count('CompositeShape') > 0:
			dc = wx.ClientDC(self)
			px = self.pos_X.GetValue()
			py = self.pos_Y.GetValue()
			self.shape_selected.Move(dc, px, py)
			self.shape_selected.GetCanvas().Refresh(True)
		else:
			self.shape_selected.SetX(self.pos_X.GetValue() + w)
			self.canvas.Refresh(True)

	def function_position_shape_y(self,evt):
		h, w = 0, 0
		if self.shape_selected != None:
			h = self.shape_selected.GetHeight() / 2
			w = self.shape_selected.GetWidth() / 2

		if str(self.shape_selected).count('CompositeShape') > 0:
			dc = wx.ClientDC(self)
			px = self.pos_X.GetValue()
			py = self.pos_Y.GetValue()
			self.shape_selected.Move(dc, px, py)
			self.shape_selected.GetCanvas().Refresh(True)
		else:
			self.shape_selected.SetY(self.pos_Y.GetValue() + h)
			self.canvas.Refresh(True)
	
	def function_size_shape_x(self,evt):
		if str(self.shape_selected).count('CompositeShape') > 0:
			self.shape_selected.SetSize(self.width_shape.GetValue(), self.height_shape.GetValue())
			self.shape_selected.GetCanvas().Refresh(True)
		else:
			self.shape_selected.SetWidth(self.width_shape.GetValue())
			self.canvas.Refresh(True)

	def function_size_shape_y(self,evt):
		if str(self.shape_selected).count('CompositeShape') > 0:
			self.shape_selected.SetSize(self.width_shape.GetValue(), self.height_shape.GetValue())
			self.shape_selected.GetCanvas().Refresh(True)
		else:
			self.shape_selected.SetHeight(self.height_shape.GetValue())
			self.canvas.Refresh(True)

	#===============================#
	#		Shapes info				#
	#===============================#
	
	def shape_propierties(self,shape,x,y):
		self.shape_selected = shape
		if str(self.shape_selected).count('CompositeShape') == 0:
			self.pos_X.SetValue(x - (shape.GetWidth() / 2))
			self.pos_Y.SetValue(y - (shape.GetHeight() / 2))
		else:
			self.pos_X.SetValue(x)
			self.pos_Y.SetValue(y)

		self.width_shape.SetValue(shape.GetWidth())
		self.height_shape.SetValue(shape.GetHeight())

	def print_diccionary_contents(self,evt=None):
		i = 0
		for raw in self.list_shape:
			
			e = 0
			for row in self.diccionary_shapes_info:
				if raw.GetId() == row[1]:
					self.diccionary_shapes_info.pop(e)
					self.diccionary_shapes_info.insert(i,row)
				e = e + 1
			
			i = i + 1

	def modify_label(self,texto,h,shape=None):
		self.shape_selected.ClearText()
		self.shape_selected.AddText(texto)
		if str(h).isdigit():
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
		
		if str(self.shape_selected).count('CompositeShape') == 1:
			t = texto
			img = h
			self._search_and_modify_diccionary(self.shape_selected,'content',img,t)
		else:
			self._search_and_modify_diccionary(self.shape_selected,'content',texto,h)

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

		for row in self.diccionary_shapes_info:
			if row[1] == shape.GetId():
				dato = row[n]
		return dato

	#===============================#
	#		Private functions		#
	#===============================#
	
	def shapes_view(self,evt):
		dialog = List_Shapes_(self,'Listas').ShowModal()
	
	def _redraw(self):
		x = 0
		
		#for i in self.list_shape:
		#	self.canvas.RemoveShape(i)
		self.diagram.RemoveAllShapes()
		
		for e in self.list_shape:
			self.canvas.AddShape( e )
			self.diagram.ShowAll( 1 )
			
			if x > 0:
				e.SetDraggable(True)
			
			e.GetCanvas().Refresh(True)
			x = x + 1

	def _shape_to_handler(self,shape,type_s,content,extra,arg):
		if self._id_shape == None:
			shape.SetId(random.randint(10000,90000))
		else:
			shape.SetId(self._id_shape)

		self.canvas.AddShape( shape )
		self.diagram.ShowAll( 1 )

		if type_s != 'Button' or type_s != 'TextField' or type_s != 'Rectangle':
			dc = wx.ClientDC(self)
			shape.Move(dc, random.randint(10,500), random.randint(10,500))
		else:
			shape.SetX( random.randint(100,190) )
			shape.SetY( random.randint(100,190) )
		
		shape.SetCentreResize(False)

		shape.GetCanvas().Refresh(True)
		
		# Add shape to list
		self.list_shape.append(shape)

		# Add shape to diccionary
		self._add_shape_to_diccionary(shape,shape.GetId(),type_s,content,extra,arg)

		evthandler = MyEvtHandler(self)
		evthandler.SetShape(shape)
		evthandler.SetPreviousHandler(shape.GetEventHandler())
		shape.SetEventHandler(evthandler)

	def _add_shape_to_diccionary(self,shape,id_shape,type_shape,content,extra,arg):
		array = [shape,id_shape,type_shape,content,extra]
		self.diccionary_shapes_info.append(array)

	def _search_and_modify_diccionary(self,shape,atributo,contenido,extra=''):
		i = 0
		for row in self.diccionary_shapes_info:
			if row[1] == shape.GetId():
				if atributo == 'content':
					row[3] = contenido
					row[4] = extra
			i = i + 1


class List_Shapes_(wx.Dialog):
	
	def __init__(self, parent, title):
		super(List_Shapes_, self).__init__(parent, title=title,size=(150,350))
		self.parent = parent

		array = []
		for row in self.parent.diccionary_shapes_info:
			array.append(str(row[2]) + ' - ' + str(row[1]))

		self.listBox = wx.ListBox(self, -1, (220, 10), (90, 170), array, wx.LB_SINGLE)

		self.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBox)
		
		print(self.parent.diccionary_shapes_info)

	def onListBox(self,evt):
		objeto = evt.GetEventObject().GetStringSelection()
		array = objeto.split(' - ')
		self.parent.update_shape_selected(array[1])

class Dialog_image_collection(wx.Dialog):
	
	def __init__(self,parent):
		super(Dialog_image_collection, self).__init__(parent, size=(600,500))
		self.parent = parent
		il = wx.ImageList(24,24, True)
		self.images_l = self.file_lists()
		
		for name in self.images_l:
			bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
			il_max = il.Add(bmp)

		# create the list control
		self.list = wx.ListCtrl(self, -1, pos=(0,0), size=(600,390),style=wx.LC_ICON | wx.LC_AUTOARRANGE)

		# assign the image list to it
		self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

		# create some items for the list
		for x in range(308):
			img = x % (il_max+1)
			self.list.InsertImageStringItem(x, "Image " + str(x), img)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListBox, self.list)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.deselect, self.list)

		self.lista_imagenes = []

		self.aceptar = wx.Button(self,-1,'Aceptar',pos=(80,400))
		self.aceptar.Bind(wx.EVT_BUTTON,self.listar)

	def listar(self,evt):
		self.parent.image_collection(None,True,self.lista_imagenes)
		self.Destroy()

	def deselect(self,evt):
		item = evt.GetItem()
		i = int(str(item.GetText()).replace("Image ",""))
		self.lista_imagenes.remove(self.images_l[i])

	def onListBox(self,evt):
		item = evt.GetItem()
		i = int(str(item.GetText()).replace("Image ",""))
		self.lista_imagenes.append(self.images_l[i])

	def file_lists(self):
		ruta = os.getcwd()
		nueva_ruta = os.chdir(ruta + '/icons/icons')
		
		proceso = Popen(['ls'], stdout=PIPE, stderr=PIPE)
		error_encontrado = proceso.stderr.read()
		proceso.stderr.close()
		listado = proceso.stdout.read()
		proceso.stdout.close()
		ruta = os.chdir(ruta)

		if not error_encontrado:
			array = []
			listado = listado.rstrip('\n')
			for row in listado.split('\n'):
				array.append('icons/icons/' + str(row))
			return array
		else:
			return 'Error'

class Dialog_icon_resize(wx.Dialog):
	
	def __init__(self, parent, title, img):
		super(Dialog_icon_resize, self).__init__(parent, title=title,size=(180,100))
		self.parent = parent
		self.img = img
		wx.StaticText(self,-1,'Size:',pos=(10,10),size=(50,30))
		
		tam = ['24','48','96','196','256']

		self.size_cbo_img = wx.ComboBox(self, -1, value="24", pos=(60,5),size=(100,30), choices=tam)

		btn = wx.Button(self,-1,'Aceptar',pos=(60,40))

		btn.Bind(wx.EVT_BUTTON,self.size)

	def size(self,evt):
		s = self.size_cbo_img.GetValue()
		self.parent.modify_size_bitmap(self.img,s)
		self.Destroy()

class Dialog_export_image(wx.Dialog):
	def __init__(self, parent, title):
		super(Dialog_export_image, self).__init__(parent, title=title,size=(260,150))
		self.parent = parent
		self.fileName = ''

		self.txt_nombre = wx.TextCtrl(self,-1, pos=(10,10),size=(150,30))
		btn_files = wx.Button(self,-1,'File',pos=(170,10))

		wx.StaticText(self,-1,'Width',pos=(10,50),size=(50,30))
		self.width_shape = wx.SpinCtrl(self, -1, pos=(60,45), size=(50, -1))
		self.width_shape.SetRange(16,1000)
		self.width_shape.SetValue(100)

		wx.StaticText(self,-1,'Heigth',pos=(140,50),size=(50,30))
		self.height_shape = wx.SpinCtrl(self, -1, pos=(195,45),size=(50, -1))
		self.height_shape.SetRange(16,1000)
		self.height_shape.SetValue(100)

		btn = wx.Button(self,-1,'Exportar',pos=(10,80))

		btn_files.Bind(wx.EVT_BUTTON,self.file_route)
		btn.Bind(wx.EVT_BUTTON,self.export)
		
	def export(self,evt):
		if self.fileName != "":
			self.parent.export_image(self.fileName,self.width_shape.GetValue(),self.height_shape.GetValue())
			self.Destroy()

	def file_route(self,evt):
		curDir = os.getcwd()

		self.fileName = wx.FileSelector("Export", "Export",
			default_filename='mockup',
			default_extension="png",
			wildcard="*.png",
			flags = wx.SAVE | wx.OVERWRITE_PROMPT)
		
		if self.fileName != "":
			self.fileName = os.path.join(os.getcwd(), self.fileName)
			os.chdir(curDir)
			self.txt_nombre.SetValue(self.fileName)

class ExceptionHandler:
	def __init__(self):
		self._buff = ""
		if os.path.exists("errors.txt"):
			os.remove("errors.txt")


	def write(self, s):
		if (s[-1] != "\n") and (s[-1] != "\r"):
			self._buff = self._buff + s
			return

		try:
			s = self._buff + s
			self._buff = ""

			f = open("errors.txt", "a")
			f.write(s)
			f.close()

			if s[:9] == "Traceback":
				wx.MessageBox("An internal error has occurred.\nPlease " + \
					"refer to the 'errors.txt' file for details.",
					"Error", wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)

		except:
			pass

#----------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		global _docList
		_docList = []

		ogl.OGLInitialize()

		bmp = wx.Image("icons/splash.png").ConvertToBitmap()
		wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,1000, None, -1)
		wx.Yield()

		frame = MyMockup(None)
		frame.Centre()
		frame.Show(True)
		_docList.append(frame)

		return True

#----------------------------------------------------------------------------
def main():
	global _app
	sys.stderr = ExceptionHandler()
	_app = MyApp(0)
	_app.MainLoop()