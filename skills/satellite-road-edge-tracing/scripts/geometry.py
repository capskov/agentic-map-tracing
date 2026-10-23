"""Deterministic helpers only; no road recognition or CAD writes. Python 3.9+."""
import math
import argparse

def pixel_to_world(point, size, origin, u, v, *, pixel_center=False):
    w,h=size
    if w<=0 or h<=0:raise ValueError('positive raster size required')
    x,y=point
    if pixel_center:x+=.5;y+=.5
    return tuple(origin[k]+x/w*u[k]+(1-y/h)*v[k] for k in range(2))

def world_to_pixel(point,size,origin,u,v,*,pixel_center=False):
    w,h=size
    if w<=0 or h<=0:raise ValueError('positive raster size required')
    det=u[0]*v[1]-u[1]*v[0]
    if abs(det)<1e-12:raise ValueError('singular raster basis')
    dx,dy=point[0]-origin[0],point[1]-origin[1]
    a=(dx*v[1]-dy*v[0])/det;b=(u[0]*dy-u[1]*dx)/det
    offset=.5 if pixel_center else 0
    return (a*w-offset,(1-b)*h-offset)

def offset_polyline(points,width,*,miter_limit=4):
    if width<=0 or len(points)<2:raise ValueError('positive width and at least two points required')
    normals=[]
    for a,b in zip(points,points[1:]):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        if length<=1e-12:raise ValueError('repeated adjacent point')
        normals.append((-dy/length,dx/length))
    edges=[[],[]]
    for i,p in enumerate(points):
        if i==0:n=normals[0];factor=1
        elif i==len(points)-1:n=normals[-1];factor=1
        else:
            a,b=normals[i-1],normals[i];x,y=a[0]+b[0],a[1]+b[1];length=math.hypot(x,y)
            if length<1e-10:raise ValueError('reversing turn requires a new trace')
            n=(x/length,y/length);factor=1/(n[0]*b[0]+n[1]*b[1])
            if abs(factor)>miter_limit:raise ValueError('sharp miter requires visual redesign')
        for j,sign in enumerate([-1,1]):edges[j].append(tuple(p[k]+sign*width/2*factor*n[k] for k in range(2)))
    return edges

def self_test():
    # Synthetic rotated, non-square raster; no project coordinates.
    size=(100,80);origin=(10,20);u=(60,80);v=(-64,48)
    for center in (False,True):
        for pt in ((0,0),(99,79),(12.25,45.75)):
            world=pixel_to_world(pt,size,origin,u,v,pixel_center=center)
            back=world_to_pixel(world,size,origin,u,v,pixel_center=center)
            assert math.dist(pt,back)<1e-10
    corner=pixel_to_world((0,0),size,origin,u,v)
    center=pixel_to_world((0,0),size,origin,u,v,pixel_center=True)
    assert math.dist(center,tuple(corner[k]+.5*u[k]/100-.5*v[k]/80 for k in range(2)))<1e-10
    pts=[(0,0),(30,0),(45,20),(60,25)];width=6;edges=offset_polyline(pts,width)
    for i,(a,b) in enumerate(zip(pts,pts[1:])):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length)
        for k in (i,i+1):
            gap=sum((edges[1][k][j]-edges[0][k][j])*n[j] for j in range(2))
            assert abs(gap-width)<1e-10
    try:offset_polyline([(0,0),(1,0),(0,0)],2)
    except ValueError:pass
    else:raise AssertionError('reversing turn accepted')
    print('PASS: rotated affine round trips, half-pixel convention, normal widths, reversing-turn rejection')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    if args.self_test:self_test()
    else:ap.print_help()
