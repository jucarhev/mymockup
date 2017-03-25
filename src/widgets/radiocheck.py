#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.ogl as ogl

class Dialog_widget_edit(wx.Dialog):
	def __init__(self, parent, title,img):
		super(Dialog_widget_edit, self).__init__(parent, title=title,size=(240,120))
		self.parent = parent
		self.img = img
		self.texto = wx.TextCtrl( self, wx.ID_ANY, size=(220,30), pos=(10,10))
		
		aceptar = wx.Button( self, wx.ID_ANY, u"Aceptar",pos=(10,50))

		aceptar.Bind(wx.EVT_BUTTON,self.text)

		self.label_content()

	def text(self,evt):
		r = self.texto.GetValue()
		
		self.parent.modify_label(r,self.img)
		self.Destroy()

	def label_content(self):
		id_shape = self.parent.shape_selected.GetId()
		self.type_shape = ''
		for data in self.parent.diccionary_shapes_info:
			if data[1] == id_shape:
				self.texto.SetValue(str(data[4]))
				type_shape = str(data[2])
				
class RadioCheck(ogl.CompositeShape):
	
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