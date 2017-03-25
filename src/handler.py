#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class MyEvtHandler(ogl.ShapeEvtHandler):
	
	def __init__(self,parent):
		ogl.ShapeEvtHandler.__init__(self)
		self.parent = parent

	def UpdateStatusBar(self, shape):
		x, y = shape.GetX(), shape.GetY()
		width, height = shape.GetBoundingBoxMax()

	def OnLeftClick(self, x, y, keys=0, attachment=0):
		shape = self.GetShape()
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
		self.parent.shape_propierties(shape,x,y)
		ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

		if not shape.Selected():
			self.OnLeftClick(x, y, keys, attachment)

		self.UpdateStatusBar(shape)

	def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
		shape = self.GetShape()
		self.parent.shape_propierties(shape,x,y)
		ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
		self.UpdateStatusBar(self.GetShape())

	def OnMovePost(self, dc, x, y, oldX, oldY, display):
		shape = self.GetShape()
		self.parent.shape_propierties(shape,x,y)
		ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
		self.UpdateStatusBar(shape)
		if "wxMac" in wx.PlatformInfo:
			shape.GetCanvas().Refresh(False)

	def OnRightClick(self, *dontcare):
		shape = self.GetShape()
		self.parent.double_click(shape)

	def OnLeftDoubleClick(self, *dontcare):
		shape = self.GetShape()
		self.parent.double_click(shape)