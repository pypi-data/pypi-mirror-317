BH='매스가 존재하지 않습니다.'
BG='POLYGON EMPTY'
BF='officetel'
BE='dormitory'
BD='urbanhousing_bundong'
BC='urbanhousing_small'
BB='panmae'
BA='WideETCSE'
B9='SlimETCSE'
B8='WideETCS'
B7='SlimETCS'
B6='WideETM'
B5='SlimETM'
B4='WideETC'
B3='SlimETC'
B2='WideEM'
B1='SlimEM'
B0='WideEC'
A_='SlimEC'
Az='SlimEL'
Ay='ExWideE'
Ax='ExSlimE'
Aw='ExSlim'
Av='WideET'
Au='SlimET'
At='ExWideET'
As='ExSlimET'
Ar='ExSlimT'
Aq='ssmh'
Ap='ssr'
Ao='parking_residential'
An='use_small_core'
Am=reversed
AS='core'
AR='mass'
AQ='geoms'
AP='오피스텔'
AO='임대형기숙사'
AN='도생(소형주택다세대)'
AM='dasedae'
AL='parking_area_divisor'
AK='floor_height'
AJ='estimated_parklot_count'
AI='open_space_buffer_len'
AH='parking_commercial'
AG='has_commercial'
AF=tuple
AE=filter
AD=hasattr
A3='right'
x='dajung'
w='dagagu'
v='max_height'
r='geunsaeng'
q='max_floor'
p='max_far'
o=property
m=zip
l=min
k=1.
j='max_bcr'
i='has_elevator'
g=sorted
f=sum
d=int
c=Exception
Z='has_piloti'
Y='regulations'
X=enumerate
V='options'
M='left'
L=isinstance
K=range
I=map
H=list
F=False
E=True
C=None
A=len
import copy as y,math as A4,time as O,numpy as D
from typing import List,Tuple,Union,Iterable as A5
import shapely.affinity,shapely.ops
from shapely import wkt
from shapely.geometry import box as W
from shapely.geometry import LineString as J
from shapely.geometry import MultiLineString as s
from shapely.geometry import Point as P
from shapely.geometry import MultiPoint as AT
from shapely.geometry import Polygon as G
from shapely.geometry import MultiPolygon as R
from shapely.geometry import JOIN_STYLE as N
from shapely.geometry import CAP_STYLE as A6
from shapely.geometry.base import BaseGeometry
AU={'bbc':0,'dcg':0,'cpc':1,'gss':.3,'mcl':2.8,An:F,'tolr':.0003,'usc':F}
AV={'amin':0,'amax':90,'tolr_angle':.1,'dsang':15.,'mmaa':14,'sdl':1.8,'bcm':1.03,'fmg':.11,'fmg_for_commercial':.1,'umis':E,'pacc':F,'usep':E,'used':E,'usg':E,'bsc':E,'urpa':F,'iav':E,'cccm':E,'acac':E,'mmw':2.,'mcd':1.6,'ecp':1,'uec':E,'llb':2.6,'slb':1.2,'mab':6.,'mass_bb_slb':4.2,'csl':C,'ctl':C,i:C}
h={V:{i:[E],'unit_type':['1r'],Z:[E],AG:[F]},Y:{j:.6,p:2.,q:7,v:.0,Ao:C,AH:C}}
S={AI:.5,AJ:8,Ap:.5,Aq:1e1,AK:3.,AL:134,i:E,Z:E,j:.6,p:2.,q:7,v:.0}
class AW:
	def __init__(A,dict_obj):
		for(B,C)in dict_obj.items():setattr(A,B,C)
	def set_core_config(G,archi_line,mass,building_purpose,use_small_core,is_commercial_area,commercial_type,res,engine_type,usc=F):
		N=use_small_core;I=F;Q=F;R=F;S=F;U=[r];J=res[V][i][0]
		if is_commercial_area and building_purpose in U:
			if I:C=B.CORE_WIDE_ESCAPE_TALL;D=B.CORE_NARR_ESCAPE_TALL;J=E
			elif N:C=B.CORE_WIDE_TALL_SMALL;D=B.CORE_NARR_TALL_SMALL
			else:C=B.CORE_WIDE_TALL;D=B.CORE_NARR_TALL
		else:
			W=N
			if I:C=B.CORE_WIDE_ESCAPE;D=B.CORE_NARR_ESCAPE;J=E
			elif N and W:C=B.CORE_WIDE_SMALL;D=B.CORE_NARR_SMALL
			else:C=B.CORE_WIDE;D=B.CORE_NARR
		if not J:C=[C[0]];D=[D[0]];L=[0]
		elif not I:C=C[1:];D=D[1:];L=[A+1 for A in K(A(C))]
		else:L=[A+1 for A in K(A(C))]
		O=[]
		for H in K(A(C)):O.append([C[H],D[H]])
		assert A(O)==A(L),'코어타입과 코어사이즈 길이가 다릅니다.';T=[]
		if Q:
			if R:
				if S:M=B.CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL;P=B.CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL
				else:M=B.CORE_WIDE_SPECIFIC_ESCAPE_TALL;P=B.CORE_NARR_SPECIFIC_ESCAPE_TALL
			else:M=C;P=D
			for H in K(A(M)):T.append([M[H],P[H]])
		G.has_elevator=J;G.ctl=L;G.csl=O;G.sub_csl=T;G.is_escape_core=I;G.is_sub_core_necessary=Q;G.is_specific_escape_sub_core=R;G.is_specific_escape_emgcy_elev_sub_core=S;G.commercial_type=commercial_type
class A7(c):
	def __init__(A,msg):super().__init__();A._msg=msg
	def __str__(A):return A._msg
class B:EPSILON=1e-06;TOLERANCE=1e-06;TOLERANCE_LARGE=1e-05;TOLERANCE_SLIVER=.001;TOLERANCE_GROUPING=.1;TOLERANCE_ANGLE=.01;TOLERANCE_MARGIN=.01;TOLERANCE_MACRO=.1;MASS_DEADSPACE_LENGTH=3.001;UNITSPACE_DEADSPACE_LENGTH=2.001;TOLERANCE_UNIT=1;FLAG_LOT_CHECK_MIN_AREA=200;EACH_UNIT_DEADSPACE_LENGTH_M=1.999;POSTPROCESS_DEADSPACE_LENGTH_M=2;COMMERCIAL_ADDITIONAL_DEADSPACE_LENGTH=3;U_SHAPE_DEADSPACE_LENGTH=.3;BCR_EXTRA=.03;GFA_CUT_VECTOR=0,1;GFA_CUT_RANGE=1;GFA_CUT_KEEP_FLOOR=3;GRID_INTERVAL=.15;MASS_CUT_LENGTH=3;MASS_EMBOSS_LENGTH=3;MIN_REDUCE_FLOOR_AREA=300;STAGGER_UPPER_LENGTH=4;STAGGER_UPPER_DEPTH=.8;STAGGER_LOWER_LENGTH=3;STAGGER_LOWER_DEPTH=.5;STAGGER_MIN_LENGTH=2;ANGLECUT_LENGTH=10;MASSREMOVER_LENGTH=40;PARTITIONSPLITTER_LENGTH=30;PARTITIONSPLITTER_INTERVAL=1.05;PARTITIONSPLITTER_MARGIN=2.4;PARTITIONSPLITTER_MERGE=1.5;PARTITIONSPLITTER_KEEPOUT_LENGTH=.7;CORE_SPLITTER_DIVIDE_COUNT=2;CORRIDORTUNE_INTERVAL=.35;HALL_WIDTH_OFFSET_MARGIN=.15;HALL_WIDTH=1.4;HALL_WIDTH_EMGCY=1.5;HALL_WIDTH_ESCAPE=1.6;ELEV_WIDTH=1.93;ELEV_HEIGHT=2.35;ADJUSTED_ELEV_WIDTH=1.9;ADJUSTED_ELEV_HEIGHT=2.4;ELEV_WIDTH_SMALL=1.68;ELEV_HEIGHT_SMALL=2.05;ELEV_WIDTH_SPECIFIC=2.;ELEV_HEIGHT_SPECIFIC=2.7;EMERGENCY_ROOM_WIDTH=2.75;STAIR_WIDTH=2.8;ADJUSTED_ELEV_WIDTH=1.9;ADJUSTED_ELEV_HEIGHT=2.4;ADJUSTED_REMAIN_HALL_DIS=2.83;CORE_VOID_WIDTH=1.25;CORE_VOID_SPECIFIC=1.35;ELEV_DISABLED_MIN_AREA=4;CORRIDOR_WIDE_BY_BUILDING_TYPE=[2,2,1.7,1.5,1.5,1.5,2,2];CORRIDOR_NARR_WIDTH=1.4;INNER_WALL_THICKNESS=.2;OUTER_WALL_THICKNESS=.4;CORE_SEGMENT_GAP_LENGTH=3.;OUTER_WALL_THICKNESS_FOR_VISUALIZE=.3;CURTAIN_WALL_THICKNESS=.2;CURTAIN_WALL_MULLION_THICKNESS=.05;CURTAIN_WALL_PANE_THICKNESS=.05;CURTAIN_WALL_INTERVAL=1.2;CORE_WIDE_TALL_SMALL=[5.55,7.23,5.55];CORE_NARR_TALL_SMALL=[1.6,2.05,3.65];CORE_STR_TALL_SMALL=[Ar,As,At];CORE_WIDE_TALL=[5.55,7.68,5.75];CORE_NARR_TALL=[2.8,2.8,5.15];CORE_STR_TALL=['SlimT',Au,Av];CORE_WIDE_SMALL=[4.2,6.48,4.8];CORE_NARR_SMALL=[1.6,2.05,3.65];CORE_STR_SMALL=[Aw,Ax,Ay];CORE_WIDE=[4.8,6.55,4.4,7.75];CORE_NARR=[2.8,2.8,5.2,2.8];CORE_STR=['Slim','SlimE','WideE',Az];CORE_WIDE_ESCAPE=[7.15,4.8];CORE_NARR_ESCAPE=[4.4,5.15];CORE_STR_ESCAPE=[A_,B0];CORE_WIDE_CENTER_ESCAPE=[8.33,6.4];CORE_NARR_CENTER_ESCAPE=[2.8,5.15];CORE_STR_CENTER_ESCAPE=[B1,B2];CORE_WIDE_ESCAPE_TALL=[7.9,5.55];CORE_NARR_ESCAPE_TALL=[4.4,5.15];CORE_STR_ESCAPE_TALL=[B3,B4];CORE_WIDE_CENTER_ESCAPE_TALL=[9.08,7.15];CORE_NARR_CENTER_ESCAPE_TALL=[2.8,5.15];CORE_STR_CENTER_ESCAPE_TALL=[B5,B6];CORE_WIDE_SPECIFIC_ESCAPE_TALL=[8.25,6.4];CORE_NARR_SPECIFIC_ESCAPE_TALL=[4.2,5.55];CORE_STR_SPECIFIC_ESCAPE_TALL=[B7,B8];CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[10.2,5.5];CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[4.2,7.05];CORE_STR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[B9,BA];ELEV_PERSONS_MAP={Ar:0,As:7,At:7,'SlimT':0,'SlimE':13,'WideE':13,Az:13,Aw:0,Ax:7,Ay:7,'Slim':0,Au:13,Av:13,B5:13,B6:13,B3:13,B4:13,B1:13,B2:13,A_:13,B0:13,B7:16,B8:16,B9:16,BA:16,'EmergencyExit':0};CORE_LYING_NO_CHECK_AREA_MAX=170;CORE_TRANSLATE_RADIUS=2;CORE_TRANSLATE_MAX_TRIALS=20;SMALL_CORE_MAX_AREA=132;SMALL_CORE_MAX_FA=200;UNIT_MIN_WIDTH=2.4;UNIT_MIN_AREA=14;MARKET_MIN_AREA=14;PARTITIONED_MIN_AREA=.001;UNITENTRY_MIN_WIDTH=1.4;WIDECORRIDOR_CHECK_WIDTH=1.6;BALCONY_MIN_LENGTH=2;BALCONY_MAX_WIDTH=1.3;BALCONYUNIT_MIN_WIDTH=2.3;BALCONY_MARGIN=0;POSTPROCESS_PARK_GAP_CHECK=2.49;PARK_MAX_PARKING_EDGE_LEN=2.6;PARK_N_MAX_PARKING_EDGES=3;PARK_CELL_WIDE_PER=5;PARK_CELL_NARR_PER=2.5;PARK_CELL_WIDE_PAR=6;PARK_CELL_NARR_PAR=2;PARK_N_MAX_CELLS=8;PARK_N_FRONT_CELLS=5;PARK_GAP_LOT=2.5;PARK_CHECKER_LENGTH=30;PARK_PLOT_INTERVAL=.1;PARK_CENTERLINE_DIST_PER=6;PARK_CENTERLINE_DIST_PAR=4;PATH_NET_GAP=1;PATH_WIDTH_NARR=1.1;PATH_WIDTH_WIDE=1.7;MAX_TYPE_AREA_LIST_OF_LISTS_OF_LISTS=[[[36,42,45],[55,60,70],[72,76,80]],[[36,42,45],[55,60,70],[72,76,80]],[[16,18,20],[32,36,40],[52,56,60]],[],[],[],[[36,42,45],[55,60,70],[72,76,80]],[[36,42,45],[55,60,70],[72,76,80]]];AREA_COST=[-1e4,700,550,300,150];AREA_COST_COMMERCIAL=640;PACKING_OFFSET_INTERVAL_M=.3;PACKING_SEGMENT_DIVISION_MIN_LENGTH_M=6;PACKING_SEGMENT_DIVISION_UNIT_LENGTH_M=2;PACKING_ROOM_CHECK_BUFFER_M=.05;PACKING_MINIMUM_SEGMENT_LENGTH_M=2;PACKING_LOOP_MAX_NUMBER=10;PACKING_FAR_ADD=.2;PACKING_MAX_RESIDENTIAL_GFA=660;FINAL_DEADSPACE_LENGTH=1.499;TRENCH_FILL_ENTRY_LENGTH=1.1;TRENCH_FILL_LENGTH=3.;MAX_GROUP_PARKING_COUNT=5;OUTER_PARKING_UNDER_TWELVE=12;CENTERLINE_BB_DEADSPACE_LENGTH=3.501;CENTERLINE_BB_OFF_THE_WALL_LENGTH=3.001;RULE_PARKING_SITE_CUT_LENGTH=4.001;FRONT_PARKING_CHECK_INTERVAL=.3;PARKING_PARTITION_COUNT=3;PARKING_GAP_WIDTH=.001;SHIFT_STEP_SINGLE=.5;MINIMUM_OUTER_PARKING_ROAD_WIDTH=[6,4];PARKING_WIDTH=[2.5,6];PARKING_SPOT_HEIGHT=[5,2];PARKING_SPACE_HEIGHT=[-6,-5];PARKING_ADD_ROAD_EDGE_ADDITION_CHECKER=4.999;VEHICLE_ROAD_WIDTH=2.499;MAX_COUNT_WHEN_BACK_PARKING=8;MIN_INNER_PARKING_ROAD_EDGE_LENGTH=2.501;GAP_CHECK_MAX_ANGLE=30;PEDESTRIAN_PATH_WIDTH_ADD=.199;START_PT_OFFSET_DIST=1.25;CORE_EXPAND_DISTANCE=5;PARKING_SCALE_UP_RATIO=1.01;PARKING_SCALE_DOWN_RATIO=.99;CORE_ENTRY_LENGTH=1.2;CORE_ENTRY_SHIFT_LENGTH=.6;BACK_PARKING_SHIFT_MAX_TRIALS=15;MASS_PARK_GAP=.15;PLANES_ENTRY_LENGTH=2;INNER_ROAD_OFFSET_WIDTH=3;WEIGHTED_SHORTEST_PATHS_PENALTY=100;PARAM_Y_SINGLE=10;TRENCH_FILL_LENGTH=3.;RAND_POINTS_NUM=.1;FRONT_PARKING_GROUP_DISTANCE=2.499;RIGHT_ANGLE_DEGREE=90;FILTER_PED_PATH_NETWORK_WITH_PATH=E;FINAL_ADDITION_PLANE_INTERVAL=.5;ROAD_EDGE_ENTRY_MIN_SEG_LENGTH=2.9;PARKING_PATTERN_RANGE_MAX=6;SHIFT_MAX_COUNT=10;RAMP_TYPE_LIST=[0,1];UNDERGROUND_PARKING_GAP_WIDTH=.5;UNDERGROUND_RAMP_OFFSET_LENGTH=5;UNDERGROUND_OFFSET_LENGTH=1;UNDERGROUND_AREA_TOL_ANGLE=30;RAMP_LENGTH=31.8;RAMP_WIDTH_LIST=[3.3,6];RAMP_SUB_LENGTH=6.5;RAMP_BODY_LENGTH=18.8;RAMP_INNER_RADIUS=6.;RAMP_L_TYPE_ADDITIONAL_LENGTH_EACH_SIDE=3.4;MAX_PARKING_COUNT_WHEN_NARROW_RAMP=49;RAMP_ROTATION_CHECK_AREA=5.;RAMP_OBSTACLE_TEST_BUFFER_LENGTH=[5,8];RAMP_OBSTACLE_ALLOW_RATIO_MAXIMUM=.2;UNDERGROUND_MASS_REMOVER_LENGTH=100;UNDERGROUND_MASS_CORE_PLACE_BASEAREA=200;UNDERGROUND_MASS_EXIT_PLACE_BASEAREA=50;UNDERGROUND_EMERGENCY_EXIT_SIZE=1.4;UNDERGROUND_CORE_MAXIMUM_DISTANCE=50;NARROW_UNIT_ENTRY_MAX_RATIO=4;PREVENT_NARROW_ENTRY_ON_SETBACK=F;BUILDING_DIVISION_CORE_LOC_BUFFER_LEN=k;BUILDING_DIVISION_DISTANCE_BETWEEN=4.;BUILDING_DIVISION_LEGAL_GEOM_INNER_SIZE_TEST_LEN=2.6;SIMPLE_REDUCE_RATIO_INTERVAL=.05;SIMPLE_DEADSPACE_LEN=1.4;SIMPLE_MIN_MASS_WIDTH=2.1;SIMPLE_BCR_MARGIN=1.03;SIMPLE_FAR_MARGIN=.0;SIMPLE_FAR_MARGIN_FOR_COMMERCIAL=.3;SIMPLE_MECH_PARK_CHECK_MIN_AREA=3e2;BUILDING_PURPOSE_MAP={w:0,AM:1,x:2,r:3,BB:4,'upmu':5,BC:6,BD:7,BE:8,BF:9};MAX_HOUSING_FLOOR_MAP={w:3,AM:4,x:3,r:0,BB:0,'upmu':0,BC:4,BD:5,BE:0,BF:0};PEDESTRAIN_PATH_WIDTH_BY_BUILDING_TYPE=[1.1,1.7,1.1,1.7,1.5,1.5,1.7,1.7,1.7,1.7];BUILDING_PURPOSE_STR_LIST=['다가구','다세대','다중','상가','판매','업무',AN,'단지형다세대',AO,AP];BUILDING_PURPOSE_GENERAL_SHORT_STR_LIST=['다가구','다세대','다중','근린','판매','업무',AN,'도생(단지형다세대)',AO,AP];BUILDING_PURPOSE_GENERAL_STR_LIST=['다가구주택','다세대주택','다중주택','근린생활시설','판매시설','업무시설',AN,'단지형다세대주택',AO,AP];SIMPLE_CORE_PLACEMENT_MIN_LENGTH=1;SIMPLE_DEFAULT_AVERAGE_AREA=38;SIMPLE_UNIT_AREA_FOR_DAJUNG=25;SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE=.5;SIMPLE_MASS_ASPECT_RATIO_BASEINE=6.;POSTPROCESS_CORRIDOR_ITERATION_COUNT=2;DOOR_SIZE=.9;DOOR_SIZE_LARGE=k;DOOR_MARGIN=.05;DOOR_FRAME_WIDTH=.04;DOOR_FRAME_WIDTH_MARGIN=.01;DOOR_DEADSPACE_AFTER_SETBACK=1.399;DOOR_SETBACK_ITERATION=3;GREEN_POLYGON_MIN_WIDTH=1;GREEN_POLYGON_MARGIN=.3;GREEN_POLYGON_MIN_AREA=35;GREEN_POLYGON_BOUNDARY_WIDTH=2;ESCAPE_CORE_TRUE_AREA=200;MAX_HOUSEHOLDS_NUM_DAGAGU=19;MAX_HOUSEHOLDS_NUM_DAJUNG=20;BINARY_VOID='0';BINARY_SOLID='1';ENGINE_TYPE_LIGHT='light';ENGINE_TYPE_BASIC='basic';RULE_OUTER_NO_PARKING_ADJACENT_DISTANCE=2;SIMPLE_FAR_RESULT_FAR_ADJUSTMENTS=.0001;HAS_CENTERLINE_TRUE_BASELINE=20;LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM=3;LIGHT_LOWER_COMMERCIAL_FLOOR_MAX=3;LIGHT_LOWER_COMMERCIAL_FLOOR_MIN=1;LIGHT_SCORE_FOR_PARKLOT_ERROR=0;BASIC_ERROR_SUBCODE_MAENGJI=50101;BASIC_ERROR_SUBCODE_FAE_ZERO=50102;BASIC_ERROR_SUBCODE_EMPTY_OPTION=50103;PARKING_AREA_DIVISOR=134
def A8(curve,start=0,end=0):A=H(curve.coords);B=A[0][0];C=A[0][1];F=A[1][0];G=A[1][1];I=start/((F-B)**2+(G-C)**2)**.5;K=A[-2][0];L=A[-2][1];D=A[-1][0];E=A[-1][1];M=end/((D-K)**2+(E-L)**2)**.5;N=B-(F-B)*I,C-(G-C)*I;O=D+(D-K)*M,E+(E-L)*M;A[0]=N;A[-1]=O;P=J(A);return P
def T(curve):
	B=H(curve.coords)
	if A(B)==0:return[]
	C=[];D=B[0]
	for F in K(A(B)-1):E=B[F+1];C.append(J([D,E]));D=E
	return C
def a(curve,distance,side,return_offset_line=F):
	C=curve;B=side;A=H(C.coords);I,D=BI(C,distance,B,segment_coords=A,return_coords=E,join_style=2)
	if B==M:0
	elif B==A3:A=A[::-1]
	else:raise c('지원되지 않는 offset 방향입니다.')
	F=G(A+D)
	if return_offset_line:return F,J(D)
	else:return F
def BI(segment,distance,side,segment_coords=C,return_coords=F,join_style=1):
	S=distance;R=segment;K=side;B=segment_coords
	if not B:B=R.coords
	if A(B)==0:return J()
	elif A(B)>2:L=R.parallel_offset(S,K,join_style);return L
	C=B[0][0];D=B[0][1];E=B[1][0];F=B[1][1];I=S/((E-C)**2+(F-D)**2)**.5
	if K==A3:G=I*(F-D);H=-I*(E-C);N=C+G;O=D+H;P=E+G;Q=F+H
	elif K==M:G=-I*(F-D);H=I*(E-C);P=C+G;Q=D+H;N=E+G;O=F+H
	if return_coords:return B,[(N,O),(P,Q)]
	L=J([(P,Q),(N,O)]);return L
def n(polygon):
	F=polygon
	if F.is_empty:return[]
	C=H(F.exterior.coords);E=[(B[0]-C[1:][A-1][0],B[1]-C[1:][A-1][1])for(A,B)in X(C[1:])];J=[(-A,-B)for(A,B)in[E[-1]]+E[:-1]];K=[A4.atan2(A[1],A[0])for A in J];L=[A4.atan2(A[1],A[0])for A in E];G=[B-L[A]for(A,B)in X(K)];B=[A%(2*D.pi)for A in G];I=f(B)
	if I>A(B)*D.pi*2-I:B=[A*-1%(2*D.pi)for A in G]
	B=B+[B[0]];return B
def Q(polygon,tol_angle=.001,tol_length=1e-06,use_simplify=E,container_geometry=C,skip_angle_simplifying_when_interiors=F):
	K=skip_angle_simplifying_when_interiors;J=container_geometry;I=tol_angle;F=tol_length;B=polygon
	if B.is_empty:return B
	if not B.is_valid:
		B=B.buffer(0)
		if L(B,R):B=U(B)
	assert L(B,(G,R)),f"polygon이 Polygon 또는 MultiPolygon type이 아닙니다. 현재 타입은 {type(B)}입니다."
	if L(B,R):
		M=[]
		for O in B.geoms:M.append(Q(O,I,F,skip_angle_simplifying_when_interiors=K))
		return R(M)
	else:
		if K and A(B.interiors)>0:E=B.simplify(F)
		else:
			B=shapely.geometry.polygon.orient(B,sign=k);N=B.simplify(F);H=[]
			for(P,S)in X(n(N)[:-1]):
				if D.abs(S-D.pi)>I:H.append(N.exterior.coords[P])
			if A(H)<3:E=G()
			else:E=G(H)
		if J is not C:E=B if not E.within(J)else E
		return E
def BJ(polygon,vector,return_bb=F):
	E=polygon
	if E.is_empty:A=1;B=G()
	else:B=A9(E,vector);F=T(B.exterior);C,D=F[0].length,F[1].length;A=C/D if C>D else D/C
	if return_bb:return A,B
	return A
def U(inputs):
	B=inputs
	if L(B,G):return B
	elif AD(B,AQ)or L(B,A5):
		C=H(AE(lambda x:L(x,G),B.geoms))
		if A(C)==0:return G()
		E=D.array(C,dtype=object)[D.argmax([A.area for A in C])];return E
	else:return G()
def BK(inputs):
	C=inputs
	if L(C,G):return C,R()
	elif AD(C,AQ)or L(C,A5):
		B=D.array(H(AE(lambda x:L(x,G),C)),dtype=object)
		if A(B)==0:return G(),R()
		E=D.eye(A(B),dtype=bool)[D.argmax([A.area for A in B])];B,F=B[E],B[~E];return B[0],R(H(F))
	else:return G(),R()
def t(lists):
	B=lists
	if L(B,H):
		if A(B)<1:return B
		elif L(B[0],H):return t(B[0])+t(B[1:])
		else:return B[:1]+t(B[1:])
	else:return[B]
def b(polygon,buffer_distance,join_style=N.mitre,use_intersection=E,choose_biggest_polygon=E,choose_biggest_polygon_before_dilation=F):
	G=choose_biggest_polygon;F=join_style;E=buffer_distance;A=polygon
	if A.is_empty:return A
	C=A.buffer(-E,join_style=F)
	if L(C,R)and choose_biggest_polygon_before_dilation:C=U(C)
	B=C.buffer(E,join_style=F)
	if L(B,R)and G:B=U(B)
	if use_intersection and not A.contains(B)and A.is_valid:D=B.intersection(A)
	else:D=B
	if G:H=U(D)
	else:H=D
	return H
def e(polygon,buffer_distance,join_style=N.mitre,use_simplification=E,simplify_tolr=.001,choose_biggest_polygon=E):
	E=simplify_tolr;D=join_style;C=buffer_distance;B=polygon
	if use_simplification:F=B.simplify(E)
	else:F=B
	A=F.buffer(C,join_style=D);A=A.simplify(E);G=A.buffer(-C,join_style=D)
	if choose_biggest_polygon:H=U(G)
	else:H=G
	return H
def A9(bb_original,bb_vec):
	A=bb_original
	if A.is_empty:return G()
	C=D.array([bb_vec]);B=D.degrees(D.arctan2(*C.T[::-1]))%36e1;E=shapely.affinity.rotate(A,-B[0],origin=A.centroid);F=shapely.geometry.box(*E.bounds);H=shapely.affinity.rotate(F,B[0],origin=A.centroid);return H
def AX(polygon,deadspace_len,tolr,core=G(),regulation=G(),building_purpose=C,return_only_splits=F):
	S=building_purpose;Q=regulation;P=deadspace_len;J=polygon;G=tolr;d=T(J.boundary);V=J.buffer(-G);K=[]
	for W in d:
		X=A8(W,start=P,end=P)
		if X.crosses(V):K.append(X)
		else:f=A8(W,start=G,end=G);K.append(f)
	g=shapely.ops.unary_union(K);h=shapely.ops.unary_union(g);i=H(shapely.ops.polygonize(h));I=[A for A in i if not V.disjoint(A)]
	if return_only_splits:return I
	if not core.is_empty:
		j=D.argmax([A.area for A in I]);A=I.pop(j);k=core.buffer(G,join_style=N.mitre)
		for Y in I:
			M=F
			if not Q.is_empty:
				if Q.contains(Y):M=E
			else:M=E
			if M:
				A=shapely.ops.unary_union([A,Y])
				if S is not C:
					if S==r:A=b(polygon=A,buffer_distance=B.TOLERANCE_MARGIN,choose_biggest_polygon=E)
					else:
						O:0;O=[];Z=[A]
						if L(A,R):Z=H(A.geoms)
						for a in Z:
							if not a.disjoint(k):O.append(a)
						A=shapely.ops.unary_union(O)
				A=e(polygon=A,buffer_distance=G,use_simplification=E,choose_biggest_polygon=E)
		if A.is_empty:return J
		return A
	c=U(R(I))
	if c.is_empty:return J
	return c
def BL(geom_one,geom_two,entry_width):
	G=entry_width;E=geom_two;H=geom_one.buffer(B.TOLERANCE_MARGIN,join_style=2)
	if H.disjoint(E):return F
	I=E.exterior;A=I.intersection(H).simplify(B.TOLERANCE);C=[]
	if L(A,J):C=T(A)
	elif L(A,s):
		for K in A.geoms:C+=T(K)
	return any(D.isclose(A.length,G)or A.length>=G for A in C)
def AY(geometry,target_type):
	C=target_type;A=geometry;B=[]
	if L(A,C):B=[A]
	elif AD(A,AQ)or L(A,A5):
		for D in A.geoms:B+=AY(D,C)
	return B
def AZ(geometry):return AY(geometry,G)
def BM(polygon):B=D.array(polygon.exterior.coords);A=B[1:]-B[:-1];C=D.argmax([D.linalg.norm(A)for A in A]);E=D.arctan2(A[C][1],A[C][0]);return E
def Aa(mass,has_piloti,regulation,mmaa):
	C=mass;D=[]
	for B in K(A(C)):
		if B==0 and has_piloti or B==0 and C[B][0].is_empty:D.append([wkt.loads(BG)])
		elif C[B][0].area>=mmaa:C[B]=[C[B][0].intersection(regulation[B])];D.append(C[B])
		else:break
	return D
def BN(mass,core,engine_type,regulation,sdl):
	D=mass
	for F in K(2,A(D)):
		C=D[F][0].intersection(D[F-1][0]);C=Q(C,tol_length=B.TOLERANCE,container_geometry=regulation[F])
		if engine_type==B.ENGINE_TYPE_BASIC:C=C.union(core.buffer(B.TOLERANCE,join_style=N.mitre))
		C=b(polygon=C,buffer_distance=sdl/2,use_intersection=E,choose_biggest_polygon=E);D[F]=[C]
	return D
def AA(polygon):
	B=n(polygon);A=[]
	for C in B:
		if C<D.pi:A.append(1)
		else:A.append(0)
	return A
def AB(polygon,width,policy,time_counter_dict,is_postprocess,tolr_angle,mcd=k,uec=F,llb=C,slb=C):
	X=slb;W=llb;V=policy;R=is_postprocess;N=width;M=tolr_angle;K=polygon;Y=O.process_time()
	if K.is_empty:O.process_time()-Y;return K
	Z=N/mcd;J=AA(K);J=J[:-1];F=H(K.exterior.coords);F=F[:-1];L=[]
	if R:L=H(n(K))
	a=A(J);I=0;b=V==0;c=V==1
	while E:
		if J[I%A(F)]==0 and J[(I+1)%A(F)]==1 and J[(I+2)%A(F)]==0:
			k=P(F[(I-1)%A(F)]);S=P(F[I%A(F)]);d=P(F[(I+1)%A(F)]);l=P(F[(I+2)%A(F)])
			if R:
				m=L[I%A(F)];o=L[(I+1)%A(F)];p=L[(I+2)%A(F)]
				if D.pi/2-M>m%(D.pi/2)>M:I+=1;continue
				if D.pi/2-M>o%(D.pi/2)>M:I+=1;continue
				if D.pi/2-M>p%(D.pi/2)>M:I+=1;continue
			T=S.distance(d);U=k.distance(S)
			if uec:e,f=g([T,U]);h=b and(e<=X and f<=W);i=c and(e<=X or f<=W)
			else:h=b and(T<=N and U<=Z);i=c and(T<=N or U<=Z)
			q=h or i
			if q:
				r=D.array(l.coords[0])-D.array(d.coords[0]);j=D.array(S.coords[0])+r
				if K.contains(P(j)):
					F=H(F);F[I%A(F)]=C;F[(I+1)%A(F)]=AF(j);F[(I+2)%A(F)]=C;J[I%A(F)]=C;J[(I+1)%A(F)]=0;J[(I+2)%A(F)]=C
					if R:L[I%A(F)]=C;L[(I+1)%A(F)]=0;L[(I+2)%A(F)]=C;L=[A for A in L if A is not C]
					if I+2>=A(F):I-=1
					F=[A for A in F if A is not C];J=[A for A in J if A is not C];a-=2;continue
		I+=1
		if I>=a:break
	K=G(F);K=Q(K,tol_length=B.TOLERANCE);O.process_time()-Y;return K
def BO(mass,core,tolr,tolr_angle,regulation,postprocess_emboss_cut_length,time_counter_dict,mcd):
	F=regulation;D=tolr_angle;G=[]
	for(H,I)in X(mass):C=Q(I[0],tol_angle=D,tol_length=B.TOLERANCE,container_geometry=F[H]);A=R([C,core]);A=e(polygon=A,buffer_distance=B.TOLERANCE_MARGIN,use_simplification=E,choose_biggest_polygon=E);A=Q(A,tol_angle=D,tol_length=tolr,container_geometry=F[H]);A=AB(A,postprocess_emboss_cut_length,0,time_counter_dict,E,D,mcd=mcd);C=A.difference(core);C=b(polygon=C,buffer_distance=B.TOLERANCE_SLIVER,use_intersection=E,choose_biggest_polygon=E);G.append([C])
	return G
def BP(mass,tolr_angle,tolr,core,engine_type,sdl,regulation):
	C=[]
	for(D,E)in X(mass):
		A=Q(E[0],tol_angle=tolr_angle,tol_length=tolr,container_geometry=regulation[D])
		if A.is_empty:C.append([A]);continue
		if engine_type==B.ENGINE_TYPE_BASIC and D>0:A=e(shapely.ops.unary_union([A,core]),B.TOLERANCE_MARGIN)
		A=b(A,sdl/2);C.append([A])
	return C
def BQ(mass,core,regulation):
	A=[]
	for H in mass:C=shapely.ops.unary_union([H[0],core]);C=e(polygon=C,buffer_distance=B.TOLERANCE_SLIVER,use_simplification=E,choose_biggest_polygon=E);A.append([C])
	I=l(A.length for A in T(core.boundary))
	for(D,F)in X(A):
		if F[0].is_empty:continue
		G=e(polygon=F[0],buffer_distance=I/2)
		if G.within(regulation[D]):A[D]=[G]
	return A
def BR(regulation,mass_angle):A=shapely.ops.unary_union(regulation);B=shapely.affinity.rotate(A,-mass_angle,(0,0),use_radians=E);C=shapely.ops.unary_union(B).bounds;return C
def BS(mass_polygon):
	for E in n(mass_polygon):A=D.pi/2;C=E%A;assert-B.TOLERANCE_ANGLE<=C<=B.TOLERANCE_ANGLE or A-B.TOLERANCE_ANGLE<=C<=A+B.TOLERANCE_ANGLE
def z(core_segs,mass_boundary,is_using_short_segs,is_core_translate_use=F,existing_hall=G()):
	M=existing_hall;L=mass_boundary;J=[];K=[]
	for Q in core_segs:
		A=Q.geoms
		if A[0].length>=A[1].length:J.append([A[0],A[2]]);K.append([A[1],A[3]])
		else:J.append([A[1],A[3]]);K.append([A[0],A[2]])
	N=AT(H(I(lambda x:x.boundary.centroid,L))).centroid
	if not M.is_empty:N=M.centroid
	if is_using_short_segs:C=K
	else:C=J
	R=H(I(lambda x:[N.distance(A)for A in x],C));S,T=H(m(*I(lambda x:(D.argmin(x),D.argmax(x)),R)));E:0;F:0;E=H(I(lambda x,y:x[y],C,S));F=H(I(lambda x,y:x[y],C,T));O=C[0];U=G(G([*O[0].coords,*O[1].coords]));V=L[-1]-U.buffer(B.TOLERANCE);P=V.buffer(B.TOLERANCE_LARGE)
	if is_core_translate_use:
		W=F[0].within(P);X=not E[0].within(P)
		if W and X:E,F=F,E
	return J,K,E,F
def A0(core,core_type,mass_boundary,use_small_core,is_commercial_area,is_escape_core,is_center_core_placed,is_using_adjusted_core,is_last_gen_core_called=F,is_specific_escape_sub_core=F,is_specific_escape_emgcy_elev_sub_core=F,is_core_translate_use=F,existing_hall=G()):
	o=existing_hall;n=is_using_adjusted_core;m=use_small_core;d=is_core_translate_use;b=core_type;W=core;K=mass_boundary;L=X=P=C;W=H(I(lambda x:shapely.ops.orient(x,sign=k).simplify(B.TOLERANCE),W));e=H(I(lambda x:s(T(x.boundary)),W));Y:0;R,p=BU(m,n);y=[G()]*A(K);A0=[G()]*A(K)
	if b==0:S,f,F,O=z(e,K,is_using_short_segs=E,is_core_translate_use=d);Y=S;Z=F;h=H(I(lambda x:x.parallel_offset(B.HALL_WIDTH,M),Z));L=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords[::-1]])),Z,h));U=O;X=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords])),U,h));P=H(I(lambda x:G(),W))
	elif b==1:S,f,F,O=z(e,K,is_using_short_segs=E,is_core_translate_use=d,existing_hall=o);Y=S;V=F;q=H(I(lambda x:x.parallel_offset(R,M),F));P=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords[::-1]])),V,q));A1=.15;r=H(I(lambda x:x.parallel_offset(B.HALL_WIDTH+A1+R,M),F));L=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords[::-1]])),q,r));U=O;X=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords])),r,U))
	elif b==2:
		A2=bool(m or is_commercial_area or is_center_core_placed and is_escape_core);S,f,F,O=z(e,K,is_using_short_segs=A2,is_core_translate_use=d,existing_hall=o);Y=f;Z=F;h=H(I(lambda x:x.parallel_offset(B.HALL_WIDTH,M),Z));L=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords[::-1]])),Z,h));t=F[0].interpolate(p);A3=O[0].interpolate(O[0].length-p);A4=J([F[0].coords[0],t]);V=[A4 for A in F];V=H(I(lambda x:x.parallel_offset(B.HALL_WIDTH,M),V));u=H(I(lambda x:x.parallel_offset(R,M),V));P=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords[::-1]])),V,u));A5=J([t,F[0].coords[1]]);U=[A5 for A in F];U=H(I(lambda x:x.parallel_offset(B.HALL_WIDTH,M),U));A7=J([O[0].coords[0],A3]);A8=[A7 for A in O];X=H(I(lambda x,y:G(D.concatenate([x.coords,y.coords])),U,A8))
		if n:v=f[0][0].length-B.HALL_WIDTH-R;A9=a(V[0],v,M);w=A9.buffer(B.TOLERANCE,join_style=N.mitre);j=shapely.ops.unary_union([L[0],w]);L=[Q(j,tol_length=B.TOLERANCE)]*A(L);AA=a(u[0],v,M);AB=AA.buffer(B.TOLERANCE,join_style=N.mitre);i=shapely.ops.unary_union([P[0]-w,AB]);P=[Q(i,tol_length=B.TOLERANCE)]*A(P)
	elif b==3:S,_,F,O=z(e,K,is_using_short_segs=E,is_core_translate_use=d);Y=S;l=F[0].parallel_offset(R,M);AC=a(l,B.HALL_WIDTH,M);AD=l.parallel_offset(B.HALL_WIDTH,M);AE=S[0][0].length-B.HALL_WIDTH-R;AF=a(AD,AE,M);AG=l.parallel_offset(B.HALL_WIDTH,M);AH=AT(AG.coords);AI=g(AH.geoms,key=lambda x:x.distance(K[-1].boundary));AJ=J(AI);AK=shapely.ops.substring(AJ,.5,1,normalized=E);AL=B.ADJUSTED_REMAIN_HALL_DIS;AM=AK.buffer(AL,join_style=N.mitre,cap_style=A6.flat);i=a(F[0],R,M);AN=i.buffer(B.TOLERANCE,join_style=N.mitre);x=AM-AN;j=Q(shapely.ops.unary_union([AC,x]),tol_length=B.TOLERANCE);AO=AF-x.buffer(B.TOLERANCE,join_style=N.mitre);P=[i]*A(K);L=[j]*A(K);X=[AO]*A(K)
	else:raise c('FIXME: 잘못된 core type을 전달 받았습니다.')
	L=H(I(lambda x:shapely.ops.orient(x,sign=k).simplify(B.TOLERANCE),L));return L,X,P,W,y,A0,F,O,Y
def BT(hall,mass,core,corridor_entries_direction):
	E=corridor_entries_direction;C=hall;assert A(C)>0;C,E=BW(C[0],E,core);F=[]
	for I in C:J=T(I.boundary);L=g(J,key=lambda x:x.length)[:2];M=[a(A,B.HALL_WIDTH,A3)for A in L];F.append(M)
	O=core.minimum_rotated_rectangle.buffer(B.TOLERANCE)
	for(P,D)in m(mass,F):
		Q=P.buffer(B.TOLERANCE_LARGE,join_style=N.mitre)
		for H in K(A(D)):
			R=D[H].within(Q);S=D[H].within(O)
			if not R or S:D[H]=G()
	return F,E
def BU(use_small_core,is_using_adjusted_core):
	A=B.ELEV_WIDTH;C=B.ELEV_HEIGHT
	if use_small_core:A=B.ELEV_WIDTH_SMALL;C=B.ELEV_HEIGHT_SMALL
	elif is_using_adjusted_core:A=B.ADJUSTED_ELEV_WIDTH;C=B.ADJUSTED_ELEV_HEIGHT
	return A,C
def BV(core,long_hall_segs):
	A=J()
	for C in long_hall_segs:
		D=A8(C,-B.TOLERANCE_MARGIN,-B.TOLERANCE_MARGIN).buffer(B.TOLERANCE)
		if D.intersects(core.boundary):A=C;break
	return A
def BW(hall,corridor_entries_direction,core,corridor_loading=C):
	I=corridor_loading;D=corridor_entries_direction
	if I is not C:
		for(N,O)in X(I):
			if O==0:D[N]=F
	J:0;J=T(hall.boundary);E=g(J,key=lambda x:x.length);P=E[-2:];K=BV(core,P);L=K.is_empty;Q=E[-1].distance(E[-2]);R=a(E[-1],Q,M)
	if not L:H=a(K,B.HALL_WIDTH,A3);H=shapely.ops.orient(H,-k)
	else:D=[F]*A(D)
	G=[]
	for S in D:
		if S:G.append(H)
		elif L:G.append(hall)
		else:G.append(R)
	return G,D
class BX:
	def __init__(A,packed_unit_space,parking_cells,parking_regulation,commercial_type):A._packed_unit_space=packed_unit_space;A._parking_cells=parking_cells;A._parking_regulation=parking_regulation;A._commercial_type=commercial_type
	@o
	def parking_cells(self):return self._parking_cells
	@parking_cells.setter
	def parking_cells(self,value):self._parking_cells=value
	@o
	def packed_unit_space(self):return self._packed_unit_space
	@packed_unit_space.setter
	def packed_unit_space(self,value):self._packed_unit_space=value
	@o
	def parklot_count(self):return A(self.parking_cells)
	@o
	def parking_regulation(self):return self._parking_regulation
	@parking_regulation.setter
	def parking_regulation(self,value):self._parking_regulation=value
	@o
	def commercial_type(self):return self._commercial_type
	@commercial_type.setter
	def commercial_type(self,value):self._commercial_type=value
	@o
	def law_parklot_count(self):return A4.floor(f(f(A.area for A in A)for A in self.packed_unit_space)/self.parking_regulation+.5)
def Bt(res):
	C='use_district';B='field';A=E
	if'준주거지역'in res[B][C]:A=F
	if'일반상업지역'in res[B][C]:A=F
	return A
def BY(polygon):B=polygon;A=BM(B);C=shapely.affinity.rotate(B,-A,(0,0),use_radians=E);D,F,G,H=C.bounds;I=W(D,F,G,H);J=shapely.affinity.rotate(I,A,(0,0),use_radians=E);return J,A
def BZ(polygon):
	F=polygon;G=D.array(F.convex_hull.exterior.coords);J=G[1:]-G[:-1];A=[];B=[]
	for H in J:I=D.arctan2(H[1],H[0]);A.append(I);K=shapely.affinity.rotate(F,-I,(0,0),use_radians=E);L,M,N,O=K.bounds;P=W(L,M,N,O);B.append(P)
	C=D.argmin([A.area for A in B]);Q=shapely.affinity.rotate(B[C],A[C],(0,0),use_radians=E);return Q,A[C]
def Ba(polygon,mass_angle,gss,tolr,time_counter_dict,regulation_bounds):
	m=regulation_bounds;l=mass_angle;Z=polygon;H=tolr;F=gss;z=O.process_time();Z=b(polygon=Z,buffer_distance=B.TOLERANCE_SLIVER,use_intersection=E,choose_biggest_polygon=E);n=shapely.affinity.rotate(Z,-l,(0,0),use_radians=E);R,S,a,c=n.bounds
	if m is not C:R,S,a,c=m
	o=shapely.affinity.translate(n,xoff=-R+F-H,yoff=-S+F-H);p=d(D.ceil((a-R)/F)+2);q=d(D.ceil((c-S)/F)+2);I=D.array(o.exterior.coords);M=[]
	for Q in K(A(I)-1):
		r=J([I[Q],I[Q+1]]);T=I[Q][0]//F*F;U=I[Q][1]//F*F;T=T+F/2;U=U+F/2;e=I[Q+1][0]//F*F;f=I[Q+1][1]//F*F;e=e+F/2;f=f+F/2;A0=e-T;A1=f-U;V=d(round(A0/F));X=d(round(A1/F))
		if V>=0:s=F
		else:s=-F
		if X>=0:t=F
		else:t=-F
		V=abs(V);X=abs(X);M.append(P(T,U));g=T;h=U
		while E:
			if V==0 or X==0:break
			u=g+s;v=h+t;w=P(u,h);A2=r.distance(w);x=P(g,v);A3=r.distance(x)
			if A2<=A3:M.append(w);g=u;V-=1
			else:M.append(x);h=v;X-=1
	A4=J(M);Y=A4.buffer(F/2+H,cap_style=A6.square,join_style=N.mitre);A5=J([M[0],M[-1]]);A7=A5.buffer(F/2+H,cap_style=A6.square);Y=shapely.ops.unary_union([Y,A7]);Y=Y.buffer(-H,join_style=N.mitre);p=d(D.ceil((a-R)/F)+2);q=d(D.ceil((c-S)/F)+2);A8=W(0,0,p*F,q*F);i=AZ(A8.difference(Y));y=[];A9=o.buffer(max([F*.8,B.TOLERANCE_MARGIN]),join_style=N.mitre)
	for j in i:
		if L(j,G)and A9.contains(j):y.append(j)
	i=y;AA,_=BK(i);k=shapely.affinity.translate(AA,xoff=R-F+H,yoff=S-F+H);k=shapely.affinity.rotate(k,l,(0,0),use_radians=E);O.process_time()-z;return k
def Ab(polygon,depth,width,tolr,time_counter_dict):
	X=depth;S=tolr;N=polygon;Y=O.process_time()
	if N.is_empty:O.process_time()-Y;return N
	b=D.pi/2-.1;N=Q(N,tol_angle=b,tol_length=S);J=AA(N);F=H(N.exterior.coords);J=J[:-1];F=F[:-1];R=A(J);I=0
	while E:
		if J[(I+2)%A(F)]==1 and J[(I+3)%A(F)]==1:
			Z=P(F[(I+2)%A(F)]);a=P(F[(I+3)%A(F)])
			if S<=Z.distance(a)<=width:
				c=P(F[(I+1)%A(F)]);d=P(F[(I+4)%A(F)]);T=c.distance(Z);U=a.distance(d)
				if T<=X or U<=X:
					if abs(T-U)<S:
						for L in K(4):F[(I+1+L)%A(F)]=C;J[(I+1+L)%A(F)]=C
						M=0
						for L in K(4):
							if I+1+L>=A(F):M+=1
						I-=M;F=[A for A in F if A is not C];J=[A for A in J if A is not C];R-=4
						if I>=2 and J[I]==1:I-=2;continue
					elif T>U:
						V=D.array(F[(I+4)%A(F)])-D.array(F[(I+3)%A(F)]);e=D.array(F[(I+2)%A(F)])+V;F[(I+2)%A(F)]=AF(e)
						for L in K(2):F[(I+3+L)%A(F)]=C;J[(I+3+L)%A(F)]=C
						M=0
						for L in K(4):
							if I+1+L>=A(F):M+=1
						I-=M;F=[A for A in F if A is not C];J=[A for A in J if A is not C];R-=2;continue
					else:
						V=D.array(F[(I+1)%A(F)])-D.array(F[(I+2)%A(F)]);f=D.array(F[(I+3)%A(F)])+V;F[(I+3)%A(F)]=AF(f)
						for L in K(2):F[(I+1+L)%A(F)]=C;J[(I+1+L)%A(F)]=C
						M=0
						for L in K(4):
							if I+1+L>=A(F):M+=1
						I-=M;F=[A for A in F if A is not C];J=[A for A in J if A is not C];R-=2
						if I>=2 and J[I]==1:I-=2;continue
		I+=1
		if I>=R:break
	W=G(F);W=Q(W,tol_length=B.TOLERANCE);O.process_time()-Y;return W
def Bb(regulation_polygon,grid_polygon,amin,amax):
	N=grid_polygon
	if N.is_empty:return N
	L=AA(N);L=L[:-1];B=H(N.exterior.coords);B=B[:-1];I=y.deepcopy(B)
	for F in K(A(B)):
		if L[F]==1 and L[(F+1)%A(B)]==0 and L[(F+2)%A(B)]==1:
			U=P(B[F]);V=P(B[(F+2)%A(B)]);W=J([U,V])
			if regulation_polygon.contains(W):
				O=D.array(B[F]);X=D.array(B[(F+1)%A(B)]);Y=D.array(B[(F+2)%A(B)]);Q=X-O;R=Y-O;M=D.dot(Q,R)/(D.linalg.norm(Q)*D.linalg.norm(R))
				if M>1:M=1
				elif M<-1:M=-1
				E=D.arccos(M);E=E*180/D.pi
				if E>90:E=E-90
				if E<=45:S=E;T=90-E
				else:T=E;S=90-E
				if S>=amin and T<=amax:I[(F+1)%A(B)]=C
	I=[A for A in I if A];I.append(I[0]);Z=G(I);return Z
def Bc(diagonalized_polygon,dsang,regulation_polygon):
	E=diagonalized_polygon
	if E.is_empty:return E
	B=D.array(E.exterior.coords)[:-1];L=n(E)[:-1];F=y.deepcopy(B)
	for H in K(A(B)):
		I=dsang/180*D.pi
		if D.pi-I<L[H]<D.pi+I:
			M=P(B[(H-1)%A(B)]);N=P(B[(H+1)%A(B)]);O=J([M,N])
			if regulation_polygon.contains(O):F[H]=C
	F=[A for A in F if not D.isnan(A).all()];Q=G(F);return Q
def Bd(obb):
	C=obb;C=shapely.ops.orient(C);B=H(C.exterior.coords)[:-1];F=D.argmin([P(A).y for A in B]);E=[]
	for I in K(A(B)):E.append(B[(F+I)%A(B)])
	E.append(B[F]);J=G(E);return J
def AC(obb,cutting_policy,core):
	H=obb;G=cutting_policy;B=core;H=Bd(H);A=T(H.boundary)
	if G==0:
		E,C,F=A[2],A[0],A[1]
		if A[1].length>A[2].length:E,C,F=A[1],A[3],A[2]
		D=E;K=F.length
		if not B.is_empty:
			if C.distance(B)>D.distance(B):D=C
	elif G==1:
		E,C,F=A[2],A[0],A[1]
		if A[1].length<A[2].length:E,C,F=A[1],A[3],A[2]
		D=E;K=F.length
		if not B.is_empty:
			if C.distance(B)>D.distance(B):D=C
	elif G==2:
		I,L=A[2],A[0];J,M=A[1],A[3]
		if not B.is_empty:
			if I.distance(B)<L.distance(B):I=L
			if J.distance(B)<M.distance(B):J=M
		return I,J
	else:raise ValueError(f"cut_policy value is invalid: {G}")
	return D,K
def Ac(mass_polygon,target_area):
	E=mass_polygon;G,H,I,A=E.bounds;J=A-H;B=1;C=100
	while B<=C:
		D=(B+C)//2;K=W(G,A-J*(D/100),I,A);F=E.difference(K)
		if F.area>target_area:B=D+1
		else:C=D-1
	return F
def Ad(mass_polygon,obb,target_area,core=G()):
	E,F=AC(obb=obb,cutting_policy=0,core=core);A=1;B=100
	while A<=B:
		C=(A+B)//2;G=a(E,F*(C/100),M);D=mass_polygon.difference(G)
		if D.area>target_area:A=C+1
		else:B=C-1
	return D
def Be(mass_polygon,obb,target_area,core=G()):
	E,F=AC(obb=obb,cutting_policy=1,core=core);A=1;B=100
	while A<=B:
		C=(A+B)//2;G=a(E,F*(C/100),M);D=mass_polygon.difference(G)
		if D.area>target_area:A=C+1
		else:B=C-1
	return D
def Ae(mass_polygon,obb,target_area,core=G()):
	F,G=AC(obb=obb,cutting_policy=2,core=core);C=1;D=100
	while C<=D:
		A=(C+D)//2;E=a(F,G.length*(A/100),M);B=mass_polygon.difference(E);E=a(G,F.length*(A/100),M);B=B.difference(E)
		if B.area>target_area:C=A+1
		else:D=A-1
	return B
def A1(regulation_polygon,floor_polygon,obb,bcr,cut_policy,bcm,iav,mass_angle=C,is_premium=F,core=G()):
	J=regulation_polygon;I=core;H=mass_angle;G=cut_policy;F=obb;A=floor_polygon
	if H is not C:F=A9(A,(D.cos(H),D.sin(H)))
	B=J.area*bcr*bcm
	if iav:B=J.area
	E=A
	if E.area>B or is_premium:
		if G==0:E=Ac(A,B)
		elif G==1:E=Ad(A,F,B,I)
		elif G==2:E=Be(A,F,B,I)
		elif G==3:E=Ae(A,F,B,I)
		else:raise c('FIXME: invaild input for cut policy')
	return E
def Bf(regulation_polygon,obb,floors,max_far_with_margin,smallest_core_area,cut_policy,mmaa,has_piloti,building_purpose,iav,elev_area_for_advantage,use_small_core):
	N=smallest_core_area;J=cut_policy;I=floors;G=regulation_polygon.area*max_far_with_margin
	if use_small_core:G=l(G,B.SMALL_CORE_MAX_FA)
	if building_purpose in(x,w,AM):G*=1.3
	G=G-N;D=[];L=0;O=0;P=F
	for M in K(A(I)):
		D.append(I[M])
		if M!=0 or not has_piloti:L+=I[M].area-elev_area_for_advantage
		if L>G:O=L-G;P=E;break
	if not P:return I,E,10000
	H=D[-1].area-O
	if iav:return D,F,H
	if H<N:return D[:-1],C,C
	if J==0:D[-1]=Ac(D[-1],H)
	elif J==1:D[-1]=Ad(D[-1],obb,H)
	elif J==2:D[-1]=Ae(D[-1],obb,H)
	if D[-1].area<mmaa+6.72:D=D[:-1]
	return D,C,C
def Bg(parcel,road_edges):
	B=[];C=parcel.exterior.coords
	for(E,F)in m(C[:-1],C[1:]):
		D=J([E,F])
		if not road_edges.contains(D):B.append(D)
	if A(B)==1:return B[0]
	else:return shapely.ops.linemerge(shapely.ops.unary_union(B))
def Af(area,road_edge_list,width):
	C=width;A=area;F=[A.buffer(C+B.EPSILON)for A in road_edge_list]
	if L(A,G):A=R([A])
	D=[]
	for E in A.geoms:
		H=b(E,C)
		for I in F:
			if H.intersects(I):D.append(E);break
	return R(D)
def Bh(possible_core,possible_core_type,rotated_floors,floors_result,use_small_core,is_commercial_area):D=possible_core;C=floors_result;B=rotated_floors;E=A0([D]*A(B[:A(C)]),possible_core_type,B[:A(C)],use_small_core,is_commercial_area,is_escape_core=F,is_center_core_placed=F,is_using_adjusted_core=F)[0];G=[F]*A(B[:A(C)]);H,I=BT(E,B[:A(C)],D,G);return any(all(A.is_empty for A in A)for A in H)
def Ag(buffered_top_floor,core_corner,core_size,core_type,allow_outside=F):
	I=core_type;H=buffered_top_floor;A,B=core_corner;C,D=core_size;F=[];G=[];J=[W(A,B,A+C,B+D),W(A,B,A+C,B-D),W(A,B,A-C,B+D),W(A,B,A-C,B-D),W(A,B,A+D,B+C),W(A,B,A-D,B+C),W(A,B,A+D,B-C),W(A,B,A-D,B-C)]
	for E in J:
		if E.within(H):F.append(E);G.append(I)
		elif allow_outside:
			K=E.intersection(H)
			if K.area/E.area>=.9:F.append(E);G.append(I)
	return F,G
def Bi(floors,mass_angle,tolr,sdl,gss,refined_site,road_edge,is_commercial_area,use_small_core,mass_config,regulation):
	AI='Polygon';p=road_edge;o=sdl;k=tolr;j=floors;d=mass_angle;Y=refined_site;I=mass_config
	if not I.is_escape_core:
		q=[];r=[];q.append(I.csl[0]);r.append(I.ctl[0])
		for O in K(A(I.csl)):
			if O>1:
				if I.csl[O][0]<I.csl[0][0]or I.csl[O][1]<I.csl[0][1]:q.append(I.csl[O]);r.append(I.ctl[O])
		I.csl=q;I.ctl=r
	Z=y.deepcopy(j);S=[shapely.affinity.rotate(A,-d,(0,0),use_radians=E)for A in j];S=[A.simplify(B.TOLERANCE)for A in S];AJ=[shapely.affinity.rotate(A,-d,(0,0),use_radians=E)for A in regulation];e=A(S)-1;a=C
	for V in Am(S):
		if e==0:return[[G(),j,0,G(),0]]
		Q=D.array(V.exterior.coords);Q=Q[:-1];AK=n(V);w=[]
		for O in K(A(Q)):
			if not AK[O]<D.pi/2*.999:w.append(Q[O])
		Q=w
		if I.acac and not I.is_sub_core_necessary:
			AL=l(l(A)for A in I.csl);AM=T(V.exterior)
			for x in AM:
				if x.length>B.CORE_SEGMENT_GAP_LENGTH+AL+B.CORE_SEGMENT_GAP_LENGTH:Q.append(D.array(x.centroid.coords[0]))
		z=[];A0=S[e-1];t=A0.difference(V);t=b(polygon=t,buffer_distance=gss/2,use_intersection=E,choose_biggest_polygon=F);A1=[]
		for(AN,A3)in X(Q):
			AO=P(A3);A4=AO.buffer(k)
			if A4.disjoint(t):
				if not A4.disjoint(A0):z.append(A3);A1.append(AN)
		e-=1;A5=[];A6=[];AP=[];AQ=[];A8=V.buffer(k);A9=T(V.boundary)
		for(u,AA)in m(z,A1):
			if AA<A(A9):
				AR=A9[AA]
				if AR.length<B.SIMPLE_CORE_PLACEMENT_MIN_LENGTH:continue
			for(AS,v)in m(I.csl,I.ctl):
				AT,AU=Ag(A8,u,AS,v);A5.extend(AT);A6.extend(AU)
				if I.is_sub_core_necessary:
					AV=[A for A in Q if not D.isclose(A,u).all()];AW=g(AV,key=lambda x,c=u:D.linalg.norm(x-c),reverse=E);AX=AW[:3]
					for AY in AX:
						AZ=I.sub_csl[v-1];Aa,Ab=Ag(A8,AY,AZ,v,allow_outside=E);AB=[];AC=[]
						for(AD,Ac)in m(Aa,Ab):
							if AD.within(AJ[e].buffer(B.TOLERANCE)):AB.append(AD);AC.append(Ac)
						AP.extend(AB);AQ.extend(AC)
		c=[]
		for(R,AE)in m(A5,A6):
			U=E;M=G();f=C
			for Ad in S[:A(Z)]:
				J=A2(Ad,shapely.ops.unary_union([R,M]),o,use_simplify=F)
				if not U:break
				Ae=J.buffer(B.TOLERANCE_MARGIN,join_style=N.mitre)
				if A(H(Ae.interiors))!=0:U=F;break
				if J.disjoint(R.buffer(B.TOLERANCE_MARGIN,join_style=N.mitre)):U=F;break
				if J.area<I.mmaa:U=F;break
				Ai,Aj,Ak,Al=J.bounds
				if Ak-Ai<I.mmw or Al-Aj<I.mmw:U=F;break
				if I.has_elevator and not Ah(R,J,k,I.cccm):U=F;break
			if not U:continue
			if Bh(R,AE,S,Z,use_small_core,is_commercial_area):continue
			R=shapely.affinity.rotate(R,d,(0,0),use_radians=E);M=shapely.affinity.rotate(M,d,(0,0),use_radians=E);W=Bg(Y,p);W=W if L(W,s)else s([W]);An=shapely.ops.unary_union([*W.geoms,R,M]);h=Y.convex_hull.difference(W.buffer(B.VEHICLE_ROAD_WIDTH/2,join_style=2)).intersection(Y);h=Af(h,p.geoms,B.VEHICLE_ROAD_WIDTH/2);Ao=1 if h.geom_type==AI else A(h.geoms);Ap=An.buffer(B.VEHICLE_ROAD_WIDTH/2,join_style=2);i=Y.convex_hull.difference(Ap).intersection(Y);i=Af(i,p.geoms,B.VEHICLE_ROAD_WIDTH/2);Aq=1 if i.geom_type==AI else A(i.geoms)
			if Ao!=Aq:continue
			c.append([R,J,AE,M,f])
		if A(c)==0:Z=Z[:-1];continue
		a,_,AF,M,f=c[D.argmax([A[1].area for A in c])];break
	if a is C:raise A7('코어 배치에 실패하였습니다.')
	Ar=g(c,key=lambda x:x[1].area,reverse=E)[:B.LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM];AG=[]
	for As in Ar:
		a,_,AF,M,f=As;AH=[]
		for At in Z:
			J=A2(At,a,o)
			if I.is_sub_core_necessary:J=A2(J,M,o)
			AH.append(J)
		AG.append([a,AH,AF,M,f])
	return AG
def Ah(core,mass,tolr,cccm):
	B=tolr;A=mass;D=T(core.boundary);C=g(D,key=lambda x:x.length,reverse=E)
	if cccm:
		if C[0].centroid.buffer(B).disjoint(A)and C[1].centroid.buffer(B).disjoint(A):return F
	elif all(C.centroid.buffer(B).disjoint(A)for C in C):return F
	return E
def A2(floor,core,sdl,use_simplify=E):
	D=sdl;A=floor.difference(core);C=A.buffer(-D/2,join_style=N.mitre);C=U(C);A=C.buffer(D/2,join_style=N.mitre).intersection(A);A=U(A)
	if use_simplify:A=Q(A,tol_length=B.TOLERANCE)
	return A
def u(archi_line,each_floor_regulation,preset,mcl,gss,tolr,tolr_angle,dsang,amin,amax,pacc,time_counter_dict,preset_mass_dict,mass_angle=C,mcd=k,fill_gap=E,regulation_bounds=C,ecp=0,uec=F,llb=C,slb=C):
	R=mcd;P=preset_mass_dict;N=tolr_angle;M=mcl;L=preset;J=time_counter_dict;I=tolr;H=gss;E=each_floor_regulation;B=mass_angle;K:0;B:0
	if B is not C:K=A9(E,(D.cos(B),D.sin(B)))
	elif L.bbc==0:K,B=BY(E)
	elif L.bbc==1:K,B=BZ(E)
	else:raise c('FIXME: invaild input for bounding box creation')
	S=B,E.wkt;T=P.get(S)
	if T is not C:V,G=T;A=wkt.loads(V)
	else:
		G=[];A=Ba(E,B,H,I,J,regulation_bounds);G.append(A)
		if fill_gap:
			U=Q(e(A,H))
			if E.contains(U):A=U
		A=Ab(A,H*10000,M,I,J);G.append(A);A=AB(A,M,ecp,J,F,N,mcd=R,uec=uec,llb=llb,slb=slb);G.append(A);A=Ab(A,H+I,H*10000,I,J);A=AB(A,H+I,1,J,F,N,mcd=R);G.append(A);P[S]=A.wkt,G
	W=O.process_time();O.process_time()-W;BS(A)
	if L.dcg==1:A=Bb(E,A,amin,amax);A=Bc(A,dsang,E)
	A=A.buffer(0);G.append(A);return A,G,K,B
def Bj(archi_line,regulation,preset,mcl,gss,tolr,time_counter_dict,preset_mass_dict,bcr,mass_config):
	T=regulation;Q=bcr;P=preset_mass_dict;O=time_counter_dict;N=tolr;M=gss;L=mcl;I=preset;F=archi_line;A=mass_config
	if not A.iav:G,V,J,K=u(F,T[0],I,L,M,N,A.tolr_angle,A.dsang,A.amin,A.amax,A.pacc,O,P,mcd=A.mcd,ecp=A.ecp,uec=A.uec,llb=A.llb,slb=A.slb);G=A1(F,G,J,Q,I.cpc,A.bcm,A.iav)
	else:
		D=T[:];R=0
		while E:
			G,V,J,K=u(F,D[0],I,L,M,N,A.tolr_angle,A.dsang,A.amin,A.amax,A.pacc,O,P,mcd=A.mcd,ecp=A.ecp,uec=A.uec,llb=A.llb,slb=A.slb)
			if G.area<=F.area*Q*A.bcm or R>d(1/B.SIMPLE_REDUCE_RATIO_INTERVAL):break
			else:R+=1;Y=shapely.affinity.scale(F,1-R*B.SIMPLE_REDUCE_RATIO_INTERVAL);D[0]=A1(Y,D[0],J,Q,I.cpc,A.bcm,A.iav);D[0]=U(D[0])
		D[1:]=[A.intersection(D[0])for A in D[1:]];D[1:]=[U(A)for A in D[1:]];D=H(AE(lambda x:not x.is_empty,D));W=[G];S=C
		if A.usg:S=BR(D,K)
		for Z in D[1:]:
			try:a,X,X,X=u(F,Z,I,L,M,N,A.tolr_angle,A.dsang,A.amin,A.amax,A.pacc,O,P,K,mcd=A.mcd,regulation_bounds=S,ecp=A.ecp,uec=A.uec,llb=A.llb,slb=A.slb);W.append(a)
			except c:pass
	return W,G,V,J,K,D,S
def Bk(archi_line,bounding_box,mass,max_far_with_margin,smallest_core_area,preset,has_piloti,building_purpose,regulation_cut,mass_angle,mcl,gss,tolr,time_counter_dict,preset_mass_dict,regulation_bounds,mass_config,elev_area_for_advantage,use_small_core):
	P=mass_angle;O=bounding_box;N=archi_line;K=regulation_cut;J=preset;I=smallest_core_area;D=mass_config;C=mass;Q=[]
	for T in C:
		R=b(T,D.sdl)
		if R.is_empty:break
		else:Q.append(R)
	C=Q;C,V,G=Bf(N,O,C,max_far_with_margin,I,J.cpc,D.mmaa,has_piloti,building_purpose,D.iav,elev_area_for_advantage,use_small_core)
	if D.iav and not V:
		W=K[A(C)-1];L=1;M=1/B.SIMPLE_REDUCE_RATIO_INTERVAL-1
		try:
			while E:
				if L<M:F=(L+M)//2
				elif C[-1].area>G:F=F+1
				else:break
				X=shapely.affinity.scale(W,1-F*B.SIMPLE_REDUCE_RATIO_INTERVAL);H=A1(X,K[A(C)-1],O,0,J.cpc,0,D.iav,P);H=U(H);C[-1],S,S,S=u(N,H,J,mcl,gss,tolr,D.tolr_angle,D.dsang,D.amin,D.amax,D.pacc,time_counter_dict,preset_mass_dict,P,mcd=D.mcd,regulation_bounds=regulation_bounds)
				if C[-1].area>G:L=F+1
				else:M=F-1
			K[A(C)-1]=H
		except c:pass
		if C[-1].area>G:C=C[:-1]
		elif G<I:C=C[:-1]
		elif C[-1].area<D.mmaa+I:C=C[:-1]
	return C
def Bl(mass,mass_angle,tolr,engine_type,gss,refined_site,road_edge,is_commercial_area,use_small_core,has_piloti,archi_line,regulation,max_far_with_margin,bcr,mass_config):
	Q=use_small_core;P=is_commercial_area;I=mass_config;H=mass;g=Bi(H,mass_angle,tolr,I.sdl if engine_type==B.ENGINE_TYPE_LIGHT else B.TOLERANCE,gss,refined_site,s([A['edge_geom']for A in road_edge['edges']]),P,Q,I,regulation);Y=[]
	for h in g:
		L,H,Z,a,c=h
		if L.is_empty:continue
		if has_piloti:d=[[G()]]+[[A]for A in H[1:]]
		else:d=[[A]for A in H]
		M=d;i,j,k,R,S,S,m,S,n=A0([L],Z,H,Q,P,is_escape_core=I.is_escape_core,is_center_core_placed=F,is_using_adjusted_core=F,is_last_gen_core_called=E);o=J(D.array(m[0].coords)).wkt
		if I.is_escape_core:
			N=b(L-R[0],B.TOLERANCE_MARGIN)
			if not N.is_empty:
				O=l(T(N.exterior),key=lambda s:s.length).length;O+=B.TOLERANCE_MARGIN;O/=2
				for(U,V)in X(H):K=e(shapely.ops.unary_union([V,N]),B.TOLERANCE_MARGIN);K=b(K,O);H[U]=K
				for(U,V)in X(M):K=e(shapely.ops.unary_union([V[0],N]),B.TOLERANCE_MARGIN);K=b(K,O);M[U][0]=K
				L=R[0]
		W=[H,M,[G()],[G()],[G()],[G()],[G()],[G()],G(),J().wkt,C,C]
		if I.is_sub_core_necessary:p,q,r,t,u,v,w,S,x=A0([a],c,H,Q,P,is_escape_core=I.is_escape_core,is_center_core_placed=F,is_using_adjusted_core=F,is_specific_escape_sub_core=I.is_specific_escape_sub_core,is_specific_escape_emgcy_elev_sub_core=I.is_specific_escape_emgcy_elev_sub_core,is_last_gen_core_called=E);y=J(D.array(w[0].coords)).wkt;W=[H,M,p,q,r,t,u,v,a,y,c,x]
		f=[H,M,i,j,k,[G()],[G()],R,L,o,Z,n];assert A(f)==A(W);Y.append([f,W])
	return Y
def Ai(mass_for_parklot_check,law_parklot_count,estimated_parklot_count,parklot_datas,underground_parking_boundaries,regulation_cut,bounding_box,mass_generation_preset,mass_config,mass_angle,core,hall_geom,stair_geom,elev_geom,archi_line,time_counter_dict,preset_mass_dict,regulation_bounds,engine_type,building_purpose,parking_commercial,commercial_type,first_floor_reduce_area,has_piloti,packed_unit_space_area_test_set_index,packed_unit_space_equal_division,packed_unit_space_sequantial,res,env_plan):
	c=mass_angle;X=estimated_parklot_count;V=packed_unit_space_sequantial;T=packed_unit_space_area_test_set_index;S=packed_unit_space_equal_division;Q=building_purpose;P=mass_generation_preset;O=parklot_datas;M=law_parklot_count;J=regulation_cut;I=core;H=env_plan;G=mass_config;C=mass_for_parklot_check;W=0;l=I.buffer(B.TOLERANCE_MACRO,join_style=N.mitre);e=J[A(C)-1];Y=F;G.is_sub_core_necessary=Y;m=A(AZ(I));Z=D.inf
	if Q==w:Z=B.MAX_HOUSEHOLDS_NUM_DAGAGU
	elif Q==x:Z=B.MAX_HOUSEHOLDS_NUM_DAJUNG
	while M>X or G.is_sub_core_necessary and m==1 or Q in(x,w)and A([A for B in H.packed_unit_space for A in B if not A.is_empty])>Z:
		if A(C)<=3:break
		n=C[-1][:];W+=1;o=shapely.affinity.scale(e,1-W*B.SIMPLE_REDUCE_RATIO_INTERVAL);J[A(C)-1]=A1(o,J[A(C)-1],bounding_box,0,P.cpc,0,iav=E,mass_angle=c,core=I);J[A(C)-1]=U(J[A(C)-1]);K,g,g,g=u(archi_line,J[A(C)-1],P,P.mcl,P.gss,P.tolr,G.tolr_angle,G.dsang,G.amin,G.amax,G.pacc,time_counter_dict,preset_mass_dict,c,mcd=G.mcd,regulation_bounds=regulation_bounds);K=A2(K,I,G.sdl if engine_type==B.ENGINE_TYPE_LIGHT else B.TOLERANCE);C[-1]=[K];a=[I]
		if L(I,R):a=I.geoms
		h=E
		for b in a:
			if not BL(K,b,B.UNITENTRY_MIN_WIDTH):h=F;break
		i=E
		if G.has_elevator:
			for b in a:
				if not Ah(b,K,P.tolr,G.cccm):i=F;break
		if K.area<G.mmaa or W>=d(1/B.SIMPLE_REDUCE_RATIO_INTERVAL)or l.disjoint(K)or not h or G.has_elevator and not i or B.BUILDING_PURPOSE_MAP[Q]>=3 and(M-X)*B.PARKING_AREA_DIVISOR>f(A.area for A in n):
			C=C[:-1];e=J[A(C)-1];W=0
			if commercial_type>0:H.commercial_type=max(H.commercial_type-1,B.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN+d(has_piloti))
		S,V=C,C;H.packed_unit_space=S
		if B.BUILDING_PURPOSE_MAP[Q]in[r]:H.commercial_type=A(S)
		j=H.law_parklot_count;H.packed_unit_space=V;k=H.law_parklot_count
		if j<=k:M=j;T=0
		else:M=k;T=1
		Y=F;G.is_sub_core_necessary=Y
	p=[[A.area for A in A]for A in S];q=[[A.area for A in A]for A in V];s=[p,q];H.packed_unit_space=[S,V][T];O[0]=X;O[1]=M;O[2]=s;O[3].append(f(A.area for A in t(C))+I.area*A(C));O[4]=T;return C,O,H,M
def Bm(use_mech_parking,use_under_parking,core_list,hall_geom,stair_geom,elev_geom,parking_result_dict,refined_site,archi_line,road_edge,mass,building_purpose,is_flag_lot,max_far,core,regulation_cut,bounding_box,mass_generation_preset,time_counter_dict,preset_mass_dict,mass_angle,engine_type,mass_after_pack,first_floor_reduce_area,estimated_parklot_count,regulation_bounds,mass_config,commercial_type,sub_core_related_geoms,res):
	N=commercial_type;M=mass_config;H=estimated_parklot_count;F=res;D=mass_after_pack;U=F[V][Z][0];F[Y][j];F[Y][Ao];W=F[Y][AH];X=[];a=J();b=C;c=J();d=C;u=G();G();G();G();v=[];e=[];w=[];x=[];g=[];h,i,k,l,m,n=sub_core_related_geoms;O=shapely.ops.unary_union([core,h]);o=shapely.ops.unary_union([hall_geom,i,m]);p=shapely.ops.unary_union([stair_geom,k]);q=shapely.ops.unary_union([elev_geom,l,n]);I=[H,0,[],[f(A.area for A in t(D))+O.area*A(D)],0,X]
	if M.bsc:
		K=D;P,Q=K,K;E=BX(P,[C]*H,B.PARKING_AREA_DIVISOR,N);R=E.law_parklot_count;E.packed_unit_space=Q;S=E.law_parklot_count
		if R<=S:L=R;T=0
		else:L=S;T=1
		D,I,E,L=Ai(K,L,H,I,e,regulation_cut,bounding_box,mass_generation_preset,M,mass_angle,O,o,p,q,archi_line,time_counter_dict,preset_mass_dict,regulation_bounds,engine_type,building_purpose,W,N,first_floor_reduce_area,U,T,P,Q,F,E);mass=D
	r=C;s=C;return I,D,mass,E,a,b,r,s,g,c,d
def Bn(mass,has_piloti,mmaa,regulation,umis,engine_type,sdl,core,usep,tolr_angle,tolr,postprocess_emboss_cut_length,time_counter_dict,mcd,used,first_floor_reduce_area,urpa,mab,mass_bb_slb,is_mech_park_weight_needed,env_plan):
	L=env_plan;K=tolr;J=tolr_angle;I=mmaa;G=sdl;F=engine_type;E=has_piloti;D=regulation;C=core;A=mass;A=Aa(A,E,D,I)
	if umis:A=BN(A,C,F,D,G)
	if usep:A=BO(A,C,K,J,D,postprocess_emboss_cut_length,time_counter_dict,mcd)
	elif E:A[0]=[wkt.loads(BG)]
	if used:
		M=l(T(C.exterior),key=lambda s:s.length).length;N=G
		if M<=G:N=M-B.TOLERANCE
		A=BP(A,J,K,C,F,N,D)
	A=Aa(A,E,D,I);H=Ak(C,A,first_floor_reduce_area,E,urpa,F==B.ENGINE_TYPE_BASIC)
	if is_mech_park_weight_needed:H*=B.MECH_PARK_SCORE_WEIGHT_FACTOR_LIGHT
	if L.law_parklot_count>L.parklot_count:H=B.LIGHT_SCORE_FOR_PARKLOT_ERROR
	if F==B.ENGINE_TYPE_BASIC:A=BQ(A,C,D)
	A=Bp(A,C,mab,mass_bb_slb);return A,H
def Aj(engine_type,res,score,core,hall_geom,stair_geom,elev_geom,sub_core,sub_hall_geom,sub_stair_geom,sub_elev_geom,sub_core_attached_room,sub_core_emergency_elev,sub_path,sub_path_poly,mass,mass_angle,intermediate_results,parklot_datas,first_floor_reduce_area,path,path_poly,road_edge,core_type,sub_core_type,core_orientation,mech_park_visual_data,under_parking_visul_data,error_type,elev_area_for_advantage,env_plan,summary_is_escape_core,use_small_core,has_elevator,is_commercial_area,has_commercial,is_specific_escape_sub_core,is_specific_escape_emgcy_elev_sub_core,regulation,parking_objects_list_of_list,visualize_inside_get_mass):A=regulation;return{'score':score,AR:mass,AS:core,'regulation':A,'hall_geom':hall_geom,'stair_geom':stair_geom,'elev_geom':elev_geom,'mass_angle':mass_angle,'intermediate_results':intermediate_results,'parklot_datas':parklot_datas,'first_floor_reduce_area':first_floor_reduce_area,'path':path,'path_poly':path_poly,'road_edge':road_edge,'legal_geom':A,'core_type':core_type,'core_orientation':core_orientation,'error_type':error_type,'elev_area_for_advantage':elev_area_for_advantage,An:use_small_core}
def Ak(core,mass,first_floor_reduce_area,has_piloti,urpa,is_engine_type_basic):
	B=mass
	if A(B)==0:raise c(BH)
	else:C=Bo(core,B,first_floor_reduce_area,has_piloti,urpa,is_engine_type_basic);C-=core.area*A(B);D=C
	return D
def Bo(core,mass,first_floor_reduce_area,has_piloti,urpa,is_engine_type_basic):
	D=mass
	if D is C or A(D)==0:return 0
	E=f(f(A.area for A in A)for A in D)
	if not urpa:
		F=f(A.area for A in D[0])
		if not has_piloti:
			G=max(0,F-first_floor_reduce_area)
			if G>=B.UNIT_MIN_AREA:E+=G
		else:E-=F
	if not is_engine_type_basic:E+=core.area*A(D)
	return E
def Bp(mass,core,mab,mass_bb_slb):
	C=D.array(T(core.exterior)[0].coords);H=C[1]-C[0];B=[]
	for(I,A)in X(mass):
		if I==0:B.append(A);continue
		J,K=BJ(A[0],H,return_bb=E);L=g([A.length for A in T(K.exterior)])[0];F=E;G=E;F=L>=mass_bb_slb;G=J<mab
		if not A[0].is_empty and(G or F):B.append([Q(A[0])])
	return B
def Bq(original_mass,regulation,tolr,tolr_angle,sdl):
	J=sdl;I=regulation;H=tolr;L=[]
	for D in original_mass:D=U(D);D=b(polygon=D,buffer_distance=H,use_intersection=E,choose_biggest_polygon=E);L.append(D)
	C=L;M=[]
	for(O,P)in X(C):R=Q(P,tol_angle=tolr_angle,tol_length=B.TOLERANCE,container_geometry=I[O]);M.append(R)
	C=M
	for F in K(1,A(C)):
		N=C[F].intersection(C[F-1]);G=e(polygon=N,buffer_distance=B.SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE)
		if not G.within(I[F]):C[F]=Q(N);continue
		while A(AX(polygon=G,deadspace_len=J,tolr=H,return_only_splits=E))>1:G=AX(polygon=G,deadspace_len=J,tolr=H)
		C[F]=Q(G)
	return C
def Al(e,first_floor_reduce_area,road_edge,engine_type):
	A=str(e)
	if A=='주차 대수가 0대입니다.':B='parking_failed'
	elif A==BH:B='mass_creation_failed'
	elif A=='기계식주차 배치 실패로 중복 결과가 생성됩니다.':B='duplicate_result_mech_park'
	elif A=='저층상가 배치 실패로 중복 결과가 생성됩니다.':B='duplicate_result_lower_commercial'
	else:B=A
	D=Aj(engine_type=engine_type,res=C,score=-10000,core=C,hall_geom=C,stair_geom=C,elev_geom=C,sub_core=C,sub_hall_geom=C,sub_stair_geom=C,sub_elev_geom=C,sub_core_attached_room=C,sub_core_emergency_elev=C,sub_path=C,sub_path_poly=C,mass=C,mass_angle=C,intermediate_results=C,parklot_datas=C,first_floor_reduce_area=first_floor_reduce_area,path=C,path_poly=C,road_edge=road_edge,core_type=C,sub_core_type=C,core_orientation=C,mech_park_visual_data=C,under_parking_visul_data=C,error_type=B,elev_area_for_advantage=0,env_plan=C,summary_is_escape_core=F,use_small_core=F,has_elevator=F,is_commercial_area=F,has_commercial=F,is_specific_escape_sub_core=F,is_specific_escape_emgcy_elev_sub_core=F,regulation=C,parking_objects_list_of_list=C,visualize_inside_get_mass=F);return D
def Br(mass_generation_preset,refined_site,archi_line,regulation,building_purpose,time_counter_dict,postprocess_emboss_cut_length,estimated_parklot_count,first_floor_reduce_area,preset_mass_dict,parking_result_dict,road_edge,use_small_core,is_commercial_area,is_flag_lot,use_mech_parking,use_under_parking,custom_config,engine_type,mass_config,res,commercial_type,visualize_inside_get_mass):
	A9=use_mech_parking;A8=refined_site;o=commercial_type;f=preset_mass_dict;b=is_commercial_area;a=road_edge;X=time_counter_dict;R=use_small_core;P=building_purpose;L=first_floor_reduce_area;K=archi_line;J=regulation;I=engine_type;H=res;G=mass_generation_preset;C=mass_config;AJ='';h=[]
	try:
		AA=H[Y][p];AB=AA+C.fmg_for_commercial;S=[];J=[Q(A,tol_length=B.TOLERANCE)for A in J];AK=A(J);AL=O.process_time();D,q,S,r,d,s,t=Bj(K,J,G,G.mcl,G.gss,G.tolr,X,f,H[Y][j],C);O.process_time()-AL;S.append(q)
		if not C.iav:
			D=[q]
			for AM in J[1:]:D.append(AM.intersection(q))
		C.set_core_config(K,D,P,R,b,o,H,I,usc=G.usc);AC=W(0,0,C.csl[0][0],C.csl[0][1]);u=A0([AC],C.ctl[0],[AC],R,b,is_escape_core=C.is_escape_core,is_center_core_placed=F,is_using_adjusted_core=F,is_last_gen_core_called=E)[2][0].area;AD=C.csl[0][0]*C.csl[0][1]-u;v=y.deepcopy(D)
		for w in Am(D):
			w=U(w)
			if w.area<C.mmaa+AD:v=v[:-1]
			else:break
		D=v;S.append(D);AN=O.process_time();D=Bk(K,r,D,AB,AD,G,H[V][Z][0],P,s,d,G.mcl,G.gss,G.tolr,X,f,t,C,u,R);S.append(D);C.set_core_config(K,D,P,R,b,o,H,I,usc=G.usc);O.process_time()-AN;D=Bq(D,J,G.tolr,C.tolr_angle,C.sdl);AO=O.process_time();k=Bl(D,d,G.tolr,I,G.gss,A8,a,b,R,H[V][Z][0],K,J,AB,H[Y][j],C)
		if I==B.ENGINE_TYPE_BASIC or C.urpa and A9:k=k[:1]
		if A(k)==0:raise A7('코어 배치 실패')
		for(AP,AQ)in k:
			try:
				D,x,AR,AS,AT,M,M,AU,e,AV,AW,Aw=AP;M,M,AX,AY,AZ,M,Aa,Ab,z,M,Ac,M=AQ
				if C.commercial_type>0 and AK!=A(D):C.commercial_type=l(C.commercial_type,max(B.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN+H[V][Z][0],A(D)-B.MAX_HOUSING_FLOOR_MAP[P]))
				A1=AR[0];A2=AS[0];A3=AT[0];A4=AX[0];A5=AY[0];A6=AZ[0];AE=Aa[0];AF=Ab[0];Ad=z,A4,A5,A6,AE,AF;O.process_time()-AO;Ae=O.process_time();T,x,D,m,Af,Ag,Ah,An,Ao,Ap,Aq=Bm(A9,use_under_parking,AU,A1,A2,A3,parking_result_dict,A8,K,a,D,P,is_flag_lot,AA,e,s,r,G,X,f,d,I,x,L,estimated_parklot_count,t,C,C.commercial_type,Ad,H)
				if G.usc and not C.is_sub_core_necessary:raise A7('코어 2개소가 배치되지 않아도 되는 설계안에서 코어 2개소가 배치되었습니다.')
				O.process_time()-Ae;D=x;S.append([A[0]for A in D]);Ar=F;D,AI=Bn(D,H[V][Z][0],C.mmaa,J,C.umis,I,C.sdl,e,C.usep,C.tolr_angle,G.tolr,postprocess_emboss_cut_length,X,C.mcd,C.used,L,C.urpa,C.mab,C.mass_bb_slb,Ar,m);As=C.is_escape_core;At,Au=D,D;D,T,m,M=Ai(D,T[1],T[0],T,[],s,r,G,C,d,shapely.ops.unary_union([e,z]),shapely.ops.unary_union([A1,A4]),shapely.ops.unary_union([A2,A5]),shapely.ops.unary_union([A3,A6]),K,X,f,t,I,P,H[Y][AH],o,L,H[V][Z][0],T[4],At,Au,H,m);AI=Ak(e,D,L,H[V][Z][0],C.urpa,I==B.ENGINE_TYPE_BASIC);N=Aj(I,H,AI,e,A1,A2,A3,z,A4,A5,A6,AE,AF,Ap,Aq,D,d,S,T,L,Af,Ag,a,AW,Ac,AV,Ah,An,AJ,u,m,As,R,H[V][i][0],b,H[V][AG][0],C.is_specific_escape_sub_core,C.is_specific_escape_emgcy_elev_sub_core,J,Ao,visualize_inside_get_mass);h.append(N)
			except c as n:N=Al(n,L,a,I);h.append(N)
	except c as n:print(n);N=Al(n,L,a,I);h.append(N)
	finally:Av=g(h,key=lambda x:x['score'],reverse=E);N=Av[0]
	return N
def Bs(site_polygon,solar_setback_flag_polygon,openspace_buffer_len,estimated_parklot_count,floor_height,ssmh,ssr_from_user_input,mass_generation_preset,mass_config,engine_input):
	H=engine_input;G=ssr_from_user_input;D=mass_config;C=mass_generation_preset;B=estimated_parklot_count;A=site_polygon;L=A;M=A;I=H[Y][q];E=[A.buffer(-openspace_buffer_len,join_style=N.mitre)]*I
	for(J,O)in X(E):
		K=floor_height*(J+1)
		if K>ssmh:E[J]=O.intersection(shapely.affinity.translate(solar_setback_flag_polygon,0,-G*K))
	P=r;Q={};R=2.4;B=B;S=0;T={};U={};V={'edges':[]};W=F;Z=G==.0;a=F;b=F;c=F;d='basic';C=AW(C);D=AW(D);e=H;f={};g=I;h=F;return Br(C,L,M,E,P,Q,R,B,S,T,U,V,W,Z,a,b,c,f,d,D,e,g,h)
class Bu:
	def __init__(A,site_polygon_from_user_input,solar_setback_flag_polygon,open_space_buffer_len,estimated_parklot_count,floor_height,parking_area_divisor,has_elevator,has_piloti,max_bcr,max_far,max_floor,max_height):A.site_polygon_from_user_input=site_polygon_from_user_input;A.solar_setback_flag_polygon=solar_setback_flag_polygon;A.open_space_buffer_len=open_space_buffer_len;A.estimated_parklot_count=estimated_parklot_count;A.floor_height=floor_height;A.parking_area_divisor=parking_area_divisor;A.has_elevator=has_elevator;A.has_piloti=has_piloti;A.max_bcr=max_bcr;A.max_far=max_far;A.max_floor=max_floor;A.max_height=max_height
	def run(A):E={AI:A.open_space_buffer_len,AJ:A.estimated_parklot_count,AK:A.floor_height,AL:A.parking_area_divisor,i:A.has_elevator,Z:A.has_piloti,j:A.max_bcr,p:A.max_far,q:A.max_floor,v:A.max_height};S.update(E);D=S[AJ];F=S[AI];G=S[Ap];H=S[AK];I=S[Aq];B.PARKING_AREA_DIVISOR=S[AL];AU.update(S);AV.update(S);h[V][i]=[S[i]];h[V][Z]=[S[Z]];h[V][AG]=[not S[Z]];h[Y][j]=S[j];h[Y][p]=S[p];h[Y][q]=S[q];h[Y][v]=S[v];D=d(D);J=shapely.ops.orient(A.site_polygon_from_user_input);K=shapely.ops.orient(A.solar_setback_flag_polygon);C=Bs(J,K,F,D,H,I,G,AU,AV,h);C[AR]=[[shapely.ops.orient(A)for A in A]for A in C[AR]];C[AS]=shapely.ops.orient(C[AS]);return C
