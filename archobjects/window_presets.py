#***************************************************************************
#*  Copyright (c) 2020 Carlo Dormeletti (onekk) carlo.dormeletti@yahoo.com *
#*                                                                         *
#*  This program is free software; you can redistribute it and/or modify   *
#*  it under the terms of the GNU Lesser General Public License (LGPL)     *
#*  as published by the Free Software Foundation; either version 2 of      *
#*  the License, or (at your option) any later version.                    *
#*  for detail see the LICENCE text file.                                  *
#*                                                                         *
#*  This program is distributed in the hope that it will be useful,        *
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*  GNU Library General Public License for more details.                   *
#*                                                                         *
#*  You should have received a copy of the GNU Library General Public      *
#*  License along with this program; if not, write to the Free Software    *
#*  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*  USA                                                                    *
#*                                                                         *
#***************************************************************************
"""Provide the window presets to be used in the Arch Opening object
"""
## @package window_presets
# \ingroup ARCH
# \brief Provide the window presets to be used in the Arch Opening object.

import FreeCAD
import FreeCADGui
from FreeCAD import Rotation, Vector

App = FreeCAD

# BEGIN DOC Settings
DEBUG = True
DBG_LOAD = False
DOC_NAME = "finestra"
# END DOC settings

EPS = 0.002

VZOR = App.Vector(0, 0, 0)
ROT0 = App.Rotation(0, 0, 0)
ROTX90 = App.Rotation(0, 0, 90)
ROTXN90 = App.Rotation(0, 0, -90)
ROTY90 = App.Rotation(0, 90, 0)
ROTZ180 = App.Rotation(180, 0, 0)
#Used to shorten most Placements
PL0 = App.Placement(VZOR, ROT0)

# DOCUMENT START HERE

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Components

def frame_rectangular(tel_w, tel_h , tel_ww, tel_wh, tel_th, et=0):
    """ Return the shape of a rectangular frame.
    """
    import Part

    i_tel_w = tel_w - tel_ww * 2
    i_tel_h = tel_h - tel_wh * 2

    ep0 = (tel_w * -0.5, 0, 0)
    ep1 = (tel_w * 0.5, 0, 0)
    ep2 = (tel_w * 0.5, 0, tel_h)
    ep3 = (tel_w * -0.5, 0, tel_h)

    ip0 = (i_tel_w * -0.5, 0, tel_ww)
    ip1 = (i_tel_w * 0.5, 0, tel_ww)
    ip2 = (i_tel_w * 0.5, 0, tel_ww + i_tel_h)
    ip3 = (i_tel_w * -0.5, 0, tel_ww + i_tel_h)
  
    tel_b = (ep0, ep1, ip1, ip0, ep0)
    tel_bp = Part.makePolygon([Vector(*vtx) for vtx in tel_b])

    tel_r = (ep1, ep2, ip2, ip1, ep1)
    tel_rp = Part.makePolygon([Vector(*vtx) for vtx in tel_r])

    tel_t = (ep2, ep3, ip3, ip2, ep2)
    tel_tp = Part.makePolygon([Vector(*vtx) for vtx in tel_t])

    tel_l = (ep3, ep0, ip0, ip3, ep3)
    tel_lp = Part.makePolygon([Vector(*vtx) for vtx in tel_l])

    tel_fb = Part.makeFilledFace(tel_bp.Edges) 
    tel_fbs = tel_fb.extrude(Vector(0, tel_th, 0))

    tel_fr = Part.makeFilledFace(tel_rp.Edges) 
    tel_frs = tel_fr.extrude(Vector(0, tel_th, 0))
    
    tel_ft = Part.makeFilledFace(tel_tp.Edges) 
    tel_fts = tel_ft.extrude(Vector(0, tel_th, 0))

    tel_fl = Part.makeFilledFace(tel_lp.Edges) 
    tel_fls = tel_fl.extrude(Vector(0, tel_th, 0))    
    
    return Part.makeCompound([tel_fbs, tel_frs, tel_fts, tel_fls])


def glass(ea_w, ea_h, ef_w, ef_h, v_a, frame_th, glass_th): 
    """Return the shape of a rectangular glass panel.
    TODO: Check if a Part::Box is faster
    """
    import Part

    v_w = ea_w - ef_w + v_a * 2
    v_h = ea_h - ef_h + v_a * 2
    
    vp0 = (v_w * -0.5, 0, ef_w - v_a)
    vp1 = (v_w * 0.5, 0, ef_w  - v_a)
    vp2 = (v_w * 0.5, 0, ef_h - v_a + v_h)
    vp3 = (v_w * -0.5, 0, ef_h - v_a + v_h)
    
    glass_pt = (vp0, vp1, vp2, vp3, vp0)    
    glass_p = Part.makePolygon([Vector(*vtx) for vtx in glass_pt])
        
    glass_f = Part.makeFilledFace(glass_p.Edges) 
    glass_s = glass_f.extrude(Vector(0, glass_th, 0))

    return glass_s


def default_sill(opening_width, host_thickness, sill_thickness, front_protrusion, lateral_protrusion, inner_covering): 
    """Return the shape of a rectangular glass panel.
    TODO: Check if a Part::Box is faster
    """
    import Part

    sill_wid = opening_width + lateral_protrusion * 2
    sill_th = sill_thickness
    sill_len = host_thickness + front_protrusion - inner_covering
    sill = Part.makeBox(sill_wid, sill_len, sill_th)
    sill.Placement.Base = Vector(sill_wid * -0.5, host_thickness * -0.5 + inner_covering , sill_thickness * -1)

    return sill

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Windows

def window_single_pane(opening_th=300, opening_height=1400, opening_width=1200,
             frame_width=50, frame_th=50, glass_th=21, n_pan=1):
    """Return the shape of a full n_panes rectangular window.
    """
    import Part

    # permit to differentiate from the top-bottom and left right    
    frame_height = frame_width 
    
    # congruency check:
    frame_ov_wid = n_pan * (frame_width * 2) + frame_width * 2
    
    light_fact = (opening_width - frame_ov_wid) / opening_width 
    #print("FW LF >",frame_ov_wid, light_fact)

    # frame reduction 
    ef_w = frame_width * 2
    ef_h = frame_height * 2
    
    res_w = opening_width - ef_w     
    res_h = opening_height - ef_h
    
    # glass margin into the frame
    v_a = 0

    # TODO Adapt the warning to FreeCAD warning standard
    if  light_fact < 0.40 :
        print("Too Many panes in the window resulting in < 40% of the opening")
        return 

    # CREATE COMPONENTS
    components = []

    # CREATE FIXED FRAME
    components.append(frame_rectangular(opening_width, opening_height, frame_width, 
                   frame_height, frame_th))

    # CREATE OPENING PANELS
    if n_pan == 0:
        # TODO: If n_pan == 0 create a fixed window
        return

    if n_pan == 1:
        # Create a single pane window
        ea_w = res_w
        ea_h = res_h
        
        open_frame = frame_rectangular(ea_w, ea_h, frame_width,  frame_height, frame_th)
        open_frame.Placement = FreeCAD.Placement(Vector(0, 0, frame_height), ROT0)
        components.append(open_frame)

        glass_s = glass(ea_w, ea_h, ef_w, ef_h, v_a, frame_th, glass_th)  
        pl_v = FreeCAD.Placement(Vector(0, (frame_th - glass_th) * 0.5, 0), ROT0)        
        glass_s.Placement = pl_v

        components.append(glass_s)        

    elif n_pan > 1 and n_pan < 10: 
        # Create a multi pane window
        fact_w = res_w / n_pan
        
        loop = True
        cnt = 1
        while loop is True:
            if cnt > n_pan:
                break
            ea_w = fact_w
            adv_x = (cnt - 1) * fact_w
            ofx = (res_w * -0.5) + fact_w * 0.5 + adv_x
            ea_h = res_h

            open_frame = frame_rectangular(ea_w, ea_h, frame_width,  frame_height, frame_th)
            pl_ea = FreeCAD.Placement(Vector(ofx, 0, frame_height), ROT0)               
            open_frame.Placement = pl_ea
        
            components.append(open_frame)        
        
            glass_s = glass(ea_w, ea_h, ef_w, ef_h, v_a, frame_th, glass_th)  
            pl_v = FreeCAD.Placement(Vector(ofx, (frame_th - glass_th) * 0.5, 0), ROT0)        
            glass_s.Placement = pl_v

            components.append(glass_s)

            cnt += 1

    window = Part.makeCompound(components)
 
    return window