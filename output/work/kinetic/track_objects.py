from pathlib import Path
import cv2,numpy as np,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[3];W=R/'output/work/kinetic';P=R/'output/reports'
# Manually selected real object ROIs on the raw assembly, in 1080x1920 coordinates.
# Short windows avoid scene boundaries and uncertain AI geometry; pixel tracking is not engineering validation.
targets=[('formwork_jack',18.5,20.0,[390,970,140,250]),('translator',39.3,42.4,[270,710,510,180]),('red_support',43.9,45.8,[580,880,150,650]),('mast_tip',55.2,57.8,[675,530,160,180])]
tracks=[];thumbs=[]
for name,start,end,roi in targets:
 cap=cv2.VideoCapture(str(R/'output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4'));first=round(start*30);last=round(end*30);cap.set(cv2.CAP_PROP_POS_FRAMES,first)
 ok,frame=cap.read();assert ok
 def gray(im):return cv2.cvtColor(cv2.resize(im,(540,960)),cv2.COLOR_BGR2GRAY)
 prev=gray(frame);x,y,w,h=np.array(roi)/2;mask=np.zeros_like(prev);mask[round(y):round(y+h),round(x):round(x+w)]=255
 points=cv2.goodFeaturesToTrack(prev,100,.015,5,mask=mask);assert points is not None and len(points)>10,(name,points)
 center=np.array([x+w/2,y+h/2]);rows=[]
 for n in range(first,last):
  fb_err=0.;kept=len(points);residual=0.
  if n>first:
   ok,frame=cap.read();assert ok;cur=gray(frame)
   nxt,st,_=cv2.calcOpticalFlowPyrLK(prev,cur,points,None,winSize=(25,25),maxLevel=3)
   back,bst,_=cv2.calcOpticalFlowPyrLK(cur,prev,nxt,None,winSize=(25,25),maxLevel=3)
   fb=np.linalg.norm(back-points,axis=2).ravel();good=(st.ravel()==1)&(bst.ravel()==1)&(fb<1.5)
   old=points[good].reshape(-1,2);new=nxt[good].reshape(-1,2);assert len(old)>=8,(name,n,len(old))
   delta=new-old;shift=np.median(delta,axis=0);errors=np.linalg.norm(delta-shift,axis=1);inliers=errors<3.0
   assert inliers.sum()>=6,(name,n,'inliers')
   center+=np.median(delta[inliers],axis=0);points=new[inliers].reshape(-1,1,2);prev=cur;fb_err=float(np.median(fb[good]));residual=float(np.median(errors[inliers]));kept=int(inliers.sum())
  if len(points)<30 or (n-first)%10==9:
   mask=np.zeros_like(prev);mx,my=center-[w/2,h/2];mask[max(0,round(my)):min(960,round(my+h)),max(0,round(mx)):min(540,round(mx+w))]=255
   reseeded=cv2.goodFeaturesToTrack(prev,100,.015,5,mask=mask)
   if reseeded is not None and len(reseeded)>=10:points=reseeded
  rows.append({'frame':n,'time':n/30,'cx':round(float(center[0]*2),2),'cy':round(float(center[1]*2),2),'points':kept,'median_fb_error_halfres_px':fb_err,'median_motion_residual_halfres_px':residual})
  if n in [first,(first+last)//2,last-1]:
   im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im);cx,cy=center*2;radius=max(w,h)*.55*2
   # Preview window is a small pointer halo rather than a claim about exact physical dimensions.
   radius={'drill':100,'formwork_jack':100,'translator':165,'red_support':130,'mast_tip':95}[name]
   d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline='#FFD400',width=7)
   im.thumbnail((216,384));thumbs.append((name,n/30,im))
 cap.release();tracks.append({'object':name,'start':start,'end':end,'initial_roi':roi,'method':'ROI KLT optical flow; forward/backward rejection <1.5 px at half resolution; median translation; not physical reconstruction','samples':rows})
(P/'object_tracks.json').write_text(json.dumps(tracks,indent=2))
sheet=Image.new('RGB',(648,len(targets)*410),'#202020');d=ImageDraw.Draw(sheet)
for i,(name,t,im) in enumerate(thumbs):x=i%3*216;y=i//3*410;sheet.paste(im,(x,y+26));d.text((x+5,y+5),f'{name} {t:.2f}',fill='white')
sheet.save(W/'tracked_objects_review.jpg')
for t in tracks:print(t['object'],len(t['samples']),'frames; min points',min(x['points'] for x in t['samples']),'max median FB',max(x['median_fb_error_halfres_px'] for x in t['samples']))
