#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Tooltip(ogl.DrawnShape):
	def __init__(self):
		ogl.DrawnShape.__init__(self)
		
		self.SetDrawnPen(wx.BLACK_PEN)
		self.SetDrawnBrush(wx.WHITE_BRUSH)
		self.DrawPolygon([(-100, -12), (100,-12),(100,12),(80,12),(75,30),(70,12),(-100,12),(-100,-12)])

		self.CalculateSize()