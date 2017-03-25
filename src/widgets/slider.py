#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Slider(ogl.CompositeShape):
	
	def __init__(self, canvas,img):
		ogl.CompositeShape.__init__(self)

		self.SetCanvas(canvas)

		constraining_shape = ogl.BitmapShape()
		constraining_shape.SetBitmap(wx.Bitmap( img, wx.BITMAP_TYPE_ANY ))
		constrained_shape1 = ogl.RectangleShape(100, 2)

		self.AddChild(constrained_shape1)
		self.AddChild(constraining_shape)

		constraint = ogl.Constraint(ogl.CONSTRAINT_CENTRED_BOTH, constraining_shape, [constrained_shape1])
		self.AddConstraint(constraint)

		self.Recompute()

		# If we don't do this, the shapes will be able to move on their
		# own, instead of moving the composite
		constraining_shape.SetDraggable(False)
		constrained_shape1.SetDraggable(False)

		# If we don't do this the shape will take all left-clicks for itself
		constraining_shape.SetSensitivityFilter(0)