"""Create coordinate-labelled evidence strips; does not identify roads or choose edges."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--image',required=True);a.add_argument('--output',required=True)
    a.add_argument('--axis',choices=['row','column'],default='row')
    a.add_argument('--positions',required=True,help='Comma-separated original pixel row/column indices')
    a.add_argument('--start',type=int,required=True);a.add_argument('--end',type=int,required=True)
    a.add_argument('--half-band',type=int,default=2);a.add_argument('--scale',type=int,default=4)
    a.add_argument('--tick',type=int,default=10);a.add_argument('--font')
    args=a.parse_args();src=Path(args.image);out=Path(args.output)
    if args.scale<1 or args.half_band<0 or args.tick<1: a.error('Invalid display parameters')
    ps=[int(s.strip()) for s in args.positions.split(',') if s.strip()]
    if not ps:a.error('No positions')
    with Image.open(src) as f:
        source_mode=f.mode;im=f.convert('RGB');source_size=f.size
    extent=im.width if args.axis=='row' else im.height
    normal_extent=im.height if args.axis=='row' else im.width
    if not (0<=args.start<args.end<=extent):a.error('Along-strip extent is outside the source')
    if any(v-args.half_band<0 or v+args.half_band>=normal_extent for v in ps):a.error('Band extends outside the source')
    width=(args.end-args.start)*args.scale;band=(2*args.half_band+1)*args.scale
    height=band+65;canvas=Image.new('RGB',(max(width,360),height*len(ps)),'white')
    font=ImageFont.truetype(args.font,14) if args.font else ImageFont.load_default(size=14)
    d=ImageDraw.Draw(canvas);bounds=[]
    for i,v in enumerate(ps):
        box=(args.start,v-args.half_band,args.end,v+args.half_band+1) if args.axis=='row' else (v-args.half_band,args.start,v+args.half_band+1,args.end)
        q=im.crop(box)
        if args.axis=='column':q=q.transpose(Image.Transpose.TRANSPOSE)
        top=i*height;d.text((3,top+2),f'{args.axis}={v}; original pixels {args.start}..{args.end-1}',font=font,fill='black')
        canvas.paste(q.resize((width,band),Image.Resampling.NEAREST),(0,top+25))
        for t in range(args.start,args.end,args.tick):
            x=(t-args.start)*args.scale;d.line((x,top+25,x,top+25+band),fill=(210,140,30),width=1)
            d.text((x,top+29+band),str(t),font=font,fill='black')
        bounds.append(dict(position=v,source_crop=list(box),display_scale=args.scale))
    out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out)
    metadata=dict(schema='satellite-evidence-strips-v1',source=str(src.resolve()),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_mode=source_mode,source_size=list(source_size),axis=args.axis,bands=bounds,output=str(out.resolve()),notes='Original pixel indices; enlargement adds no detail. No edge recognition or geometry acceptance performed.')
    out.with_suffix('.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Saved {len(ps)} evidence bands')

if __name__=='__main__':main()
