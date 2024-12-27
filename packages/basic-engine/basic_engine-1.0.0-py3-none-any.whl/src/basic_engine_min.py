_A7='매스가 존재하지 않습니다.'
_A6='POLYGON EMPTY'
_A5='officetel'
_A4='dormitory'
_A3='urbanhousing_bundong'
_A2='urbanhousing_small'
_A1='WideETCSE'
_A0='SlimETCSE'
_z='SlimETCS'
_y='WideETM'
_x='SlimETM'
_w='WideETC'
_v='SlimETC'
_u='WideEM'
_t='SlimEM'
_s='WideEC'
_r='SlimEC'
_q='SlimEL'
_p='ExWideE'
_o='ExSlimE'
_n='ExSlim'
_m='WideET'
_l='SlimET'
_k='ExWideET'
_j='ExSlimET'
_i='ExSlimT'
_h='solar_setback_min_height'
_g='solar_setback_ratio'
_f='parking_residential'
_e='use_small_core'
_d='core'
_c='mass'
_b='geoms'
_a='오피스텔'
_Z='임대형기숙사'
_Y='도생(소형주택다세대)'
_X='dasedae'
_W='parking_area_divisor'
_V='floor_height'
_U='estimated_parklot_count'
_T='open_space_buffer_len'
_S='parking_commercial'
_R='has_commercial'
_Q='right'
_P='dajung'
_O='dagagu'
_N='max_height'
_M='geunsaeng'
_L='max_floor'
_K='max_far'
_J=1.
_I='max_bcr'
_H='has_elevator'
_G='has_piloti'
_F='regulations'
_E='options'
_D='left'
_C=False
_B=True
_A=None
import copy,math,time,numpy as np
from typing import List,Tuple,Union,Iterable
import shapely.affinity,shapely.ops
from shapely import wkt
from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import JOIN_STYLE
from shapely.geometry import CAP_STYLE
from shapely.geometry.base import BaseGeometry
mass_generation_preset_default={'bounding_box_config':0,'diagonalize_config':0,'cutting_policy_config':1,'gridsize':.3,'mass_cut_length':2.8,_e:_C,'tolerance':.0003,'use_sub_core':_C}
mass_config_default={'angle_min':0,'angle_max':90,'tolerance_angle':.1,'diangonals_simplifying_angle':15.,'min_mass_area':14,'simple_deadspace_len':1.8,'bcr_margin':1.03,'far_margin':.11,'far_margin_for_commercial':.1,'use_mass_intersection':_B,'pack_after_cut':_C,'use_postprocess_emboss_cut':_B,'use_deadspace_cut_with_exterior':_B,'use_same_grid':_B,'build_simple_check_parking':_B,'use_real_parking':_C,'is_alt_ver':_B,'check_core_center_intersecting_mass':_B,'add_core_center_as_candidates':_B,'min_mass_width':2.,'mass_cut_depth_divider':1.6,'emboss_cut_policy':1,'use_emboss_cut_length_sorting':_B,'longest_length_baseline':2.6,'shortest_length_baseline':1.2,'mass_aspect_ratio_baseline':6.,'mass_bb_shortest_length_baseline':4.2,'core_size_list':_A,'core_type_list':_A,_H:_A}
engine_input_default={_E:{_H:[_B],'unit_type':['1r'],_G:[_B],_R:[_C]},_F:{_I:.6,_K:2.,_L:7,_N:.0,_f:_A,_S:_A}}
custom_input={_T:.5,_U:8,_g:.5,_h:1e1,_V:3.,_W:134,_H:_B,_G:_B,_I:.6,_K:2.,_L:7,_N:.0}
class CustomClassForAttrFromDict:
	def __init__(A,dict_obj):
		for(B,C)in dict_obj.items():setattr(A,B,C)
	def set_core_config(C,archi_line,mass,building_purpose,use_small_core,is_commercial_area,commercial_type,res,engine_type,use_sub_core=_C):
		I=use_small_core;E=_C;L=_C;M=_C;N=_C;P=[_M];F=res[_E][_H][0]
		if is_commercial_area and building_purpose in P:
			if E:A=consts.CORE_WIDE_ESCAPE_TALL;B=consts.CORE_NARR_ESCAPE_TALL;F=_B
			elif I:A=consts.CORE_WIDE_TALL_SMALL;B=consts.CORE_NARR_TALL_SMALL
			else:A=consts.CORE_WIDE_TALL;B=consts.CORE_NARR_TALL
		else:
			Q=I
			if E:A=consts.CORE_WIDE_ESCAPE;B=consts.CORE_NARR_ESCAPE;F=_B
			elif I and Q:A=consts.CORE_WIDE_SMALL;B=consts.CORE_NARR_SMALL
			else:A=consts.CORE_WIDE;B=consts.CORE_NARR
		if not F:A=[A[0]];B=[B[0]];G=[0]
		elif not E:A=A[1:];B=B[1:];G=[A+1 for A in range(len(A))]
		else:G=[A+1 for A in range(len(A))]
		J=[]
		for D in range(len(A)):J.append([A[D],B[D]])
		assert len(J)==len(G),'코어타입과 코어사이즈 길이가 다릅니다.';O=[]
		if L:
			if M:
				if N:H=consts.CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL;K=consts.CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL
				else:H=consts.CORE_WIDE_SPECIFIC_ESCAPE_TALL;K=consts.CORE_NARR_SPECIFIC_ESCAPE_TALL
			else:H=A;K=B
			for D in range(len(H)):O.append([H[D],K[D]])
		C.has_elevator=F;C.core_type_list=G;C.core_size_list=J;C.sub_core_size_list=O;C.is_escape_core=E;C.is_sub_core_necessary=L;C.is_specific_escape_sub_core=M;C.is_specific_escape_emgcy_elev_sub_core=N;C.commercial_type=commercial_type
class ConstructionError(Exception):
	def __init__(A,msg):super().__init__();A._msg=msg
	def __str__(A):return A._msg
class consts:EPSILON=1e-06;TOLERANCE=1e-06;TOLERANCE_LARGE=1e-05;TOLERANCE_SLIVER=.001;TOLERANCE_GROUPING=.1;TOLERANCE_ANGLE=.01;TOLERANCE_MARGIN=.01;TOLERANCE_MACRO=.1;MASS_DEADSPACE_LENGTH=3.001;UNITSPACE_DEADSPACE_LENGTH=2.001;TOLERANCE_UNIT=1;FLAG_LOT_CHECK_MIN_AREA=200;EACH_UNIT_DEADSPACE_LENGTH_M=1.999;POSTPROCESS_DEADSPACE_LENGTH_M=2;COMMERCIAL_ADDITIONAL_DEADSPACE_LENGTH=3;U_SHAPE_DEADSPACE_LENGTH=.3;BCR_EXTRA=.03;GFA_CUT_VECTOR=0,1;GFA_CUT_RANGE=1;GFA_CUT_KEEP_FLOOR=3;GRID_INTERVAL=.15;MASS_CUT_LENGTH=3;MASS_EMBOSS_LENGTH=3;MIN_REDUCE_FLOOR_AREA=300;STAGGER_UPPER_LENGTH=4;STAGGER_UPPER_DEPTH=.8;STAGGER_LOWER_LENGTH=3;STAGGER_LOWER_DEPTH=.5;STAGGER_MIN_LENGTH=2;ANGLECUT_LENGTH=10;MASSREMOVER_LENGTH=40;PARTITIONSPLITTER_LENGTH=30;PARTITIONSPLITTER_INTERVAL=1.05;PARTITIONSPLITTER_MARGIN=2.4;PARTITIONSPLITTER_MERGE=1.5;PARTITIONSPLITTER_KEEPOUT_LENGTH=.7;CORE_SPLITTER_DIVIDE_COUNT=2;CORRIDORTUNE_INTERVAL=.35;HALL_WIDTH_OFFSET_MARGIN=.15;HALL_WIDTH=1.4;HALL_WIDTH_EMGCY=1.5;HALL_WIDTH_ESCAPE=1.6;ELEV_WIDTH=1.93;ELEV_HEIGHT=2.35;ADJUSTED_ELEV_WIDTH=1.9;ADJUSTED_ELEV_HEIGHT=2.4;ELEV_WIDTH_SMALL=1.68;ELEV_HEIGHT_SMALL=2.05;ELEV_WIDTH_SPECIFIC=2.;ELEV_HEIGHT_SPECIFIC=2.7;EMERGENCY_ROOM_WIDTH=2.75;STAIR_WIDTH=2.8;ADJUSTED_ELEV_WIDTH=1.9;ADJUSTED_ELEV_HEIGHT=2.4;ADJUSTED_REMAIN_HALL_DIS=2.83;CORE_VOID_WIDTH=1.25;CORE_VOID_SPECIFIC=1.35;ELEV_DISABLED_MIN_AREA=4;CORRIDOR_WIDE_BY_BUILDING_TYPE=[2,2,1.7,1.5,1.5,1.5,2,2];CORRIDOR_NARR_WIDTH=1.4;INNER_WALL_THICKNESS=.2;OUTER_WALL_THICKNESS=.4;CORE_SEGMENT_GAP_LENGTH=3.;OUTER_WALL_THICKNESS_FOR_VISUALIZE=.3;CURTAIN_WALL_THICKNESS=.2;CURTAIN_WALL_MULLION_THICKNESS=.05;CURTAIN_WALL_PANE_THICKNESS=.05;CURTAIN_WALL_INTERVAL=1.2;CORE_WIDE_TALL_SMALL=[5.55,7.23,5.55];CORE_NARR_TALL_SMALL=[1.6,2.05,3.65];CORE_STR_TALL_SMALL=[_i,_j,_k];CORE_WIDE_TALL=[5.55,7.68,5.75];CORE_NARR_TALL=[2.8,2.8,5.15];CORE_STR_TALL=['SlimT',_l,_m];CORE_WIDE_SMALL=[4.2,6.48,4.8];CORE_NARR_SMALL=[1.6,2.05,3.65];CORE_STR_SMALL=[_n,_o,_p];CORE_WIDE=[4.8,6.55,4.4,7.75];CORE_NARR=[2.8,2.8,5.2,2.8];CORE_STR=['Slim','SlimE','WideE',_q];CORE_WIDE_ESCAPE=[7.15,4.8];CORE_NARR_ESCAPE=[4.4,5.15];CORE_STR_ESCAPE=[_r,_s];CORE_WIDE_CENTER_ESCAPE=[8.33,6.4];CORE_NARR_CENTER_ESCAPE=[2.8,5.15];CORE_STR_CENTER_ESCAPE=[_t,_u];CORE_WIDE_ESCAPE_TALL=[7.9,5.55];CORE_NARR_ESCAPE_TALL=[4.4,5.15];CORE_STR_ESCAPE_TALL=[_v,_w];CORE_WIDE_CENTER_ESCAPE_TALL=[9.08,7.15];CORE_NARR_CENTER_ESCAPE_TALL=[2.8,5.15];CORE_STR_CENTER_ESCAPE_TALL=[_x,_y];CORE_WIDE_SPECIFIC_ESCAPE_TALL=[8.25,6.4];CORE_NARR_SPECIFIC_ESCAPE_TALL=[4.2,5.55];CORE_STR_SPECIFIC_ESCAPE_TALL=[_z,'WideETCS'];CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[10.2,5.5];CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[4.2,7.05];CORE_STR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL=[_A0,_A1];ELEV_PERSONS_MAP={_i:0,_j:7,_k:7,'SlimT':0,'SlimE':13,'WideE':13,_q:13,_n:0,_o:7,_p:7,'Slim':0,_l:13,_m:13,_x:13,_y:13,_v:13,_w:13,_t:13,_u:13,_r:13,_s:13,_z:16,'WideETCS':16,_A0:16,_A1:16,'EmergencyExit':0};CORE_LYING_NO_CHECK_AREA_MAX=170;CORE_TRANSLATE_RADIUS=2;CORE_TRANSLATE_MAX_TRIALS=20;SMALL_CORE_MAX_AREA=132;SMALL_CORE_MAX_FA=200;UNIT_MIN_WIDTH=2.4;UNIT_MIN_AREA=14;MARKET_MIN_AREA=14;PARTITIONED_MIN_AREA=.001;UNITENTRY_MIN_WIDTH=1.4;WIDECORRIDOR_CHECK_WIDTH=1.6;BALCONY_MIN_LENGTH=2;BALCONY_MAX_WIDTH=1.3;BALCONYUNIT_MIN_WIDTH=2.3;BALCONY_MARGIN=0;POSTPROCESS_PARK_GAP_CHECK=2.49;PARK_MAX_PARKING_EDGE_LEN=2.6;PARK_N_MAX_PARKING_EDGES=3;PARK_CELL_WIDE_PER=5;PARK_CELL_NARR_PER=2.5;PARK_CELL_WIDE_PAR=6;PARK_CELL_NARR_PAR=2;PARK_N_MAX_CELLS=8;PARK_N_FRONT_CELLS=5;PARK_GAP_LOT=2.5;PARK_CHECKER_LENGTH=30;PARK_PLOT_INTERVAL=.1;PARK_CENTERLINE_DIST_PER=6;PARK_CENTERLINE_DIST_PAR=4;PATH_NET_GAP=1;PATH_WIDTH_NARR=1.1;PATH_WIDTH_WIDE=1.7;MAX_TYPE_AREA_LIST_OF_LISTS_OF_LISTS=[[[36,42,45],[55,60,70],[72,76,80]],[[36,42,45],[55,60,70],[72,76,80]],[[16,18,20],[32,36,40],[52,56,60]],[],[],[],[[36,42,45],[55,60,70],[72,76,80]],[[36,42,45],[55,60,70],[72,76,80]]];AREA_COST=[-1e4,700,550,300,150];AREA_COST_COMMERCIAL=640;PACKING_OFFSET_INTERVAL_M=.3;PACKING_SEGMENT_DIVISION_MIN_LENGTH_M=6;PACKING_SEGMENT_DIVISION_UNIT_LENGTH_M=2;PACKING_ROOM_CHECK_BUFFER_M=.05;PACKING_MINIMUM_SEGMENT_LENGTH_M=2;PACKING_LOOP_MAX_NUMBER=10;PACKING_FAR_ADD=.2;PACKING_MAX_RESIDENTIAL_GFA=660;FINAL_DEADSPACE_LENGTH=1.499;TRENCH_FILL_ENTRY_LENGTH=1.1;TRENCH_FILL_LENGTH=3.;MAX_GROUP_PARKING_COUNT=5;OUTER_PARKING_UNDER_TWELVE=12;CENTERLINE_BB_DEADSPACE_LENGTH=3.501;CENTERLINE_BB_OFF_THE_WALL_LENGTH=3.001;RULE_PARKING_SITE_CUT_LENGTH=4.001;FRONT_PARKING_CHECK_INTERVAL=.3;PARKING_PARTITION_COUNT=3;PARKING_GAP_WIDTH=.001;SHIFT_STEP_SINGLE=.5;MINIMUM_OUTER_PARKING_ROAD_WIDTH=[6,4];PARKING_WIDTH=[2.5,6];PARKING_SPOT_HEIGHT=[5,2];PARKING_SPACE_HEIGHT=[-6,-5];PARKING_ADD_ROAD_EDGE_ADDITION_CHECKER=4.999;VEHICLE_ROAD_WIDTH=2.499;MAX_COUNT_WHEN_BACK_PARKING=8;MIN_INNER_PARKING_ROAD_EDGE_LENGTH=2.501;GAP_CHECK_MAX_ANGLE=30;PEDESTRIAN_PATH_WIDTH_ADD=.199;START_PT_OFFSET_DIST=1.25;CORE_EXPAND_DISTANCE=5;PARKING_SCALE_UP_RATIO=1.01;PARKING_SCALE_DOWN_RATIO=.99;CORE_ENTRY_LENGTH=1.2;CORE_ENTRY_SHIFT_LENGTH=.6;BACK_PARKING_SHIFT_MAX_TRIALS=15;MASS_PARK_GAP=.15;PLANES_ENTRY_LENGTH=2;INNER_ROAD_OFFSET_WIDTH=3;WEIGHTED_SHORTEST_PATHS_PENALTY=100;PARAM_Y_SINGLE=10;TRENCH_FILL_LENGTH=3.;RAND_POINTS_NUM=.1;FRONT_PARKING_GROUP_DISTANCE=2.499;RIGHT_ANGLE_DEGREE=90;FILTER_PED_PATH_NETWORK_WITH_PATH=_B;FINAL_ADDITION_PLANE_INTERVAL=.5;ROAD_EDGE_ENTRY_MIN_SEG_LENGTH=2.9;PARKING_PATTERN_RANGE_MAX=6;SHIFT_MAX_COUNT=10;RAMP_TYPE_LIST=[0,1];UNDERGROUND_PARKING_GAP_WIDTH=.5;UNDERGROUND_RAMP_OFFSET_LENGTH=5;UNDERGROUND_OFFSET_LENGTH=1;UNDERGROUND_AREA_TOL_ANGLE=30;RAMP_LENGTH=31.8;RAMP_WIDTH_LIST=[3.3,6];RAMP_SUB_LENGTH=6.5;RAMP_BODY_LENGTH=18.8;RAMP_INNER_RADIUS=6.;RAMP_L_TYPE_ADDITIONAL_LENGTH_EACH_SIDE=3.4;MAX_PARKING_COUNT_WHEN_NARROW_RAMP=49;RAMP_ROTATION_CHECK_AREA=5.;RAMP_OBSTACLE_TEST_BUFFER_LENGTH=[5,8];RAMP_OBSTACLE_ALLOW_RATIO_MAXIMUM=.2;UNDERGROUND_MASS_REMOVER_LENGTH=100;UNDERGROUND_MASS_CORE_PLACE_BASEAREA=200;UNDERGROUND_MASS_EXIT_PLACE_BASEAREA=50;UNDERGROUND_EMERGENCY_EXIT_SIZE=1.4;UNDERGROUND_CORE_MAXIMUM_DISTANCE=50;NARROW_UNIT_ENTRY_MAX_RATIO=4;PREVENT_NARROW_ENTRY_ON_SETBACK=_C;BUILDING_DIVISION_CORE_LOC_BUFFER_LEN=_J;BUILDING_DIVISION_DISTANCE_BETWEEN=4.;BUILDING_DIVISION_LEGAL_GEOM_INNER_SIZE_TEST_LEN=2.6;SIMPLE_REDUCE_RATIO_INTERVAL=.05;SIMPLE_DEADSPACE_LEN=1.4;SIMPLE_MIN_MASS_WIDTH=2.1;SIMPLE_BCR_MARGIN=1.03;SIMPLE_FAR_MARGIN=.0;SIMPLE_FAR_MARGIN_FOR_COMMERCIAL=.3;SIMPLE_MECH_PARK_CHECK_MIN_AREA=3e2;BUILDING_PURPOSE_MAP={_O:0,_X:1,_P:2,_M:3,'panmae':4,'upmu':5,_A2:6,_A3:7,_A4:8,_A5:9};MAX_HOUSING_FLOOR_MAP={_O:3,_X:4,_P:3,_M:0,'panmae':0,'upmu':0,_A2:4,_A3:5,_A4:0,_A5:0};PEDESTRAIN_PATH_WIDTH_BY_BUILDING_TYPE=[1.1,1.7,1.1,1.7,1.5,1.5,1.7,1.7,1.7,1.7];BUILDING_PURPOSE_STR_LIST=['다가구','다세대','다중','상가','판매','업무',_Y,'단지형다세대',_Z,_a];BUILDING_PURPOSE_GENERAL_SHORT_STR_LIST=['다가구','다세대','다중','근린','판매','업무',_Y,'도생(단지형다세대)',_Z,_a];BUILDING_PURPOSE_GENERAL_STR_LIST=['다가구주택','다세대주택','다중주택','근린생활시설','판매시설','업무시설',_Y,'단지형다세대주택',_Z,_a];SIMPLE_CORE_PLACEMENT_MIN_LENGTH=1;SIMPLE_DEFAULT_AVERAGE_AREA=38;SIMPLE_UNIT_AREA_FOR_DAJUNG=25;SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE=.5;SIMPLE_MASS_ASPECT_RATIO_BASEINE=6.;POSTPROCESS_CORRIDOR_ITERATION_COUNT=2;DOOR_SIZE=.9;DOOR_SIZE_LARGE=_J;DOOR_MARGIN=.05;DOOR_FRAME_WIDTH=.04;DOOR_FRAME_WIDTH_MARGIN=.01;DOOR_DEADSPACE_AFTER_SETBACK=1.399;DOOR_SETBACK_ITERATION=3;GREEN_POLYGON_MIN_WIDTH=1;GREEN_POLYGON_MARGIN=.3;GREEN_POLYGON_MIN_AREA=35;GREEN_POLYGON_BOUNDARY_WIDTH=2;ESCAPE_CORE_TRUE_AREA=200;MAX_HOUSEHOLDS_NUM_DAGAGU=19;MAX_HOUSEHOLDS_NUM_DAJUNG=20;BINARY_VOID='0';BINARY_SOLID='1';ENGINE_TYPE_LIGHT='light';ENGINE_TYPE_BASIC='basic';RULE_OUTER_NO_PARKING_ADJACENT_DISTANCE=2;SIMPLE_FAR_RESULT_FAR_ADJUSTMENTS=.0001;HAS_CENTERLINE_TRUE_BASELINE=20;LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM=3;LIGHT_LOWER_COMMERCIAL_FLOOR_MAX=3;LIGHT_LOWER_COMMERCIAL_FLOOR_MIN=1;LIGHT_SCORE_FOR_PARKLOT_ERROR=0;BASIC_ERROR_SUBCODE_MAENGJI=50101;BASIC_ERROR_SUBCODE_FAE_ZERO=50102;BASIC_ERROR_SUBCODE_EMPTY_OPTION=50103;PARKING_AREA_DIVISOR=134
def extend_curve(curve,start=0,end=0):'여러 개의 점으로 이루어진 linestring을 양쪽으로 확대 혹은 축소한다.\n    Args:\n        curve (LineString): Curve to extend\n        start (float, optional): Extension length at start of curve. Defaults to 0.\n        end (float, optional): Extension length at end of curve. Defaults to 0.\n    Returns:\n        (LineString): Extended curve\n    ';A=list(curve.coords);B=A[0][0];C=A[0][1];F=A[1][0];G=A[1][1];H=start/((F-B)**2+(G-C)**2)**.5;I=A[-2][0];J=A[-2][1];D=A[-1][0];E=A[-1][1];K=end/((D-I)**2+(E-J)**2)**.5;L=B-(F-B)*H,C-(G-C)*H;M=D+(D-I)*K,E+(E-J)*K;A[0]=L;A[-1]=M;N=LineString(A);return N
def explode_to_segments(curve):
	'Explode a curve into smaller segments\n\n    Args:\n        curve (LineString): Curve to explode\n\n    Returns:\n        segments(List[Linestring]): Exploded segments that make up the base curve\n    ';A=list(curve.coords)
	if len(A)==0:return[]
	B=[];C=A[0]
	for E in range(len(A)-1):D=A[E+1];B.append(LineString([C,D]));C=D
	return B
def offset_curve_polygon(curve,distance,side,return_offset_line=_C):
	'Offset LineString and make polygon with original LineString & new LineString\n\n    Args:\n        curve (LineString): Curve to offset\n        distance (int): Offset distance\n        side (string ("left"|"right")): Offset direction\n\n    Returns:\n        (tuple): tuple containing:\n\n            polygon (Polygon): Polygon made from original & new LineString\n            curve_offset (LineString): Offsetted new LineString\n    ';C=curve;B=side;A=list(C.coords);F,D=parallel_offset_segment(C,distance,B,segment_coords=A,return_coords=_B,join_style=2)
	if B==_D:0
	elif B==_Q:A=A[::-1]
	else:raise Exception('지원되지 않는 offset 방향입니다.')
	E=Polygon(A+D)
	if return_offset_line:return E,LineString(D)
	else:return E
def parallel_offset_segment(segment,distance,side,segment_coords=_A,return_coords=_C,join_style=1):
	P=distance;O=segment;I=side;A=segment_coords
	if not A:A=O.coords
	if len(A)==0:return LineString()
	elif len(A)>2:J=O.parallel_offset(P,I,join_style);return J
	B=A[0][0];C=A[0][1];D=A[1][0];E=A[1][1];H=P/((D-B)**2+(E-C)**2)**.5
	if I==_Q:F=H*(E-C);G=-H*(D-B);K=B+F;L=C+G;M=D+F;N=E+G
	elif I==_D:F=-H*(E-C);G=H*(D-B);M=B+F;N=C+G;K=D+F;L=E+G
	if return_coords:return A,[(K,L),(M,N)]
	J=LineString([(M,N),(K,L)]);return J
def angle_of_polygon_vertices(polygon):
	'Get angles of polygon vertices\n\n    Args:\n        polygon (Polygon): Polygon to find angle\n\n    Returns:\n        (List[float]): Angles of polygon vertices\n    ';D=polygon
	if D.is_empty:return[]
	B=list(D.exterior.coords);C=[(C[0]-B[1:][A-1][0],C[1]-B[1:][A-1][1])for(A,C)in enumerate(B[1:])];G=[(-A,-B)for(A,B)in[C[-1]]+C[:-1]];H=[math.atan2(A[1],A[0])for A in G];I=[math.atan2(A[1],A[0])for A in C];E=[B-I[A]for(A,B)in enumerate(H)];A=[A%(2*np.pi)for A in E];F=sum(A)
	if F>len(A)*np.pi*2-F:A=[A*-1%(2*np.pi)for A in E]
	A=A+[A[0]];return A
def simplify_polygon(polygon,tol_angle=.001,tol_length=1e-06,use_simplify=_B,container_geometry=_A,skip_angle_simplifying_when_interiors=_C):
	G=skip_angle_simplifying_when_interiors;F=container_geometry;E=tol_angle;C=tol_length;A=polygon
	if A.is_empty:return A
	if not A.is_valid:
		A=A.buffer(0)
		if isinstance(A,MultiPolygon):A=filter_polygon(A)
	assert isinstance(A,(Polygon,MultiPolygon)),f"polygon이 Polygon 또는 MultiPolygon type이 아닙니다. 현재 타입은 {type(A)}입니다."
	if isinstance(A,MultiPolygon):
		H=[]
		for J in A.geoms:H.append(simplify_polygon(J,E,C,skip_angle_simplifying_when_interiors=G))
		return MultiPolygon(H)
	else:
		if G and len(A.interiors)>0:B=A.simplify(C)
		else:
			A=shapely.geometry.polygon.orient(A,sign=_J);I=A.simplify(C);D=[]
			for(K,L)in enumerate(angle_of_polygon_vertices(I)[:-1]):
				if np.abs(L-np.pi)>E:D.append(I.exterior.coords[K])
			if len(D)<3:B=Polygon()
			else:B=Polygon(D)
		if F is not _A:B=A if not B.within(F)else B
		return B
def get_aspect_ratio(polygon,vector,return_bb=_C):
	E=polygon
	if E.is_empty:A=1;B=Polygon()
	else:B=get_rotated_bb(E,vector);F=explode_to_segments(B.exterior);C,D=F[0].length,F[1].length;A=C/D if C>D else D/C
	if return_bb:return A,B
	return A
def filter_polygon(inputs):
	A=inputs
	if isinstance(A,Polygon):return A
	elif hasattr(A,_b)or isinstance(A,Iterable):
		B=list(filter(lambda x:isinstance(x,Polygon),A.geoms))
		if len(B)==0:return Polygon()
		C=np.array(B,dtype=object)[np.argmax([A.area for A in B])];return C
	else:return Polygon()
def new_filter_polygon(inputs):
	B=inputs
	if isinstance(B,Polygon):return B,MultiPolygon()
	elif hasattr(B,_b)or isinstance(B,Iterable):
		A=np.array(list(filter(lambda x:isinstance(x,Polygon),B)),dtype=object)
		if len(A)==0:return Polygon(),MultiPolygon()
		C=np.eye(len(A),dtype=bool)[np.argmax([A.area for A in A])];A,D=A[C],A[~C];return A[0],MultiPolygon(list(D))
	else:return Polygon(),MultiPolygon()
def flatten_list(lists):
	A=lists
	if isinstance(A,list):
		if len(A)<1:return A
		elif isinstance(A[0],list):return flatten_list(A[0])+flatten_list(A[1:])
		else:return A[:1]+flatten_list(A[1:])
	else:return[A]
def buffer_erosion_and_dilation(polygon,buffer_distance,join_style=JOIN_STYLE.mitre,use_intersection=_B,choose_biggest_polygon=_B,choose_biggest_polygon_before_dilation=_C):
	'데드스페이스 제거 용도로 buffer 이중 연산을 수행한다.\n        버퍼 연산시, 뾰족하게 남은 형상은, dilation 후 돌출 가능하므로 intersection 기능을 추가하여 이 함수에서 처리.\n\n    Args:\n        polygon (Union[Polygon, MultiPolygon]): 기본적으로 폴리곤이 대상이지만,\n        difference의 결과 등 multipolygon인 경우도 처리 가능함.\n        buffer_distance (float): 같은 수치로 erosion과 dilation할 거리(양의 실수).\n        join_style (int, optional): buffer 연산 join 옵션. Defaults to JOIN_STYLE.mitre.\n        use_intersection (bool, optional): 결과에 원본의 intersection을 통해, 뾰족하게 돌출하는 것 방지하는 기능에 대한 flag. Defaults to True.\n        choose_biggest_polygon (bool, optional): 연산 결과중 가장 큰 폴리곤 하나만 선택하는 flag. Defaults to True.\n        choose_biggest_polygon_before_dilation (bool, optional): shrink 하고 가장 큰 것 만 고르고 싶을 경우 사용\n\n    Returns:\n        BaseGeometry: buffer 및 intersection 연산의 결과. flag 사용하지 않을 시 polygon이 아닐 수도 있음\n    ';G=choose_biggest_polygon;F=join_style;E=buffer_distance;A=polygon
	if A.is_empty:return A
	C=A.buffer(-E,join_style=F)
	if isinstance(C,MultiPolygon)and choose_biggest_polygon_before_dilation:C=filter_polygon(C)
	B=C.buffer(E,join_style=F)
	if isinstance(B,MultiPolygon)and G:B=filter_polygon(B)
	if use_intersection and not A.contains(B)and A.is_valid:D=B.intersection(A)
	else:D=B
	if G:H=filter_polygon(D)
	else:H=D
	return H
def buffer_dilation_and_erosion(polygon,buffer_distance,join_style=JOIN_STYLE.mitre,use_simplification=_B,simplify_tolerance=.001,choose_biggest_polygon=_B):
	'dilation 후 erosion 하는 buffer 이중 연산을 수행하는 함수\n        해당 연산 전 비슷한 좌표의 점을 가지는 simplify 되지 않은 입력은 buffer 버그를 발생시키기 때문에, 해당 함수로 처리함.\n\n    Args:\n        polygon (Polygon): 대상 폴리곤. 현재 쓰이는 곳은 모두 의도 상 polygon이어야 함\n        buffer_distance (float): dilation 후 erosion 할 거리, 양의 실수.\n        join_style (int, optional): 버퍼 joint 옵션. Defaults to JOIN_STYLE.mitre.\n        use_simplification (bool, optional): simplify를 사전에 호출할지 flag. Defaults to True.\n        simplify_tolerance (float, optional): mm 단위를 기본으로 1을 기본으로하고, m 단위 사용시 1e-3으로 사용. Defaults to 1.0.\n        choose_biggest_polygon (bool, optional): 연산 결과 중 가장 큰 폴리곤 하나. Defaults to True.\n\n    Returns:\n        BaseGeometry: simplify 후 함수 결과, flag 사용하지 않을 시 polygon인지는 보장하지 않음\n    ';E=simplify_tolerance;D=join_style;C=buffer_distance;B=polygon
	if use_simplification:F=B.simplify(E)
	else:F=B
	A=F.buffer(C,join_style=D);A=A.simplify(E);G=A.buffer(-C,join_style=D)
	if choose_biggest_polygon:H=filter_polygon(G)
	else:H=G
	return H
def get_rotated_bb(bb_original,bb_vec):
	'지정된 각도를 가지고 bounding box 를 생성합니다.\n\n    Args:\n        bb_original (Polygon): bounding box 를 생성하고자 하는 기준 폴리곤\n        bb_vec (np.ndarray): 지정 각도 벡터\n\n    Returns:\n        Polygon: 지정된 각도를 가지고 생성한 bounding box\n    ';A=bb_original
	if A.is_empty:return Polygon()
	C=np.array([bb_vec]);B=np.degrees(np.arctan2(*C.T[::-1]))%36e1;D=shapely.affinity.rotate(A,-B[0],origin=A.centroid);E=shapely.geometry.box(*D.bounds);F=shapely.affinity.rotate(E,B[0],origin=A.centroid);return F
def remove_deadspace_with_extended_exterior(polygon,deadspace_len,tolerance,core=Polygon(),regulation=Polygon(),building_purpose=_A,return_only_splits=_C):
	'외곽선을 연장 데드스페이스를 삭제하는 방식의 데드스페이스 처리 함수\n\n    여러 곳에서 사용하기 위해 geom 으로 옮김.\n\n    Args:\n        polygon (Polygon): 데드스페이스를 삭제하고자 하는 원본 폴리곤\n        deadspace_len (float): 데드스페이스 기준 길이\n        tolerance (float): 도형을 자를 때 길이 여유분\n        core (Polygon): if given, use all areas that meet the core\n        regulation(Polyogn): if given, prevent areas that go outside the regulation\n\n    Returns:\n        Polygon: 외곽선 연장 방식으로 데드스페이스 처리한 후의 폴리곤\n    ';J=building_purpose;I=regulation;H=deadspace_len;D=polygon;B=tolerance;R=explode_to_segments(D.boundary);K=D.buffer(-B);E=[]
	for L in R:
		M=extend_curve(L,start=H,end=H)
		if M.crosses(K):E.append(M)
		else:S=extend_curve(L,start=B,end=B);E.append(S)
	T=shapely.ops.unary_union(E);U=shapely.ops.unary_union(T);V=list(shapely.ops.polygonize(U));C=[A for A in V if not K.disjoint(A)]
	if return_only_splits:return C
	if not core.is_empty:
		W=np.argmax([A.area for A in C]);A=C.pop(W);X=core.buffer(B,join_style=JOIN_STYLE.mitre)
		for N in C:
			F=_C
			if not I.is_empty:
				if I.contains(N):F=_B
			else:F=_B
			if F:
				A=shapely.ops.unary_union([A,N])
				if J is not _A:
					if J==_M:A=buffer_erosion_and_dilation(polygon=A,buffer_distance=consts.TOLERANCE_MARGIN,choose_biggest_polygon=_B)
					else:
						G:0;G=[];O=[A]
						if isinstance(A,MultiPolygon):O=list(A.geoms)
						for P in O:
							if not P.disjoint(X):G.append(P)
						A=shapely.ops.unary_union(G)
				A=buffer_dilation_and_erosion(polygon=A,buffer_distance=B,use_simplification=_B,choose_biggest_polygon=_B)
		if A.is_empty:return D
		return A
	Q=filter_polygon(MultiPolygon(C))
	if Q.is_empty:return D
	return Q
def is_entry_secured_between_geoms(geom_one,geom_two,entry_width):
	D=entry_width;C=geom_two;E=geom_one.buffer(consts.TOLERANCE_MARGIN,join_style=2)
	if E.disjoint(C):return _C
	F=C.exterior;A=F.intersection(E).simplify(consts.TOLERANCE);B=[]
	if isinstance(A,LineString):B=explode_to_segments(A)
	elif isinstance(A,MultiLineString):
		for G in A.geoms:B+=explode_to_segments(G)
	return any(np.isclose(A.length,D)or A.length>=D for A in B)
def flatten_geometry_to_certain_type(geometry,target_type):
	C=target_type;A=geometry;B=[]
	if isinstance(A,C):B=[A]
	elif hasattr(A,_b)or isinstance(A,Iterable):
		for D in A.geoms:B+=flatten_geometry_to_certain_type(D,C)
	return B
def polygon_or_multipolygon_to_list_of_polygon(geometry):return flatten_geometry_to_certain_type(geometry,Polygon)
def get_mass_angle_from_a_polygon(polygon):B=np.array(polygon.exterior.coords);A=B[1:]-B[:-1];C=np.argmax([np.linalg.norm(A)for A in A]);D=np.arctan2(A[C][1],A[C][0]);return D
def check_min_size(mass,has_piloti,regulation,min_mass_area):
	'Check that each floor is within the regulation polygon and\n    that each floor is big enough\n\n    Args:\n        mass (list): List of mass polygon\n        has_piloti (bool): piloti or not\n        regulation (list): List of regulation polygon\n        min_mass_area (float): minimum area for a floor\n\n    Returns:\n        list: the new mass\n    ';B=mass;C=[]
	for A in range(len(B)):
		if A==0 and has_piloti or A==0 and B[A][0].is_empty:C.append([wkt.loads(_A6)])
		elif B[A][0].area>=min_mass_area:B[A]=[B[A][0].intersection(regulation[A])];C.append(B[A])
		else:break
	return C
def check_mass_intersection(mass,core,engine_type,regulation,simple_deadspace_len):
	B=mass
	for C in range(2,len(B)):
		A=B[C][0].intersection(B[C-1][0]);A=simplify_polygon(A,tol_length=consts.TOLERANCE,container_geometry=regulation[C])
		if engine_type==consts.ENGINE_TYPE_BASIC:A=A.union(core.buffer(consts.TOLERANCE,join_style=JOIN_STYLE.mitre))
		A=buffer_erosion_and_dilation(polygon=A,buffer_distance=simple_deadspace_len/2,use_intersection=_B,choose_biggest_polygon=_B);B[C]=[A]
	return B
def gen_convexity_list(polygon):
	B=angle_of_polygon_vertices(polygon);A=[]
	for C in B:
		if C<np.pi:A.append(1)
		else:A.append(0)
	return A
def cut_emboss(polygon,width,policy,time_counter_dict,is_postprocess,tolerance_angle,mass_cut_depth_divider=_J,use_emboss_cut_length_sorting=_C,longest_length_baseline=_A,shortest_length_baseline=_A):
	N=shortest_length_baseline;M=longest_length_baseline;L=policy;H=is_postprocess;G=width;F=tolerance_angle;D=polygon;O=time.process_time()
	if D.is_empty:time.process_time()-O;return D
	P=G/mass_cut_depth_divider;C=gen_convexity_list(D);C=C[:-1];A=list(D.exterior.coords);A=A[:-1];E=[]
	if H:E=list(angle_of_polygon_vertices(D))
	Q=len(C);B=0;R=L==0;S=L==1
	while _B:
		if C[B%len(A)]==0 and C[(B+1)%len(A)]==1 and C[(B+2)%len(A)]==0:
			Z=Point(A[(B-1)%len(A)]);I=Point(A[B%len(A)]);T=Point(A[(B+1)%len(A)]);a=Point(A[(B+2)%len(A)])
			if H:
				b=E[B%len(A)];c=E[(B+1)%len(A)];d=E[(B+2)%len(A)]
				if np.pi/2-F>b%(np.pi/2)>F:B+=1;continue
				if np.pi/2-F>c%(np.pi/2)>F:B+=1;continue
				if np.pi/2-F>d%(np.pi/2)>F:B+=1;continue
			J=I.distance(T);K=Z.distance(I)
			if use_emboss_cut_length_sorting:U,V=sorted([J,K]);W=R and(U<=N and V<=M);X=S and(U<=N or V<=M)
			else:W=R and(J<=G and K<=P);X=S and(J<=G or K<=P)
			e=W or X
			if e:
				f=np.array(a.coords[0])-np.array(T.coords[0]);Y=np.array(I.coords[0])+f
				if D.contains(Point(Y)):
					A=list(A);A[B%len(A)]=_A;A[(B+1)%len(A)]=tuple(Y);A[(B+2)%len(A)]=_A;C[B%len(A)]=_A;C[(B+1)%len(A)]=0;C[(B+2)%len(A)]=_A
					if H:E[B%len(A)]=_A;E[(B+1)%len(A)]=0;E[(B+2)%len(A)]=_A;E=[A for A in E if A is not _A]
					if B+2>=len(A):B-=1
					A=[A for A in A if A is not _A];C=[A for A in C if A is not _A];Q-=2;continue
		B+=1
		if B>=Q:break
	D=Polygon(A);D=simplify_polygon(D,tol_length=consts.TOLERANCE);time.process_time()-O;return D
def postprocess_emboss_cut(mass,core,tolerance,tolerance_angle,regulation,postprocess_emboss_cut_length,time_counter_dict,mass_cut_depth_divider):
	D=regulation;C=tolerance_angle;E=[]
	for(F,G)in enumerate(mass):B=simplify_polygon(G[0],tol_angle=C,tol_length=consts.TOLERANCE,container_geometry=D[F]);A=MultiPolygon([B,core]);A=buffer_dilation_and_erosion(polygon=A,buffer_distance=consts.TOLERANCE_MARGIN,use_simplification=_B,choose_biggest_polygon=_B);A=simplify_polygon(A,tol_angle=C,tol_length=tolerance,container_geometry=D[F]);A=cut_emboss(A,postprocess_emboss_cut_length,0,time_counter_dict,_B,C,mass_cut_depth_divider=mass_cut_depth_divider);B=A.difference(core);B=buffer_erosion_and_dilation(polygon=B,buffer_distance=consts.TOLERANCE_SLIVER,use_intersection=_B,choose_biggest_polygon=_B);E.append([B])
	return E
def deadspacecut_with_exterior(mass,tolerance_angle,tolerance,core,engine_type,simple_deadspace_len,regulation):
	B=[]
	for(C,D)in enumerate(mass):
		A=simplify_polygon(D[0],tol_angle=tolerance_angle,tol_length=tolerance,container_geometry=regulation[C])
		if A.is_empty:B.append([A]);continue
		if engine_type==consts.ENGINE_TYPE_BASIC and C>0:A=buffer_dilation_and_erosion(shapely.ops.unary_union([A,core]),consts.TOLERANCE_MARGIN)
		A=buffer_erosion_and_dilation(A,simple_deadspace_len/2);B.append([A])
	return B
def basic_final_postprocessing(mass,core,regulation):
	'Postprocessing only for basic engine\n\n    Args:\n        mass (list): the mass\n        core (Polygon): the core\n        regulation (list): the regulation\n\n    Returns:\n        list: new mass\n    ';A=[]
	for F in mass:B=shapely.ops.unary_union([F[0],core]);B=buffer_dilation_and_erosion(polygon=B,buffer_distance=consts.TOLERANCE_SLIVER,use_simplification=_B,choose_biggest_polygon=_B);A.append([B])
	G=min(A.length for A in explode_to_segments(core.boundary))
	for(C,D)in enumerate(A):
		if D[0].is_empty:continue
		E=buffer_dilation_and_erosion(polygon=D[0],buffer_distance=G/2)
		if E.within(regulation[C]):A[C]=[E]
	return A
def get_regulation_bounds(regulation,mass_angle):A=shapely.ops.unary_union(regulation);B=shapely.affinity.rotate(A,-mass_angle,(0,0),use_radians=_B);C=shapely.ops.unary_union(B).bounds;return C
def no_diagonals_before_diagonalize(mass_polygon):
	'diagonalize 실행 전 사선이 없는 것을 확인합니다.'
	for C in angle_of_polygon_vertices(mass_polygon):A=np.pi/2;B=C%A;assert-consts.TOLERANCE_ANGLE<=B<=consts.TOLERANCE_ANGLE or A-consts.TOLERANCE_ANGLE<=B<=A+consts.TOLERANCE_ANGLE
def gen_segs_to_use_from_core(core_segs,mass_boundary,is_using_short_segs,is_core_translate_use=_C,existing_hall=Polygon()):
	H=existing_hall;G=mass_boundary;E=[];F=[]
	for L in core_segs:
		A=L.geoms
		if A[0].length>=A[1].length:E.append([A[0],A[2]]);F.append([A[1],A[3]])
		else:E.append([A[1],A[3]]);F.append([A[0],A[2]])
	I=MultiPoint(list(map(lambda x:x.boundary.centroid,G))).centroid
	if not H.is_empty:I=H.centroid
	if is_using_short_segs:B=F
	else:B=E
	M=list(map(lambda x:[I.distance(A)for A in x],B));N,O=list(zip(*map(lambda x:(np.argmin(x),np.argmax(x)),M)));C:0;D:0;C=list(map(lambda x,y:x[y],B,N));D=list(map(lambda x,y:x[y],B,O));J=B[0];P=Polygon(Polygon([*J[0].coords,*J[1].coords]));Q=G[-1]-P.buffer(consts.TOLERANCE);K=Q.buffer(consts.TOLERANCE_LARGE)
	if is_core_translate_use:
		R=D[0].within(K);S=not C[0].within(K)
		if R and S:C,D=D,C
	return E,F,C,D
def gen_core(core,core_type,mass_boundary,use_small_core,is_commercial_area,is_escape_core,is_center_core_placed,is_using_adjusted_core,is_last_gen_core_called=_C,is_specific_escape_sub_core=_C,is_specific_escape_emgcy_elev_sub_core=_C,is_core_translate_use=_C,existing_hall=Polygon()):
	'Generate core inner geometry.\n\n    Args:\n        core (list(Polygon)): sampled list of core polygon\n        core_type (int): selected core type\n        mass_boundary (list(Polygon)): list of mass polygon\n        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)\n        is_commercial_area (bool): 상업지역 여부\n        is_escape_core (bool): 피난계단 사용 여부\n        is_center_core_placed (bool): 코어의 위치가 중심인지 모서리인지\n        is_last_gen_core_called (bool): premium.py에서 사용되는 gen_core인지 여부\n    Raises:\n        Exception: when core type is not in 0~2\n    Returns:\n        (tuple): tuple containing:\n            hall (list(Polygon)): list of hall polygon (코어 내 복도)\n            stair (list(Polygon)): list of stair polygon (코어 내 계단)\n            elev (list(Polygon)): list of elev polygon (코어 내 승강기)\n            core (list(Polygon)): list of core polygon\n            close_seg (list(LineString)): list of short core segment close from mass centroid\n            (매스 센트로이드와 가까운 짧은 코어 세그먼트)\n            far_seg (list(LineString)): list of short core segment far from mass centroid\n            (매스 센트로이드와 먼 짧은 코어 세그먼트)\n            core_segs_for_parking (list(MultiLineString)): list of long core segment\n            (주차모듈에서 사용되는 코어 세그먼트들, 긴 두개의 선분 혹은 짧은 두개의 선분이 됨)\n    ';X=existing_hall;W=is_using_adjusted_core;V=use_small_core;O=is_core_translate_use;N=core_type;J=core;B=mass_boundary;C=K=E=_A;J=list(map(lambda x:shapely.ops.orient(x,sign=_J).simplify(consts.TOLERANCE),J));P=list(map(lambda x:MultiLineString(explode_to_segments(x.boundary)),J));L:0;F,Y=get_elev_size(V,W);g=[Polygon()]*len(B);h=[Polygon()]*len(B)
	if N==0:G,Q,A,D=gen_segs_to_use_from_core(P,B,is_using_short_segs=_B,is_core_translate_use=O);L=G;M=A;R=list(map(lambda x:x.parallel_offset(consts.HALL_WIDTH,_D),M));C=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords[::-1]])),M,R));H=D;K=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords])),H,R));E=list(map(lambda x:Polygon(),J))
	elif N==1:G,Q,A,D=gen_segs_to_use_from_core(P,B,is_using_short_segs=_B,is_core_translate_use=O,existing_hall=X);L=G;I=A;Z=list(map(lambda x:x.parallel_offset(F,_D),A));E=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords[::-1]])),I,Z));i=.15;a=list(map(lambda x:x.parallel_offset(consts.HALL_WIDTH+i+F,_D),A));C=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords[::-1]])),Z,a));H=D;K=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords])),a,H))
	elif N==2:
		j=bool(V or is_commercial_area or is_center_core_placed and is_escape_core);G,Q,A,D=gen_segs_to_use_from_core(P,B,is_using_short_segs=j,is_core_translate_use=O,existing_hall=X);L=Q;M=A;R=list(map(lambda x:x.parallel_offset(consts.HALL_WIDTH,_D),M));C=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords[::-1]])),M,R));b=A[0].interpolate(Y);k=D[0].interpolate(D[0].length-Y);l=LineString([A[0].coords[0],b]);I=[l for A in A];I=list(map(lambda x:x.parallel_offset(consts.HALL_WIDTH,_D),I));c=list(map(lambda x:x.parallel_offset(F,_D),I));E=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords[::-1]])),I,c));m=LineString([b,A[0].coords[1]]);H=[m for A in A];H=list(map(lambda x:x.parallel_offset(consts.HALL_WIDTH,_D),H));n=LineString([D[0].coords[0],k]);o=[n for A in D];K=list(map(lambda x,y:Polygon(np.concatenate([x.coords,y.coords])),H,o))
		if W:d=Q[0][0].length-consts.HALL_WIDTH-F;p=offset_curve_polygon(I[0],d,_D);e=p.buffer(consts.TOLERANCE,join_style=JOIN_STYLE.mitre);T=shapely.ops.unary_union([C[0],e]);C=[simplify_polygon(T,tol_length=consts.TOLERANCE)]*len(C);q=offset_curve_polygon(c[0],d,_D);r=q.buffer(consts.TOLERANCE,join_style=JOIN_STYLE.mitre);S=shapely.ops.unary_union([E[0]-e,r]);E=[simplify_polygon(S,tol_length=consts.TOLERANCE)]*len(E)
	elif N==3:G,_,A,D=gen_segs_to_use_from_core(P,B,is_using_short_segs=_B,is_core_translate_use=O);L=G;U=A[0].parallel_offset(F,_D);s=offset_curve_polygon(U,consts.HALL_WIDTH,_D);t=U.parallel_offset(consts.HALL_WIDTH,_D);u=G[0][0].length-consts.HALL_WIDTH-F;v=offset_curve_polygon(t,u,_D);w=U.parallel_offset(consts.HALL_WIDTH,_D);x=MultiPoint(w.coords);y=sorted(x.geoms,key=lambda x:x.distance(B[-1].boundary));z=LineString(y);A0=shapely.ops.substring(z,.5,1,normalized=_B);A1=consts.ADJUSTED_REMAIN_HALL_DIS;A2=A0.buffer(A1,join_style=JOIN_STYLE.mitre,cap_style=CAP_STYLE.flat);S=offset_curve_polygon(A[0],F,_D);A3=S.buffer(consts.TOLERANCE,join_style=JOIN_STYLE.mitre);f=A2-A3;T=simplify_polygon(shapely.ops.unary_union([s,f]),tol_length=consts.TOLERANCE);A4=v-f.buffer(consts.TOLERANCE,join_style=JOIN_STYLE.mitre);E=[S]*len(B);C=[T]*len(B);K=[A4]*len(B)
	else:raise Exception('FIXME: 잘못된 core type을 전달 받았습니다.')
	C=list(map(lambda x:shapely.ops.orient(x,sign=_J).simplify(consts.TOLERANCE),C));return C,K,E,J,g,h,A,D,L
def gen_corridor_entries(hall,mass,core,corridor_entries_direction):
	'복도 출입구 생성 (코어 내 복도와 접하는 최소 복도 셀).\n\n    Args:\n        hall (List[Polygon]): 층별 코어 내 복도. 최소 1층은 존재해야함.\n        mass (List[Polygon]): 층별 매스. 매스 층수를 기준으로 복도 출입구를 생성함.\n        core (Polygon): 층별 코어 폴리곤\n\n    Returns:\n        List[List[Polygon]]: 층별 복도 출입구 (길이는 매스와 같은 층수), 층마다 2개이며 공간이 부족한 경우는 빈 폴리곤이 들어간다.\n    ';C=corridor_entries_direction;A=hall;assert len(A)>0;A,C=get_temp_hall(A[0],C,core);D=[]
	for F in A:G=explode_to_segments(F.boundary);H=sorted(G,key=lambda x:x.length)[:2];I=[offset_curve_polygon(A,consts.HALL_WIDTH,_Q)for A in H];D.append(I)
	J=core.minimum_rotated_rectangle.buffer(consts.TOLERANCE)
	for(K,B)in zip(mass,D):
		L=K.buffer(consts.TOLERANCE_LARGE,join_style=JOIN_STYLE.mitre)
		for E in range(len(B)):
			M=B[E].within(L);N=B[E].within(J)
			if not M or N:B[E]=Polygon()
	return D,C
def get_elev_size(use_small_core,is_using_adjusted_core):
	'입력받은 조건을 기반으로 엘리베이터 사이즈 반환\n\n    Args:\n        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)\n        is_using_adjusted_core (bool): CORE_WIDE, CORE_NARR에 해당하는 코어인지 여부\n\n    Returns:\n        Tuple[float]: 엘리베이터 사이즈\n    ';A=consts.ELEV_WIDTH;B=consts.ELEV_HEIGHT
	if use_small_core:A=consts.ELEV_WIDTH_SMALL;B=consts.ELEV_HEIGHT_SMALL
	elif is_using_adjusted_core:A=consts.ADJUSTED_ELEV_WIDTH;B=consts.ADJUSTED_ELEV_HEIGHT
	return A,B
def get_core_boundary_intsc_long_hall_seg(core,long_hall_segs):
	'홀 장변 선분과 코어 도형이 공유하는 선분 도출\n\n    Args:\n        core (Polygon): 1개층 코어 도형\n        long_hall_segs (List[LineString]): 1개층 hall 장변 선분\n\n    Returns:\n        LineString: 코어와 홀 장변 선분이 공유하는 선분\n    ';A=LineString()
	for B in long_hall_segs:
		C=extend_curve(B,-consts.TOLERANCE_MARGIN,-consts.TOLERANCE_MARGIN).buffer(consts.TOLERANCE)
		if C.intersects(core.boundary):A=B;break
	return A
def get_temp_hall(hall,corridor_entries_direction,core,corridor_loading=_A):
	'corridor_entries, dirs, corridor_skeletons 등을 생성하는데 사용할 임시 hall 생성\n\n    Args:\n        hall (Polygon): 1개층 hall Polygon\n        corridor_entries_direction (List[bool]): corridor_entries 생성 방향\n        core (Polygon): 1개층 core Polygon\n        corridor_loading (List[int], optional): 복도 타입. Defaults to None.\n\n    Returns:\n        Tuple[List[Polygon], List[bool]]: 임시로 사용할 hall 리스트, corridor_entries 생성 방향\n    ';E=corridor_loading;A=corridor_entries_direction
	if E is not _A:
		for(I,J)in enumerate(E):
			if J==0:A[I]=_C
	F:0;F=explode_to_segments(hall.boundary);B=sorted(F,key=lambda x:x.length);K=B[-2:];G=get_core_boundary_intsc_long_hall_seg(core,K);H=G.is_empty;L=B[-1].distance(B[-2]);M=offset_curve_polygon(B[-1],L,_D)
	if not H:D=offset_curve_polygon(G,consts.HALL_WIDTH,_Q);D=shapely.ops.orient(D,-_J)
	else:A=[_C]*len(A)
	C=[]
	for N in A:
		if N:C.append(D)
		elif H:C.append(hall)
		else:C.append(M)
	return C,A
class EnvPlan:
	def __init__(A,packed_unit_space,parking_cells,parking_regulation,commercial_type):A._packed_unit_space=packed_unit_space;A._parking_cells=parking_cells;A._parking_regulation=parking_regulation;A._commercial_type=commercial_type
	@property
	def parking_cells(self):return self._parking_cells
	@parking_cells.setter
	def parking_cells(self,value):self._parking_cells=value
	@property
	def packed_unit_space(self):return self._packed_unit_space
	@packed_unit_space.setter
	def packed_unit_space(self,value):self._packed_unit_space=value
	@property
	def parklot_count(self):return len(self.parking_cells)
	@property
	def parking_regulation(self):return self._parking_regulation
	@parking_regulation.setter
	def parking_regulation(self,value):self._parking_regulation=value
	@property
	def commercial_type(self):return self._commercial_type
	@commercial_type.setter
	def commercial_type(self,value):self._commercial_type=value
	@property
	def law_parklot_count(self):return math.floor(sum(sum(A.area for A in A)for A in self.packed_unit_space)/self.parking_regulation+.5)
def get_use_district_small_core(res):
	C='use_district';B='field';A=_B
	if'준주거지역'in res[B][C]:A=_C
	if'일반상업지역'in res[B][C]:A=_C
	return A
def gen_obb_from_longest_segment(polygon):B=polygon;A=get_mass_angle_from_a_polygon(B);C=shapely.affinity.rotate(B,-A,(0,0),use_radians=_B);D,E,F,G=C.bounds;H=box(D,E,F,G);I=shapely.affinity.rotate(H,A,(0,0),use_radians=_B);return I,A
def gen_obb_from_convex_hull(polygon):
	D=polygon;E=np.array(D.convex_hull.exterior.coords);H=E[1:]-E[:-1];A=[];B=[]
	for F in H:G=np.arctan2(F[1],F[0]);A.append(G);I=shapely.affinity.rotate(D,-G,(0,0),use_radians=_B);J,K,L,M=I.bounds;N=box(J,K,L,M);B.append(N)
	C=np.argmin([A.area for A in B]);O=shapely.affinity.rotate(B[C],A[C],(0,0),use_radians=_B);return O,A[C]
def gen_grid_polygon(polygon,mass_angle,gridsize,tolerance,time_counter_dict,regulation_bounds):
	'입력 폴리곤에 그리드를 적용한다. 폴리곤 내부에 완전히 포함된 그리드 영역들에 해당하는 새로운 폴리곤을 만든다.\n\n    Args:\n        polygon (Polygon): 연산 대상 입력 폴리곤\n        mass_angle (float): 폴리곤의 바운딩 박스가 회전된 각도 (그리드를 생성할 각도)\n        gridsize (float): 그리드 셀 한 변의 길이\n        tolerance (float): 폴리곤 외곽선과 그리드 선 사이의 거리 tolerance. 셀 크기의 1/100를 추천\n\n    Returns:\n        mass_poly (Polygon): 입력 폴리곤 내부의 격자화된 폴리곤\n    ';X=regulation_bounds;W=mass_angle;M=polygon;B=tolerance;A=gridsize;k=time.process_time();M=buffer_erosion_and_dilation(polygon=M,buffer_distance=consts.TOLERANCE_SLIVER,use_intersection=_B,choose_biggest_polygon=_B);Y=shapely.affinity.rotate(M,-W,(0,0),use_radians=_B);F,G,N,O=Y.bounds
	if X is not _A:F,G,N,O=X
	Z=shapely.affinity.translate(Y,xoff=-F+A-B,yoff=-G+A-B);a=int(np.ceil((N-F)/A)+2);b=int(np.ceil((O-G)/A)+2);C=np.array(Z.exterior.coords);D=[]
	for E in range(len(C)-1):
		c=LineString([C[E],C[E+1]]);H=C[E][0]//A*A;I=C[E][1]//A*A;H=H+A/2;I=I+A/2;P=C[E+1][0]//A*A;Q=C[E+1][1]//A*A;P=P+A/2;Q=Q+A/2;l=P-H;m=Q-I;J=int(round(l/A));K=int(round(m/A))
		if J>=0:d=A
		else:d=-A
		if K>=0:e=A
		else:e=-A
		J=abs(J);K=abs(K);D.append(Point(H,I));R=H;S=I
		while _B:
			if J==0 or K==0:break
			f=R+d;g=S+e;h=Point(f,S);n=c.distance(h);i=Point(R,g);o=c.distance(i)
			if n<=o:D.append(h);R=f;J-=1
			else:D.append(i);S=g;K-=1
	p=LineString(D);L=p.buffer(A/2+B,cap_style=CAP_STYLE.square,join_style=JOIN_STYLE.mitre);q=LineString([D[0],D[-1]]);r=q.buffer(A/2+B,cap_style=CAP_STYLE.square);L=shapely.ops.unary_union([L,r]);L=L.buffer(-B,join_style=JOIN_STYLE.mitre);a=int(np.ceil((N-F)/A)+2);b=int(np.ceil((O-G)/A)+2);s=box(0,0,a*A,b*A);T=polygon_or_multipolygon_to_list_of_polygon(s.difference(L));j=[];t=Z.buffer(max([A*.8,consts.TOLERANCE_MARGIN]),join_style=JOIN_STYLE.mitre)
	for U in T:
		if isinstance(U,Polygon)and t.contains(U):j.append(U)
	T=j;u,v=new_filter_polygon(T);V=shapely.affinity.translate(u,xoff=F-A+B,yoff=G-A+B);V=shapely.affinity.rotate(V,W,(0,0),use_radians=_B);time.process_time()-k;return V
def cut_extrude(polygon,depth,width,tolerance,time_counter_dict):
	M=depth;H=tolerance;F=polygon;N=time.process_time()
	if F.is_empty:time.process_time()-N;return F
	Q=np.pi/2-.1;F=simplify_polygon(F,tol_angle=Q,tol_length=H);C=gen_convexity_list(F);A=list(F.exterior.coords);C=C[:-1];A=A[:-1];G=len(C);B=0
	while _B:
		if C[(B+2)%len(A)]==1 and C[(B+3)%len(A)]==1:
			O=Point(A[(B+2)%len(A)]);P=Point(A[(B+3)%len(A)])
			if H<=O.distance(P)<=width:
				R=Point(A[(B+1)%len(A)]);S=Point(A[(B+4)%len(A)]);I=R.distance(O);J=P.distance(S)
				if I<=M or J<=M:
					if abs(I-J)<H:
						for D in range(4):A[(B+1+D)%len(A)]=_A;C[(B+1+D)%len(A)]=_A
						E=0
						for D in range(4):
							if B+1+D>=len(A):E+=1
						B-=E;A=[A for A in A if A is not _A];C=[A for A in C if A is not _A];G-=4
						if B>=2 and C[B]==1:B-=2;continue
					elif I>J:
						K=np.array(A[(B+4)%len(A)])-np.array(A[(B+3)%len(A)]);T=np.array(A[(B+2)%len(A)])+K;A[(B+2)%len(A)]=tuple(T)
						for D in range(2):A[(B+3+D)%len(A)]=_A;C[(B+3+D)%len(A)]=_A
						E=0
						for D in range(4):
							if B+1+D>=len(A):E+=1
						B-=E;A=[A for A in A if A is not _A];C=[A for A in C if A is not _A];G-=2;continue
					else:
						K=np.array(A[(B+1)%len(A)])-np.array(A[(B+2)%len(A)]);U=np.array(A[(B+3)%len(A)])+K;A[(B+3)%len(A)]=tuple(U)
						for D in range(2):A[(B+1+D)%len(A)]=_A;C[(B+1+D)%len(A)]=_A
						E=0
						for D in range(4):
							if B+1+D>=len(A):E+=1
						B-=E;A=[A for A in A if A is not _A];C=[A for A in C if A is not _A];G-=2
						if B>=2 and C[B]==1:B-=2;continue
		B+=1
		if B>=G:break
	L=Polygon(A);L=simplify_polygon(L,tol_length=consts.TOLERANCE);time.process_time()-N;return L
def diagonalize(regulation_polygon,grid_polygon,angle_min,angle_max):
	'폴리곤의 오목한 부분을 대각선으로 대체한다.\n\n    Args:\n        regulation_polygon (Polygon): 법규선 폴리곤\n        grid_polygon (Polygon): 격자화된 매스 폴리곤\n\n    Returns:\n        result_polygon (Polygon): 대각화 결과\n    ';G=grid_polygon
	if G.is_empty:return G
	E=gen_convexity_list(G);E=E[:-1];A=list(G.exterior.coords);A=A[:-1];D=copy.deepcopy(A)
	for C in range(len(A)):
		if E[C]==1 and E[(C+1)%len(A)]==0 and E[(C+2)%len(A)]==1:
			M=Point(A[C]);N=Point(A[(C+2)%len(A)]);O=LineString([M,N])
			if regulation_polygon.contains(O):
				H=np.array(A[C]);P=np.array(A[(C+1)%len(A)]);Q=np.array(A[(C+2)%len(A)]);I=P-H;J=Q-H;F=np.dot(I,J)/(np.linalg.norm(I)*np.linalg.norm(J))
				if F>1:F=1
				elif F<-1:F=-1
				B=np.arccos(F);B=B*180/np.pi
				if B>90:B=B-90
				if B<=45:K=B;L=90-B
				else:L=B;K=90-B
				if K>=angle_min and L<=angle_max:D[(C+1)%len(A)]=_A
	D=[A for A in D if A];D.append(D[0]);R=Polygon(D);return R
def merge_diagonals(diagonalized_polygon,diangonals_simplifying_angle,regulation_polygon):
	'폴리곤 도형이 diagonalized 된 이후 사선 사이의 각도가 tolerance 이하면 사선 사이를 simplify 합니다.\n\n    Args:\n        diagonalized_polygon (Polygon): diagonalize 를 통해 사선이 생성된 폴리곤.\n        diangonals_simplifying_angle (float): 사선 사이를 simplify 할 떄 사용할 사이각 톨러런스. 디그리입니다.\n        regulation_polygon (Polygon): 해당 층의 법규선\n\n    Returns:\n        Tuple(Polygon, bool): 사선 simplified 된 도형, simplify 가 실행되었는지, 즉 삭제된 점이 있는지 여부\n    ';B=diagonalized_polygon
	if B.is_empty:return B
	A=np.array(B.exterior.coords)[:-1];F=angle_of_polygon_vertices(B)[:-1];C=copy.deepcopy(A)
	for D in range(len(A)):
		E=diangonals_simplifying_angle/180*np.pi
		if np.pi-E<F[D]<np.pi+E:
			G=Point(A[(D-1)%len(A)]);H=Point(A[(D+1)%len(A)]);I=LineString([G,H])
			if regulation_polygon.contains(I):C[D]=_A
	C=[A for A in C if not np.isnan(A).all()];J=Polygon(C);return J
def orient_obb(obb):
	B=obb;B=shapely.ops.orient(B);A=list(B.exterior.coords)[:-1];D=np.argmin([Point(A).y for A in A]);C=[]
	for E in range(len(A)):C.append(A[(D+E)%len(A)])
	C.append(A[D]);F=Polygon(C);return F
def get_cut_line_and_depth(obb,cutting_policy,core):
	'매스 커팅 함수에서 제거 기준선분 도출. 코어가 empty가 아닌 경우 코어와 먼 것을 선택\n\n    Args:\n        obb (Polygon): 바운딩박스\n        cutting_policy (int): 커팅 방식\n        core (Polygon): 코어 도형\n\n    Raises:\n        ValueError: 잘못된 커팅 방식 입력이 들어온 경우\n    ';H=obb;G=cutting_policy;B=core;H=orient_obb(H);A=explode_to_segments(H.boundary)
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
def cut_north(mass_polygon,target_area):
	'target_area 를 만족할 때까지 북쪽에서 매스 폴리곤을 잘라내며 축소한다.\n\n    Args:\n        mass_polygon (Polygon): 축소 대상 매스\n        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.\n\n    Returns:\n        Polygon: 축소된 매스\n    ';E=mass_polygon;G,H,I,A=E.bounds;J=A-H;B=1;C=100
	while B<=C:
		D=(B+C)//2;K=box(G,A-J*(D/100),I,A);F=E.difference(K)
		if F.area>target_area:B=D+1
		else:C=D-1
	return F
def cut_major(mass_polygon,obb,target_area,core=Polygon()):
	'target_area 를 만족할 때까지 OBB 장변과 평행한 선분을 사용하여 매스 폴리곤을 잘라내며 축소한다.\n\n    Args:\n        mass_polygon (Polygon): 축소 대상 매스\n        obb (Polygon): mass_polygon의 바운딩 박스\n        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.\n        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.\n\n    Returns:\n        Polygon: 축소된 매스\n    ';E,F=get_cut_line_and_depth(obb=obb,cutting_policy=0,core=core);A=1;B=100
	while A<=B:
		C=(A+B)//2;G=offset_curve_polygon(E,F*(C/100),_D);D=mass_polygon.difference(G)
		if D.area>target_area:A=C+1
		else:B=C-1
	return D
def cut_minor(mass_polygon,obb,target_area,core=Polygon()):
	'target_area 를 만족할 때까지 OBB 단변과 평행한 선분을 사용하여 매스 폴리곤을 잘라내며 축소한다.\n\n    Args:\n        mass_polygon (Polygon): 축소 대상 매스\n        obb (Polygon): mass_polygon의 바운딩 박스\n        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.\n        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.\n\n    Returns:\n        Polygon: 축소된 매스\n    ';E,F=get_cut_line_and_depth(obb=obb,cutting_policy=1,core=core);A=1;B=100
	while A<=B:
		C=(A+B)//2;G=offset_curve_polygon(E,F*(C/100),_D);D=mass_polygon.difference(G)
		if D.area>target_area:A=C+1
		else:B=C-1
	return D
def cut_diag(mass_polygon,obb,target_area,core=Polygon()):
	'target_area 를 만족할 때까지 OBB 장변 및 단변과 평행한 선분을 동시에 사용하여 매스 폴리곤을 잘라내며 축소한다.\n\n    Args:\n        mass_polygon (Polygon): 축소 대상 매스\n        obb (Polygon): mass_polygon의 바운딩 박스\n        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.\n        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.\n\n    Returns:\n        Polygon: 축소된 매스\n    ';F,G=get_cut_line_and_depth(obb=obb,cutting_policy=2,core=core);C=1;D=100
	while C<=D:
		A=(C+D)//2;E=offset_curve_polygon(F,G.length*(A/100),_D);B=mass_polygon.difference(E);E=offset_curve_polygon(G,F.length*(A/100),_D);B=B.difference(E)
		if B.area>target_area:C=A+1
		else:D=A-1
	return B
def bcr_cut(regulation_polygon,floor_polygon,obb,bcr,cut_policy,bcr_margin,is_alt_ver,mass_angle=_A,is_premium=_C,core=Polygon()):
	H=regulation_polygon;G=core;F=mass_angle;E=cut_policy;D=obb;A=floor_polygon
	if F is not _A:D=get_rotated_bb(A,(np.cos(F),np.sin(F)))
	B=H.area*bcr*bcr_margin
	if is_alt_ver:B=H.area
	C=A
	if C.area>B or is_premium:
		if E==0:C=cut_north(A,B)
		elif E==1:C=cut_major(A,D,B,G)
		elif E==2:C=cut_minor(A,D,B,G)
		elif E==3:C=cut_diag(A,D,B,G)
		else:raise Exception('FIXME: invaild input for cut policy')
	return C
def far_cut(regulation_polygon,obb,floors,max_far_with_margin,smallest_core_area,cut_policy,min_mass_area,has_piloti,building_purpose,is_alt_ver,elev_area_for_advantage,use_small_core):
	H=smallest_core_area;E=cut_policy;D=floors;B=regulation_polygon.area*max_far_with_margin
	if use_small_core:B=min(B,consts.SMALL_CORE_MAX_FA)
	if building_purpose in(_P,_O,_X):B*=1.3
	B=B-H;A=[];F=0;I=0;J=_C
	for G in range(len(D)):
		A.append(D[G])
		if G!=0 or not has_piloti:F+=D[G].area-elev_area_for_advantage
		if F>B:I=F-B;J=_B;break
	if not J:return D,_B,10000
	C=A[-1].area-I
	if is_alt_ver:return A,_C,C
	if C<H:return A[:-1],_A,_A
	if E==0:A[-1]=cut_north(A[-1],C)
	elif E==1:A[-1]=cut_major(A[-1],obb,C)
	elif E==2:A[-1]=cut_diag(A[-1],obb,C)
	if A[-1].area<min_mass_area+6.72:A=A[:-1]
	return A,_A,_A
def get_hard_walls(parcel,road_edges):
	'_summary_\n    Args:\n        parcel (Polygon): parcel polygon\n        road_edges (_type_): the road edges\n    Returns:\n        hard walls: The walls of the plot_geom that are not road_edges\n    ';A=[];B=parcel.exterior.coords
	for(D,E)in zip(B[:-1],B[1:]):
		C=LineString([D,E])
		if not road_edges.contains(C):A.append(C)
	if len(A)==1:return A[0]
	else:return shapely.ops.linemerge(shapely.ops.unary_union(A))
def keep_exit(area,road_edge_list,width):
	'Returns areas that are accessible from the outside\n    Args:\n        area (MultiPolygon): areas that we want to know if they are accessible\n        road_edge_list (list): The road edges\n        width (float): Width of objects (ped or cars)\n    Returns:\n        MultiPolygon: the areas that are accessible\n    ';B=width;A=area;E=[A.buffer(B+consts.EPSILON)for A in road_edge_list]
	if isinstance(A,Polygon):A=MultiPolygon([A])
	C=[]
	for D in A.geoms:
		F=buffer_erosion_and_dilation(D,B)
		for G in E:
			if F.intersects(G):C.append(D);break
	return MultiPolygon(C)
def get_is_corridor_entry_failed(possible_core,possible_core_type,rotated_floors,floors_result,use_small_core,is_commercial_area):C=possible_core;B=floors_result;A=rotated_floors;D=gen_core([C]*len(A[:len(B)]),possible_core_type,A[:len(B)],use_small_core,is_commercial_area,is_escape_core=_C,is_center_core_placed=_C,is_using_adjusted_core=_C)[0];E=[_C]*len(A[:len(B)]);F,G=gen_corridor_entries(D,A[:len(B)],C,E);return any(all(A.is_empty for A in A)for A in F)
def get_possible_cores_and_types(buffered_top_floor,core_corner,core_size,core_type,allow_outside=_C):
	I=core_type;H=buffered_top_floor;A,B=core_corner;C,D=core_size;F=[];G=[];J=[box(A,B,A+C,B+D),box(A,B,A+C,B-D),box(A,B,A-C,B+D),box(A,B,A-C,B-D),box(A,B,A+D,B+C),box(A,B,A-D,B+C),box(A,B,A+D,B-C),box(A,B,A-D,B-C)]
	for E in J:
		if E.within(H):F.append(E);G.append(I)
		elif allow_outside:
			K=E.intersection(H)
			if K.area/E.area>=.9:F.append(E);G.append(I)
	return F,G
def place_cores(floors,mass_angle,tolerance,simple_deadspace_len,gridsize,refined_site,road_edge,is_commercial_area,use_small_core,mass_config,regulation):
	'모든 층의 변에 가장 많이 접한 코너들을 선택하여 코어 배치를 시도한다.\n    해당 층에 코어를 배치하지 못한 경우, 층을 제거하고 재시도한다.\n\n    Args:\n        floors (Polygon): _description_\n        cores (List(List(float, float))): 배치할 코어들의 모음 [코어 장변 길이, 코어 단변 길이]\n        core_types (List[int]): 각 코어 배치 후보의 코어 타입\n        mass_angle (float): 기준 바운딩 박스의 각도\n        has_elevator (bool): 엘리베이터 사용 여부\n        tolerance (float): 겹침 등 확인에 사용되는 tolerance값\n        simple_deadspace_len (float): 데드스페이스 폭\n        gridsize (float): 그리드 한 칸의 폭\n        check_core_center_intersecting_mass (bool): 엘레베이터 있는 코어 긴변쪽 중심부가 매스와 닿는지 체크할지 여부\n        add_core_center_as_candidates (bool): 각\n\n    Returns:\n        max_mass_core(Polygon), final_mass(List(Polygon)), core_type(int):\n        결과값 코어 폴리곤, 코어 영역이 제외된 층별 매스 폴리곤, 결과 코어 타입\n    ';v='Polygon';W=road_edge;V=simple_deadspace_len;U=tolerance;T=floors;O=mass_angle;K=refined_site;A=mass_config
	if not A.is_escape_core:
		X=[];Y=[];X.append(A.core_size_list[0]);Y.append(A.core_type_list[0])
		for D in range(len(A.core_size_list)):
			if D>1:
				if A.core_size_list[D][0]<A.core_size_list[0][0]or A.core_size_list[D][1]<A.core_size_list[0][1]:X.append(A.core_size_list[D]);Y.append(A.core_type_list[D])
		A.core_size_list=X;A.core_type_list=Y
	L=copy.deepcopy(T);G=[shapely.affinity.rotate(A,-O,(0,0),use_radians=_B)for A in T];G=[A.simplify(consts.TOLERANCE)for A in G];w=[shapely.affinity.rotate(A,-O,(0,0),use_radians=_B)for A in regulation];P=len(G)-1;M=_A
	for I in reversed(G):
		if P==0:return[[Polygon(),T,0,Polygon(),0]]
		E=np.array(I.exterior.coords);E=E[:-1];x=angle_of_polygon_vertices(I);c=[]
		for D in range(len(E)):
			if not x[D]<np.pi/2*.999:c.append(E[D])
		E=c
		if A.add_core_center_as_candidates and not A.is_sub_core_necessary:
			y=min(min(A)for A in A.core_size_list);z=explode_to_segments(I.exterior)
			for d in z:
				if d.length>consts.CORE_SEGMENT_GAP_LENGTH+y+consts.CORE_SEGMENT_GAP_LENGTH:E.append(np.array(d.centroid.coords[0]))
		e=[];f=G[P-1];Z=f.difference(I);Z=buffer_erosion_and_dilation(polygon=Z,buffer_distance=gridsize/2,use_intersection=_B,choose_biggest_polygon=_C);g=[]
		for(A0,h)in enumerate(E):
			A1=Point(h);i=A1.buffer(U)
			if i.disjoint(Z):
				if not i.disjoint(f):e.append(h);g.append(A0)
		P-=1;j=[];k=[];A2=[];A3=[];l=I.buffer(U);m=explode_to_segments(I.boundary)
		for(a,n)in zip(e,g):
			if n<len(m):
				A4=m[n]
				if A4.length<consts.SIMPLE_CORE_PLACEMENT_MIN_LENGTH:continue
			for(A5,b)in zip(A.core_size_list,A.core_type_list):
				A6,A7=get_possible_cores_and_types(l,a,A5,b);j.extend(A6);k.extend(A7)
				if A.is_sub_core_necessary:
					A8=[A for A in E if not np.isclose(A,a).all()];A9=sorted(A8,key=lambda x,c=a:np.linalg.norm(x-c),reverse=_B);AA=A9[:3]
					for AB in AA:
						AC=A.sub_core_size_list[b-1];AD,AE=get_possible_cores_and_types(l,AB,AC,b,allow_outside=_B);o=[];p=[]
						for(q,AF)in zip(AD,AE):
							if q.within(w[P].buffer(consts.TOLERANCE)):o.append(q);p.append(AF)
						A2.extend(o);A3.extend(p)
		N=[]
		for(F,r)in zip(j,k):
			H=_B;C=Polygon();Q=_A
			for AG in G[:len(L)]:
				B=make_floor_mass_after_core(AG,shapely.ops.unary_union([F,C]),V,use_simplify=_C)
				if not H:break
				AH=B.buffer(consts.TOLERANCE_MARGIN,join_style=JOIN_STYLE.mitre)
				if len(list(AH.interiors))!=0:H=_C;break
				if B.disjoint(F.buffer(consts.TOLERANCE_MARGIN,join_style=JOIN_STYLE.mitre)):H=_C;break
				if B.area<A.min_mass_area:H=_C;break
				AI,AJ,AK,AL=B.bounds
				if AK-AI<A.min_mass_width or AL-AJ<A.min_mass_width:H=_C;break
				if A.has_elevator and not is_elev_core_mass_connection_valid(F,B,U,A.check_core_center_intersecting_mass):H=_C;break
			if not H:continue
			if get_is_corridor_entry_failed(F,r,G,L,use_small_core,is_commercial_area):continue
			F=shapely.affinity.rotate(F,O,(0,0),use_radians=_B);C=shapely.affinity.rotate(C,O,(0,0),use_radians=_B);J=get_hard_walls(K,W);J=J if isinstance(J,MultiLineString)else MultiLineString([J]);AM=shapely.ops.unary_union([*J.geoms,F,C]);R=K.convex_hull.difference(J.buffer(consts.VEHICLE_ROAD_WIDTH/2,join_style=2)).intersection(K);R=keep_exit(R,W.geoms,consts.VEHICLE_ROAD_WIDTH/2);AN=1 if R.geom_type==v else len(R.geoms);AO=AM.buffer(consts.VEHICLE_ROAD_WIDTH/2,join_style=2);S=K.convex_hull.difference(AO).intersection(K);S=keep_exit(S,W.geoms,consts.VEHICLE_ROAD_WIDTH/2);AP=1 if S.geom_type==v else len(S.geoms)
			if AN!=AP:continue
			N.append([F,B,r,C,Q])
		if len(N)==0:L=L[:-1];continue
		M,_,s,C,Q=N[np.argmax([A[1].area for A in N])];break
	if M is _A:raise ConstructionError('코어 배치에 실패하였습니다.')
	AQ=sorted(N,key=lambda x:x[1].area,reverse=_B)[:consts.LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM];t=[]
	for AR in AQ:
		M,_,s,C,Q=AR;u=[]
		for AS in L:
			B=make_floor_mass_after_core(AS,M,V)
			if A.is_sub_core_necessary:B=make_floor_mass_after_core(B,C,V)
			u.append(B)
		t.append([M,u,s,C,Q])
	return t
def is_elev_core_mass_connection_valid(core,mass,tolerance,check_core_center_intersecting_mass):
	B=tolerance;A=mass;D=explode_to_segments(core.boundary);C=sorted(D,key=lambda x:x.length,reverse=_B)
	if check_core_center_intersecting_mass:
		if C[0].centroid.buffer(B).disjoint(A)and C[1].centroid.buffer(B).disjoint(A):return _C
	elif all(C.centroid.buffer(B).disjoint(A)for C in C):return _C
	return _B
def make_floor_mass_after_core(floor,core,simple_deadspace_len,use_simplify=_B):
	C=simple_deadspace_len;A=floor.difference(core);B=A.buffer(-C/2,join_style=JOIN_STYLE.mitre);B=filter_polygon(B);A=B.buffer(C/2,join_style=JOIN_STYLE.mitre).intersection(A);A=filter_polygon(A)
	if use_simplify:A=simplify_polygon(A,tol_length=consts.TOLERANCE)
	return A
def get_mass_each_floor(archi_line,each_floor_regulation,preset,mass_cut_length,gridsize,tolerance,tolerance_angle,diangonals_simplifying_angle,angle_min,angle_max,pack_after_cut,time_counter_dict,preset_mass_dict,mass_angle=_A,mass_cut_depth_divider=_J,fill_gap=_B,regulation_bounds=_A,emboss_cut_policy=0,use_emboss_cut_length_sorting=_C,longest_length_baseline=_A,shortest_length_baseline=_A):
	'매스를 한층만 생성합나디. 변화하는\n\n    Args:\n        archi_line (Polygon):\n        preset (List[int]): _description_\n        mass_cut_length (float): _description_\n        gridsize (float): _description_\n        tolerance (float): _description_\n        diangonals_simplifying_angle (float): _description_\n        bounding_box (Polygon): 특정 매스 각도로 생성하고 싶을 경우 mass angle 과 같이 넘겨줍니다..\n        preset_mass_dict (dict): 같은 프리셋으로 알 수 있는 매스는 공유하기 위한 dict\n        mass_angle (flooat): 특정 매스 각도로 생성하고 싶을 경우 사용합니다.\n\n    Raises:\n        Exception: _description_\n\n    Returns:\n        Tuple[Polygon, List[Polygon], Polygon, float]: _description_\n    ';M=mass_cut_depth_divider;L=preset_mass_dict;K=tolerance_angle;J=mass_cut_length;I=preset;G=time_counter_dict;F=tolerance;E=gridsize;C=each_floor_regulation;B=mass_angle;H:0;B:0
	if B is not _A:H=get_rotated_bb(C,(np.cos(B),np.sin(B)))
	elif I.bounding_box_config==0:H,B=gen_obb_from_longest_segment(C)
	elif I.bounding_box_config==1:H,B=gen_obb_from_convex_hull(C)
	else:raise Exception('FIXME: invaild input for bounding box creation')
	N=B,C.wkt;O=L.get(N)
	if O is not _A:Q,D=O;A=wkt.loads(Q)
	else:
		D=[];A=gen_grid_polygon(C,B,E,F,G,regulation_bounds);D.append(A)
		if fill_gap:
			P=simplify_polygon(buffer_dilation_and_erosion(A,E))
			if C.contains(P):A=P
		A=cut_extrude(A,E*10000,J,F,G);D.append(A);A=cut_emboss(A,J,emboss_cut_policy,G,_C,K,mass_cut_depth_divider=M,use_emboss_cut_length_sorting=use_emboss_cut_length_sorting,longest_length_baseline=longest_length_baseline,shortest_length_baseline=shortest_length_baseline);D.append(A);A=cut_extrude(A,E+F,E*10000,F,G);A=cut_emboss(A,E+F,1,G,_C,K,mass_cut_depth_divider=M);D.append(A);L[N]=A.wkt,D
	R=time.process_time();time.process_time()-R;no_diagonals_before_diagonalize(A)
	if I.diagonalize_config==1:A=diagonalize(C,A,angle_min,angle_max);A=merge_diagonals(A,diangonals_simplifying_angle,C)
	A=A.buffer(0);D.append(A);return A,D,H,B
def make_first_mass(archi_line,regulation,preset,mass_cut_length,gridsize,tolerance,time_counter_dict,preset_mass_dict,bcr,mass_config):
	P=regulation;M=bcr;L=preset_mass_dict;K=time_counter_dict;J=tolerance;I=gridsize;H=mass_cut_length;E=preset;C=archi_line;A=mass_config
	if not A.is_alt_ver:D,Q,F,G=get_mass_each_floor(C,P[0],E,H,I,J,A.tolerance_angle,A.diangonals_simplifying_angle,A.angle_min,A.angle_max,A.pack_after_cut,K,L,mass_cut_depth_divider=A.mass_cut_depth_divider,emboss_cut_policy=A.emboss_cut_policy,use_emboss_cut_length_sorting=A.use_emboss_cut_length_sorting,longest_length_baseline=A.longest_length_baseline,shortest_length_baseline=A.shortest_length_baseline);D=bcr_cut(C,D,F,M,E.cutting_policy_config,A.bcr_margin,A.is_alt_ver)
	else:
		B=P[:];N=0
		while _B:
			D,Q,F,G=get_mass_each_floor(C,B[0],E,H,I,J,A.tolerance_angle,A.diangonals_simplifying_angle,A.angle_min,A.angle_max,A.pack_after_cut,K,L,mass_cut_depth_divider=A.mass_cut_depth_divider,emboss_cut_policy=A.emboss_cut_policy,use_emboss_cut_length_sorting=A.use_emboss_cut_length_sorting,longest_length_baseline=A.longest_length_baseline,shortest_length_baseline=A.shortest_length_baseline)
			if D.area<=C.area*M*A.bcr_margin or N>int(1/consts.SIMPLE_REDUCE_RATIO_INTERVAL):break
			else:N+=1;T=shapely.affinity.scale(C,1-N*consts.SIMPLE_REDUCE_RATIO_INTERVAL);B[0]=bcr_cut(T,B[0],F,M,E.cutting_policy_config,A.bcr_margin,A.is_alt_ver);B[0]=filter_polygon(B[0])
		B[1:]=[A.intersection(B[0])for A in B[1:]];B[1:]=[filter_polygon(A)for A in B[1:]];B=list(filter(lambda x:not x.is_empty,B));R=[D];O=_A
		if A.use_same_grid:O=get_regulation_bounds(B,G)
		for U in B[1:]:
			try:V,S,S,S=get_mass_each_floor(C,U,E,H,I,J,A.tolerance_angle,A.diangonals_simplifying_angle,A.angle_min,A.angle_max,A.pack_after_cut,K,L,G,mass_cut_depth_divider=A.mass_cut_depth_divider,regulation_bounds=O,emboss_cut_policy=A.emboss_cut_policy,use_emboss_cut_length_sorting=A.use_emboss_cut_length_sorting,longest_length_baseline=A.longest_length_baseline,shortest_length_baseline=A.shortest_length_baseline);R.append(V)
			except Exception:pass
	return R,D,Q,F,G,B,O
def cut_mass_far(archi_line,bounding_box,mass,max_far_with_margin,smallest_core_area,preset,has_piloti,building_purpose,regulation_cut,mass_angle,mass_cut_length,gridsize,tolerance,time_counter_dict,preset_mass_dict,regulation_bounds,mass_config,elev_area_for_advantage,use_small_core):
	M=mass_angle;L=bounding_box;K=archi_line;H=regulation_cut;G=preset;F=smallest_core_area;B=mass_config;A=mass;N=[]
	for Q in A:
		O=buffer_erosion_and_dilation(Q,B.simple_deadspace_len)
		if O.is_empty:break
		else:N.append(O)
	A=N;A,R,D=far_cut(K,L,A,max_far_with_margin,F,G.cutting_policy_config,B.min_mass_area,has_piloti,building_purpose,B.is_alt_ver,elev_area_for_advantage,use_small_core)
	if B.is_alt_ver and not R:
		S=H[len(A)-1];I=1;J=1/consts.SIMPLE_REDUCE_RATIO_INTERVAL-1
		try:
			while _B:
				if I<J:C=(I+J)//2
				elif A[-1].area>D:C=C+1
				else:break
				T=shapely.affinity.scale(S,1-C*consts.SIMPLE_REDUCE_RATIO_INTERVAL);E=bcr_cut(T,H[len(A)-1],L,0,G.cutting_policy_config,0,B.is_alt_ver,M);E=filter_polygon(E);A[-1],P,P,P=get_mass_each_floor(K,E,G,mass_cut_length,gridsize,tolerance,B.tolerance_angle,B.diangonals_simplifying_angle,B.angle_min,B.angle_max,B.pack_after_cut,time_counter_dict,preset_mass_dict,M,mass_cut_depth_divider=B.mass_cut_depth_divider,regulation_bounds=regulation_bounds)
				if A[-1].area>D:I=C+1
				else:J=C-1
			H[len(A)-1]=E
		except Exception:pass
		if A[-1].area>D:A=A[:-1]
		elif D<F:A=A[:-1]
		elif A[-1].area<B.min_mass_area+F:A=A[:-1]
	return A
def core_placement(mass,mass_angle,tolerance,engine_type,gridsize,refined_site,road_edge,is_commercial_area,use_small_core,has_piloti,archi_line,regulation,max_far_with_margin,bcr,mass_config):
	I=use_small_core;H=is_commercial_area;B=mass_config;A=mass;U=place_cores(A,mass_angle,tolerance,B.simple_deadspace_len if engine_type==consts.ENGINE_TYPE_LIGHT else consts.TOLERANCE,gridsize,refined_site,MultiLineString([A['edge_geom']for A in road_edge['edges']]),H,I,B,regulation);O=[]
	for V in U:
		D,A,P,Q,R=V
		if D.is_empty:continue
		if has_piloti:S=[[Polygon()]]+[[A]for A in A[1:]]
		else:S=[[A]for A in A]
		E=S;W,X,Y,J,K,K,Z,K,a=gen_core([D],P,A,I,H,is_escape_core=B.is_escape_core,is_center_core_placed=_C,is_using_adjusted_core=_C,is_last_gen_core_called=_B);b=LineString(np.array(Z[0].coords)).wkt
		if B.is_escape_core:
			F=buffer_erosion_and_dilation(D-J[0],consts.TOLERANCE_MARGIN)
			if not F.is_empty:
				G=min(explode_to_segments(F.exterior),key=lambda s:s.length).length;G+=consts.TOLERANCE_MARGIN;G/=2
				for(L,M)in enumerate(A):C=buffer_dilation_and_erosion(shapely.ops.unary_union([M,F]),consts.TOLERANCE_MARGIN);C=buffer_erosion_and_dilation(C,G);A[L]=C
				for(L,M)in enumerate(E):C=buffer_dilation_and_erosion(shapely.ops.unary_union([M[0],F]),consts.TOLERANCE_MARGIN);C=buffer_erosion_and_dilation(C,G);E[L][0]=C
				D=J[0]
		N=[A,E,[Polygon()],[Polygon()],[Polygon()],[Polygon()],[Polygon()],[Polygon()],Polygon(),LineString().wkt,_A,_A]
		if B.is_sub_core_necessary:c,d,e,f,g,h,i,K,j=gen_core([Q],R,A,I,H,is_escape_core=B.is_escape_core,is_center_core_placed=_C,is_using_adjusted_core=_C,is_specific_escape_sub_core=B.is_specific_escape_sub_core,is_specific_escape_emgcy_elev_sub_core=B.is_specific_escape_emgcy_elev_sub_core,is_last_gen_core_called=_B);k=LineString(np.array(i[0].coords)).wkt;N=[A,E,c,d,e,f,g,h,Q,k,R,j]
		T=[A,E,W,X,Y,[Polygon()],[Polygon()],J,D,b,P,a];assert len(T)==len(N);O.append([T,N])
	return O
def adjust_mass_by_laws(mass_for_parklot_check,law_parklot_count,estimated_parklot_count,parklot_datas,underground_parking_boundaries,regulation_cut,bounding_box,mass_generation_preset,mass_config,mass_angle,core,hall_geom,stair_geom,elev_geom,archi_line,time_counter_dict,preset_mass_dict,regulation_bounds,engine_type,building_purpose,parking_commercial,commercial_type,first_floor_reduce_area,has_piloti,packed_unit_space_area_test_set_index,packed_unit_space_equal_division,packed_unit_space_sequantial,res,env_plan):
	T=mass_angle;O=estimated_parklot_count;M=packed_unit_space_sequantial;L=packed_unit_space_area_test_set_index;K=packed_unit_space_equal_division;J=building_purpose;I=mass_generation_preset;H=parklot_datas;G=law_parklot_count;E=regulation_cut;D=core;C=env_plan;B=mass_config;A=mass_for_parklot_check;N=0;a=D.buffer(consts.TOLERANCE_MACRO,join_style=JOIN_STYLE.mitre);U=E[len(A)-1];P=_C;B.is_sub_core_necessary=P;b=len(polygon_or_multipolygon_to_list_of_polygon(D));Q=np.inf
	if J==_O:Q=consts.MAX_HOUSEHOLDS_NUM_DAGAGU
	elif J==_P:Q=consts.MAX_HOUSEHOLDS_NUM_DAJUNG
	while G>O or B.is_sub_core_necessary and b==1 or J in(_P,_O)and len([A for B in C.packed_unit_space for A in B if not A.is_empty])>Q:
		if len(A)<=3:break
		c=A[-1][:];N+=1;d=shapely.affinity.scale(U,1-N*consts.SIMPLE_REDUCE_RATIO_INTERVAL);E[len(A)-1]=bcr_cut(d,E[len(A)-1],bounding_box,0,I.cutting_policy_config,0,is_alt_ver=_B,mass_angle=T,core=D);E[len(A)-1]=filter_polygon(E[len(A)-1]);F,V,V,V=get_mass_each_floor(archi_line,E[len(A)-1],I,I.mass_cut_length,I.gridsize,I.tolerance,B.tolerance_angle,B.diangonals_simplifying_angle,B.angle_min,B.angle_max,B.pack_after_cut,time_counter_dict,preset_mass_dict,T,mass_cut_depth_divider=B.mass_cut_depth_divider,regulation_bounds=regulation_bounds);F=make_floor_mass_after_core(F,D,B.simple_deadspace_len if engine_type==consts.ENGINE_TYPE_LIGHT else consts.TOLERANCE);A[-1]=[F];R=[D]
		if isinstance(D,MultiPolygon):R=D.geoms
		W=_B
		for S in R:
			if not is_entry_secured_between_geoms(F,S,consts.UNITENTRY_MIN_WIDTH):W=_C;break
		X=_B
		if B.has_elevator:
			for S in R:
				if not is_elev_core_mass_connection_valid(S,F,I.tolerance,B.check_core_center_intersecting_mass):X=_C;break
		if F.area<B.min_mass_area or N>=int(1/consts.SIMPLE_REDUCE_RATIO_INTERVAL)or a.disjoint(F)or not W or B.has_elevator and not X or consts.BUILDING_PURPOSE_MAP[J]>=3 and(G-O)*consts.PARKING_AREA_DIVISOR>sum(A.area for A in c):
			A=A[:-1];U=E[len(A)-1];N=0
			if commercial_type>0:C.commercial_type=max(C.commercial_type-1,consts.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN+int(has_piloti))
		K,M=A,A;C.packed_unit_space=K
		if consts.BUILDING_PURPOSE_MAP[J]in[_M]:C.commercial_type=len(K)
		Y=C.law_parklot_count;C.packed_unit_space=M;Z=C.law_parklot_count
		if Y<=Z:G=Y;L=0
		else:G=Z;L=1
		P=_C;B.is_sub_core_necessary=P
	e=[[A.area for A in A]for A in K];f=[[A.area for A in A]for A in M];g=[e,f];C.packed_unit_space=[K,M][L];H[0]=O;H[1]=G;H[2]=g;H[3].append(sum(A.area for A in flatten_list(A))+D.area*len(A));H[4]=L;return A,H,C,G
def gen_parking(use_mech_parking,use_under_parking,core_list,hall_geom,stair_geom,elev_geom,parking_result_dict,refined_site,archi_line,road_edge,mass,building_purpose,is_flag_lot,max_far,core,regulation_cut,bounding_box,mass_generation_preset,time_counter_dict,preset_mass_dict,mass_angle,engine_type,mass_after_pack,first_floor_reduce_area,estimated_parklot_count,regulation_bounds,mass_config,commercial_type,sub_core_related_geoms,res):
	I=commercial_type;H=mass_config;D=estimated_parklot_count;C=res;A=mass_after_pack;P=C[_E][_G][0];C[_F][_I];C[_F][_f];Q=C[_F][_S];R=[];S=LineString();T=_A;U=LineString();V=_A;j=Polygon();Polygon();Polygon();Polygon();k=[];W=[];l=[];m=[];X=[];Y,Z,a,b,c,d=sub_core_related_geoms;J=shapely.ops.unary_union([core,Y]);e=shapely.ops.unary_union([hall_geom,Z,c]);f=shapely.ops.unary_union([stair_geom,a]);g=shapely.ops.unary_union([elev_geom,b,d]);E=[D,0,[],[sum(A.area for A in flatten_list(A))+J.area*len(A)],0,R]
	if H.build_simple_check_parking:
		F=A;K,L=F,F;B=EnvPlan(K,[_A]*D,consts.PARKING_AREA_DIVISOR,I);M=B.law_parklot_count;B.packed_unit_space=L;N=B.law_parklot_count
		if M<=N:G=M;O=0
		else:G=N;O=1
		A,E,B,G=adjust_mass_by_laws(F,G,D,E,W,regulation_cut,bounding_box,mass_generation_preset,H,mass_angle,J,e,f,g,archi_line,time_counter_dict,preset_mass_dict,regulation_bounds,engine_type,building_purpose,Q,I,first_floor_reduce_area,P,O,K,L,C,B);mass=A
	h=_A;i=_A;return E,A,mass,B,S,T,h,i,X,U,V
def postprocess_mass(mass,has_piloti,min_mass_area,regulation,use_mass_intersection,engine_type,simple_deadspace_len,core,use_postprocess_emboss_cut,tolerance_angle,tolerance,postprocess_emboss_cut_length,time_counter_dict,mass_cut_depth_divider,use_deadspace_cut_with_exterior,first_floor_reduce_area,use_real_parking,mass_aspect_ratio_baseline,mass_bb_shortest_length_baseline,is_mech_park_weight_needed,env_plan):
	K=env_plan;J=tolerance;I=tolerance_angle;H=min_mass_area;F=simple_deadspace_len;E=engine_type;D=has_piloti;C=regulation;B=core;A=mass;A=check_min_size(A,D,C,H)
	if use_mass_intersection:A=check_mass_intersection(A,B,E,C,F)
	if use_postprocess_emboss_cut:A=postprocess_emboss_cut(A,B,J,I,C,postprocess_emboss_cut_length,time_counter_dict,mass_cut_depth_divider)
	elif D:A[0]=[wkt.loads(_A6)]
	if use_deadspace_cut_with_exterior:
		L=min(explode_to_segments(B.exterior),key=lambda s:s.length).length;M=F
		if L<=F:M=L-consts.TOLERANCE
		A=deadspacecut_with_exterior(A,I,J,B,E,M,C)
	A=check_min_size(A,D,C,H);G=get_score(B,A,first_floor_reduce_area,D,use_real_parking,E==consts.ENGINE_TYPE_BASIC)
	if is_mech_park_weight_needed:G*=consts.MECH_PARK_SCORE_WEIGHT_FACTOR_LIGHT
	if K.law_parklot_count>K.parklot_count:G=consts.LIGHT_SCORE_FOR_PARKLOT_ERROR
	if E==consts.ENGINE_TYPE_BASIC:A=basic_final_postprocessing(A,B,C)
	A=get_final_mass(A,B,mass_aspect_ratio_baseline,mass_bb_shortest_length_baseline);return A,G
def create_mass_result(engine_type,res,score,core,hall_geom,stair_geom,elev_geom,sub_core,sub_hall_geom,sub_stair_geom,sub_elev_geom,sub_core_attached_room,sub_core_emergency_elev,sub_path,sub_path_poly,mass,mass_angle,intermediate_results,parklot_datas,first_floor_reduce_area,path,path_poly,road_edge,core_type,sub_core_type,core_orientation,mech_park_visual_data,under_parking_visul_data,error_type,elev_area_for_advantage,env_plan,summary_is_escape_core,use_small_core,has_elevator,is_commercial_area,has_commercial,is_specific_escape_sub_core,is_specific_escape_emgcy_elev_sub_core,regulation,parking_objects_list_of_list,visualize_inside_get_mass):A=regulation;return{'score':score,_c:mass,_d:core,'regulation':A,'hall_geom':hall_geom,'stair_geom':stair_geom,'elev_geom':elev_geom,'mass_angle':mass_angle,'intermediate_results':intermediate_results,'parklot_datas':parklot_datas,'first_floor_reduce_area':first_floor_reduce_area,'path':path,'path_poly':path_poly,'road_edge':road_edge,'legal_geom':A,'core_type':core_type,'core_orientation':core_orientation,'error_type':error_type,'elev_area_for_advantage':elev_area_for_advantage,_e:use_small_core}
def get_score(core,mass,first_floor_reduce_area,has_piloti,use_real_parking,is_engine_type_basic):
	'aspect_ratio, ombr_ratio를 사용하여 결과의 점수를 계산\n\n    Args:\n        core (Polygon): 코어 폴리곤\n        mass (List(List(Polygon))): 층별 매스 폴리곤. 세대구분이 있는 프리미엄과 동일한 형식 사용\n        has_piloti (bool): 필로티 여부, 1층에서 용적 제외 용도\n        use_real_parking (bool): 실제 주차 배치 사용 여부\n\n    Returns:\n        float: 해당 매스의 점수\n    ';A=mass
	if len(A)==0:raise Exception(_A7)
	else:B=get_gfa(core,A,first_floor_reduce_area,has_piloti,use_real_parking,is_engine_type_basic);B-=core.area*len(A);C=B
	return C
def get_gfa(core,mass,first_floor_reduce_area,has_piloti,use_real_parking,is_engine_type_basic):
	A=mass
	if A is _A or len(A)==0:return 0
	B=sum(sum(A.area for A in A)for A in A)
	if not use_real_parking:
		C=sum(A.area for A in A[0])
		if not has_piloti:
			D=max(0,C-first_floor_reduce_area)
			if D>=consts.UNIT_MIN_AREA:B+=D
		else:B-=C
	if not is_engine_type_basic:B+=core.area*len(A)
	return B
def get_final_mass(mass,core,mass_aspect_ratio_baseline,mass_bb_shortest_length_baseline):
	'최종적으로 매스를 정돈한다\n\n    Args:\n        mass (List[List[Polygon]]): 층별 매스 도형\n        mass_aspect_ratio_baseline (float): 가로 세로 비율 최대 허용값\n        core (Polygon): 코어 도형\n\n    Returns:\n        List[List[Polygon]]: 최종 층별 매스 도형\n    ';C=np.array(explode_to_segments(core.exterior)[0].coords);F=C[1]-C[0];B=[]
	for(G,A)in enumerate(mass):
		if G==0:B.append(A);continue
		H,I=get_aspect_ratio(A[0],F,return_bb=_B);J=sorted([A.length for A in explode_to_segments(I.exterior)])[0];D=_B;E=_B;D=J>=mass_bb_shortest_length_baseline;E=H<mass_aspect_ratio_baseline
		if not A[0].is_empty and(E or D):B.append([simplify_polygon(A[0])])
	return B
def get_valid_mass_before_placing_core(original_mass,regulation,tolerance,tolerance_angle,simple_deadspace_len):
	'코어 배치 이전 단계에서 유효하지 않은 층별 매스 제거\n\n    Args:\n        original_mass (List[Polygon]): 정리 대상 매스\n        regulation (List[Polygon]): 법규선\n        tolerance (float): 데드스페이스 제거 관련 상수\n        tolerance_angle (float): 데드스페이스 제거 관련 상수\n        simple_deadspace_len (float): 데드스페이스 제거 관련 상수\n\n    Returns:\n        List[Polygon]: 정리 후 층별 매스\n    ';G=simple_deadspace_len;F=regulation;E=tolerance;H=[]
	for B in original_mass:B=filter_polygon(B);B=buffer_erosion_and_dilation(polygon=B,buffer_distance=E,use_intersection=_B,choose_biggest_polygon=_B);H.append(B)
	A=H;I=[]
	for(K,L)in enumerate(A):M=simplify_polygon(L,tol_angle=tolerance_angle,tol_length=consts.TOLERANCE,container_geometry=F[K]);I.append(M)
	A=I
	for C in range(1,len(A)):
		J=A[C].intersection(A[C-1]);D=buffer_dilation_and_erosion(polygon=J,buffer_distance=consts.SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE)
		if not D.within(F[C]):A[C]=simplify_polygon(J);continue
		while len(remove_deadspace_with_extended_exterior(polygon=D,deadspace_len=G,tolerance=E,return_only_splits=_B))>1:D=remove_deadspace_with_extended_exterior(polygon=D,deadspace_len=G,tolerance=E)
		A[C]=simplify_polygon(D)
	return A
def get_error_result(e,first_floor_reduce_area,road_edge,engine_type):
	A=str(e)
	if A=='주차 대수가 0대입니다.':B='parking_failed'
	elif A==_A7:B='mass_creation_failed'
	elif A=='기계식주차 배치 실패로 중복 결과가 생성됩니다.':B='duplicate_result_mech_park'
	elif A=='저층상가 배치 실패로 중복 결과가 생성됩니다.':B='duplicate_result_lower_commercial'
	else:B=A
	C=create_mass_result(engine_type=engine_type,res=_A,score=-10000,core=_A,hall_geom=_A,stair_geom=_A,elev_geom=_A,sub_core=_A,sub_hall_geom=_A,sub_stair_geom=_A,sub_elev_geom=_A,sub_core_attached_room=_A,sub_core_emergency_elev=_A,sub_path=_A,sub_path_poly=_A,mass=_A,mass_angle=_A,intermediate_results=_A,parklot_datas=_A,first_floor_reduce_area=first_floor_reduce_area,path=_A,path_poly=_A,road_edge=road_edge,core_type=_A,sub_core_type=_A,core_orientation=_A,mech_park_visual_data=_A,under_parking_visul_data=_A,error_type=B,elev_area_for_advantage=0,env_plan=_A,summary_is_escape_core=_C,use_small_core=_C,has_elevator=_C,is_commercial_area=_C,has_commercial=_C,is_specific_escape_sub_core=_C,is_specific_escape_emgcy_elev_sub_core=_C,regulation=_A,parking_objects_list_of_list=_A,visualize_inside_get_mass=_C);return C
def get_mass(mass_generation_preset,refined_site,archi_line,regulation,building_purpose,time_counter_dict,postprocess_emboss_cut_length,estimated_parklot_count,first_floor_reduce_area,preset_mass_dict,parking_result_dict,road_edge,use_small_core,is_commercial_area,is_flag_lot,use_mech_parking,use_under_parking,custom_config,engine_type,mass_config,res,commercial_type,visualize_inside_get_mass):
	'매스를 생성합니다.\n\n    Args:\n        mass_generation_preset (List(int)): 필지 축 생성 방식, 대각화 여부, 커팅 정책을 결정하는 상수\n        refined_site (Polygon): 사이트 도형\n        archi_line (Polygon): 건축선 폴리곤\n        regulation (List(Polygon)): 일조사선 적용된 층별 법규 폴리곤\n        building_purpose (str): 설계 대상 건물 용도\n        time_counter_dict (dict[str, float]): 함수별 시간 체크용 dict\n        postprocess_emboss_cut_length (float), 최종 단계 엠보스 컷 길이\n        estimated_parklot_count (int): 대지 면적으로 가늠한 예상 주차 대수\n        first_floor_reduce_area (float): 1층 매스에서 제외해야 할 면적 - 가상 주차로 인해 깎이는 부분을 가정\n        preset_mass_dict (dict): 같은 프리셋으로 알 수 있는 매스는 공유하기 위한 dict\n        parking_result_dict (dict): 같은 프리셋으로 알 수 있는 주차를 공유하기 위한 dict\n        road_edge (dict[str, Any]): 도로 정보\n        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)\n        is_commercial_area (bool): 상업지역 여부\n        is_flag_lot (bool): 자루형필지 여부\n        use_mech_parking (bool): 기계식주차 사용 여부\n        custom_config (dict): 교체할 config\n        engine_type (str): 입력받은 엔진 타입\n        mass_config (SimpleConfig): 매스 생성 config. custom_config를 덮어씌움\n        res (dict): 엔진입력서비스 데이터\n        commercial_type (int): 상가 층수\n        visualize_inside_get_mass (bool): visualize 실행 여부\n    Returns:\n        mass (List(Polygon)): 조건에 따라 생성된 층별 매스 폴리곤\n    ';p=use_mech_parking;o=refined_site;Y=commercial_type;T=preset_mass_dict;Q=is_commercial_area;P=road_edge;O=time_counter_dict;L=use_small_core;K=building_purpose;H=first_floor_reduce_area;G=archi_line;F=regulation;E=engine_type;D=res;C=mass_generation_preset;A=mass_config;x='';U=[]
	try:
		q=D[_F][_K];r=q+A.far_margin_for_commercial;M=[];F=[simplify_polygon(A,tol_length=consts.TOLERANCE)for A in F];y=len(F);z=time.process_time();B,Z,M,a,R,b,c=make_first_mass(G,F,C,C.mass_cut_length,C.gridsize,C.tolerance,O,T,D[_F][_I],A);time.process_time()-z;M.append(Z)
		if not A.is_alt_ver:
			B=[Z]
			for A0 in F[1:]:B.append(A0.intersection(Z))
		A.set_core_config(G,B,K,L,Q,Y,D,E,use_sub_core=C.use_sub_core);s=box(0,0,A.core_size_list[0][0],A.core_size_list[0][1]);d=gen_core([s],A.core_type_list[0],[s],L,Q,is_escape_core=A.is_escape_core,is_center_core_placed=_C,is_using_adjusted_core=_C,is_last_gen_core_called=_B)[2][0].area;t=A.core_size_list[0][0]*A.core_size_list[0][1]-d;e=copy.deepcopy(B)
		for f in reversed(B):
			f=filter_polygon(f)
			if f.area<A.min_mass_area+t:e=e[:-1]
			else:break
		B=e;M.append(B);A1=time.process_time();B=cut_mass_far(G,a,B,r,t,C,D[_E][_G][0],K,b,R,C.mass_cut_length,C.gridsize,C.tolerance,O,T,c,A,d,L);M.append(B);A.set_core_config(G,B,K,L,Q,Y,D,E,use_sub_core=C.use_sub_core);time.process_time()-A1;B=get_valid_mass_before_placing_core(B,F,C.tolerance,A.tolerance_angle,A.simple_deadspace_len);A2=time.process_time();V=core_placement(B,R,C.tolerance,E,C.gridsize,o,P,Q,L,D[_E][_G][0],G,F,r,D[_F][_I],A)
		if E==consts.ENGINE_TYPE_BASIC or A.use_real_parking and p:V=V[:1]
		if len(V)==0:raise ConstructionError('코어 배치 실패')
		for(A3,A4)in V:
			try:
				B,g,A5,A6,A7,I,I,A8,S,A9,AA,AV=A3;I,I,AB,AC,AD,I,AE,AF,h,I,AG,I=A4
				if A.commercial_type>0 and y!=len(B):A.commercial_type=min(A.commercial_type,max(consts.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN+D[_E][_G][0],len(B)-consts.MAX_HOUSING_FLOOR_MAP[K]))
				i=A5[0];j=A6[0];k=A7[0];l=AB[0];m=AC[0];n=AD[0];u=AE[0];v=AF[0];AH=h,l,m,n,u,v;time.process_time()-A2;AI=time.process_time();N,g,B,W,AJ,AK,AL,AM,AN,AO,AP=gen_parking(p,use_under_parking,A8,i,j,k,parking_result_dict,o,G,P,B,K,is_flag_lot,q,S,b,a,C,O,T,R,E,g,H,estimated_parklot_count,c,A,A.commercial_type,AH,D)
				if C.use_sub_core and not A.is_sub_core_necessary:raise ConstructionError('코어 2개소가 배치되지 않아도 되는 설계안에서 코어 2개소가 배치되었습니다.')
				time.process_time()-AI;B=g;M.append([A[0]for A in B]);AQ=_C;B,w=postprocess_mass(B,D[_E][_G][0],A.min_mass_area,F,A.use_mass_intersection,E,A.simple_deadspace_len,S,A.use_postprocess_emboss_cut,A.tolerance_angle,C.tolerance,postprocess_emboss_cut_length,O,A.mass_cut_depth_divider,A.use_deadspace_cut_with_exterior,H,A.use_real_parking,A.mass_aspect_ratio_baseline,A.mass_bb_shortest_length_baseline,AQ,W);AR=A.is_escape_core;AS,AT=B,B;B,N,W,I=adjust_mass_by_laws(B,N[1],N[0],N,[],b,a,C,A,R,shapely.ops.unary_union([S,h]),shapely.ops.unary_union([i,l]),shapely.ops.unary_union([j,m]),shapely.ops.unary_union([k,n]),G,O,T,c,E,K,D[_F][_S],Y,H,D[_E][_G][0],N[4],AS,AT,D,W);w=get_score(S,B,H,D[_E][_G][0],A.use_real_parking,E==consts.ENGINE_TYPE_BASIC);J=create_mass_result(E,D,w,S,i,j,k,h,l,m,n,u,v,AO,AP,B,R,M,N,H,AJ,AK,P,AA,AG,A9,AL,AM,x,d,W,AR,L,D[_E][_H][0],Q,D[_E][_R][0],A.is_specific_escape_sub_core,A.is_specific_escape_emgcy_elev_sub_core,F,AN,visualize_inside_get_mass);U.append(J)
			except Exception as X:J=get_error_result(X,H,P,E);U.append(J)
	except Exception as X:print(X);J=get_error_result(X,H,P,E);U.append(J)
	finally:AU=sorted(U,key=lambda x:x['score'],reverse=_B);J=AU[0]
	return J
def run_basic(site_polygon,solar_setback_flag_polygon,openspace_buffer_len,estimated_parklot_count,floor_height,solar_setback_min_height,solar_setback_ratio_from_user_input,mass_generation_preset,mass_config,engine_input):
	G=engine_input;F=solar_setback_ratio_from_user_input;D=mass_config;C=mass_generation_preset;B=estimated_parklot_count;A=site_polygon;K=A;L=A;H=G[_F][_L];E=[A.buffer(-openspace_buffer_len,join_style=JOIN_STYLE.mitre)]*H
	for(I,M)in enumerate(E):
		J=floor_height*(I+1)
		if J>solar_setback_min_height:E[I]=M.intersection(shapely.affinity.translate(solar_setback_flag_polygon,0,-F*J))
	N=_M;O={};P=2.4;B=B;Q=0;R={};S={};T={'edges':[]};U=_C;V=F==.0;W=_C;X=_C;Y=_C;Z='basic';C=CustomClassForAttrFromDict(C);D=CustomClassForAttrFromDict(D);a=G;b={};c=H;d=_C;return get_mass(C,K,L,E,N,O,P,B,Q,R,S,T,U,V,W,X,Y,b,Z,D,a,c,d)
class BasicEngine:
	def __init__(A,site_polygon_from_user_input,solar_setback_flag_polygon,open_space_buffer_len,estimated_parklot_count,floor_height,parking_area_divisor,has_elevator,has_piloti,max_bcr,max_far,max_floor,max_height):A.site_polygon_from_user_input=site_polygon_from_user_input;A.solar_setback_flag_polygon=solar_setback_flag_polygon;A.open_space_buffer_len=open_space_buffer_len;A.estimated_parklot_count=estimated_parklot_count;A.floor_height=floor_height;A.parking_area_divisor=parking_area_divisor;A.has_elevator=has_elevator;A.has_piloti=has_piloti;A.max_bcr=max_bcr;A.max_far=max_far;A.max_floor=max_floor;A.max_height=max_height
	def run(A):D={_T:A.open_space_buffer_len,_U:A.estimated_parklot_count,_V:A.floor_height,_W:A.parking_area_divisor,_H:A.has_elevator,_G:A.has_piloti,_I:A.max_bcr,_K:A.max_far,_L:A.max_floor,_N:A.max_height};custom_input.update(D);C=custom_input[_U];E=custom_input[_T];F=custom_input[_g];G=custom_input[_V];H=custom_input[_h];consts.PARKING_AREA_DIVISOR=custom_input[_W];mass_generation_preset_default.update(custom_input);mass_config_default.update(custom_input);engine_input_default[_E][_H]=[custom_input[_H]];engine_input_default[_E][_G]=[custom_input[_G]];engine_input_default[_E][_R]=[not custom_input[_G]];engine_input_default[_F][_I]=custom_input[_I];engine_input_default[_F][_K]=custom_input[_K];engine_input_default[_F][_L]=custom_input[_L];engine_input_default[_F][_N]=custom_input[_N];C=int(C);I=shapely.ops.orient(A.site_polygon_from_user_input);J=shapely.ops.orient(A.solar_setback_flag_polygon);B=run_basic(I,J,E,C,G,H,F,mass_generation_preset_default,mass_config_default,engine_input_default);B[_c]=[[shapely.ops.orient(A)for A in A]for A in B[_c]];B[_d]=shapely.ops.orient(B[_d]);return B