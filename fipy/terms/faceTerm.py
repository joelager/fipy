"""
## -*-Pyth-*-
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "faceTerm.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 11/28/03 {9:55:23 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-17 JEG 1.0 original
 # ###################################################################
 ##
"""
 
from term import Term
import Numeric

class FaceTerm(Term):
    def __init__(self,stencil,mesh,boundaryConditions):
	"""
        Stencil is for a mixed explicit/implicit scheme
        stencil = ( ( phi_adj, phi ) , ( phi_adj_exp , phi_exp ) )
        for a completly implicit scheme use:
        ( ( 1, 1) , 'None' )
        and for an explicit scheme use:
        ( 'None', ( 1, 1) )
        for a mixed explicit, implicit scheme:
        ( ( .8, .8), (.2, .2) ) for example
	"""
	Term.__init__(self,stencil)
        self.mesh = mesh
        self.interiorN = len(self.mesh.getInteriorFaces())
        self.boundaryConditions = boundaryConditions
	
    def buildMatrix(self,L,array,b):
	
	id1, id2 = self.mesh.getAdjacentCellIDs()
	id1 = id1[:self.interiorN]
	id2 = id2[:self.interiorN]
	
        ## implicit
        if self.stencil[0]!='None':
            stencil = self.stencil[0]
            aa =  self.coeff[:self.interiorN]*stencil[1]
            bb = -self.coeff[:self.interiorN]*stencil[0]
	
	    L.update_add_something(aa,id1,id1)
	    L.update_add_something(bb,id1,id2)
	    L.update_add_something(bb,id2,id1)
	    L.update_add_something(aa,id2,id2)
            
            for boundaryCondition in self.boundaryConditions:
                for face in boundaryCondition.getFaces():
                    cellId = face.getCellId()
                    faceId = face.getId()
                    LL,bb = boundaryCondition.update(face,self.coeff[faceId],stencil)
                    L[cellId,cellId] += LL
                    b[cellId] += bb

        ## explicit
        if self.stencil[1]!='None':
            stencil = self.stencil[1]
            aa = -self.coeff[:self.interiorN]*stencil[1]
            bb = self.coeff[:self.interiorN]*stencil[0]

            for i in range(self.interiorN):
                b[id1[i]] += aa[i] * array[id1[i]] + bb[i] * array[id2[i]]
                b[id2[i]] += aa[i] * array[id2[i]] + bb[i] * array[id1[i]]
	
            for boundaryCondition in self.boundaryConditions:
                for face in boundaryCondition.getFaces():
                    cellId = face.getCellId()
                    faceId = face.getId()
                    LL,bb = boundaryCondition.update(face,self.coeff[faceId],stencil)
                    b[cellId] -= LL * array[cellId]
                    b[cellId] += bb
        
