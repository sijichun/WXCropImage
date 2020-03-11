#!/usr/bin/python3

from PIL import Image
import argparse
import os.path as ospath


if __name__=="__main__":
    ## load options
    parser=argparse.ArgumentParser(description="裁剪图像符合微信公众号要求。")
    parser.add_argument("input", help="图片文件，必须有后缀名")
    parser.add_argument("--heigh", type=int, default=float('inf'), help="图片高度，可选，如果高度大于计算的可行高度，则使用可行高度。")
    parser.add_argument("--quality", type=int, default=90, help="图片质量，0-100，默认为90")
    parser.add_argument("--output", default=None, help="输出文件前缀，默认为原文件名加数字")
    args=parser.parse_args()
    file_dir=ospath.dirname(args.input)
    filename,extname=ospath.splitext(ospath.basename(args.input))
    if args.output!=None:
        filename=args.output
    ## crop image
    image=Image.open(args.input)
    W,H=image.size
    ## 计算尺寸
    LIMIT=6000000
    h=int(min(args.heigh,LIMIT/W-1))
    ## 截取
    begin_x,begin_y=0,0
    end_x,end_y=W,h
    count=1
    while begin_y<H:
        end_y=min(end_y,H)
        sub_image=image.crop((begin_x,begin_y,end_x,end_y))
        output=ospath.join(file_dir,filename+str(count)+extname)
        sub_image.save(output,quality=args.quality)
        count+=1
        begin_x,begin_y,end_x,end_y=0,end_y+1,W,end_y+1+h
