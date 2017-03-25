#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Frame(ogl.CompositeShape):
	
	def __init__(self, canvas):
		ogl.CompositeShape.__init__(self)

		self.SetCanvas(canvas)

		constraining_shape = ogl.RectangleShape(400, 30)
		constrained_shape1 = ogl.BitmapShape()
		constrained_shape1.SetBitmap(wx.Bitmap( 'icons/frame.png', wx.BITMAP_TYPE_ANY ))

		self.AddChild(constraining_shape)
		self.AddChild(constrained_shape1)

		constraints = ogl.Constraint(ogl.CONSTRAINT_ALIGNED_LEFT, constraining_shape, [constrained_shape1])
		self.AddConstraint(constraints)
		self.Recompute()

		# If we don't do this, the shapes will be able to move on their
		# own, instead of moving the composite
		constraining_shape.SetDraggable(False)
		constrained_shape1.SetDraggable(False)

		# If we don't do this the shape will take all left-clicks for itself
		constraining_shape.SetSensitivityFilter(0)