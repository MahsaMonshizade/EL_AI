#!/usr/local/bin/python3
#
# Authors: 
# Yu Mo (moyu)
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys, imageio, copy

# calculate "Edge strength map" of an image                                                                                                                                      
def cal_edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


def Simple(edge_strength, air_bdry = None):
    em_matrix = EmissionProb( edge_strength )
    if air_bdry == None:
        return argmax(em_matrix, axis = 0).tolist()
    else:
        x,y = shape(em_matrix)
        icerock_range = [ x+10 for x in air_bdry ]
        icerock_bdry = [0.0]*y
        for j in range(y):
            sub_col = em_matrix[ icerock_range[j]:, j]
            icerock_bdry[j] = argmax(sub_col) + icerock_range[j]
        return icerock_bdry
    
def EmissionProb(edge_strength):
    em_prob = edge_strength/sum(edge_strength, axis = 0)
    return em_prob

def TransitionProbability(pre_row_ind, curr_col_ind, vtb_mat, rowrange = -1):
    x,y = shape(vtb_mat)
    t_prob = array( [0.0]*x )
    for i in range(x):
        if abs(pre_row_ind-i)<5 and pre_row_ind>rowrange:
            t_prob[i] = 0.8*vtb_mat[i][curr_col_ind-1] 
        else:
            t_prob[i] = 0.001*vtb_mat[i][curr_col_ind-1]
    t_prob = t_prob/sum(t_prob)
    return t_prob

def Viterbi(edge_strength, air_bdry = None):
    x, y = shape(edge_strength)
    ems_mat = EmissionProb(edge_strength)
    vtb_mat = EmissionProb(edge_strength)*1e3
    trs_mat = zeros( [x,y] )
    if air_bdry == None:
        rowrange = [-1]*y
    else:
        rowrange = [ bdry+10 for bdry in air_bdry ]
        
    for j in range(1,y):
        max_ind_curr_pxl = []
        for i in range(x):
            t_p_curr_pxl = TransitionProbability(i, j, vtb_mat, rowrange[j])
            max_val = max(t_p_curr_pxl)
            vtb_mat[i,j] = ems_mat[i,j]*max_val
            max_ind_curr_pxl.append( argmax(t_p_curr_pxl) )
        trs_mat[:,j] = max_ind_curr_pxl
    trs_mat = trs_mat.astype(int)
    
    path = [argmax(vtb_mat[:, 0], axis=0)]
    track_ind = path[0]
    for j in range(1, y):
        path.append( trs_mat[track_ind,j] )
        track_ind = trs_mat[track_ind,j]
    return path
            


# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]
    
    # load in image
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = cal_edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # air-ice boundary
    airice_simple = Simple(edge_strength)
    airice_hmm = Viterbi(edge_strength)
    r1, c1 = gt_airice
    edge_strength_air = copy.deepcopy(edge_strength)
    edge_strength_air[ :, c1] = 0.0
    edge_strength_air[r1, c1] = 1.0
    airice_feedback = Viterbi(edge_strength_air)
    
    
    # ice-rock boundary
    icerock_simple= Simple(edge_strength, airice_simple)
    icerock_hmm = Viterbi(edge_strength, airice_hmm)
    r2, c2 = gt_icerock
    edge_strength_ice = copy.deepcopy(edge_strength)
    edge_strength_ice[ :, c2] = 0.0
    edge_strength_ice[r2, c2] = 1.0
    icerock_feedback = Viterbi(edge_strength_ice, airice_feedback)
    
    
    # Now write out the results as images and a text file
    
    # simple
    input_image = Image.open(input_filename).convert('RGB')
    new_image_simple = draw_boundary(input_image, airice_simple, (255, 255, 0), 2)
    new_image_simple = draw_boundary(input_image, icerock_simple, (255, 255, 0), 2)
    imageio.imwrite("simple.png", new_image_simple)
    
    # hmm with Viterbi
    input_image = Image.open(input_filename).convert('RGB')
    new_image_hmm = draw_boundary(input_image, airice_hmm, (0, 0, 255), 2)
    new_image_hmm = draw_boundary(input_image, icerock_hmm, (0, 0, 255), 2)
    imageio.imwrite("hmm.png", new_image_hmm)
    
    # hmm with human feedback
    input_image = Image.open(input_filename).convert('RGB')
    new_image_fb = draw_boundary(input_image, airice_feedback, (255, 0, 0), 2)
    new_image_fb = draw_boundary(input_image, icerock_feedback, (255, 0, 0), 2)
    new_image_fb = draw_asterisk(input_image, (c1,r1), (255, 0, 0), 2)
    new_image_fb = draw_asterisk(input_image, (c2,r2), (255, 0, 0), 2)
    imageio.imwrite("feedback.png", new_image_fb)
    

    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
