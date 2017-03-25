#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Canvas(ogl.ShapeCanvas):
	
	def __init__(self,parent):
		ogl.ShapeCanvas.__init__(self, parent)
		self.parent = parent

		self.gridsize = 20

		self.SetBackgroundColour( "WHITE" )
		self.SetScrollbars(20, 20, 2000/20, 2000/20)

		diagram = ogl.Diagram()
		self.SetDiagram(diagram)