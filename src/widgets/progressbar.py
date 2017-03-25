#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class ProgressBar(ogl.CompositeShape):
	
	def __init__(self, canvas):
		ogl.CompositeShape.__init__(self)

		self.SetCanvas(canvas)

		constraining_shape = ogl.RectangleShape(150, 20)
		constrained_shape1 = ogl.RectangleShape(70, 20)

		self.AddChild(constraining_shape)
		self.AddChild(constrained_shape1)

		constrained_shape1.SetBrush(wx.Brush(wx.Colour(50, 50, 50)))
		constraining_shape.SetBrush(wx.WHITE_BRUSH)
		
		constrained_shape1.SetCornerRadius(10)
		constraining_shape.SetCornerRadius(10)

		constraint = ogl.Constraint(ogl.CONSTRAINT_ALIGNED_LEFT, constraining_shape, [constrained_shape1])
		self.AddConstraint(constraint)

		self.Recompute()

		# If we don't do this, the shapes will be able to move on their
		# own, instead of moving the composite
		constraining_shape.SetDraggable(False)
		constrained_shape1.SetDraggable(False)

		# If we don't do this the shape will take all left-clicks for itself
		constraining_shape.SetSensitivityFilter(0)