# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2    
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                # Définir ici les sommets
                [0,0,0], 
                [0, 0, self.parameters['height']],
                [0, self.parameters['thickness'], self.parameters['height']],
                [0, self.parameters['thickness'], 0],
                [self.parameters['width'], 0 , 0 ],
                [self.parameters['width'], 0 , self.parameters['height']],
                [self.parameters['width'], self.parameters['thickness'], self.parameters['height']],
                [self.parameters['width'], self.parameters['thickness'], 0]
                ]

        self.faces = [
                # définir ici les faces
                [0,1,2,3],
                [4,5,6,7],
                [0,1,5,4],
                [0,3,7,4],
                [2,3,7,6],
                [1,2,6,5]
                ]   
        

    # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
        # A compléter en remplaçant pass par votre code
        if x.parameters['thickness'] == self.parameters['thickness'] :
          if x.parameters['position'][0] >= self.parameters['position'][0] :
            if x.parameters['position'][1] >= self.parameters['position'][1] :
              if x.parameters['position'][2] >= self.parameters['position'][2] :
                if x.parameters['position'][2] + x.parameters['height'] <= self.parameters['position'][2] + self.parameters['height']:
                  if x.parameters['position'][0] + x.parameters['width'] <= self.parameters['position'][0] + self.parameters['width']:
                    return True 
        return False

        

    # Creates the new sections for the object x
    def createOpening(self, x):
        # A compléter en remplaçant pass par votre code
        if self.canCreateOpening(x) :
          L = []
          s1 = Section({'position': self.parameters['position'], 'width': x.parameters['position'][0] - self.parameters['position'][0], 'height': self.parameters['height'], 'thickness': self.parameters['thickness'], 'color' :[1, 0, 0]})
          L.append(s1)

          s2 = Section({'position': [x.parameters['position'][0] + x.parameters['width'], self.parameters['position'][1], self.parameters['position'][2]], 'width': - self.parameters['position'][0] + self.parameters['width'] - x.parameters['position'][0] - x.parameters['width'], 'height': self.parameters['height'], 'thickness': self.parameters['thickness'], 'color' :[0, 1, 0]})
          L.append(s2)

          s3 = Section({'position': [x.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2]], 'width': x.parameters['width'], 'height': x.parameters['position'][2] - self.parameters['position'][2], 'thickness': self.parameters['thickness'], 'color' :[0, 0, 1]})
          L.append(s3)

          s4 = Section({'position': [x.parameters['position'][0], x.parameters['position'][1], x.parameters['position'][2] + x.parameters['height']], 'width': x.parameters['width'], 'height': self.parameters['height'] - x.parameters['height'] - x.parameters['position'][2], 'thickness': self.parameters['thickness']})
          L.append(s4)

          return L
        
    # Draws the edges
    def drawEdges(self):
        # A compléter en remplaçant pass par votre code
        gl.glPushMatrix()
        gl.glTranslatef(self.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2])
        gl.glBegin(gl.GL_LINES) # Indique que l'on va commencer un trace en mode lignes (segments)
        gl.glColor3fv([0, 0, 0]) # Indique la couleur du prochian segment en RGB
        
        gl.glVertex3fv(self.vertices[0]) # Premier vertice : départ de la ligne
        gl.glVertex3fv(self.vertices[3]) # Deuxième vertice : fin de la ligne

        gl.glVertex3fv(self.vertices[0])
        gl.glVertex3fv(self.vertices[1])
        
        gl.glVertex3fv(self.vertices[0])
        gl.glVertex3fv(self.vertices[4])

        gl.glVertex3fv(self.vertices[1])
        gl.glVertex3fv(self.vertices[2])

        gl.glVertex3fv(self.vertices[1])
        gl.glVertex3fv(self.vertices[5])

        gl.glVertex3fv(self.vertices[2])
        gl.glVertex3fv(self.vertices[3])

        gl.glVertex3fv(self.vertices[2])
        gl.glVertex3fv(self.vertices[6])

        gl.glVertex3fv(self.vertices[3])
        gl.glVertex3fv(self.vertices[7])

        gl.glVertex3fv(self.vertices[4])
        gl.glVertex3fv(self.vertices[5])

        gl.glVertex3fv(self.vertices[5])
        gl.glVertex3fv(self.vertices[6])
        
        gl.glVertex3fv(self.vertices[6])
        gl.glVertex3fv(self.vertices[7])
        
        gl.glVertex3fv(self.vertices[4])
        gl.glVertex3fv(self.vertices[7])
        gl.glEnd() # Find du tracé
        gl.glPopMatrix()
         
    # Draws the faces
    def draw(self):
        # A compléter en remplaçant pass par votre code
      gl.glPushMatrix()
      self.drawEdges() 
      gl.glTranslatef(self.parameters['position'][0], self.parameters['position'][1], self.parameters['position'][2])
      gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
      for i in self.faces :
        gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
        gl.glColor3fv(self.parameters['color'])
        for j in i :
          gl.glVertex3fv(self.vertices[j])
        gl.glEnd()
      gl.glPopMatrix()
