# requirements: numpy>=1.23.5
# requirements: shapely>=1.8.5

import copy
import math
import time
import numpy as np
from typing import List, Tuple, Union, Iterable

import shapely.affinity
import shapely.ops
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


mass_generation_preset_default = {
    "bounding_box_config": 0,  # 0: 장변, 1: obb
    "diagonalize_config": 0,  # 0: no, 1: yes
    "cutting_policy_config": 1,  # 0: north, 1: major, 2: minor 3: diagonal
    "gridsize": 0.3,
    "mass_cut_length": 2.8,
    "use_small_core": False,
    "tolerance": 0.0003,
    "use_sub_core": False,
}


mass_config_default = {
    "angle_min": 0,
    "angle_max": 90,
    "tolerance_angle": 0.1,
    "diangonals_simplifying_angle": 15.0,
    "min_mass_area": 14,
    "simple_deadspace_len": 1.8,
    "bcr_margin": 1.03,
    "far_margin": 0.11,
    "far_margin_for_commercial": 0.1,
    "use_mass_intersection": True,
    "pack_after_cut": False,
    "use_postprocess_emboss_cut": True,
    "use_deadspace_cut_with_exterior": True,
    "use_same_grid": True,
    "build_simple_check_parking": True,
    "use_real_parking": False,
    "is_alt_ver": True,
    "check_core_center_intersecting_mass": True,
    "add_core_center_as_candidates": True,
    "min_mass_width": 2.0,
    "mass_cut_depth_divider": 1.6,
    "emboss_cut_policy": 1,
    "use_emboss_cut_length_sorting": True,
    "longest_length_baseline": 2.6,
    "shortest_length_baseline": 1.2,
    "mass_aspect_ratio_baseline": 6.0,
    "mass_bb_shortest_length_baseline": 4.2,
    "core_size_list": None,
    "core_type_list": None,
    "has_elevator": None,
}


engine_input_default = {
    "options": {
        "has_elevator": [True],
        "unit_type": ["1r"],
        "has_piloti": [True],
        "has_commercial": [False],
    },
    "regulations": {
        "max_bcr": 0.6,
        "max_far": 2.0,
        "max_floor": 7,
        "max_height": 0.0,
        "parking_residential": None,
        "parking_commercial": None,
    },
}

custom_input = {
    "open_space_buffer_len": 0.5,
    "estimated_parklot_count": 8,
    "solar_setback_ratio": 0.5,
    "solar_setback_min_height": 10.0,
    "floor_height": 3.0,
    "parking_area_divisor": 134,
    "has_elevator": True,
    "has_piloti": True,
    "max_bcr": 0.6,
    "max_far": 2.0,
    "max_floor": 7,
    "max_height": 0.0,
}


class CustomClassForAttrFromDict:
    def __init__(self, dict_obj: dict):
        for key, value in dict_obj.items():
            setattr(self, key, value)

    def set_core_config(
        self,
        archi_line: Polygon,
        mass: List[Polygon],
        building_purpose: str,
        use_small_core: bool,
        is_commercial_area: bool,
        commercial_type: int,
        res: dict,
        engine_type: str,
        use_sub_core: bool = False,
    ):

        # 피난계단 설치 여부. 베이직 엔진에서는 False 고정
        is_escape_core = False
        is_sub_core_necessary = False
        is_specific_escape_sub_core = False
        is_specific_escape_emgcy_elev_sub_core = False

        commercial_purposes = ["geunsaeng"]

        has_elevator = res["options"]["has_elevator"][0]

        if is_commercial_area and building_purpose in commercial_purposes:
            if is_escape_core:
                # 층고 4m 피난계단
                core_wide_list = consts.CORE_WIDE_ESCAPE_TALL
                core_narr_list = consts.CORE_NARR_ESCAPE_TALL

                # 피난계단은 엘리베이터가 무조건 포함되기 때문에 프리셋과 관계없이 True로 고정
                has_elevator = True

            # 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)
            elif use_small_core:
                core_wide_list = consts.CORE_WIDE_TALL_SMALL
                core_narr_list = consts.CORE_NARR_TALL_SMALL

            else:
                core_wide_list = consts.CORE_WIDE_TALL
                core_narr_list = consts.CORE_NARR_TALL

        else:
            use_district_small_core = use_small_core

            if is_escape_core:
                core_wide_list = consts.CORE_WIDE_ESCAPE
                core_narr_list = consts.CORE_NARR_ESCAPE

                # 피난계단은 엘리베이터가 무조건 포함되기 때문에 프리셋과 관계없이 True로 고정
                has_elevator = True

            elif use_small_core and use_district_small_core:
                core_wide_list = consts.CORE_WIDE_SMALL
                core_narr_list = consts.CORE_NARR_SMALL
            else:
                core_wide_list = consts.CORE_WIDE
                core_narr_list = consts.CORE_NARR

        # 엘리베이터 유무에 따른 코어 선택
        if not has_elevator:
            core_wide_list = [core_wide_list[0]]
            core_narr_list = [core_narr_list[0]]
            core_type_list = [0]
        else:
            if not is_escape_core:
                core_wide_list = core_wide_list[1:]
                core_narr_list = core_narr_list[1:]
                core_type_list = [i + 1 for i in range(len(core_wide_list))]

            else:
                # 피난계단 코어는 사이즈 리스트가 2개이므로 슬라이싱 하지 않음
                core_type_list = [i + 1 for i in range(len(core_wide_list))]

        core_size_list = []
        for i in range(len(core_wide_list)):
            core_size_list.append([core_wide_list[i], core_narr_list[i]])

        assert len(core_size_list) == len(core_type_list), "코어타입과 코어사이즈 길이가 다릅니다."

        sub_core_size_list = []
        if is_sub_core_necessary:
            if is_specific_escape_sub_core:
                if is_specific_escape_emgcy_elev_sub_core:
                    sub_core_wide = consts.CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL
                    sub_core_narr = consts.CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL
                else:
                    sub_core_wide = consts.CORE_WIDE_SPECIFIC_ESCAPE_TALL
                    sub_core_narr = consts.CORE_NARR_SPECIFIC_ESCAPE_TALL

            else:
                sub_core_wide = core_wide_list
                sub_core_narr = core_narr_list

            for i in range(len(sub_core_wide)):
                sub_core_size_list.append([sub_core_wide[i], sub_core_narr[i]])

        # 코어 관련 config들 매스 생성에 사용할 수 있도록 인스턴스 변수로 저장
        self.has_elevator = has_elevator
        self.core_type_list = core_type_list
        self.core_size_list = core_size_list
        self.sub_core_size_list = sub_core_size_list

        self.is_escape_core = is_escape_core
        self.is_sub_core_necessary = is_sub_core_necessary
        self.is_specific_escape_sub_core = is_specific_escape_sub_core
        self.is_specific_escape_emgcy_elev_sub_core = is_specific_escape_emgcy_elev_sub_core

        self.commercial_type = commercial_type


class ConstructionError(Exception):
    def __init__(self, msg: str):
        super().__init__()
        self._msg = msg

    def __str__(self) -> str:
        return self._msg


class consts:
    EPSILON = 1e-6  # 필로티로 인한 면적 0세대 보정용

    # 붙어 있어야 하는 설계요소 사이의 공차는 다르게 명시되는 부분이 없을 경우 TOLERANCE까지 인정한다.
    # NOTE(ckc): 모든 기하연산에 사용되는 길이의 최소 단위는 TOLERANCE임을 보장해야함.
    TOLERANCE = 1e-6  # 0.001mm

    TOLERANCE_LARGE = 1e-5

    # 겹치는 설계요소끼리의 연산 이후 발생할 수 있는 sliver 제거에 TOLERANCE_SLIVER를 사용한다.
    TOLERANCE_SLIVER = 1e-3  # 1mm
    TOLERANCE_GROUPING = 1e-1
    TOLERANCE_ANGLE = 1e-2

    # 설계요소를 의도적으로 확장하여 intersection을 확인할 때는 TOLERANCE_MARGIN을 사용한다.
    TOLERANCE_MARGIN = 1e-2  # 1cm

    TOLERANCE_MACRO = 1e-1
    MASS_DEADSPACE_LENGTH = 3 + 1e-3
    UNITSPACE_DEADSPACE_LENGTH = 2 + 1e-3

    TOLERANCE_UNIT = 1

    # 자루형 필지 판단할 최소 필지 크기
    FLAG_LOT_CHECK_MIN_AREA = 200

    # EACH_UNIT_DEADSPACE_LENGTH_M가 POSTPROCESS_DEADSPACE_LENGTH_M보다 클 경우 매스에 구멍이 생길 수 있다.
    EACH_UNIT_DEADSPACE_LENGTH_M = 1.999
    POSTPROCESS_DEADSPACE_LENGTH_M = 2
    COMMERCIAL_ADDITIONAL_DEADSPACE_LENGTH = 3
    U_SHAPE_DEADSPACE_LENGTH = 0.3
    BCR_EXTRA = 0.03  # 건폐율 보정 상한
    GFA_CUT_VECTOR = (0, 1)
    GFA_CUT_RANGE = 1
    GFA_CUT_KEEP_FLOOR = 3
    GRID_INTERVAL = 0.15
    MASS_CUT_LENGTH = 3
    MASS_EMBOSS_LENGTH = 3
    MIN_REDUCE_FLOOR_AREA = 300
    STAGGER_UPPER_LENGTH = 4
    STAGGER_UPPER_DEPTH = 0.8
    STAGGER_LOWER_LENGTH = 3
    STAGGER_LOWER_DEPTH = 0.5
    STAGGER_MIN_LENGTH = 2
    ANGLECUT_LENGTH = 10
    MASSREMOVER_LENGTH = 40
    PARTITIONSPLITTER_LENGTH = 30
    PARTITIONSPLITTER_INTERVAL = 1.05
    # PARTITIONSPLITTER_MARGIN = 3.4
    PARTITIONSPLITTER_MARGIN = 2.4
    PARTITIONSPLITTER_MERGE = 1.5
    # PARTITIONSPLITTER_KEEPOUT_LENGTH = 1.5
    PARTITIONSPLITTER_KEEPOUT_LENGTH = 0.7
    CORE_SPLITTER_DIVIDE_COUNT = 2
    CORRIDORTUNE_INTERVAL = 0.35
    # 편복도 최소 너비. 중심선치수 1.4m
    # 중복도 최소 너비는 중심선 치수 2m로, 1.4m은 모든 복도의 최소 너비가 된다.
    HALL_WIDTH_OFFSET_MARGIN = 0.15
    HALL_WIDTH = 1.4
    HALL_WIDTH_EMGCY = 1.5
    HALL_WIDTH_ESCAPE = 1.6
    # 엘리베이터 승강로 규격: 1.93m x 2.35m
    ELEV_WIDTH = 1.93
    ELEV_HEIGHT = 2.35
    ADJUSTED_ELEV_WIDTH = 1.9
    ADJUSTED_ELEV_HEIGHT = 2.4
    ELEV_WIDTH_SMALL = 1.68
    ELEV_HEIGHT_SMALL = 2.05
    ELEV_WIDTH_SPECIFIC = 2.0
    ELEV_HEIGHT_SPECIFIC = 2.7
    EMERGENCY_ROOM_WIDTH = 2.75
    STAIR_WIDTH = 2.8
    ADJUSTED_ELEV_WIDTH = 1.900
    ADJUSTED_ELEV_HEIGHT = 2.400
    ADJUSTED_REMAIN_HALL_DIS = 2.830
    CORE_VOID_WIDTH = 1.25
    CORE_VOID_SPECIFIC = 1.35
    ELEV_DISABLED_MIN_AREA = 4
    CORRIDOR_WIDE_BY_BUILDING_TYPE = [2, 2, 1.7, 1.5, 1.5, 1.5, 2, 2]
    CORRIDOR_NARR_WIDTH = 1.4
    INNER_WALL_THICKNESS = 0.2
    OUTER_WALL_THICKNESS = 0.4
    CORE_SEGMENT_GAP_LENGTH = 3.0
    OUTER_WALL_THICKNESS_FOR_VISUALIZE = 0.3
    CURTAIN_WALL_THICKNESS = 0.2
    CURTAIN_WALL_MULLION_THICKNESS = 0.05
    CURTAIN_WALL_PANE_THICKNESS = 0.05
    CURTAIN_WALL_INTERVAL = 1.2

    # 코어 유형별(0번~2번) 규격 (m, m) - 층고 4m 기준, 소형 필지
    CORE_WIDE_TALL_SMALL = [5.550, 7.230, 5.550]
    CORE_NARR_TALL_SMALL = [1.600, 2.050, 3.650]
    CORE_STR_TALL_SMALL = ["ExSlimT", "ExSlimET", "ExWideET"]
    # 코어 유형별(0번~2번) 규격 (m, m) - 층고 4m 기준
    CORE_WIDE_TALL = [5.550, 7.680, 5.750]
    CORE_NARR_TALL = [2.800, 2.800, 5.150]
    CORE_STR_TALL = ["SlimT", "SlimET", "WideET"]
    # 코어 유형별(0번~2번) 규격 (m, m) - 소형 필지
    CORE_WIDE_SMALL = [4.200, 6.480, 4.800]
    CORE_NARR_SMALL = [1.600, 2.050, 3.650]
    CORE_STR_SMALL = ["ExSlim", "ExSlimE", "ExWideE"]
    # 코어 유형별(0번~2번) 규격 (m, m)
    CORE_WIDE = [4.800, 6.550, 4.400, 7.750]
    CORE_NARR = [2.800, 2.800, 5.200, 2.800]
    CORE_STR = ["Slim", "SlimE", "WideE", "SlimEL"]
    # 코어를 피난계단으로 설치해야 하는 경우 (지하 2층 이하 or 지상5층 이상인 층의 면적이 200m² 이상인 경우)
    CORE_WIDE_ESCAPE = [7.15, 4.8]
    CORE_NARR_ESCAPE = [4.4, 5.15]
    CORE_STR_ESCAPE = ["SlimEC", "WideEC"]
    CORE_WIDE_CENTER_ESCAPE = [8.33, 6.4]
    CORE_NARR_CENTER_ESCAPE = [2.8, 5.15]
    CORE_STR_CENTER_ESCAPE = ["SlimEM", "WideEM"]
    # 코어를 피난계단으로 설치해야 하는 경우 - 층고 4m 기준 (지하 2층 이하 or 지상5층 이상인 층의 면적이 200m² 이상인 경우)
    CORE_WIDE_ESCAPE_TALL = [7.9, 5.55]
    CORE_NARR_ESCAPE_TALL = [4.4, 5.15]
    CORE_STR_ESCAPE_TALL = ["SlimETC", "WideETC"]
    CORE_WIDE_CENTER_ESCAPE_TALL = [9.08, 7.15]
    CORE_NARR_CENTER_ESCAPE_TALL = [2.8, 5.15]
    CORE_STR_CENTER_ESCAPE_TALL = ["SlimETM", "WideETM"]
    # 코어를 특별피난계단으로 설치하는 경우. 층고 4m만 있음
    CORE_WIDE_SPECIFIC_ESCAPE_TALL = [8.250, 6.400]
    CORE_NARR_SPECIFIC_ESCAPE_TALL = [4.200, 5.550]
    CORE_STR_SPECIFIC_ESCAPE_TALL = ["SlimETCS", "WideETCS"]
    CORE_WIDE_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL = [10.200, 5.500]
    CORE_NARR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL = [4.200, 7.050]
    CORE_STR_SPECIFIC_ESCAPE_EMGCY_ELEV_TALL = ["SlimETCSE", "WideETCSE"]
    ELEV_PERSONS_MAP = {
        "ExSlimT": 0,
        "ExSlimET": 7,
        "ExWideET": 7,
        "SlimT": 0,
        "SlimE": 13,
        "WideE": 13,
        "SlimEL": 13,
        "ExSlim": 0,
        "ExSlimE": 7,
        "ExWideE": 7,
        "Slim": 0,
        "SlimET": 13,
        "WideET": 13,
        "SlimETM": 13,
        "WideETM": 13,
        "SlimETC": 13,
        "WideETC": 13,
        "SlimEM": 13,
        "WideEM": 13,
        "SlimEC": 13,
        "WideEC": 13,
        "SlimETCS": 16,
        "WideETCS": 16,
        "SlimETCSE": 16,
        "WideETCSE": 16,
        "EmergencyExit": 0,
    }

    CORE_LYING_NO_CHECK_AREA_MAX = 170
    CORE_TRANSLATE_RADIUS = 2
    CORE_TRANSLATE_MAX_TRIALS = 20
    SMALL_CORE_MAX_AREA = 132
    SMALL_CORE_MAX_FA = 200
    UNIT_MIN_WIDTH = 2.4
    UNIT_MIN_AREA = 14
    MARKET_MIN_AREA = 14
    PARTITIONED_MIN_AREA = 1e-3
    UNITENTRY_MIN_WIDTH = 1.4
    WIDECORRIDOR_CHECK_WIDTH = 1.6
    BALCONY_MIN_LENGTH = 2
    BALCONY_MAX_WIDTH = 1.3
    BALCONYUNIT_MIN_WIDTH = 2.3
    BALCONY_MARGIN = 0
    POSTPROCESS_PARK_GAP_CHECK = 2.49
    PARK_MAX_PARKING_EDGE_LEN = 2.6
    PARK_N_MAX_PARKING_EDGES = 3
    PARK_CELL_WIDE_PER = 5
    PARK_CELL_NARR_PER = 2.5
    PARK_CELL_WIDE_PAR = 6
    PARK_CELL_NARR_PAR = 2
    PARK_N_MAX_CELLS = 8
    PARK_N_FRONT_CELLS = 5
    PARK_GAP_LOT = 2.5
    PARK_CHECKER_LENGTH = 30
    PARK_PLOT_INTERVAL = 0.1
    PARK_CENTERLINE_DIST_PER = 6
    PARK_CENTERLINE_DIST_PAR = 4

    PATH_NET_GAP = 1
    PATH_WIDTH_NARR = 1.1
    PATH_WIDTH_WIDE = 1.7
    MAX_TYPE_AREA_LIST_OF_LISTS_OF_LISTS = [
        [[36, 42, 45], [55, 60, 70], [72, 76, 80]],  # 다가구
        [[36, 42, 45], [55, 60, 70], [72, 76, 80]],  # 다세대
        [[16, 18, 20], [32, 36, 40], [52, 56, 60]],  # 다중
        [],  # 근린은 사용하지 않습니다.
        [],  # 판매는 사용하지 않습니다.
        [],  # 업무는 사용하지 않습니다.
        [[36, 42, 45], [55, 60, 70], [72, 76, 80]],  # 도시형생활주택 중 소형
        [[36, 42, 45], [55, 60, 70], [72, 76, 80]],  # 도시형생활주택 중 단지형다세대
    ]
    AREA_COST = [-1e4, 700, 550, 300, 150]
    AREA_COST_COMMERCIAL = 640

    # packer 관련 상수
    PACKING_OFFSET_INTERVAL_M = 0.3
    PACKING_SEGMENT_DIVISION_MIN_LENGTH_M = 6
    PACKING_SEGMENT_DIVISION_UNIT_LENGTH_M = 2
    PACKING_ROOM_CHECK_BUFFER_M = 0.05
    PACKING_MINIMUM_SEGMENT_LENGTH_M = 2
    PACKING_LOOP_MAX_NUMBER = 10
    PACKING_FAR_ADD = 0.2
    PACKING_MAX_RESIDENTIAL_GFA = 660
    FINAL_DEADSPACE_LENGTH = 1.499
    TRENCH_FILL_ENTRY_LENGTH = 1.100
    TRENCH_FILL_LENGTH = 3.000

    # PMP 관련 상수
    MAX_GROUP_PARKING_COUNT = 5
    OUTER_PARKING_UNDER_TWELVE = 12
    CENTERLINE_BB_DEADSPACE_LENGTH = 3.5 + 1e-3
    CENTERLINE_BB_OFF_THE_WALL_LENGTH = 3 + 1e-3
    RULE_PARKING_SITE_CUT_LENGTH = 4 + 1e-3
    FRONT_PARKING_CHECK_INTERVAL = 0.3
    PARKING_PARTITION_COUNT = 3
    PARKING_GAP_WIDTH = 0.001
    SHIFT_STEP_SINGLE = 0.5
    MINIMUM_OUTER_PARKING_ROAD_WIDTH = [6, 4]
    PARKING_WIDTH = [2.5, 6]
    PARKING_SPOT_HEIGHT = [5, 2]
    PARKING_SPACE_HEIGHT = [-6, -5]
    PARKING_ADD_ROAD_EDGE_ADDITION_CHECKER = 4.999
    VEHICLE_ROAD_WIDTH = 2.499
    MAX_COUNT_WHEN_BACK_PARKING = 8
    MIN_INNER_PARKING_ROAD_EDGE_LENGTH = 2.501
    GAP_CHECK_MAX_ANGLE = 30
    PEDESTRIAN_PATH_WIDTH_ADD = 0.199
    START_PT_OFFSET_DIST = 1.25
    CORE_EXPAND_DISTANCE = 5
    PARKING_SCALE_UP_RATIO = 1.01
    PARKING_SCALE_DOWN_RATIO = 0.99
    CORE_ENTRY_LENGTH = 1.2
    CORE_ENTRY_SHIFT_LENGTH = 0.6
    BACK_PARKING_SHIFT_MAX_TRIALS = 15
    MASS_PARK_GAP = 0.15
    PLANES_ENTRY_LENGTH = 2
    INNER_ROAD_OFFSET_WIDTH = 3
    WEIGHTED_SHORTEST_PATHS_PENALTY = 100  # 10미터로는 지하주차 등에서 뚫고 가는 경우도 있어서 100미터로 사용
    PARAM_Y_SINGLE = 10
    TRENCH_FILL_LENGTH = 3.000
    RAND_POINTS_NUM = 0.1  # FIXME: 실제로는 100개 인데, 움직이는 과정에서 오류 확인 후 수정
    FRONT_PARKING_GROUP_DISTANCE = 2.499
    RIGHT_ANGLE_DEGREE = 90
    FILTER_PED_PATH_NETWORK_WITH_PATH = True  # NOTE: path 쪽도 제거 대상으로 사용할지 말지 switch
    FINAL_ADDITION_PLANE_INTERVAL = 0.5

    # 룰주차 관련
    ROAD_EDGE_ENTRY_MIN_SEG_LENGTH = 2.9
    PARKING_PATTERN_RANGE_MAX = 6
    SHIFT_MAX_COUNT = 10

    # 지하주차 관련
    RAMP_TYPE_LIST = [0, 1]  # I, L shape 대응 (2번은 U shape 인데 사용 X)
    UNDERGROUND_PARKING_GAP_WIDTH = 0.5
    UNDERGROUND_RAMP_OFFSET_LENGTH = 5  # 기본적으로는 수직 주차의 깊이 만큼
    UNDERGROUND_OFFSET_LENGTH = 1
    UNDERGROUND_AREA_TOL_ANGLE = 30
    RAMP_LENGTH = 31.8
    RAMP_WIDTH_LIST = [3.3, 6]
    RAMP_SUB_LENGTH = 6.5
    RAMP_BODY_LENGTH = 18.8
    RAMP_INNER_RADIUS = 6.0
    RAMP_L_TYPE_ADDITIONAL_LENGTH_EACH_SIDE = 3.4
    MAX_PARKING_COUNT_WHEN_NARROW_RAMP = 49
    RAMP_ROTATION_CHECK_AREA = 5.0

    RAMP_OBSTACLE_TEST_BUFFER_LENGTH = [5, 8]
    RAMP_OBSTACLE_ALLOW_RATIO_MAXIMUM = 0.2

    UNDERGROUND_MASS_REMOVER_LENGTH = 100
    UNDERGROUND_MASS_CORE_PLACE_BASEAREA = 200
    UNDERGROUND_MASS_EXIT_PLACE_BASEAREA = 50
    UNDERGROUND_EMERGENCY_EXIT_SIZE = 1.4
    UNDERGROUND_CORE_MAXIMUM_DISTANCE = 50

    # NARROW_UNIT_ENTRY_MAX_RATIO : 데드스페이스 제거 단계, 좁고 깊은 세대 입구 한계 비율 (콩나물 세대 방지에 사용되는 비율)
    # NARROW_UNIT_ENTRY_MAX_RATIO = 4일 경우, 폭:깊이 1:4까지의 면적은 세대 면적으로 하용된다.
    NARROW_UNIT_ENTRY_MAX_RATIO = 4

    # PREVENT_NARROW_ENTRY_ON_SETBACK : 중복도 셋백 단계, 셋백하려는 영역이 3개의 세대와 닿아 있다면 셋백을 중단하여
    # 좁고 깊은 세대 입구를 방지한다.
    # true일 경우 '콩나물 세대'를 만드는 셋백을 방지하고, false일 경우 복도를 최대한 셋백한다.
    PREVENT_NARROW_ENTRY_ON_SETBACK = False

    BUILDING_DIVISION_CORE_LOC_BUFFER_LEN = 1.0
    BUILDING_DIVISION_DISTANCE_BETWEEN = 4.0
    BUILDING_DIVISION_LEGAL_GEOM_INNER_SIZE_TEST_LEN = 2.6

    SIMPLE_REDUCE_RATIO_INTERVAL = 0.05
    SIMPLE_DEADSPACE_LEN = 1.4
    SIMPLE_MIN_MASS_WIDTH = 2.1
    SIMPLE_BCR_MARGIN = 1.03
    SIMPLE_FAR_MARGIN = 0.00
    SIMPLE_FAR_MARGIN_FOR_COMMERCIAL = 0.30  # 여유롭게 잡아도 상가유형에서는 코어 2개소에 의해 최대 용적을 잘 못찾음
    SIMPLE_MECH_PARK_CHECK_MIN_AREA = 300.0

    BUILDING_PURPOSE_MAP = {
        "dagagu": 0,
        "dasedae": 1,
        "dajung": 2,
        "geunsaeng": 3,
        "panmae": 4,
        "upmu": 5,
        "urbanhousing_small": 6,
        "urbanhousing_bundong": 7,
        "dormitory": 8,
        "officetel": 9,
    }

    MAX_HOUSING_FLOOR_MAP = {
        "dagagu": 3,
        "dasedae": 4,
        "dajung": 3,
        "geunsaeng": 0,
        "panmae": 0,
        "upmu": 0,
        "urbanhousing_small": 4,
        "urbanhousing_bundong": 5,
        "dormitory": 0,
        "officetel": 0,  # FIXME: placeholder. 오피스텔은 주거와 같은 형식의 주차 규정
    }
    PEDESTRAIN_PATH_WIDTH_BY_BUILDING_TYPE = [1.1, 1.7, 1.1, 1.7, 1.5, 1.5, 1.7, 1.7, 1.7, 1.7]
    BUILDING_PURPOSE_STR_LIST = [
        "다가구",
        "다세대",
        "다중",
        "상가",
        "판매",
        "업무",
        "도생(소형주택다세대)",
        "단지형다세대",
        "임대형기숙사",
        "오피스텔",
    ]
    BUILDING_PURPOSE_GENERAL_SHORT_STR_LIST = [
        "다가구",
        "다세대",
        "다중",
        "근린",
        "판매",
        "업무",
        "도생(소형주택다세대)",
        "도생(단지형다세대)",
        "임대형기숙사",
        "오피스텔",
    ]
    BUILDING_PURPOSE_GENERAL_STR_LIST = [
        "다가구주택",
        "다세대주택",
        "다중주택",
        "근린생활시설",
        "판매시설",
        "업무시설",
        "도생(소형주택다세대)",
        "단지형다세대주택",
        "임대형기숙사",
        "오피스텔",
    ]

    SIMPLE_CORE_PLACEMENT_MIN_LENGTH = 1
    SIMPLE_DEFAULT_AVERAGE_AREA = 38
    SIMPLE_UNIT_AREA_FOR_DAJUNG = 25
    SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE = 0.5
    SIMPLE_MASS_ASPECT_RATIO_BASEINE = 6.0

    POSTPROCESS_CORRIDOR_ITERATION_COUNT = 2

    DOOR_SIZE = 0.9
    DOOR_SIZE_LARGE = 1.0
    DOOR_MARGIN = 0.05
    DOOR_FRAME_WIDTH = 0.04
    DOOR_FRAME_WIDTH_MARGIN = 0.01
    DOOR_DEADSPACE_AFTER_SETBACK = 1.399
    DOOR_SETBACK_ITERATION = 3

    GREEN_POLYGON_MIN_WIDTH = 1
    GREEN_POLYGON_MARGIN = 0.3
    GREEN_POLYGON_MIN_AREA = 35
    GREEN_POLYGON_BOUNDARY_WIDTH = 2

    ESCAPE_CORE_TRUE_AREA = 200

    MAX_HOUSEHOLDS_NUM_DAGAGU = 19
    MAX_HOUSEHOLDS_NUM_DAJUNG = 20  # 취사실 제외하고 19세대

    BINARY_VOID = "0"
    BINARY_SOLID = "1"

    ENGINE_TYPE_LIGHT = "light"
    ENGINE_TYPE_BASIC = "basic"

    RULE_OUTER_NO_PARKING_ADJACENT_DISTANCE = 2

    SIMPLE_FAR_RESULT_FAR_ADJUSTMENTS = 0.0001

    HAS_CENTERLINE_TRUE_BASELINE = 20

    # 라이트 코어 배치 후보 최대 사용 개수.
    LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM = 3

    LIGHT_LOWER_COMMERCIAL_FLOOR_MAX = 3
    LIGHT_LOWER_COMMERCIAL_FLOOR_MIN = 1

    LIGHT_SCORE_FOR_PARKLOT_ERROR = 0

    BASIC_ERROR_SUBCODE_MAENGJI = 50101
    BASIC_ERROR_SUBCODE_FAE_ZERO = 50102
    BASIC_ERROR_SUBCODE_EMPTY_OPTION = 50103

    PARKING_AREA_DIVISOR = 134


def extend_curve(curve, start=0, end=0):
    """여러 개의 점으로 이루어진 linestring을 양쪽으로 확대 혹은 축소한다.
    Args:
        curve (LineString): Curve to extend
        start (float, optional): Extension length at start of curve. Defaults to 0.
        end (float, optional): Extension length at end of curve. Defaults to 0.
    Returns:
        (LineString): Extended curve
    """

    curve_coords = list(curve.coords)

    x1 = curve_coords[0][0]
    y1 = curve_coords[0][1]
    x2 = curve_coords[1][0]
    y2 = curve_coords[1][1]
    start_len_ratio = start / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    x3 = curve_coords[-2][0]
    y3 = curve_coords[-2][1]
    x4 = curve_coords[-1][0]
    y4 = curve_coords[-1][1]
    end_len_ratio = end / ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** 0.5

    start_point = (x1 - ((x2 - x1) * start_len_ratio), y1 - ((y2 - y1) * start_len_ratio))
    end_point = (x4 + ((x4 - x3) * end_len_ratio), y4 + ((y4 - y3) * end_len_ratio))

    curve_coords[0] = start_point
    curve_coords[-1] = end_point
    new_curve = LineString(curve_coords)

    return new_curve


def explode_to_segments(curve):
    """Explode a curve into smaller segments

    Args:
        curve (LineString): Curve to explode

    Returns:
        segments(List[Linestring]): Exploded segments that make up the base curve
    """
    curve_coords = list(curve.coords)

    if len(curve_coords) == 0:
        return []

    segments = []
    start_pt = curve_coords[0]

    for i in range(len(curve_coords) - 1):
        end_pt = curve_coords[i + 1]
        segments.append(LineString([start_pt, end_pt]))
        start_pt = end_pt

    return segments


def offset_curve_polygon(curve, distance, side, return_offset_line=False):
    """Offset LineString and make polygon with original LineString & new LineString

    Args:
        curve (LineString): Curve to offset
        distance (int): Offset distance
        side (string ("left"|"right")): Offset direction

    Returns:
        (tuple): tuple containing:

            polygon (Polygon): Polygon made from original & new LineString
            curve_offset (LineString): Offsetted new LineString
    """

    curve_coords = list(curve.coords)

    # 다시 계산할 필요가 없도록 curve_coords를 전달한다.
    _, offset_curve_coords = parallel_offset_segment(
        curve, distance, side, segment_coords=curve_coords, return_coords=True, join_style=2
    )

    if side == "left":
        pass
    elif side == "right":
        curve_coords = curve_coords[::-1]
    else:
        raise Exception("지원되지 않는 offset 방향입니다.")

    # offset_curve_coords는 순서가 뒤집힌 상태로 반환된다.
    polygon = Polygon(curve_coords + offset_curve_coords)

    if return_offset_line:
        return polygon, LineString(offset_curve_coords)
    else:
        return polygon


def parallel_offset_segment(segment, distance, side, segment_coords=None, return_coords=False, join_style=1):
    # 시작점과 끝점으로 이루어진 선분을 주어진 방향으로 평행이동한다.

    if not segment_coords:
        segment_coords = segment.coords

    if len(segment_coords) == 0:
        return LineString()
    elif len(segment_coords) > 2:
        offset_segment = segment.parallel_offset(distance, side, join_style)
        return offset_segment

    x1 = segment_coords[0][0]
    y1 = segment_coords[0][1]

    x2 = segment_coords[1][0]
    y2 = segment_coords[1][1]

    distance_ratio = distance / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    if side == "right":
        offset_x = distance_ratio * (y2 - y1)
        offset_y = -distance_ratio * (x2 - x1)

        # GEOS < 3.11 / shapely < 2.0에서 오른쪽 offset은 방향이 거꾸로 바뀐다.
        x2_ = x1 + offset_x
        y2_ = y1 + offset_y
        x1_ = x2 + offset_x
        y1_ = y2 + offset_y

    elif side == "left":
        offset_x = -distance_ratio * (y2 - y1)
        offset_y = distance_ratio * (x2 - x1)

        x1_ = x1 + offset_x
        y1_ = y1 + offset_y
        x2_ = x2 + offset_x
        y2_ = y2 + offset_y

    # 폴리곤을 만들 때 필요한 좌표값들만 반환한다.
    if return_coords:
        return segment_coords, [(x2_, y2_), (x1_, y1_)]

    offset_segment = LineString([(x1_, y1_), (x2_, y2_)])

    return offset_segment


def angle_of_polygon_vertices(polygon) -> List[float]:
    """Get angles of polygon vertices

    Args:
        polygon (Polygon): Polygon to find angle

    Returns:
        (List[float]): Angles of polygon vertices
    """
    # NOTE: boundary -> exterior로 수정
    # boundary는 도형내부에 빈 공간이 있는 경우에는 내부 빈 공간 경계도 반영한 MultiLineString이 되며
    # MultiLineString은 np.array로 변환 불가한 데이터 타입임.
    if polygon.is_empty:
        return []

    exterior_coords = list(polygon.exterior.coords)
    next_vec_list = [
        (
            coord[0] - exterior_coords[1:][i - 1][0],
            coord[1] - exterior_coords[1:][i - 1][1],
        )
        for i, coord in enumerate(exterior_coords[1:])
    ]
    prev_vec_list = [(-x, -y) for x, y in [next_vec_list[-1]] + next_vec_list[:-1]]

    prev_vec_view_angle_list = [math.atan2(vec[1], vec[0]) for vec in prev_vec_list]
    next_vec_view_angle_list = [math.atan2(vec[1], vec[0]) for vec in next_vec_list]

    flatten = [each_prev_vec - next_vec_view_angle_list[i] for i, each_prev_vec in enumerate(prev_vec_view_angle_list)]

    angles = [(each_flatten) % (2 * np.pi) for each_flatten in flatten]

    # 여기에서 구한 angles가 내각이라면, 외각의 합보다 작아야 한다.
    sum_angles = sum(angles)
    if sum_angles > (len(angles) * np.pi * 2) - sum_angles:
        # 외각을 구한 경우, 내각으로 변환한다.
        angles = [(each_flatten * -1) % (2 * np.pi) for each_flatten in flatten]

    angles = angles + [angles[0]]

    return angles


def simplify_polygon(
    polygon,
    tol_angle: float = 1e-3,
    tol_length: float = 1e-6,
    use_simplify: bool = True,
    container_geometry: Polygon = None,
    skip_angle_simplifying_when_interiors: bool = False,
):
    if polygon.is_empty:
        return polygon

    if not polygon.is_valid:
        # repair invalid geometry
        polygon = polygon.buffer(0)

        if isinstance(polygon, MultiPolygon):
            polygon = filter_polygon(polygon)

    assert isinstance(
        polygon, (Polygon, MultiPolygon)
    ), f"polygon이 Polygon 또는 MultiPolygon type이 아닙니다. 현재 타입은 {type(polygon)}입니다."

    if isinstance(polygon, MultiPolygon):
        simplify_result = []
        for poly in polygon.geoms:
            simplify_result.append(
                simplify_polygon(
                    poly,
                    tol_angle,
                    tol_length,
                    skip_angle_simplifying_when_interiors=skip_angle_simplifying_when_interiors,
                )
            )
        return MultiPolygon(simplify_result)
    else:
        if skip_angle_simplifying_when_interiors and len(polygon.interiors) > 0:
            result_polygon = polygon.simplify(tol_length)
        else:
            # python
            # 반시계방향 ccw로 확인한다.
            polygon = shapely.geometry.polygon.orient(polygon, sign=1.0)

            # shapely의 simplify() 함수를 호출한다.
            simplified_polygon = polygon.simplify(tol_length)

            # 새로 폴리곤 구성할 점들 저장할 list (각도 180도와 가까운 점은 제외한다.)
            simplified_poly_coords = []
            # 각 점의 angle에 대한 iteration을 수행한다. / 첫점과 끝점 이 모두 들어있으므로 마지막 점 제외함.
            for i, angle in enumerate(angle_of_polygon_vertices(simplified_polygon)[:-1]):
                if np.abs(angle - np.pi) > tol_angle:
                    # 각 점에서 전, 후 점과의 각이 180도 기준 tol_angle 이하면 제외하고,
                    # 초과인 경우 여기서 추가된다.
                    simplified_poly_coords.append(simplified_polygon.exterior.coords[i])

            # 새로 결과 폴리곤 구성한다.
            # Polygon() 생성시 첫 점, 끝 점 다르면 알아서 마지막에 추가됨.
            if len(simplified_poly_coords) < 3:
                result_polygon = Polygon()
            else:
                result_polygon = Polygon(simplified_poly_coords)

        if container_geometry is not None:
            result_polygon = polygon if not result_polygon.within(container_geometry) else result_polygon

        return result_polygon


def get_aspect_ratio(polygon: Polygon, vector: np.ndarray, return_bb: bool = False) -> float:
    if polygon.is_empty:
        aspect_ratio = 1
        ombr = Polygon()
    else:
        # ombr = polygon.minimum_rotated_rectangle
        # https://www.notion.so/spacewalkcorp/ombr-07f56e886e4840f985133afb5374f05a
        # minimum_rotated_rectangle 사용시 건물 축과 맞지 않는 바운딩박스 생성되는 경우 존재
        ombr = get_rotated_bb(polygon, vector)
        exp_ombr = explode_to_segments(ombr.exterior)
        x, y = exp_ombr[0].length, exp_ombr[1].length
        aspect_ratio = x / y if x > y else y / x

    if return_bb:
        return aspect_ratio, ombr

    return aspect_ratio


def filter_polygon(inputs) -> Polygon:
    if isinstance(inputs, Polygon):
        return inputs
    elif hasattr(inputs, "geoms") or isinstance(inputs, Iterable):
        polys = list(filter(lambda x: isinstance(x, Polygon), inputs.geoms))
        if len(polys) == 0:
            return Polygon()
        poly = np.array(polys, dtype=object)[np.argmax([poly.area for poly in polys])]
        return poly
    else:
        return Polygon()


def new_filter_polygon(inputs):
    if isinstance(inputs, Polygon):
        return inputs, MultiPolygon()
    elif hasattr(inputs, "geoms") or isinstance(inputs, Iterable):
        polys = np.array(list(filter(lambda x: isinstance(x, Polygon), inputs)), dtype=object)
        if len(polys) == 0:
            return Polygon(), MultiPolygon()
        indices_filter = np.eye(len(polys), dtype=bool)[np.argmax([x.area for x in polys])]
        polys, remains = polys[indices_filter], polys[~indices_filter]
        return polys[0], MultiPolygon(list(remains))
    else:
        return Polygon(), MultiPolygon()


def flatten_list(lists):
    if isinstance(lists, list):
        if len(lists) < 1:
            return lists
        elif isinstance(lists[0], list):
            return flatten_list(lists[0]) + flatten_list(lists[1:])
        else:
            return lists[:1] + flatten_list(lists[1:])
    else:
        return [lists]


def buffer_erosion_and_dilation(
    polygon: Union[Polygon, MultiPolygon],
    buffer_distance: float,
    join_style: int = JOIN_STYLE.mitre,
    use_intersection: bool = True,
    choose_biggest_polygon: bool = True,
    choose_biggest_polygon_before_dilation: bool = False,
) -> BaseGeometry:
    """데드스페이스 제거 용도로 buffer 이중 연산을 수행한다.
        버퍼 연산시, 뾰족하게 남은 형상은, dilation 후 돌출 가능하므로 intersection 기능을 추가하여 이 함수에서 처리.

    Args:
        polygon (Union[Polygon, MultiPolygon]): 기본적으로 폴리곤이 대상이지만,
        difference의 결과 등 multipolygon인 경우도 처리 가능함.
        buffer_distance (float): 같은 수치로 erosion과 dilation할 거리(양의 실수).
        join_style (int, optional): buffer 연산 join 옵션. Defaults to JOIN_STYLE.mitre.
        use_intersection (bool, optional): 결과에 원본의 intersection을 통해, 뾰족하게 돌출하는 것 방지하는 기능에 대한 flag. Defaults to True.
        choose_biggest_polygon (bool, optional): 연산 결과중 가장 큰 폴리곤 하나만 선택하는 flag. Defaults to True.
        choose_biggest_polygon_before_dilation (bool, optional): shrink 하고 가장 큰 것 만 고르고 싶을 경우 사용

    Returns:
        BaseGeometry: buffer 및 intersection 연산의 결과. flag 사용하지 않을 시 polygon이 아닐 수도 있음
    """
    if polygon.is_empty:
        return polygon
    eroded = polygon.buffer(-buffer_distance, join_style=join_style)
    if isinstance(eroded, MultiPolygon) and choose_biggest_polygon_before_dilation:
        eroded = filter_polygon(eroded)
    dilated = eroded.buffer(buffer_distance, join_style=join_style)

    # 원본 폴리곤을 이루는 선분들의 길이가 buffer_distance와 가까울 경우 버퍼 오작동으로 멀티폴리곤이 발생할 수 있다.
    if isinstance(dilated, MultiPolygon) and choose_biggest_polygon:
        dilated = filter_polygon(dilated)

    # polygon 이 invalid 한 경우, intersection 시 오류 발생함.
    if use_intersection and not polygon.contains(dilated) and polygon.is_valid:
        intermediate_geometry = dilated.intersection(polygon)
    else:
        intermediate_geometry = dilated

    if choose_biggest_polygon:
        result_geometry = filter_polygon(intermediate_geometry)
    else:
        result_geometry = intermediate_geometry
    return result_geometry


# TODO: dilation 이전에 simplify 필요.
def buffer_dilation_and_erosion(
    polygon: Polygon,
    buffer_distance: float,
    join_style: int = JOIN_STYLE.mitre,
    use_simplification: bool = True,
    simplify_tolerance: float = 1e-3,
    choose_biggest_polygon: bool = True,
) -> BaseGeometry:
    """dilation 후 erosion 하는 buffer 이중 연산을 수행하는 함수
        해당 연산 전 비슷한 좌표의 점을 가지는 simplify 되지 않은 입력은 buffer 버그를 발생시키기 때문에, 해당 함수로 처리함.

    Args:
        polygon (Polygon): 대상 폴리곤. 현재 쓰이는 곳은 모두 의도 상 polygon이어야 함
        buffer_distance (float): dilation 후 erosion 할 거리, 양의 실수.
        join_style (int, optional): 버퍼 joint 옵션. Defaults to JOIN_STYLE.mitre.
        use_simplification (bool, optional): simplify를 사전에 호출할지 flag. Defaults to True.
        simplify_tolerance (float, optional): mm 단위를 기본으로 1을 기본으로하고, m 단위 사용시 1e-3으로 사용. Defaults to 1.0.
        choose_biggest_polygon (bool, optional): 연산 결과 중 가장 큰 폴리곤 하나. Defaults to True.

    Returns:
        BaseGeometry: simplify 후 함수 결과, flag 사용하지 않을 시 polygon인지는 보장하지 않음
    """
    # buffer
    if use_simplification:
        intermediate_geometry = polygon.simplify(simplify_tolerance)
    else:
        intermediate_geometry = polygon

    dilated = intermediate_geometry.buffer(buffer_distance, join_style=join_style)
    dilated = dilated.simplify(simplify_tolerance)
    eroded = dilated.buffer(-buffer_distance, join_style=join_style)
    if choose_biggest_polygon:
        result_geometry = filter_polygon(eroded)
    else:
        result_geometry = eroded

    return result_geometry


def get_rotated_bb(bb_original: Polygon, bb_vec: np.ndarray) -> Polygon:
    """지정된 각도를 가지고 bounding box 를 생성합니다.

    Args:
        bb_original (Polygon): bounding box 를 생성하고자 하는 기준 폴리곤
        bb_vec (np.ndarray): 지정 각도 벡터

    Returns:
        Polygon: 지정된 각도를 가지고 생성한 bounding box
    """
    if bb_original.is_empty:
        return Polygon()

    v = np.array([bb_vec])

    seg_angle = np.degrees(np.arctan2(*v.T[::-1])) % 360.0
    rotated_site_geom = shapely.affinity.rotate(bb_original, -seg_angle[0], origin=bb_original.centroid)
    bb = shapely.geometry.box(*rotated_site_geom.bounds)
    rotated_bb = shapely.affinity.rotate(bb, seg_angle[0], origin=bb_original.centroid)

    return rotated_bb


def remove_deadspace_with_extended_exterior(
    polygon: Polygon,
    deadspace_len: float,
    tolerance: float,
    core: Polygon = Polygon(),
    regulation: Polygon = Polygon(),
    building_purpose: str = None,
    return_only_splits: bool = False,
) -> Polygon:
    """외곽선을 연장 데드스페이스를 삭제하는 방식의 데드스페이스 처리 함수

    여러 곳에서 사용하기 위해 geom 으로 옮김.

    Args:
        polygon (Polygon): 데드스페이스를 삭제하고자 하는 원본 폴리곤
        deadspace_len (float): 데드스페이스 기준 길이
        tolerance (float): 도형을 자를 때 길이 여유분
        core (Polygon): if given, use all areas that meet the core
        regulation(Polyogn): if given, prevent areas that go outside the regulation

    Returns:
        Polygon: 외곽선 연장 방식으로 데드스페이스 처리한 후의 폴리곤
    """

    polygon_exterior_line_list = explode_to_segments(polygon.boundary)
    eroded_polygon = polygon.buffer(-tolerance)

    # 와곽선을 확장하여 폴리곤과 다시 만나는 경우 커팅 선분으로 사용한다.
    exterior_segs = []
    for exterior_line in polygon_exterior_line_list:
        extended_exterior_line = extend_curve(exterior_line, start=deadspace_len, end=deadspace_len)
        if extended_exterior_line.crosses(eroded_polygon):
            exterior_segs.append(extended_exterior_line)
        else:
            buffered_exterior_line = extend_curve(exterior_line, start=tolerance, end=tolerance)
            exterior_segs.append(buffered_exterior_line)

    # 중복된 점은 합치지고 non-node인 교차점 등도 제거한다.
    ext_seg_union: MultiLineString = shapely.ops.unary_union(exterior_segs)

    # union한 후 precision을 재설정하면 중복되는 선분이 발생 가능함.
    # 중복된 선분은 polygonize 하기 위해 없어야 하므로 한 번 더 수행
    exteriors_to_polygonize = shapely.ops.unary_union(ext_seg_union)
    splits_raw = list(shapely.ops.polygonize(exteriors_to_polygonize))
    splits = [s for s in splits_raw if not eroded_polygon.disjoint(s)]

    if return_only_splits:
        return splits

    # if core check is required, merge all splits that meets the core
    if not core.is_empty:
        largest_split_idx = np.argmax([split.area for split in splits])
        largest_split = splits.pop(largest_split_idx)

        buffered_core = core.buffer(tolerance, join_style=JOIN_STYLE.mitre)

        for split in splits:

            valid_split = False

            if not regulation.is_empty:
                if regulation.contains(split):
                    valid_split = True
            else:
                valid_split = True

            if valid_split:
                largest_split = shapely.ops.unary_union([largest_split, split])

                if building_purpose is not None:
                    if building_purpose == "geunsaeng":
                        largest_split = buffer_erosion_and_dilation(
                            polygon=largest_split,
                            buffer_distance=consts.TOLERANCE_MARGIN,
                            choose_biggest_polygon=True,
                        )

                    else:
                        core_neighbored_splits: List[Polygon]
                        core_neighbored_splits = []

                        largest_split_iter = [largest_split]
                        if isinstance(largest_split, MultiPolygon):
                            largest_split_iter = list(largest_split.geoms)

                        for s in largest_split_iter:
                            if not s.disjoint(buffered_core):
                                core_neighbored_splits.append(s)

                        largest_split = shapely.ops.unary_union(core_neighbored_splits)

                largest_split = buffer_dilation_and_erosion(
                    polygon=largest_split,
                    buffer_distance=tolerance,
                    use_simplification=True,
                    choose_biggest_polygon=True,
                )

        if largest_split.is_empty:
            return polygon
        return largest_split

    result_polygon = filter_polygon(MultiPolygon(splits))
    if result_polygon.is_empty:
        return polygon

    return result_polygon


# ====


def is_entry_secured_between_geoms(geom_one: BaseGeometry, geom_two: BaseGeometry, entry_width: float) -> bool:

    # geom_one 를 그대로 사용할 경우 geom_two와 intersection 을 했을 때
    # 오차로 인해 의도하지 않은 empty geometry 등이 생성될 수 있어서 buffer 된 도형을 사용합니다.
    # aa_fns_unit.check_unit_entry_square_exists의 버퍼 수치와 통일
    bufferred_geom_one: BaseGeometry = geom_one.buffer(consts.TOLERANCE_MARGIN, join_style=2)
    if bufferred_geom_one.disjoint(geom_two):
        return False

    exterior_of_geom_two: BaseGeometry = geom_two.exterior
    intersection_geom: BaseGeometry = exterior_of_geom_two.intersection(bufferred_geom_one).simplify(consts.TOLERANCE)

    # intersection_geom 을 각각의 segments로 분할하기 위한 로직입니다.
    #   (꺾여있거나 수직으로 만나는 연결된 두개의 세그먼트는 연결을 확인할 수 있지 않은 것으로 보고)
    # 이 exploded_intersection_geom_segments 를 이용해 세대 최소폭 검증을 수행합니다.
    exploded_intersection_geom_segments: List[BaseGeometry] = []
    if isinstance(intersection_geom, LineString):
        # explode_to_segments 는 LineString 을 segments 로 돌려줍니다.
        exploded_intersection_geom_segments = explode_to_segments(intersection_geom)
    elif isinstance(intersection_geom, MultiLineString):
        # explode_to_segments 는 LineString 인 경우를 상정한 함수이기 때문에 MultiLineString 의 경우
        # LineString 들로 나누어 explode_to_segments 후 리스트 합침.
        for intersection_geom_each_linestring in intersection_geom.geoms:
            exploded_intersection_geom_segments += explode_to_segments(intersection_geom_each_linestring)

    # 하나의 세그먼트라도 entry_width 를 만족할 경우 이 geom_one 과 geom_two 사이에는 진입길이를 확보한 것으로 판단.
    return any(
        np.isclose(segment.length, entry_width) or segment.length >= entry_width
        for segment in exploded_intersection_geom_segments
    )


def flatten_geometry_to_certain_type(geometry: BaseGeometry, target_type) -> List[BaseGeometry]:

    geometry_list: List[BaseGeometry] = []
    if isinstance(geometry, target_type):
        geometry_list = [geometry]
    elif hasattr(geometry, "geoms") or isinstance(geometry, Iterable):
        for each_geometry in geometry.geoms:
            geometry_list += flatten_geometry_to_certain_type(each_geometry, target_type)

    return geometry_list


def polygon_or_multipolygon_to_list_of_polygon(geometry: Union[Polygon, MultiPolygon]) -> List[Polygon]:
    return flatten_geometry_to_certain_type(geometry, Polygon)


def get_mass_angle_from_a_polygon(polygon: Polygon):
    polygon_exterior_coords = np.array(polygon.exterior.coords)
    polygon_exterior_vecs = polygon_exterior_coords[1:] - polygon_exterior_coords[:-1]
    max_length_idx = np.argmax([np.linalg.norm(vec) for vec in polygon_exterior_vecs])
    mass_angle = np.arctan2(polygon_exterior_vecs[max_length_idx][1], polygon_exterior_vecs[max_length_idx][0])

    return mass_angle


def check_min_size(mass, has_piloti, regulation, min_mass_area):
    """Check that each floor is within the regulation polygon and
    that each floor is big enough

    Args:
        mass (list): List of mass polygon
        has_piloti (bool): piloti or not
        regulation (list): List of regulation polygon
        min_mass_area (float): minimum area for a floor

    Returns:
        list: the new mass
    """
    valid_mass = []
    for i in range(len(mass)):
        # 주차 이후 필로티가 아니더라도 1층 매스가 empty인 경우가 존재할 수 있음
        if i == 0 and has_piloti or i == 0 and mass[i][0].is_empty:
            valid_mass.append([wkt.loads("POLYGON EMPTY")])
        elif mass[i][0].area >= min_mass_area:
            mass[i] = [mass[i][0].intersection(regulation[i])]
            valid_mass.append(mass[i])
        else:
            break
    return valid_mass


def check_mass_intersection(mass, core, engine_type, regulation, simple_deadspace_len):
    for i in range(2, len(mass)):
        floor_intersection = mass[i][0].intersection(mass[i - 1][0])
        floor_intersection = simplify_polygon(
            floor_intersection, tol_length=consts.TOLERANCE, container_geometry=regulation[i]
        )

        # In basic, the core is part of the mass and don't cause deadspace
        if engine_type == consts.ENGINE_TYPE_BASIC:
            floor_intersection = floor_intersection.union(core.buffer(consts.TOLERANCE, join_style=JOIN_STYLE.mitre))

        floor_intersection = buffer_erosion_and_dilation(
            polygon=floor_intersection,
            buffer_distance=simple_deadspace_len / 2,
            use_intersection=True,
            choose_biggest_polygon=True,
        )

        mass[i] = [floor_intersection]
    return mass


def gen_convexity_list(polygon):
    # 폴리곤을 받아 폴리곤의 꼭짓점들이 각각 오목한지, 볼록한지를 반환한다.
    # convex : 1, concave : 0

    polygon_vertice_angles = angle_of_polygon_vertices(polygon)

    convexity_list = []

    for vertice_angle in polygon_vertice_angles:
        if vertice_angle < np.pi:
            convexity_list.append(1)
        else:
            convexity_list.append(0)

    return convexity_list


def cut_emboss(
    polygon,
    width,
    policy,
    time_counter_dict,
    is_postprocess,
    tolerance_angle,
    mass_cut_depth_divider=1.0,
    use_emboss_cut_length_sorting=False,
    longest_length_baseline=None,
    shortest_length_baseline=None,
):
    # 엠보스컷. 럼프컷에서 처리하지 못한 오목한 부분 내부에서 튀어나온 모양을 제거한다.
    # 로직 상세 문서 확인: https://www.notion.so/spacewalkcorp/875c1cf57a9a422ab7a0c1253a7b7984
    start = time.process_time()

    # NOTE(pch): 빈 폴리곤이 들어오는 경우 아래 줄에서 DivisionError 발생
    # convexity_list[i % len(polygon_exterior_coords)]
    if polygon.is_empty:

        time.process_time() - start

        return polygon

    depth = width / mass_cut_depth_divider

    # 폴리곤의 꼭짓점마다 concave/convex 확인.
    convexity_list = gen_convexity_list(polygon)
    convexity_list = convexity_list[:-1]
    polygon_exterior_coords = list(polygon.exterior.coords)
    polygon_exterior_coords = polygon_exterior_coords[:-1]

    angles_list = []
    if is_postprocess:
        angles_list = list(angle_of_polygon_vertices(polygon))

    # 폴리곤 꼭짓점 개수의 초기값
    vertice_count = len(convexity_list)
    i = 0

    is_both = policy == 0
    is_at_least_one = policy == 1

    while True:
        # 연속하는 세 점 중 가운데 점만 볼록한 경우, 엠보스 형상으로 처리한다.
        if (
            convexity_list[i % len(polygon_exterior_coords)] == 0
            and convexity_list[(i + 1) % len(polygon_exterior_coords)] == 1
            and convexity_list[(i + 2) % len(polygon_exterior_coords)] == 0
        ):
            point_p = Point(polygon_exterior_coords[(i - 1) % len(polygon_exterior_coords)])
            point_a = Point(polygon_exterior_coords[i % len(polygon_exterior_coords)])
            point_b = Point(polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)])
            point_c = Point(polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)])

            # 마지막 단계에서 실행하는 경우, 90도가 아닌 각에서는 엠보스 컷을 실행할 수 없다.
            if is_postprocess:
                angle_a = angles_list[i % len(polygon_exterior_coords)]
                angle_b = angles_list[(i + 1) % len(polygon_exterior_coords)]
                angle_c = angles_list[(i + 2) % len(polygon_exterior_coords)]
                if np.pi / 2 - tolerance_angle > angle_a % (np.pi / 2) > tolerance_angle:
                    i += 1
                    continue
                if np.pi / 2 - tolerance_angle > angle_b % (np.pi / 2) > tolerance_angle:
                    i += 1
                    continue
                if np.pi / 2 - tolerance_angle > angle_c % (np.pi / 2) > tolerance_angle:
                    i += 1
                    continue

            each_width = point_a.distance(point_b)
            each_depth = point_p.distance(point_a)

            if use_emboss_cut_length_sorting:
                shortest_length, longest_length = sorted([each_width, each_depth])
                both_satisfied_condition = is_both and (
                    shortest_length <= shortest_length_baseline and longest_length <= longest_length_baseline
                )

                at_least_one_staisfied_condition = is_at_least_one and (
                    shortest_length <= shortest_length_baseline or longest_length <= longest_length_baseline
                )

            else:
                both_satisfied_condition = is_both and (each_width <= width and each_depth <= depth)

                at_least_one_staisfied_condition = is_at_least_one and (each_width <= width or each_depth <= depth)

            is_needed_cutting_emboss = both_satisfied_condition or at_least_one_staisfied_condition

            # convex한 점 양쪽의 두 선분의 길이가 모두 엠보스 컷 기준 이하인 경우, 해당 점을 안쪽으로 넣는다.
            if is_needed_cutting_emboss:

                # 점 a에서 c - b만큼 이동한 자리로 점 b를 이동한다.
                vec = np.array(point_c.coords[0]) - np.array(point_b.coords[0])
                new_b_point = np.array(point_a.coords[0]) + vec

                if polygon.contains(Point(new_b_point)):

                    polygon_exterior_coords = list(polygon_exterior_coords)

                    # 점 b는 안쪽으로 이동하고, 점 a와 점 c는 제거한다.
                    polygon_exterior_coords[i % len(polygon_exterior_coords)] = None
                    polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)] = tuple(new_b_point)
                    polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)] = None

                    convexity_list[i % len(polygon_exterior_coords)] = None
                    convexity_list[(i + 1) % len(polygon_exterior_coords)] = 0
                    convexity_list[(i + 2) % len(polygon_exterior_coords)] = None

                    if is_postprocess:
                        angles_list[i % len(polygon_exterior_coords)] = None
                        angles_list[(i + 1) % len(polygon_exterior_coords)] = 0
                        angles_list[(i + 2) % len(polygon_exterior_coords)] = None
                        angles_list = [x for x in angles_list if x is not None]

                    # 배열의 앞부분에 None이 들어간 경우 i를 앞으로 이동한다.
                    if i + 2 >= len(polygon_exterior_coords):
                        i -= 1

                    polygon_exterior_coords = [x for x in polygon_exterior_coords if x is not None]
                    convexity_list = [x for x in convexity_list if x is not None]
                    vertice_count -= 2

                    # continue. 이동된 점의 위치에서 다시 엠보스 형상 여부를 확인한다.
                    continue

        i += 1
        if i >= vertice_count:
            break

    polygon = Polygon(polygon_exterior_coords)

    # 한 선분 위의 연속된 점을 제거한다.
    polygon = simplify_polygon(polygon, tol_length=consts.TOLERANCE)

    time.process_time() - start

    return polygon


def postprocess_emboss_cut(
    mass,
    core,
    tolerance,
    tolerance_angle,
    regulation,
    postprocess_emboss_cut_length,
    time_counter_dict,
    mass_cut_depth_divider,
):
    # 아래층 밖으로 튀어나오는 면적 제거 이후 엠보스 컷 실행
    cut_mass = []
    for mfi, mass_each_floor in enumerate(mass):
        mass_polygon = simplify_polygon(
            mass_each_floor[0],
            tol_angle=tolerance_angle,
            tol_length=consts.TOLERANCE,
            container_geometry=regulation[mfi],
        )
        # 코어와 매스를 합친 영역에 엠보스 컷을 적용합니다.
        mass_polygon_with_core = MultiPolygon([mass_polygon, core])
        mass_polygon_with_core = buffer_dilation_and_erosion(
            polygon=mass_polygon_with_core,
            buffer_distance=consts.TOLERANCE_MARGIN,
            use_simplification=True,
            choose_biggest_polygon=True,
        )

        # 연속된 점을 제거합니다.
        mass_polygon_with_core = simplify_polygon(
            mass_polygon_with_core,
            tol_angle=tolerance_angle,
            tol_length=tolerance,
            container_geometry=regulation[mfi],
        )

        mass_polygon_with_core = cut_emboss(
            mass_polygon_with_core,
            postprocess_emboss_cut_length,
            0,
            time_counter_dict,
            True,
            tolerance_angle,
            mass_cut_depth_divider=mass_cut_depth_divider,
        )
        mass_polygon = mass_polygon_with_core.difference(core)
        mass_polygon = buffer_erosion_and_dilation(
            polygon=mass_polygon,
            buffer_distance=consts.TOLERANCE_SLIVER,
            use_intersection=True,
            choose_biggest_polygon=True,
        )
        cut_mass.append([mass_polygon])
    return cut_mass


def deadspacecut_with_exterior(mass, tolerance_angle, tolerance, core, engine_type, simple_deadspace_len, regulation):
    valid_mass = []
    for i, floor in enumerate(mass):
        new_mass = simplify_polygon(
            floor[0], tol_angle=tolerance_angle, tol_length=tolerance, container_geometry=regulation[i]
        )
        if new_mass.is_empty:
            valid_mass.append([new_mass])
            continue

        if engine_type == consts.ENGINE_TYPE_BASIC and i > 0:
            new_mass = buffer_dilation_and_erosion(shapely.ops.unary_union([new_mass, core]), consts.TOLERANCE_MARGIN)

        new_mass = buffer_erosion_and_dilation(new_mass, simple_deadspace_len / 2)
        valid_mass.append([new_mass])

    return valid_mass


def basic_final_postprocessing(mass, core, regulation):
    """Postprocessing only for basic engine

    Args:
        mass (list): the mass
        core (Polygon): the core
        regulation (list): the regulation

    Returns:
        list: new mass
    """
    basic_mass = []
    for mass_each_floor in mass:
        mass_union = shapely.ops.unary_union([mass_each_floor[0], core])
        mass_union = buffer_dilation_and_erosion(
            polygon=mass_union,
            buffer_distance=consts.TOLERANCE_SLIVER,
            use_simplification=True,
            choose_biggest_polygon=True,
        )
        basic_mass.append([mass_union])

    # 코어를 병합시킨 이후 틈이 생기는 매스가 발생할 수 있음
    # 따라서 코어의 선분 중 가장 짧은 것으로 dilation and erosion 한 도형이 법규선을 침범하지 않으면 변경
    shortest_core_segment_length = min(c.length for c in explode_to_segments(core.boundary))

    for ebmi, each_basic_mass in enumerate(basic_mass):
        if each_basic_mass[0].is_empty:
            continue

        filled_each_basic_mass = buffer_dilation_and_erosion(
            polygon=each_basic_mass[0],
            buffer_distance=shortest_core_segment_length / 2,
        )

        if filled_each_basic_mass.within(regulation[ebmi]):
            basic_mass[ebmi] = [filled_each_basic_mass]

    return basic_mass


def get_regulation_bounds(regulation: List[Polygon], mass_angle: float) -> List[float]:

    regulation_union = shapely.ops.unary_union(regulation)
    rotated_regulation_union = shapely.affinity.rotate(regulation_union, -mass_angle, (0, 0), use_radians=True)
    regulation_bounds = shapely.ops.unary_union(rotated_regulation_union).bounds

    return regulation_bounds


def no_diagonals_before_diagonalize(mass_polygon):
    """diagonalize 실행 전 사선이 없는 것을 확인합니다."""

    for angle in angle_of_polygon_vertices(mass_polygon):
        right_angle = np.pi / 2
        angle_converted = (angle) % (right_angle)
        assert (-consts.TOLERANCE_ANGLE <= angle_converted <= consts.TOLERANCE_ANGLE) or (
            right_angle - consts.TOLERANCE_ANGLE <= angle_converted <= right_angle + consts.TOLERANCE_ANGLE
        )


# ==== core


def gen_segs_to_use_from_core(
    core_segs: List[LineString],
    mass_boundary: List[Polygon],
    is_using_short_segs: bool,
    is_core_translate_use: bool = False,
    existing_hall: Polygon = Polygon(),
) -> Tuple[List[List[LineString]], List[List[LineString]], List[LineString], List[LineString]]:
    # 코어 직사각형을 구성하는 4개의 선분들 중 긴 선분 2개와 짧은 선분 2개를 분리한다. (긴 것은 긴 것, 짧은 것은 짧은 것끼리 서로 평행하다.)
    # 짧은 것들 혹은 긴 것들 중 하나를 선택하여, 배치의 기준이 될 선분으로 사용한다.
    long_core_segs = []
    short_core_segs = []
    for core_segs_each_floor in core_segs:
        segs = core_segs_each_floor.geoms
        if segs[0].length >= segs[1].length:
            long_core_segs.append([segs[0], segs[2]])
            short_core_segs.append([segs[1], segs[3]])
        else:
            long_core_segs.append([segs[1], segs[3]])
            short_core_segs.append([segs[0], segs[2]])

    # 각 층 mass의 중심점을 계산한다.
    avg_centroid = MultiPoint(list(map(lambda x: x.boundary.centroid, mass_boundary))).centroid

    # change_escape_core_to_general_core 함수에서 피난계단 -> 일반계단 변경하는 경우 기존 홀 위치와 동일한 곳에 배치하기 위함
    if not existing_hall.is_empty:
        avg_centroid = existing_hall.centroid

    # 긴 것을 사용할지, 짧은 것을 사용할지 결정하고, 두 경우 모두 두개의 선분이 타겟이 된다.
    if is_using_short_segs:
        target_core_segs = short_core_segs
    else:
        target_core_segs = long_core_segs

    # 타겟으로 정한 두 선분 중 중심점과 가까운 선분은 close_seg, 먼 것은 far_seg가 된다.
    distance_from_centroid = list(map(lambda x: [avg_centroid.distance(x_) for x_ in x], target_core_segs))
    close_seg_idx, far_seg_idx = list(zip(*map(lambda x: (np.argmin(x), np.argmax(x)), distance_from_centroid)))

    # close_seg, far_seg의 타입은 List[LineString]이며, 층수와 같은 길이를 가진다.
    # 이 선분들은 모두 사각형을 구성하는 선분들 중 하나이므로, 사각형을 반시계 방향으로 구성하는 방향을 가지고 있다.
    close_seg: List[LineString]
    far_seg: List[LineString]
    close_seg = list(map(lambda x, y: x[y], target_core_segs, close_seg_idx))
    far_seg = list(map(lambda x, y: x[y], target_core_segs, far_seg_idx))

    # translate_core 이후에 mass_boundary의 exterior에 위치한 선분이 close_seg가 되는 경우가 있어 한 번 더 검사하여
    # mass_boundary 안쪽에 위치한 선분을 close_seg로 사용
    target_core_seg = target_core_segs[0]
    core_polygon = Polygon(Polygon([*target_core_seg[0].coords, *target_core_seg[1].coords]))
    core_diff_mass_boundary = mass_boundary[-1] - core_polygon.buffer(consts.TOLERANCE)
    buffered_core_diff_boundary = core_diff_mass_boundary.buffer(consts.TOLERANCE_LARGE)

    if is_core_translate_use:
        is_far_seg_within_buffered_core_diff_boundary = far_seg[0].within(buffered_core_diff_boundary)
        is_not_close_seg_within_buffered_core_diff_boundary = not close_seg[0].within(buffered_core_diff_boundary)
        if is_far_seg_within_buffered_core_diff_boundary and is_not_close_seg_within_buffered_core_diff_boundary:
            close_seg, far_seg = far_seg, close_seg

    return long_core_segs, short_core_segs, close_seg, far_seg


def gen_core(
    core: List[Polygon],
    core_type: int,
    mass_boundary: List[Polygon],
    use_small_core: bool,
    is_commercial_area: bool,
    is_escape_core: bool,
    is_center_core_placed: bool,
    is_using_adjusted_core: bool,
    is_last_gen_core_called: bool = False,
    is_specific_escape_sub_core: bool = False,
    is_specific_escape_emgcy_elev_sub_core: bool = False,
    is_core_translate_use: bool = False,
    existing_hall: Polygon = Polygon(),
):
    """Generate core inner geometry.

    Args:
        core (list(Polygon)): sampled list of core polygon
        core_type (int): selected core type
        mass_boundary (list(Polygon)): list of mass polygon
        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)
        is_commercial_area (bool): 상업지역 여부
        is_escape_core (bool): 피난계단 사용 여부
        is_center_core_placed (bool): 코어의 위치가 중심인지 모서리인지
        is_last_gen_core_called (bool): premium.py에서 사용되는 gen_core인지 여부
    Raises:
        Exception: when core type is not in 0~2
    Returns:
        (tuple): tuple containing:
            hall (list(Polygon)): list of hall polygon (코어 내 복도)
            stair (list(Polygon)): list of stair polygon (코어 내 계단)
            elev (list(Polygon)): list of elev polygon (코어 내 승강기)
            core (list(Polygon)): list of core polygon
            close_seg (list(LineString)): list of short core segment close from mass centroid
            (매스 센트로이드와 가까운 짧은 코어 세그먼트)
            far_seg (list(LineString)): list of short core segment far from mass centroid
            (매스 센트로이드와 먼 짧은 코어 세그먼트)
            core_segs_for_parking (list(MultiLineString)): list of long core segment
            (주차모듈에서 사용되는 코어 세그먼트들, 긴 두개의 선분 혹은 짧은 두개의 선분이 됨)
    """
    # 코어안에 요소들, 복도에 포함될 hall, 계단 stair, 엘리베이터 elev
    hall = stair = elev = None

    # 코어를 simplify 하고, 방향은 반시계 방향으로 설정한다.
    core = list(map(lambda x: shapely.ops.orient(x, sign=1.0).simplify(consts.TOLERANCE), core))

    # 코어 사각형을 각 선분으로 분리한다.
    core_segs = list(map(lambda x: MultiLineString(explode_to_segments(x.boundary)), core))

    # 아래 코드는 코어 유형별로 코어 안에 hall(복도), stair(계단), elev(엘리베이터)를 배치한다.
    # 이들을 배치를 할 땐 직사각형인 코어의 4개 선분들 중 서로 마주보는 두 선분을 기준으로 삼는다. 코어 유형에 따라 짧은 선분 2개가 선택되기도 하고 긴 선분 2개가 선택되기도 한다.
    # 그 두 선분 중 매스의 중심점과 가까운 선분이 close_seg이고 중심점과 먼 선분이 far_seg이다.
    # 이 기준 선분들과 엘리베이터 승강로 규격, HALL 규격 상수를 이용해 hall, stair, elev를 배치한다.

    core_segs_for_parking: List[List[LineString]]

    # 조건에 따른 엘리베이터 크기 결정
    elev_width, elev_height = get_elev_size(use_small_core, is_using_adjusted_core)

    attached_room = [Polygon()] * len(mass_boundary)
    emergency_elev_room = [Polygon()] * len(mass_boundary)

    # 0번 코어 : 엘리베이터 없는 코어 / slim
    if core_type == 0:
        # stair-hall 붙어 있는 구조
        # close_seg, far_seg는 짧은 선분들 중에 결정된다.
        long_core_segs, short_core_segs, close_seg, far_seg = gen_segs_to_use_from_core(
            core_segs, mass_boundary, is_using_short_segs=True, is_core_translate_use=is_core_translate_use
        )

        # TODO : 이 값이 함수에서 return되서 주차 모듈에도 사용되는데, 변수명 long_core_segs로 이용되고 있어 전부 변경이 필요하다
        core_segs_for_parking = long_core_segs

        # hall, stair, elev 모두 사각형으로 구성이 되는데, 두개의 평행한 선분을 이용해서 사각형을 생성한다.
        # hall을 구성할 첫번째 선분으로, 코어 짧은 선분 중 매스 중심과 가까운 선분이다.
        hall_core_seg = close_seg
        # hall을 구성할 두번째 선분으로, 첫번째 선분을 평행이동 하여 구한다.
        # 이때 방향은, (hall_core_seg 선분의 첫 점) 에서 (hall_core_seg 끝 점) 방향을 기준으로 직각 왼쪽이다.
        # core의 각 선분이 반시계 방향으로 구성된 것을 고려할 때, 코어 안쪽 방향으로 상수 HALL_WIDTH 만큼 평행이동하게 된다.
        # HALL_WIDTH는 복도의 최소 너비이다.
        hall_core_seg_parallel = list(map(lambda x: x.parallel_offset(consts.HALL_WIDTH, "left"), hall_core_seg))
        # 평행한 선분 두개를 사용하면 하나의 사각형을 구성 할 수 있다.
        # 첫 번째 선분은 방향을 그대로 사용하지만, 두번째 선분은 방향을 반전시켜서 사각형이 반시계 방향으로 구성되게 한다.
        hall = list(
            map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords[::-1]])), hall_core_seg, hall_core_seg_parallel)
        )

        # stair를 구성할 첫번째 선분으로, 코어 짧은 선분 중 매스 중심과 먼 선분이다.
        stair_core_seg = far_seg
        # 첫 번째 선분은 방향을 그대로 사용, 두번째 선분도 방향을 그대로 사용하면 된다.
        stair = list(
            map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords])), stair_core_seg, hall_core_seg_parallel)
        )

        # 이 타입의 코어는 엘리베이터가 empty Polygon이다.
        elev = list(map(lambda x: Polygon(), core))

    # 1번 코어 : 엘리베이터 있음 / 장방형 코어, slimE
    elif core_type == 1:
        # stair-hall-elev 구조로 배치가 됨
        # close_seg, far_seg는 짧은 선분들 중에 결정된다
        long_core_segs, short_core_segs, close_seg, far_seg = gen_segs_to_use_from_core(
            core_segs,
            mass_boundary,
            is_using_short_segs=True,
            is_core_translate_use=is_core_translate_use,
            existing_hall=existing_hall,
        )

        # TODO : 이 값이 함수에서 return되서 주차 모듈에도 사용되는데, 변수명 long_core_segs로 이용되고 있어 전부 변경이 필요하다
        core_segs_for_parking = long_core_segs

        # elev을 구성할 첫번째 선분으로, 코어 짧은 선분 중 매스 중심과 가까운 선분이다.
        elev_core_seg = close_seg
        # 이 slimE 타입의 코어에서는 예외적으로 승강로 규격 height보다 더 큰 영역을 elev로 생성한다.
        # elev을 구성할 두번째 선분으로, 첫번재 선분을 평행이동 하여 구한다. hall과 elev가 이 선분을 공유함
        # 이때 방향은, (elev_core_seg 선분의 첫 점) 에서 (elev_core_seg 끝 점) 방향을 기준으로 직각 왼쪽이다.
        # core의 각 선분이 반시계 방향으로 구성된 것을 고려할 때, 코어 안쪽 방향으로 상수 ELEV_WIDTH 만큼 평행이동하게 된다.
        hall_elev_seg = list(map(lambda x: x.parallel_offset(elev_width, "left"), close_seg))
        # 평행이동한 선분은 방향을 반전 시켜 사용.
        elev = list(map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords[::-1]])), elev_core_seg, hall_elev_seg))

        # 다른 코어들의 경우 hall의 너비가 복도 최소 너비인 HALL_WIDTH로 생성되지만, 1번 타입 코어에서는 기획에 따라 너비에 150mm가 추가 패딩으로 들어간다.
        # 예시) slimE 타입 코어에서 계단과 엘리베이터 사이에 hall이 위치되는데, 그 사이 간격이 1400 + 150 = 1550 이다.
        elev_hall_padding = 0.15  # 엘리베이터 입구쪽 오프셋
        # hall과 stair가 공유할 선분, close_seg로 방향 기준 직각 90도 왼쪽으로 이동하여 계산한다.
        hall_stair_seg = list(
            map(lambda x: x.parallel_offset(consts.HALL_WIDTH + elev_hall_padding + elev_width, "left"), close_seg)
        )
        # hall_stair_seg만 방향 반전시켜 사용한다.
        hall = list(
            map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords[::-1]])), hall_elev_seg, hall_stair_seg)
        )

        # stair를 구성할 첫번째 선분으로, 코어 짧은 선분 중 매스 중심과 먼 선분이다.
        stair_core_seg = far_seg
        # 두 선분으로 사각형 구성
        stair = list(map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords])), hall_stair_seg, stair_core_seg))

    # 2번 코어 : 엘리베이터 있음 / 결합형 코어, wideE
    elif core_type == 2:
        # 긴 선분에 hall이 배치되고, hall에 stair와 elev가 각각 붙어있는 구조

        # 2번의 소형 및 상업지역 코어는 짧은 쪽 변에 hall 이 붙습니다.
        is_using_short_segs = bool(use_small_core or is_commercial_area or (is_center_core_placed and is_escape_core))

        # close_seg, far_seg는 긴 선분들 중에 결정된다.
        (long_core_segs, short_core_segs, close_seg, far_seg) = gen_segs_to_use_from_core(
            core_segs,
            mass_boundary,
            is_using_short_segs=is_using_short_segs,
            is_core_translate_use=is_core_translate_use,
            existing_hall=existing_hall,
        )

        # TODO : 이 값이 함수에서 return되서 주차 모듈에도 사용되는데, 변수명 long_core_segs로 이용되고 있어 전부 변경이 필요하다
        core_segs_for_parking = short_core_segs

        # 복도를 close_seg에 붙여 생성한다.
        hall_core_seg = close_seg
        hall_core_seg_parallel = list(map(lambda x: x.parallel_offset(consts.HALL_WIDTH, "left"), hall_core_seg))
        hall = list(
            map(
                lambda x, y: Polygon(np.concatenate([x.coords, y.coords[::-1]])),
                hall_core_seg,
                hall_core_seg_parallel,
            )
        )

        # 이 점은 close_seg를 축으로, elev와 stair를 나눌 기준 점이 된다.
        # close_seg(1층 값 사용)의 시작점으로부터 이 line을 따라서 ELEV_HEIGHT 만큼 이동한다.
        close_seg_elev_stair_point = close_seg[0].interpolate(elev_height)
        # 이 점은 far_seg를 축으로, elev와 stair를 나눌 기준 점이 된다.
        # far_seg(1층 값 사용)의 끝점으로부터 ELEV_HEIGHT만큼 이동 (interpolate 거리를 전체거리에서 빼주어서 끝점 기준처럼 사용)
        # close_seg와 far_seg는 벡터로서 정 반대의 방향이기 때문에, 반대 거리로 interpolate를 사용함.
        far_seg_elev_stair_point = far_seg[0].interpolate(far_seg[0].length - elev_height)

        # close_seg(1층 값 사용)의 시작점으로부터 위에서 구한 경계 점까지를 사용해 elev 구성
        elev_line_item = LineString([close_seg[0].coords[0], close_seg_elev_stair_point])

        # elev영역의 크기는 기획 도면 규격과 일치시키고, 위치는 복도와 접하게 함.
        # TODO : 사각형 hall만 가정하고 다른 로직들도 구현되어 있어, 엘리베이터 위치가 기획 도면과 다르며 이를 반영하기 위한 구현 필요함.
        # elev를 구성할 첫 선분이다.
        # 층 수 만큼 list 생성한다.
        elev_core_seg = [elev_line_item for _ in close_seg]
        elev_core_seg = list(map(lambda x: x.parallel_offset(consts.HALL_WIDTH, "left"), elev_core_seg))
        # elev를 구성할 두번째 선분이다.
        elev_oppo_seg = list(map(lambda x: x.parallel_offset(elev_width, "left"), elev_core_seg))
        # 선분 방향에 유의하여 elev 사각형 구성한다.
        elev = list(map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords[::-1]])), elev_core_seg, elev_oppo_seg))

        # close_seg 에서 경계점부터 끝점 까지의 선분이다.
        stair_core_line_item = LineString([close_seg_elev_stair_point, close_seg[0].coords[1]])
        # stair를 구성할 첫 선분이며, 층 수 만큼 list로 생성한다.
        stair_core_seg = [stair_core_line_item for _ in close_seg]
        stair_core_seg = list(map(lambda x: x.parallel_offset(consts.HALL_WIDTH, "left"), stair_core_seg))

        # stair_core_line_item과 같은 길이의 평행한 선분이며, 거리가 먼 선분으로 생성된다.
        stair_oppo_line_item = LineString([far_seg[0].coords[0], far_seg_elev_stair_point])
        # 층 수 만큼 생성한다.
        stair_oppo_seg = [stair_oppo_line_item for _ in far_seg]
        # 구성되는 두 선분이 close_seg, far_seg와 각각 같은 방향이기에 방향 그대로 사용 가능.
        stair = list(map(lambda x, y: Polygon(np.concatenate([x.coords, y.coords])), stair_core_seg, stair_oppo_seg))
        if is_using_adjusted_core:
            # https://www.notion.so/spacewalkcorp/new-WideE-235a09163ce0446280371c02059da92c

            elev_front_hall_offset_dis = short_core_segs[0][0].length - consts.HALL_WIDTH - elev_width
            elev_front_hall = offset_curve_polygon(elev_core_seg[0], elev_front_hall_offset_dis, "left")
            buffered_elev_front_hall = elev_front_hall.buffer(consts.TOLERANCE, join_style=JOIN_STYLE.mitre)

            each_hall = shapely.ops.unary_union([hall[0], buffered_elev_front_hall])
            hall = [simplify_polygon(each_hall, tol_length=consts.TOLERANCE)] * len(hall)

            new_elev_area = offset_curve_polygon(elev_oppo_seg[0], elev_front_hall_offset_dis, "left")
            buffered_new_elev_area = new_elev_area.buffer(consts.TOLERANCE, join_style=JOIN_STYLE.mitre)

            each_elev = shapely.ops.unary_union([elev[0] - buffered_elev_front_hall, buffered_new_elev_area])
            elev = [simplify_polygon(each_elev, tol_length=consts.TOLERANCE)] * len(elev)

    # core module 3
    elif core_type == 3:
        # https://www.notion.so/spacewalkcorp/core_type-3-92cd74822418423da8aac234ec2dcc93

        long_core_segs, _, close_seg, far_seg = gen_segs_to_use_from_core(
            core_segs, mass_boundary, is_using_short_segs=True, is_core_translate_use=is_core_translate_use
        )

        core_segs_for_parking = long_core_segs

        # 엘리베이터 앞의 hall 만들기 위해 close_seg를 elev_width만큼 offset시킨 선분으로 hall 일부 생성
        each_hall_part_seg = close_seg[0].parallel_offset(elev_width, "left")
        each_hall_part = offset_curve_polygon(each_hall_part_seg, consts.HALL_WIDTH, "left")

        # 계단 diff 연산에 사용할 계단 전체 덩어리 도형 생성
        each_stair_part_seg = each_hall_part_seg.parallel_offset(consts.HALL_WIDTH, "left")
        each_stair_offset_dis = long_core_segs[0][0].length - consts.HALL_WIDTH - elev_width
        each_stair_part = offset_curve_polygon(each_stair_part_seg, each_stair_offset_dis, "left")

        # hall의 ㄱ자로 꺾이는 부분을 만들기 위한 선분 생성
        offset_each_hall_part_seg = each_hall_part_seg.parallel_offset(consts.HALL_WIDTH, "left")

        remain_hall_part_seg_vertices = MultiPoint(offset_each_hall_part_seg.coords)
        sorted_remain_hall_part_seg_vertices = sorted(
            remain_hall_part_seg_vertices.geoms, key=lambda x: x.distance(mass_boundary[-1].boundary)
        )

        remain_hall_part_seg = LineString(sorted_remain_hall_part_seg_vertices)
        # close_seg 길이(2.8m)의 절반 == 계단의 절반 폭
        reduced_remain_hall_part_seg = shapely.ops.substring(remain_hall_part_seg, 0.5, 1, normalized=True)

        # hall 나머지 도형 생성
        each_remain_hall_dis = consts.ADJUSTED_REMAIN_HALL_DIS
        buffered_reduced_remain_hall_part_seg = reduced_remain_hall_part_seg.buffer(
            each_remain_hall_dis, join_style=JOIN_STYLE.mitre, cap_style=CAP_STYLE.flat
        )

        each_elev = offset_curve_polygon(close_seg[0], elev_width, "left")
        buffered_each_elev = each_elev.buffer(consts.TOLERANCE, join_style=JOIN_STYLE.mitre)
        each_remain_hall_part = buffered_reduced_remain_hall_part_seg - buffered_each_elev

        each_hall = simplify_polygon(
            shapely.ops.unary_union([each_hall_part, each_remain_hall_part]), tol_length=consts.TOLERANCE
        )
        each_stair = each_stair_part - each_remain_hall_part.buffer(consts.TOLERANCE, join_style=JOIN_STYLE.mitre)

        elev = [each_elev] * len(mass_boundary)
        hall = [each_hall] * len(mass_boundary)
        stair = [each_stair] * len(mass_boundary)

    else:
        raise Exception("FIXME: 잘못된 core type을 전달 받았습니다.")

    # corridor_entries 생성시 반시계방향 기준으로 offset하므로 ccw로 고정
    hall = list(map(lambda x: shapely.ops.orient(x, sign=1.0).simplify(consts.TOLERANCE), hall))

    return hall, stair, elev, core, attached_room, emergency_elev_room, close_seg, far_seg, core_segs_for_parking


def gen_corridor_entries(
    hall: List[Polygon],
    mass: List[Polygon],
    core: Polygon,
    corridor_entries_direction: List[bool],
) -> List[List[Polygon]]:
    """복도 출입구 생성 (코어 내 복도와 접하는 최소 복도 셀).

    Args:
        hall (List[Polygon]): 층별 코어 내 복도. 최소 1층은 존재해야함.
        mass (List[Polygon]): 층별 매스. 매스 층수를 기준으로 복도 출입구를 생성함.
        core (Polygon): 층별 코어 폴리곤

    Returns:
        List[List[Polygon]]: 층별 복도 출입구 (길이는 매스와 같은 층수), 층마다 2개이며 공간이 부족한 경우는 빈 폴리곤이 들어간다.
    """

    assert len(hall) > 0
    # 모든 hall은 같은 형상이므로 1층의 hall을 기준으로 계산한다.

    hall, corridor_entries_direction = get_temp_hall(hall[0], corridor_entries_direction, core)

    corridor_entries = []
    for each_hall in hall:
        exploded_each_hall = explode_to_segments(each_hall.boundary)

        each_short_hall_segs = sorted(exploded_each_hall, key=lambda x: x.length)[:2]
        each_entries = [offset_curve_polygon(s, consts.HALL_WIDTH, "right") for s in each_short_hall_segs]

        corridor_entries.append(each_entries)

    # 공간이 부족해 출입구가 매스를 벗어나면, 빈 폴리곤으로 변경해준다.
    core_minimum_rotated_rectangle = core.minimum_rotated_rectangle.buffer(consts.TOLERANCE)
    # 또는 코어 안쪽으로 출입구가 생긴 경우 빈 폴리곤으로 변경해준다.
    for mass_each_floor, corridor_entries_each_floor in zip(mass, corridor_entries):
        dilated_mass_each_floor = mass_each_floor.buffer(consts.TOLERANCE_LARGE, join_style=JOIN_STYLE.mitre)
        for i in range(len(corridor_entries_each_floor)):
            is_entry_within_floor = corridor_entries_each_floor[i].within(dilated_mass_each_floor)
            is_entry_within_core_ombr = corridor_entries_each_floor[i].within(core_minimum_rotated_rectangle)
            if not is_entry_within_floor or is_entry_within_core_ombr:
                corridor_entries_each_floor[i] = Polygon()

    return corridor_entries, corridor_entries_direction


def get_elev_size(use_small_core: bool, is_using_adjusted_core: bool) -> Tuple[float]:
    """입력받은 조건을 기반으로 엘리베이터 사이즈 반환

    Args:
        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)
        is_using_adjusted_core (bool): CORE_WIDE, CORE_NARR에 해당하는 코어인지 여부

    Returns:
        Tuple[float]: 엘리베이터 사이즈
    """

    elev_width = consts.ELEV_WIDTH
    elev_height = consts.ELEV_HEIGHT

    if use_small_core:
        elev_width = consts.ELEV_WIDTH_SMALL
        elev_height = consts.ELEV_HEIGHT_SMALL

    elif is_using_adjusted_core:
        elev_width = consts.ADJUSTED_ELEV_WIDTH
        elev_height = consts.ADJUSTED_ELEV_HEIGHT

    return elev_width, elev_height


def get_core_boundary_intsc_long_hall_seg(core: Polygon, long_hall_segs: List[LineString]) -> LineString:
    """홀 장변 선분과 코어 도형이 공유하는 선분 도출

    Args:
        core (Polygon): 1개층 코어 도형
        long_hall_segs (List[LineString]): 1개층 hall 장변 선분

    Returns:
        LineString: 코어와 홀 장변 선분이 공유하는 선분
    """

    core_intsc_long_hall_seg = LineString()
    for long_hall_seg in long_hall_segs:
        reduced_long_hall_seg = extend_curve(long_hall_seg, -consts.TOLERANCE_MARGIN, -consts.TOLERANCE_MARGIN).buffer(
            consts.TOLERANCE
        )

        if reduced_long_hall_seg.intersects(core.boundary):
            core_intsc_long_hall_seg = long_hall_seg
            break

    return core_intsc_long_hall_seg


def get_temp_hall(
    hall: Polygon,
    corridor_entries_direction: List[bool],
    core: Polygon,
    corridor_loading: List[int] = None,
) -> Tuple[List[Polygon], List[bool]]:
    """corridor_entries, dirs, corridor_skeletons 등을 생성하는데 사용할 임시 hall 생성

    Args:
        hall (Polygon): 1개층 hall Polygon
        corridor_entries_direction (List[bool]): corridor_entries 생성 방향
        core (Polygon): 1개층 core Polygon
        corridor_loading (List[int], optional): 복도 타입. Defaults to None.

    Returns:
        Tuple[List[Polygon], List[bool]]: 임시로 사용할 hall 리스트, corridor_entries 생성 방향
    """

    # 편복도인 경우 corridor_entries_direction 파라미터에 영향 받으면 안됨
    if corridor_loading is not None:
        for i, loading in enumerate(corridor_loading):
            if loading == 0:
                corridor_entries_direction[i] = False

    hall_segs: List[LineString]
    hall_segs = explode_to_segments(hall.boundary)

    sorted_hall_segs = sorted(hall_segs, key=lambda x: x.length)
    long_hall_segs = sorted_hall_segs[-2:]

    # corridor_entries를 hall의 수직방향으로 생성할 수 있는 코어인지 검사
    core_intsc_long_hall_seg = get_core_boundary_intsc_long_hall_seg(core, long_hall_segs)
    is_empty_core_intsc_long_hall_seg = core_intsc_long_hall_seg.is_empty

    # hall 선분들로 hall 폴리곤을 생성한다.
    temp_width = sorted_hall_segs[-1].distance(sorted_hall_segs[-2])
    not_direction_hall = offset_curve_polygon(sorted_hall_segs[-1], temp_width, "left")

    if not is_empty_core_intsc_long_hall_seg:
        direction_hall = offset_curve_polygon(core_intsc_long_hall_seg, consts.HALL_WIDTH, "right")
        direction_hall = shapely.ops.orient(direction_hall, -1.0)
    else:
        # corridor_entries를 hall의 수직방향으로 생성할 수 없다면 False로 변환
        corridor_entries_direction = [False] * len(corridor_entries_direction)

    temp_hall = []
    for entry_direction in corridor_entries_direction:
        if entry_direction:
            temp_hall.append(direction_hall)
        else:
            if is_empty_core_intsc_long_hall_seg:
                temp_hall.append(hall)
            else:
                temp_hall.append(not_direction_hall)

    return temp_hall, corridor_entries_direction


# ====


class EnvPlan:
    def __init__(
        self,
        packed_unit_space: List[List[Polygon]],
        parking_cells: List[None],
        parking_regulation: float,
        commercial_type: int,
    ):
        self._packed_unit_space = packed_unit_space
        self._parking_cells = parking_cells
        self._parking_regulation = parking_regulation
        self._commercial_type = commercial_type

    @property
    def parking_cells(self):
        return self._parking_cells

    @parking_cells.setter
    def parking_cells(self, value):
        self._parking_cells = value

    @property
    def packed_unit_space(self):
        return self._packed_unit_space

    @packed_unit_space.setter
    def packed_unit_space(self, value):
        self._packed_unit_space = value

    @property
    def parklot_count(self):
        return len(self.parking_cells)

    @property
    def parking_regulation(self):
        return self._parking_regulation

    @parking_regulation.setter
    def parking_regulation(self, value):
        self._parking_regulation = value

    @property
    def commercial_type(self):
        return self._commercial_type

    @commercial_type.setter
    def commercial_type(self, value):
        self._commercial_type = value

    @property
    def law_parklot_count(self):
        return math.floor(sum(sum(x.area for x in y) for y in self.packed_unit_space) / self.parking_regulation + 0.5)


def get_use_district_small_core(res):
    use_district_small_core = True
    if "준주거지역" in res["field"]["use_district"]:
        use_district_small_core = False
    if "일반상업지역" in res["field"]["use_district"]:
        use_district_small_core = False

    return use_district_small_core


def gen_obb_from_longest_segment(polygon):
    # 폴리곤의 가장 긴 변을 기준으로 바운딩 박스를 생성한다.
    mass_angle = get_mass_angle_from_a_polygon(polygon)

    # 폴리곤을 mass_angle 만큼 역회전하여 축과 평행한 bounding box를 생성한다.
    rotated_polygon = shapely.affinity.rotate(polygon, -mass_angle, (0, 0), use_radians=True)
    minx, miny, maxx, maxy = rotated_polygon.bounds
    rotated_bounding_box = box(minx, miny, maxx, maxy)

    # 박스 폴리곤을 원래의 위치로 회전한다.
    bounding_box = shapely.affinity.rotate(rotated_bounding_box, mass_angle, (0, 0), use_radians=True)

    return bounding_box, mass_angle


def gen_obb_from_convex_hull(polygon):
    # convex hull의 각 선분을 기준으로 바운딩 박스를 생성하고, 면적이 최소인 박스를 사용한다.

    polygon_exterior_coords = np.array(polygon.convex_hull.exterior.coords)
    polygon_exterior_vecs = polygon_exterior_coords[1:] - polygon_exterior_coords[:-1]

    mass_angles = []
    rotated_bounding_boxes = []

    # convex hull을 이루는 선분들에 평행한 바운딩 박스를 생성한다.
    for vec in polygon_exterior_vecs:
        mass_angle = np.arctan2(vec[1], vec[0])
        mass_angles.append(mass_angle)
        rotated_polygon = shapely.affinity.rotate(polygon, -mass_angle, (0, 0), use_radians=True)
        minx, miny, maxx, maxy = rotated_polygon.bounds
        rotated_bounding_box = box(minx, miny, maxx, maxy)
        rotated_bounding_boxes.append(rotated_bounding_box)

    # 가장 작은 바운딩 박스를 찾는다.
    min_bounding_box_idx = np.argmin([box.area for box in rotated_bounding_boxes])
    bounding_box = shapely.affinity.rotate(
        rotated_bounding_boxes[min_bounding_box_idx], mass_angles[min_bounding_box_idx], (0, 0), use_radians=True
    )

    return bounding_box, mass_angles[min_bounding_box_idx]


# todo: gen_obb_from_longest_segment, gen_obb_from_convex_hull 결과 같은 경우 분기 생성 x


def gen_grid_polygon(polygon, mass_angle, gridsize, tolerance, time_counter_dict, regulation_bounds):
    """입력 폴리곤에 그리드를 적용한다. 폴리곤 내부에 완전히 포함된 그리드 영역들에 해당하는 새로운 폴리곤을 만든다.

    Args:
        polygon (Polygon): 연산 대상 입력 폴리곤
        mass_angle (float): 폴리곤의 바운딩 박스가 회전된 각도 (그리드를 생성할 각도)
        gridsize (float): 그리드 셀 한 변의 길이
        tolerance (float): 폴리곤 외곽선과 그리드 선 사이의 거리 tolerance. 셀 크기의 1/100를 추천

    Returns:
        mass_poly (Polygon): 입력 폴리곤 내부의 격자화된 폴리곤
    """
    start = time.process_time()
    # remove slivers
    polygon = buffer_erosion_and_dilation(
        polygon=polygon,
        buffer_distance=consts.TOLERANCE_SLIVER,
        use_intersection=True,
        choose_biggest_polygon=True,
    )

    # 바운딩 박스의 기준축과 맞도록 폴리곤을 회전한다.
    rotated_polygon = shapely.affinity.rotate(polygon, -mass_angle, (0, 0), use_radians=True)

    # 폴리곤 바운딩 박스의 x,y값이 가장 작은 곳에서 그리드 크기만큼 한 칸 바깥쪽으로 이동한 지점을 원점으로 사용한다.
    # 폴리곤 내부에 포함되는 격차를 최대한 늘리기 위한 정렬.
    minx, miny, maxx, maxy = rotated_polygon.bounds

    if regulation_bounds is not None:
        minx, miny, maxx, maxy = regulation_bounds

    translated_polygon = shapely.affinity.translate(
        rotated_polygon, xoff=-minx + gridsize - tolerance, yoff=-miny + gridsize - tolerance
    )

    # 그리드 x방향, y방향 셀 개수를 결정한다.
    # 2를 더하여 양쪽으로 1만큼의 마진을 남긴다.
    n_gridcells_x = int(np.ceil((maxx - minx) / gridsize) + 2)
    n_gridcells_y = int(np.ceil((maxy - miny) / gridsize) + 2)

    # 폴리곤의 와곽선을 이루는 점들을 구한다.
    translated_polygon_exterior_coords = np.array(translated_polygon.exterior.coords)

    centerline_points = []

    # 폴리곤을 이루는 선분들이 포함되는 그리드 영역을 구한다.
    for i in range(len(translated_polygon_exterior_coords) - 1):

        # 선택한 점과 다음 점을 양 끝점으로 하는 폴리곤의 외곽선 선분
        exterior_line = LineString([translated_polygon_exterior_coords[i], translated_polygon_exterior_coords[i + 1]])

        # 해당 선분의 시작점이 포함되는 그리드 셀의 위치를 구한다.
        start_x = (translated_polygon_exterior_coords[i][0] // gridsize) * gridsize
        start_y = (translated_polygon_exterior_coords[i][1] // gridsize) * gridsize

        # 그리드 셀의 중심을 기준으로 사용한다.
        # 그리드 사이즈 반 칸만큼 +x, +y 방향으로 기준점을 이동한다.
        start_x = start_x + (gridsize / 2)
        start_y = start_y + (gridsize / 2)

        # 해당 선분의 끝점이 포함되는 그리드 셀의 위치를 구한다.
        end_x = (translated_polygon_exterior_coords[i + 1][0] // gridsize) * gridsize
        end_y = (translated_polygon_exterior_coords[i + 1][1] // gridsize) * gridsize

        # 그리드 셀의 중심을 기준으로 사용한다.
        # 그리드 사이즈 반 칸만큼 +x, +y 방향으로 기준점을 이동한다.
        end_x = end_x + (gridsize / 2)
        end_y = end_y + (gridsize / 2)

        # 시작점에서 끝점까지 가기 위해 x방향, y방향으로 각각 그리드 셀 폭만큼 몇 칸씩 이동해야 하는지 계산한다.
        x_distance = end_x - start_x
        y_distance = end_y - start_y

        x_distance_cells = int(round(x_distance / gridsize))
        y_distance_cells = int(round(y_distance / gridsize))

        # + 방향 또는 - 방향 중 어디로 이동해야 하는지 결정합니다.
        if x_distance_cells >= 0:
            x_increment = gridsize
        else:
            x_increment = -gridsize
        if y_distance_cells >= 0:
            y_increment = gridsize
        else:
            y_increment = -gridsize

        # 절댓값을 사용합니다.
        x_distance_cells = abs(x_distance_cells)
        y_distance_cells = abs(y_distance_cells)

        # 시작점부터 끝점까지 그리드 셀의 중심을 이은 선분들을 생성합니다.
        centerline_points.append(Point(start_x, start_y))
        current_x = start_x
        current_y = start_y
        while True:
            # x 또는 y값이 끝점에 도달했을 경우 바로 마지막 점과 이을 수 있습니다.
            # ex) x축과 평향한 선분의 경우, 첫 점과 끝 점을 잇는 선분을 사용
            if x_distance_cells == 0 or y_distance_cells == 0:
                # 마지막 점은 다음 선분의 시작점과 동일하다.
                # centerline_points.append(Point(end_x, end_y))
                break

            # x방향과 y방향으로 각각 셀 이동을 시도합니다.
            new_x = current_x + x_increment
            new_y = current_y + y_increment

            # 새로 만든 두 점 중 선분에 더 가까운 것을 선택합니다.
            new_point_x = Point(new_x, current_y)
            distance_x = exterior_line.distance(new_point_x)
            new_point_y = Point(current_x, new_y)
            distance_y = exterior_line.distance(new_point_y)

            if distance_x <= distance_y:
                centerline_points.append(new_point_x)
                current_x = new_x
                x_distance_cells -= 1
            else:
                centerline_points.append(new_point_y)
                current_y = new_y
                y_distance_cells -= 1

    centerline = LineString(centerline_points)

    border_poly = centerline.buffer((gridsize / 2) + tolerance, cap_style=CAP_STYLE.square, join_style=JOIN_STYLE.mitre)

    # centerline의 첫 점과 마지막 점을 이어줄 경우 self intersection이 발생할 수 있다.
    # 마지막 선분은 따로 만들어 합친다.
    last_segment = LineString([centerline_points[0], centerline_points[-1]])
    last_segment_poly = last_segment.buffer((gridsize / 2) + tolerance, cap_style=CAP_STYLE.square)

    border_poly = shapely.ops.unary_union([border_poly, last_segment_poly])
    border_poly = border_poly.buffer(-tolerance, join_style=JOIN_STYLE.mitre)

    # 그리드 x방향, y방향 셀 개수를 결정한다.
    # 2를 더하여 양쪽으로 1만큼의 마진을 남긴다.
    n_gridcells_x = int(np.ceil((maxx - minx) / gridsize) + 2)
    n_gridcells_y = int(np.ceil((maxy - miny) / gridsize) + 2)

    # 확장된 바운딩 박스의 영역에서 외곽선 폴리곤을 제거한다.
    extended_bb = box(0, 0, n_gridcells_x * gridsize, n_gridcells_y * gridsize)

    poly_areas = polygon_or_multipolygon_to_list_of_polygon(extended_bb.difference(border_poly))

    # 결과에서 외부 폴리곤을 제거한다.
    valid_poly_areas = []

    buffered_translated_polygon = translated_polygon.buffer(
        max([gridsize * 0.8, consts.TOLERANCE_MARGIN]), join_style=JOIN_STYLE.mitre
    )

    for poly_area in poly_areas:
        if isinstance(poly_area, Polygon) and buffered_translated_polygon.contains(poly_area):
            valid_poly_areas.append(poly_area)
    poly_areas = valid_poly_areas

    # 가장 큰 매스 영역을 선택한다.
    translated_mass_poly, _ = new_filter_polygon(poly_areas)

    mass_poly = shapely.affinity.translate(
        translated_mass_poly, xoff=minx - gridsize + tolerance, yoff=miny - gridsize + tolerance
    )
    mass_poly = shapely.affinity.rotate(mass_poly, mass_angle, (0, 0), use_radians=True)

    # gen_grid_polygon 수행시간 합산
    time.process_time() - start

    return mass_poly


def cut_extrude(polygon, depth, width, tolerance, time_counter_dict):
    # 럼프컷. 일정 폭과 깊이 미만의 ㄷ자로 튀어나온 형상을 제거한다.
    # 로직 상세 문서 확인: https://www.notion.so/spacewalkcorp/875c1cf57a9a422ab7a0c1253a7b7984

    start = time.process_time()

    # NOTE(pch): 빈 폴리곤이 들어오는 경우 아래 줄에서 DivisionError 발생
    # convexity_list[i % len(polygon_exterior_coords)]
    if polygon.is_empty:

        time.process_time() - start

        return polygon

    # 중복된 점 및 한 직선 위의 세 점 방지. 이 단계에서 모든 각은 직각이므로 큰 tol_angle 사용.
    tolerance_angle = np.pi / 2 - 0.1
    polygon = simplify_polygon(polygon, tol_angle=tolerance_angle, tol_length=tolerance)

    # 폴리곤의 꼭짓점마다 concave인지 convex인지 확인.
    convexity_list = gen_convexity_list(polygon)
    polygon_exterior_coords = list(polygon.exterior.coords)

    # 시작점과 같은 마지막 점을 제거한다.
    convexity_list = convexity_list[:-1]
    polygon_exterior_coords = polygon_exterior_coords[:-1]

    # 럼프컷 태상 폴리곤 꼭짓점의 개수의 초기값.
    vertice_count = len(convexity_list)
    i = 0

    while True:
        # i+1, i+2, i+3, i+4번째 점들이 럼프를 이루는지 확인한다.
        if (
            convexity_list[(i + 2) % len(polygon_exterior_coords)] == 1
            and convexity_list[(i + 3) % len(polygon_exterior_coords)] == 1
        ):
            point_b = Point(polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)])
            point_c = Point(polygon_exterior_coords[(i + 3) % len(polygon_exterior_coords)])

            # 튀어나온 영역의 폭이 width 상수보다 작아야 럼프 형상으로 처리할 수 있다.
            if tolerance <= point_b.distance(point_c) <= width:
                point_a = Point(polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)])
                point_d = Point(polygon_exterior_coords[(i + 4) % len(polygon_exterior_coords)])

                ab_distance = point_a.distance(point_b)
                cd_distance = point_c.distance(point_d)

                # 튀어나온 영역의 깊이 선분 2개 중 1개라도 depth 상수보다 작은 것이 있다면 럼프 형상으로 처리한다.
                if ab_distance <= depth or cd_distance <= depth:

                    # 럼프의 깊이를 이루는 두 선분의 길이가 동일한 경우, 럼프 전체를 제거할 수 있다.
                    if abs(ab_distance - cd_distance) < tolerance:

                        # 럼프 영역에 해당하는 점들을 제거한다.
                        for j in range(4):
                            polygon_exterior_coords[(i + 1 + j) % len(polygon_exterior_coords)] = None
                            convexity_list[(i + 1 + j) % len(polygon_exterior_coords)] = None

                        # 배열의 앞부분에 None이 추가되었을 경우 None 개수만큼 i를 앞으로 이동한다.
                        none_at_start_count = 0
                        for j in range(4):
                            if i + 1 + j >= len(polygon_exterior_coords):
                                none_at_start_count += 1

                        i -= none_at_start_count

                        polygon_exterior_coords = [x for x in polygon_exterior_coords if x is not None]
                        convexity_list = [x for x in convexity_list if x is not None]
                        vertice_count -= 4

                        # 4개 점이 제거된 후 새로운 럼프 영역이 나타날 수 있다.
                        # 두 칸 뒤로 이동하여 럼프 영역이 발생하는지 확인한다.
                        if i >= 2 and convexity_list[i] == 1:
                            i -= 2
                            continue

                    elif ab_distance > cd_distance:
                        # 선분 ab가 선분 cd보다 긴 경우

                        # 점 b를 d - c 만큼 이동한다.
                        vec = np.array(polygon_exterior_coords[(i + 4) % len(polygon_exterior_coords)]) - np.array(
                            polygon_exterior_coords[(i + 3) % len(polygon_exterior_coords)]
                        )
                        new_b_point = np.array(polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)]) + vec
                        polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)] = tuple(new_b_point)

                        # 점 c와 점 d는 제거한다.
                        for j in range(2):
                            polygon_exterior_coords[(i + 3 + j) % len(polygon_exterior_coords)] = None
                            convexity_list[(i + 3 + j) % len(polygon_exterior_coords)] = None

                        # 배열의 앞부분에 None이 추가되었을 경우 None 개수만큼 i를 앞으로 이동한다.
                        none_at_start_count = 0
                        for j in range(4):
                            if i + 1 + j >= len(polygon_exterior_coords):
                                none_at_start_count += 1

                        i -= none_at_start_count

                        polygon_exterior_coords = [x for x in polygon_exterior_coords if x is not None]
                        convexity_list = [x for x in convexity_list if x is not None]
                        vertice_count -= 2

                        # 점 b가 이동되고, c,d가 제거된 뒤 동일한 위치에서 다시 럼프가 발생하는지 확인한다.
                        continue

                    else:
                        # 선분 cd가 선분 ab보다 긴 경우

                        # 점 c를 a - b 만큼 이동한다.
                        vec = np.array(polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)]) - np.array(
                            polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)]
                        )
                        new_c_point = np.array(polygon_exterior_coords[(i + 3) % len(polygon_exterior_coords)]) + vec
                        polygon_exterior_coords[(i + 3) % len(polygon_exterior_coords)] = tuple(new_c_point)

                        # 점 a와 점 b는 제거한다.
                        for j in range(2):
                            polygon_exterior_coords[(i + 1 + j) % len(polygon_exterior_coords)] = None
                            convexity_list[(i + 1 + j) % len(polygon_exterior_coords)] = None

                        # 배열의 앞부분에 None이 추가되었을 경우 None 개수만큼 i를 앞으로 이동한다.
                        none_at_start_count = 0
                        for j in range(4):
                            if i + 1 + j >= len(polygon_exterior_coords):
                                none_at_start_count += 1

                        i -= none_at_start_count

                        polygon_exterior_coords = [x for x in polygon_exterior_coords if x is not None]
                        convexity_list = [x for x in convexity_list if x is not None]
                        vertice_count -= 2

                        # 2개 점이 제거된 후 새로운 럼프 영역이 나타날 수 있다.
                        # 두 칸 뒤로 이동하여 럼프 영역이 발생하는지 확인한다.
                        if i >= 2 and convexity_list[i] == 1:
                            i -= 2
                            continue

        i += 1
        if i >= vertice_count:
            break

    result_polygon = Polygon(polygon_exterior_coords)

    # 한 선분 위의 연속된 점을 제거한다.
    result_polygon = simplify_polygon(result_polygon, tol_length=consts.TOLERANCE)

    time.process_time() - start
    return result_polygon


def diagonalize(regulation_polygon, grid_polygon, angle_min, angle_max):
    """폴리곤의 오목한 부분을 대각선으로 대체한다.

    Args:
        regulation_polygon (Polygon): 법규선 폴리곤
        grid_polygon (Polygon): 격자화된 매스 폴리곤

    Returns:
        result_polygon (Polygon): 대각화 결과
    """
    # 대각화: 오목한 영역을 대각선으로 교체한다. 수정 법규선을 침범하지는 않는지 확인한다.

    # NOTE(pch): 입력 폴리곤이 비어있는 경우 아래 에러 발생
    # pyo3_runtime.PanicException: failed to get exterior ring
    if grid_polygon.is_empty:
        return grid_polygon

    # 폴리곤의 꼭짓점마다 concave인지 convex인지 확인.
    convexity_list = gen_convexity_list(grid_polygon)
    convexity_list = convexity_list[:-1]

    polygon_exterior_coords = list(grid_polygon.exterior.coords)
    polygon_exterior_coords = polygon_exterior_coords[:-1]

    new_polygon_exterior_coords = copy.deepcopy(polygon_exterior_coords)

    for i in range(len(polygon_exterior_coords)):
        # 오목한 영역: 연속된 3개의 점 a,b,c 중 a,c는 볼록한 점, b는 오목한 점이여야 한다.
        if (
            convexity_list[i] == 1
            and convexity_list[(i + 1) % len(polygon_exterior_coords)] == 0
            and convexity_list[(i + 2) % len(polygon_exterior_coords)] == 1
        ):
            # 점 a와 점 c를 이은 선분이 법규 폴리곤 내부에 포함되는지 확인한다.
            point_a = Point(polygon_exterior_coords[i])
            point_c = Point(polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)])
            diag_line = LineString([point_a, point_c])

            if regulation_polygon.contains(diag_line):

                a = np.array(polygon_exterior_coords[i])
                b = np.array(polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)])
                c = np.array(polygon_exterior_coords[(i + 2) % len(polygon_exterior_coords)])

                # 선분 ab와 선분 ac (대각선) 사이의 각도를 측정한다.
                ab = b - a
                ac = c - a

                cosine_angle = np.dot(ab, ac) / (np.linalg.norm(ab) * np.linalg.norm(ac))
                if cosine_angle > 1:
                    cosine_angle = 1
                elif cosine_angle < -1:
                    cosine_angle = -1
                angle = np.arccos(cosine_angle)
                angle = angle * 180 / np.pi
                if angle > 90:
                    angle = angle - 90
                if angle <= 45:
                    small_angle = angle
                    large_angle = 90 - angle
                else:
                    large_angle = angle
                    small_angle = 90 - angle

                # 대각화로 추가되는 영역 (직각삼각형)의 두 예각의 각도 중
                # 작은 것이 angle_min 이상, 큰 것이 angle_max 이하인 경우에만 대각화할 수 있다.
                if small_angle >= angle_min and large_angle <= angle_max:

                    # 대각선을 만들 수 있다면, 가운데 점 b를 제거한다.
                    new_polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)] = None

    new_polygon_exterior_coords = [i for i in new_polygon_exterior_coords if i]
    new_polygon_exterior_coords.append(new_polygon_exterior_coords[0])

    diagonalized_polygon = Polygon(new_polygon_exterior_coords)

    return diagonalized_polygon


def merge_diagonals(
    diagonalized_polygon: Polygon, diangonals_simplifying_angle: float, regulation_polygon: Polygon
) -> Tuple[Polygon, bool]:
    """폴리곤 도형이 diagonalized 된 이후 사선 사이의 각도가 tolerance 이하면 사선 사이를 simplify 합니다.

    Args:
        diagonalized_polygon (Polygon): diagonalize 를 통해 사선이 생성된 폴리곤.
        diangonals_simplifying_angle (float): 사선 사이를 simplify 할 떄 사용할 사이각 톨러런스. 디그리입니다.
        regulation_polygon (Polygon): 해당 층의 법규선

    Returns:
        Tuple(Polygon, bool): 사선 simplified 된 도형, simplify 가 실행되었는지, 즉 삭제된 점이 있는지 여부
    """

    # NOTE(pch): 입력 폴리곤이 비어있는 경우 아래 에러 발생
    # pyo3_runtime.PanicException: failed to get exterior ring
    if diagonalized_polygon.is_empty:
        return diagonalized_polygon

    polygon_exterior_coords = np.array(diagonalized_polygon.exterior.coords)[:-1]

    polygon_vertice_angles = angle_of_polygon_vertices(diagonalized_polygon)[:-1]

    new_polygon_exterior_coords = copy.deepcopy(polygon_exterior_coords)

    for i in range(len(polygon_exterior_coords)):
        tolerance_angle_radian = diangonals_simplifying_angle / 180 * np.pi

        # 연속한 세 점에 대해 세 점 사이의 각도를 측정한다.
        if np.pi - tolerance_angle_radian < polygon_vertice_angles[i] < np.pi + tolerance_angle_radian:
            point_a = Point(polygon_exterior_coords[(i - 1) % len(polygon_exterior_coords)])
            point_c = Point(polygon_exterior_coords[(i + 1) % len(polygon_exterior_coords)])

            diag_line = LineString([point_a, point_c])

            if regulation_polygon.contains(diag_line):
                # 대각선을 만들 수 있다면, 가운데 점을 제거한다.
                new_polygon_exterior_coords[i] = None

    new_polygon_exterior_coords = [i for i in new_polygon_exterior_coords if not np.isnan(i).all()]

    result_polygon = Polygon(new_polygon_exterior_coords)

    return result_polygon


def orient_obb(obb):
    # OBB의 4개 꼭짓점 중 y값이 가장 작은 점을 시작점으로 사용히여 폴리곤을 재구성한다.

    # 점들을 반시계방향 순서대로 정렬한다.
    obb = shapely.ops.orient(obb)

    obb_exterior_coords = list(obb.exterior.coords)[:-1]

    min_y_idx = np.argmin([Point(i).y for i in obb_exterior_coords])

    ordered_coords = []

    # 새로운 시작점부터 순서대로 추가한다.
    for i in range(len(obb_exterior_coords)):
        ordered_coords.append(obb_exterior_coords[(min_y_idx + i) % len(obb_exterior_coords)])

    # 마지막에 시작점을 다시 추가한다.
    ordered_coords.append(obb_exterior_coords[min_y_idx])

    ordered_obb = Polygon(ordered_coords)

    return ordered_obb


def get_cut_line_and_depth(obb: Polygon, cutting_policy: int, core: Polygon):
    """매스 커팅 함수에서 제거 기준선분 도출. 코어가 empty가 아닌 경우 코어와 먼 것을 선택

    Args:
        obb (Polygon): 바운딩박스
        cutting_policy (int): 커팅 방식
        core (Polygon): 코어 도형

    Raises:
        ValueError: 잘못된 커팅 방식 입력이 들어온 경우
    """

    # OBB의 점들을 y값이 가장 작은 점을 시작점으로 사용하도록 정렬한다.
    obb = orient_obb(obb)

    obb_segs = explode_to_segments(obb.boundary)

    if cutting_policy == 0:

        # 커팅 대상 선분과 커팅 깊이를 구한다.
        primary_line, opposite_line, depth_line = obb_segs[2], obb_segs[0], obb_segs[1]
        if obb_segs[1].length > obb_segs[2].length:
            primary_line, opposite_line, depth_line = obb_segs[1], obb_segs[3], obb_segs[2]

        cut_line = primary_line
        cut_depth = depth_line.length

        # 코어 도형이 입력에 있는 경우, cut_line을 코어와 멀리있는 선분을 사용하도록 변경
        if not core.is_empty:
            if opposite_line.distance(core) > cut_line.distance(core):
                cut_line = opposite_line

    elif cutting_policy == 1:

        # 커팅 대상 선분과 커팅 깊이를 구한다.
        primary_line, opposite_line, depth_line = obb_segs[2], obb_segs[0], obb_segs[1]
        if obb_segs[1].length < obb_segs[2].length:
            primary_line, opposite_line, depth_line = obb_segs[1], obb_segs[3], obb_segs[2]

        cut_line = primary_line
        cut_depth = depth_line.length

        # 코어 도형이 입력에 있는 경우, cut_line을 코어와 멀리있는 선분을 사용하도록 변경
        if not core.is_empty:
            if opposite_line.distance(core) > cut_line.distance(core):
                cut_line = opposite_line

    elif cutting_policy == 2:

        cut_line_1, cut_line_1_opposite = obb_segs[2], obb_segs[0]
        cut_line_2, cut_line_2_opposite = obb_segs[1], obb_segs[3]

        # 코어 도형이 입력에 있는 경우, cut_line을 코어와 멀리있는 선분을 사용하도록 변경
        if not core.is_empty:
            if cut_line_1.distance(core) < cut_line_1_opposite.distance(core):
                cut_line_1 = cut_line_1_opposite

            if cut_line_2.distance(core) < cut_line_2_opposite.distance(core):
                cut_line_2 = cut_line_2_opposite

        return cut_line_1, cut_line_2

    else:
        raise ValueError(f"cut_policy value is invalid: {cutting_policy}")

    return cut_line, cut_depth


def cut_north(mass_polygon, target_area):
    """target_area 를 만족할 때까지 북쪽에서 매스 폴리곤을 잘라내며 축소한다.

    Args:
        mass_polygon (Polygon): 축소 대상 매스
        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.

    Returns:
        Polygon: 축소된 매스
    """

    # 북쪽에서 폴리곤을 축소할 수 있는 최대 길이를 구한다.
    minx, miny, maxx, maxy = mass_polygon.bounds
    total_cut_length = maxy - miny

    # 이진탐색
    left = 1
    right = 100
    while left <= right:
        mid = (left + right) // 2

        # 커팅 영역에 해당하는 폴리곤을 생성한다.
        cut_area = box(minx, maxy - total_cut_length * (mid / 100), maxx, maxy)

        cut_polygon = mass_polygon.difference(cut_area)

        if cut_polygon.area > target_area:
            # 커팅을 늘려야 하는 경우
            left = mid + 1
        else:
            # 커팅을 줄여야 하는 경우
            right = mid - 1

    return cut_polygon


def cut_major(mass_polygon, obb, target_area, core=Polygon()):
    """target_area 를 만족할 때까지 OBB 장변과 평행한 선분을 사용하여 매스 폴리곤을 잘라내며 축소한다.

    Args:
        mass_polygon (Polygon): 축소 대상 매스
        obb (Polygon): mass_polygon의 바운딩 박스
        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.
        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.

    Returns:
        Polygon: 축소된 매스
    """

    cut_line, cut_depth = get_cut_line_and_depth(obb=obb, cutting_policy=0, core=core)

    # 이진탐색
    left = 1
    right = 100
    while left <= right:
        mid = (left + right) // 2

        # 커팅 영역에 해당하는 폴리곤을 생성한다.
        cut_area = offset_curve_polygon(cut_line, cut_depth * (mid / 100), "left")

        cut_polygon = mass_polygon.difference(cut_area)

        if cut_polygon.area > target_area:
            # 커팅을 늘려야 하는 경우
            left = mid + 1
        else:
            # 커팅을 줄여야 하는 경우
            right = mid - 1

    return cut_polygon


def cut_minor(mass_polygon, obb, target_area, core=Polygon()):
    """target_area 를 만족할 때까지 OBB 단변과 평행한 선분을 사용하여 매스 폴리곤을 잘라내며 축소한다.

    Args:
        mass_polygon (Polygon): 축소 대상 매스
        obb (Polygon): mass_polygon의 바운딩 박스
        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.
        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.

    Returns:
        Polygon: 축소된 매스
    """

    cut_line, cut_depth = get_cut_line_and_depth(obb=obb, cutting_policy=1, core=core)

    # 이진탐색
    left = 1
    right = 100
    while left <= right:
        mid = (left + right) // 2

        # 커팅 영역에 해당하는 폴리곤을 생성한다.
        cut_area = offset_curve_polygon(cut_line, cut_depth * (mid / 100), "left")

        cut_polygon = mass_polygon.difference(cut_area)

        if cut_polygon.area > target_area:
            # 커팅을 늘려야 하는 경우
            left = mid + 1
        else:
            # 커팅을 줄여야 하는 경우
            right = mid - 1

    return cut_polygon


def cut_diag(mass_polygon, obb, target_area, core=Polygon()):
    """target_area 를 만족할 때까지 OBB 장변 및 단변과 평행한 선분을 동시에 사용하여 매스 폴리곤을 잘라내며 축소한다.

    Args:
        mass_polygon (Polygon): 축소 대상 매스
        obb (Polygon): mass_polygon의 바운딩 박스
        target_area (float): 해당 면적 미만이 될 때까지 매스 폴리곤을 축소한다.
        core (Polygon): 코어 입력이 default가 아닌 경우 커팅용 선분을 코어와 멀리 있는 것을 사용한다.

    Returns:
        Polygon: 축소된 매스
    """

    cut_line_1, cut_line_2 = get_cut_line_and_depth(obb=obb, cutting_policy=2, core=core)

    # 이진탐색
    left = 1
    right = 100
    while left <= right:
        mid = (left + right) // 2

        # 커팅 영역에 해당하는 폴리곤을 생성한다.
        cut_area = offset_curve_polygon(cut_line_1, cut_line_2.length * (mid / 100), "left")

        cut_polygon = mass_polygon.difference(cut_area)

        cut_area = offset_curve_polygon(cut_line_2, cut_line_1.length * (mid / 100), "left")

        cut_polygon = cut_polygon.difference(cut_area)

        if cut_polygon.area > target_area:
            # 커팅을 늘려야 하는 경우
            left = mid + 1
        else:
            # 커팅을 줄여야 하는 경우
            right = mid - 1

    return cut_polygon


def bcr_cut(
    regulation_polygon,
    floor_polygon,
    obb,
    bcr,
    cut_policy,
    bcr_margin,
    is_alt_ver,
    mass_angle=None,
    is_premium=False,
    core=Polygon(),
):
    # 건폐율과 커팅 정책에 따라 1층 폴리곤의 면적을 줄인다.

    # 정해진 각도를 사용하는 최상층 깎음의 경우 mass_angle을 사용
    if mass_angle is not None:
        obb = get_rotated_bb(floor_polygon, (np.cos(mass_angle), np.sin(mass_angle)))

    # 건폐율 보정치 3%를 더한다.
    floor_area_target = regulation_polygon.area * bcr * bcr_margin

    # 알트 버전에서는 조금씩 커팅 테스트하고자 하는 경우
    if is_alt_ver:
        floor_area_target = regulation_polygon.area

    cut_polygon = floor_polygon

    if cut_polygon.area > floor_area_target or is_premium:
        if cut_policy == 0:
            cut_polygon = cut_north(floor_polygon, floor_area_target)
        elif cut_policy == 1:
            cut_polygon = cut_major(floor_polygon, obb, floor_area_target, core)
        elif cut_policy == 2:
            cut_polygon = cut_minor(floor_polygon, obb, floor_area_target, core)
        elif cut_policy == 3:
            cut_polygon = cut_diag(floor_polygon, obb, floor_area_target, core)
        else:
            raise Exception("FIXME: invaild input for cut policy")

    return cut_polygon


def far_cut(
    regulation_polygon,
    obb,
    floors,
    max_far_with_margin,
    smallest_core_area,
    cut_policy,
    min_mass_area,
    has_piloti,
    building_purpose,
    is_alt_ver,
    elev_area_for_advantage,
    use_small_core,
):
    # 1층 제외한 용적율이 법정 용적률 + 30%를 넘는 경우, 컷을 통해 용적률을 맞춘다.
    max_floors_area = regulation_polygon.area * max_far_with_margin
    # 소형 코어의 경우 2층 이상의 바닥면적을 200제곱미터로 제한한다.
    if use_small_core:
        max_floors_area = min(max_floors_area, consts.SMALL_CORE_MAX_FA)

    # 주거 용도의 건축물만 30%의 발코니 면적을 추가한다.
    if building_purpose in ("dajung", "dagagu", "dasedae"):
        max_floors_area *= 1.3

    # 지상층 코어 면적을 제거한다.
    max_floors_area = max_floors_area - smallest_core_area

    # 아래 층부터 더하면서 용적률을 초과하는 최초의 층까지 사용한다. 초과된 층은 아래에서 커팅으로 일부를 잘라낸다.
    cut_floors = []
    floors_area = 0
    invalid_area = 0
    requires_far_cut = False

    for i in range(len(floors)):
        cut_floors.append(floors[i])
        if i != 0 or not has_piloti:
            floors_area += floors[i].area - elev_area_for_advantage
        if floors_area > max_floors_area:
            invalid_area = floors_area - max_floors_area
            requires_far_cut = True
            break

    # 모든 층의 면적 합이 이미 용적률 조건 미만인 경우 early return
    if not requires_far_cut:
        return floors, True, 10000  # 임의의 큰 수

    # 최상층이 만족해야 하는 면적 조건을 구한다.
    top_floor_area_target = cut_floors[-1].area - invalid_area

    # 매스 재생성 버전의 경우, 여기서 마지막 층 커팅을 고려하지 않고 리턴합니다.
    if is_alt_ver:
        return cut_floors, False, top_floor_area_target

    # 최상층이 코어를 배치하지 못하는 영역이라면 제거한다.
    if top_floor_area_target < smallest_core_area:
        return cut_floors[:-1], None, None

    # 컷 (bcr컷과 같은 방식)을 적용하여 far을 맞춘다.
    if cut_policy == 0:
        cut_floors[-1] = cut_north(cut_floors[-1], top_floor_area_target)
    elif cut_policy == 1:
        cut_floors[-1] = cut_major(cut_floors[-1], obb, top_floor_area_target)
    elif cut_policy == 2:
        cut_floors[-1] = cut_diag(cut_floors[-1], obb, top_floor_area_target)

    # 최소 면적 14m^2 + 가장 작은 코어 면적 6.72m^2 = 20.72m^2 보다 작은 최상층이 생성되었을 경우, 해당 층을 제거한다.
    if cut_floors[-1].area < min_mass_area + 6.72:
        cut_floors = cut_floors[:-1]

    return cut_floors, None, None


def get_hard_walls(parcel, road_edges):
    """_summary_
    Args:
        parcel (Polygon): parcel polygon
        road_edges (_type_): the road edges
    Returns:
        hard walls: The walls of the plot_geom that are not road_edges
    """
    hard_walls = []
    p_coords = parcel.exterior.coords
    for p1, p2 in zip(p_coords[:-1], p_coords[1:]):
        w = LineString([p1, p2])
        if not road_edges.contains(w):
            hard_walls.append(w)

    if len(hard_walls) == 1:
        return hard_walls[0]
    else:
        return shapely.ops.linemerge(shapely.ops.unary_union(hard_walls))


def keep_exit(area, road_edge_list, width):
    """Returns areas that are accessible from the outside
    Args:
        area (MultiPolygon): areas that we want to know if they are accessible
        road_edge_list (list): The road edges
        width (float): Width of objects (ped or cars)
    Returns:
        MultiPolygon: the areas that are accessible
    """
    # Buffer the road edge with an epsilon
    road_edges = [road_edge.buffer(width + consts.EPSILON) for road_edge in road_edge_list]

    if isinstance(area, Polygon):
        area = MultiPolygon([area])

    accessible_areas = []
    for g in area.geoms:
        # Prevent to append too small geometries
        g_cleaned = buffer_erosion_and_dilation(g, width)

        for road_edge in road_edges:
            if g_cleaned.intersects(road_edge):
                accessible_areas.append(g)
                break

    # Keep only geometries that are accessible from outside of the parcel
    return MultiPolygon(accessible_areas)


def get_is_corridor_entry_failed(
    possible_core, possible_core_type, rotated_floors, floors_result, use_small_core, is_commercial_area
):
    # 코어 홀의 진입부를 확보할 수 없다면 실패
    hall = gen_core(
        [possible_core] * len(rotated_floors[: len(floors_result)]),
        possible_core_type,
        rotated_floors[: len(floors_result)],
        use_small_core,
        is_commercial_area,
        is_escape_core=False,
        is_center_core_placed=False,
        is_using_adjusted_core=False,
    )[0]
    corridor_entries_direction = [False] * len(rotated_floors[: len(floors_result)])
    corridor_entries, _ = gen_corridor_entries(
        hall, rotated_floors[: len(floors_result)], possible_core, corridor_entries_direction
    )

    # 한 층이라도 전부 empty 인 결과가 존재할 경우
    return any(all(x.is_empty for x in y) for y in corridor_entries)


def get_possible_cores_and_types(
    buffered_top_floor: Polygon,
    core_corner: np.array,
    core_size: Tuple[float],
    core_type: int,
    allow_outside: bool = False,
):

    x, y = core_corner
    core_wide, core_narr = core_size

    possible_cores = []
    possible_core_types = []

    possible_cores_candidates = [
        box(x, y, x + core_wide, y + core_narr),
        box(x, y, x + core_wide, y - core_narr),
        box(x, y, x - core_wide, y + core_narr),
        box(x, y, x - core_wide, y - core_narr),
        box(x, y, x + core_narr, y + core_wide),
        box(x, y, x - core_narr, y + core_wide),
        box(x, y, x + core_narr, y - core_wide),
        box(x, y, x - core_narr, y - core_wide),
    ]

    for possible_core_candidate in possible_cores_candidates:
        # 매스 내부에 완전히 들어온 코어 허용
        if possible_core_candidate.within(buffered_top_floor):
            possible_cores.append(possible_core_candidate)
            possible_core_types.append(core_type)

        else:
            if allow_outside:
                # 매스 내부에 90% 이상 들어온 코어 허용
                possible_core_intersection_area = possible_core_candidate.intersection(buffered_top_floor)
                if possible_core_intersection_area.area / possible_core_candidate.area >= 0.9:
                    possible_cores.append(possible_core_candidate)
                    possible_core_types.append(core_type)

    return possible_cores, possible_core_types


def place_cores(
    floors,
    mass_angle,
    tolerance,
    simple_deadspace_len,
    gridsize,
    refined_site,
    road_edge,
    is_commercial_area,
    use_small_core,
    mass_config,
    regulation,
):
    """모든 층의 변에 가장 많이 접한 코너들을 선택하여 코어 배치를 시도한다.
    해당 층에 코어를 배치하지 못한 경우, 층을 제거하고 재시도한다.

    Args:
        floors (Polygon): _description_
        cores (List(List(float, float))): 배치할 코어들의 모음 [코어 장변 길이, 코어 단변 길이]
        core_types (List[int]): 각 코어 배치 후보의 코어 타입
        mass_angle (float): 기준 바운딩 박스의 각도
        has_elevator (bool): 엘리베이터 사용 여부
        tolerance (float): 겹침 등 확인에 사용되는 tolerance값
        simple_deadspace_len (float): 데드스페이스 폭
        gridsize (float): 그리드 한 칸의 폭
        check_core_center_intersecting_mass (bool): 엘레베이터 있는 코어 긴변쪽 중심부가 매스와 닿는지 체크할지 여부
        add_core_center_as_candidates (bool): 각

    Returns:
        max_mass_core(Polygon), final_mass(List(Polygon)), core_type(int):
        결과값 코어 폴리곤, 코어 영역이 제외된 층별 매스 폴리곤, 결과 코어 타입
    """

    # 피난계단 코어가 아닌 경우, 가장 작은 코어와 비교했을 때, 장변과 단변이 모두 더 크거나 같다면 코어를 사용허지 않는다.
    if not mass_config.is_escape_core:
        valid_cores = []
        valid_core_types = []
        valid_cores.append(mass_config.core_size_list[0])
        valid_core_types.append(mass_config.core_type_list[0])
        for i in range(len(mass_config.core_size_list)):
            if i > 1:
                if (mass_config.core_size_list[i][0] < mass_config.core_size_list[0][0]) or (
                    mass_config.core_size_list[i][1] < mass_config.core_size_list[0][1]
                ):
                    valid_cores.append(mass_config.core_size_list[i])
                    valid_core_types.append(mass_config.core_type_list[i])

        mass_config.core_size_list = valid_cores
        mass_config.core_type_list = valid_core_types

    floors_result = copy.deepcopy(floors)
    # obb 기준으로 회전
    rotated_floors = [shapely.affinity.rotate(floor, -mass_angle, (0, 0), use_radians=True) for floor in floors]
    rotated_floors = [rotated_floor.simplify(consts.TOLERANCE) for rotated_floor in rotated_floors]
    rotated_regulation = [shapely.affinity.rotate(r, -mass_angle, (0, 0), use_radians=True) for r in regulation]
    idx = len(rotated_floors) - 1

    max_mass_core = None

    # 최상층 기반 코어 배치
    for rotated_top_floor in reversed(rotated_floors):
        # 코어를 배치할 코너 선택

        # 1층만 남은 경우는 코어를 배치하지 못함.
        if idx == 0:
            return [[Polygon(), floors, 0, Polygon(), 0]]

        # 회전된 top_floor의 꼭짓점 중 y값이 가장 작은 점들을 도출하여, 코어 배치에 사용한다.
        rotated_top_floor_coords = np.array(rotated_top_floor.exterior.coords)
        rotated_top_floor_coords = rotated_top_floor_coords[:-1]

        # 90도보다 작은 예각에는 코어를 배치할 수 없다.
        rotated_top_floor_angles = angle_of_polygon_vertices(rotated_top_floor)
        valid_rotated_top_floor_coords = []

        for i in range(len(rotated_top_floor_coords)):
            if not rotated_top_floor_angles[i] < np.pi / 2 * 0.999:
                valid_rotated_top_floor_coords.append(rotated_top_floor_coords[i])

        rotated_top_floor_coords = valid_rotated_top_floor_coords

        # 길이가 긴 변에 한해 중점을 후보군에 추가
        # 코어 2개소가 필요한 규모인 경우에는 두 코어간 최소 거리를 확보해야하므로 모서리에만 배치
        if mass_config.add_core_center_as_candidates and not mass_config.is_sub_core_necessary:
            shortest_core_base_len = min(min(x) for x in mass_config.core_size_list)

            top_floor_segments = explode_to_segments(rotated_top_floor.exterior)
            for top_floor_segment in top_floor_segments:
                if (
                    top_floor_segment.length
                    > consts.CORE_SEGMENT_GAP_LENGTH + shortest_core_base_len + consts.CORE_SEGMENT_GAP_LENGTH
                ):
                    rotated_top_floor_coords.append(np.array(top_floor_segment.centroid.coords[0]))

        # 모든 층의 변에 가장 많이 접한 코너에 코어 배치
        # 코너를 중심으로 만든 원이 바로 아래 층에 포함된다면 해당 코너를 사용하지 않는다.
        # 좁은 영역이 코어 주변에 닿아 있는 것을 허용하여, 코어 배치 실패를 방지합니다. 이러한 영역은 추후 데드스페이스로 제거됩니다.
        possible_core_corners = []
        floor_below = rotated_floors[idx - 1]
        floor_difference = floor_below.difference(rotated_top_floor)
        floor_difference = buffer_erosion_and_dilation(
            polygon=floor_difference,
            buffer_distance=gridsize / 2,
            use_intersection=True,
            choose_biggest_polygon=False,
        )

        possible_core_corners_segment_indices = []
        for rci, rotated_top_floor_coord in enumerate(rotated_top_floor_coords):
            checker_point = Point(rotated_top_floor_coord)
            checker = checker_point.buffer(tolerance)
            if checker.disjoint(floor_difference):
                # 아래층에 포함되는 코너만 코어 배치 후보로 사용할 수 있다.
                if not checker.disjoint(floor_below):
                    possible_core_corners.append(rotated_top_floor_coord)
                    possible_core_corners_segment_indices.append(rci)

        idx -= 1

        possible_cores = []
        possible_core_types = []
        possible_sub_cores = []
        possible_sub_core_types = []
        buffered_top_floor = rotated_top_floor.buffer(tolerance)

        rotated_top_floor_exploded = explode_to_segments(rotated_top_floor.boundary)

        # 코너 배치 후보 점에 가능한 모든 코어 배치를 시도한다.
        for core_corner, core_corner_segment_index in zip(possible_core_corners, possible_core_corners_segment_indices):

            # segment length check is already done for center cores
            if core_corner_segment_index < len(rotated_top_floor_exploded):
                core_corner_segment = rotated_top_floor_exploded[core_corner_segment_index]
                if core_corner_segment.length < consts.SIMPLE_CORE_PLACEMENT_MIN_LENGTH:
                    continue

            for core, core_type in zip(mass_config.core_size_list, mass_config.core_type_list):
                each_possible_cores, each_possible_core_types = get_possible_cores_and_types(
                    buffered_top_floor, core_corner, core, core_type
                )

                possible_cores.extend(each_possible_cores)
                possible_core_types.extend(each_possible_core_types)

                # 계단 2개소 배치 필요한 경우
                if mass_config.is_sub_core_necessary:

                    other_corner = [
                        corner for corner in rotated_top_floor_coords if not np.isclose(corner, core_corner).all()
                    ]

                    # 첫 코어가 배치된 점 기준으로 가장 먼 3개의 코너 도출
                    sorted_other_corner = sorted(
                        other_corner, key=lambda x, c=core_corner: np.linalg.norm(x - c), reverse=True
                    )

                    farthest_other_corners = sorted_other_corner[:3]
                    for farthest_other_corner in farthest_other_corners:
                        sub_core_size = mass_config.sub_core_size_list[core_type - 1]

                        # 매스 바깥으로 약간 튀어나간 서브코어 허용
                        each_possible_sub_cores, each_possible_sub_core_types = get_possible_cores_and_types(
                            buffered_top_floor, farthest_other_corner, sub_core_size, core_type, allow_outside=True
                        )

                        filtered_each_possible_sub_cores = []
                        filtered_each_possible_sub_core_types = []

                        # regulation boundary 내부에 있는 것들만 필터
                        for each_possible_sub_core, each_possible_sub_core_type in zip(
                            each_possible_sub_cores, each_possible_sub_core_types
                        ):
                            if each_possible_sub_core.within(rotated_regulation[idx].buffer(consts.TOLERANCE)):
                                filtered_each_possible_sub_cores.append(each_possible_sub_core)
                                filtered_each_possible_sub_core_types.append(each_possible_sub_core_type)

                        possible_sub_cores.extend(filtered_each_possible_sub_cores)
                        possible_sub_core_types.extend(filtered_each_possible_sub_core_types)

        valid_cores_and_mass = []
        # 매스 데드스페이스 조건, 매스 최소폭 조건을 확인한다.
        for possible_core, possible_core_type in zip(possible_cores, possible_core_types):
            is_core_valid = True

            selected_possible_sub_core = Polygon()
            selected_possible_sub_core_type = None

            for each_floor in rotated_floors[: len(floors_result)]:
                mass = make_floor_mass_after_core(
                    each_floor,
                    shapely.ops.unary_union([possible_core, selected_possible_sub_core]),
                    simple_deadspace_len,
                    use_simplify=False,
                )

                if not is_core_valid:
                    break

                # 코어와 매스가 점으로 만나서는 안된다.
                # 코어를 제외한 매스 폴리곤을 버퍼하였을 때 interior가 있는 경우는 사용할 수 없다.
                mass_interior_check = mass.buffer(consts.TOLERANCE_MARGIN, join_style=JOIN_STYLE.mitre)
                if len(list(mass_interior_check.interiors)) != 0:
                    is_core_valid = False
                    break

                # 데드스페이스 처리한 이후의 매스가 코어와 접하지 않으면 해당 코어는 사용하지 못하는 것으로 처리
                if mass.disjoint(possible_core.buffer(consts.TOLERANCE_MARGIN, join_style=JOIN_STYLE.mitre)):
                    is_core_valid = False
                    break

                # 최소 면적 조건 확인
                if mass.area < mass_config.min_mass_area:
                    is_core_valid = False
                    break

                # 최소폭 조건 확인
                minx, miny, maxx, maxy = mass.bounds
                if maxx - minx < mass_config.min_mass_width or maxy - miny < mass_config.min_mass_width:
                    is_core_valid = False
                    break

                # 엘리베이터 있는 코어의 경우, 코어의 중점이 매스와 닿아 있어야 함. - 스위치 추가
                if mass_config.has_elevator and not is_elev_core_mass_connection_valid(
                    possible_core, mass, tolerance, mass_config.check_core_center_intersecting_mass
                ):
                    is_core_valid = False
                    break

            # If the core is not valid, go straight to next core, don't check for paths problems
            if not is_core_valid:
                continue

            # 한 층이라도 corridor entry 생성에 실패한 경우
            if get_is_corridor_entry_failed(
                possible_core,
                possible_core_type,
                rotated_floors,
                floors_result,
                use_small_core,
                is_commercial_area,
            ):
                continue

            # Prevents core from creating unaccessible areas
            possible_core = shapely.affinity.rotate(possible_core, mass_angle, (0, 0), use_radians=True)
            selected_possible_sub_core = shapely.affinity.rotate(
                selected_possible_sub_core, mass_angle, (0, 0), use_radians=True
            )

            # Check that the core does not prevent cars from entering
            # Find the edges that are not road edge
            hard_walls = get_hard_walls(refined_site, road_edge)
            hard_walls = hard_walls if isinstance(hard_walls, MultiLineString) else MultiLineString([hard_walls])

            # Concatenates all obstacles
            core_obstacles = shapely.ops.unary_union([*hard_walls.geoms, possible_core, selected_possible_sub_core])

            # Accessible areas without the core
            car_accessible_area_without_core = refined_site.convex_hull.difference(
                hard_walls.buffer(consts.VEHICLE_ROAD_WIDTH / 2, join_style=2)
            ).intersection(refined_site)
            car_accessible_area_without_core = keep_exit(
                car_accessible_area_without_core, road_edge.geoms, consts.VEHICLE_ROAD_WIDTH / 2
            )
            # Number of accessible area before the core is placed
            car_accessible_area_without_core_count = (
                1
                if car_accessible_area_without_core.geom_type == "Polygon"
                else len(car_accessible_area_without_core.geoms)
            )

            # Buffer the obstacles
            car_buff_obstacles = core_obstacles.buffer(consts.VEHICLE_ROAD_WIDTH / 2, join_style=2)
            # Compute the pedestrian accessible area
            car_accessible_area = refined_site.convex_hull.difference(car_buff_obstacles).intersection(refined_site)

            #  Only keep geometries accessible from the outside
            car_accessible_area = keep_exit(car_accessible_area, road_edge.geoms, consts.VEHICLE_ROAD_WIDTH / 2)
            # Number of area where a car can go from the outside of the parcel
            accessible_area_with_exit_count = (
                1 if car_accessible_area.geom_type == "Polygon" else len(car_accessible_area.geoms)
            )
            # If we lose an accessible area, we reject the core
            if car_accessible_area_without_core_count != accessible_area_with_exit_count:
                continue

            valid_cores_and_mass.append(
                [possible_core, mass, possible_core_type, selected_possible_sub_core, selected_possible_sub_core_type]
            )

        # 코어 배치에 실패한 경우
        if len(valid_cores_and_mass) == 0:
            floors_result = floors_result[:-1]
            continue

        (
            max_mass_core,
            _,
            max_mass_core_type,
            selected_possible_sub_core,
            selected_possible_sub_core_type,
        ) = valid_cores_and_mass[np.argmax([x[1].area for x in valid_cores_and_mass])]

        break

    if max_mass_core is None:
        raise ConstructionError("코어 배치에 실패하였습니다.")

    # 가장 좋은 후보 최대 n개를 사용
    sorted_valid_cores_and_mass = sorted(valid_cores_and_mass, key=lambda x: x[1].area, reverse=True)[
        : consts.LIGHT_GET_MASS_CORE_TRIALS_MAX_NUM
    ]

    place_cores_results = []
    for each_valid_core_and_mass in sorted_valid_cores_and_mass:

        (
            max_mass_core,
            _,
            max_mass_core_type,
            selected_possible_sub_core,
            selected_possible_sub_core_type,
        ) = each_valid_core_and_mass

        final_mass = []
        for floor in floors_result:
            mass = make_floor_mass_after_core(floor, max_mass_core, simple_deadspace_len)

            if mass_config.is_sub_core_necessary:
                mass = make_floor_mass_after_core(mass, selected_possible_sub_core, simple_deadspace_len)

            final_mass.append(mass)

        place_cores_results.append(
            [max_mass_core, final_mass, max_mass_core_type, selected_possible_sub_core, selected_possible_sub_core_type]
        )

    return place_cores_results


def is_elev_core_mass_connection_valid(core, mass, tolerance, check_core_center_intersecting_mass):
    # 엘리베이터 있는 코어의 경우, 코어의 중점이 매스와 닿아 있어야 함. - 스위치 추가

    core_segs = explode_to_segments(core.boundary)
    sorted_core_segs = sorted(core_segs, key=lambda x: x.length, reverse=True)

    # check_core_center_intersecting_mass 가 True 일 때만 장변쪽 체크
    if check_core_center_intersecting_mass:
        if sorted_core_segs[0].centroid.buffer(tolerance).disjoint(mass) and sorted_core_segs[1].centroid.buffer(
            tolerance
        ).disjoint(mass):
            return False
    else:
        if all(sorted_core_seg.centroid.buffer(tolerance).disjoint(mass) for sorted_core_seg in sorted_core_segs):
            return False

    return True


def make_floor_mass_after_core(floor, core, simple_deadspace_len, use_simplify=True):

    mass = floor.difference(core)
    # 매스 축소
    buffered_mass = mass.buffer(-simple_deadspace_len / 2, join_style=JOIN_STYLE.mitre)
    # 멀티폴리곤 제거
    buffered_mass = filter_polygon(buffered_mass)
    # 매스 확장
    mass = buffered_mass.buffer(simple_deadspace_len / 2, join_style=JOIN_STYLE.mitre).intersection(mass)
    mass = filter_polygon(mass)
    if use_simplify:
        mass = simplify_polygon(mass, tol_length=consts.TOLERANCE)

    return mass


def get_mass_each_floor(
    archi_line: Polygon,
    each_floor_regulation: Polygon,
    preset: List[int],
    mass_cut_length: float,
    gridsize: float,
    tolerance: float,
    tolerance_angle: float,
    diangonals_simplifying_angle: float,
    angle_min: float,
    angle_max: float,
    pack_after_cut: bool,
    time_counter_dict: dict,
    preset_mass_dict: dict,
    mass_angle: float = None,
    mass_cut_depth_divider: float = 1.0,
    fill_gap: bool = True,
    regulation_bounds: Tuple[float] = None,
    emboss_cut_policy: int = 0,
    use_emboss_cut_length_sorting: bool = False,
    longest_length_baseline: float = None,
    shortest_length_baseline: float = None,
) -> Tuple[Polygon, List[Polygon], Polygon, float]:
    """매스를 한층만 생성합나디. 변화하는

    Args:
        archi_line (Polygon):
        preset (List[int]): _description_
        mass_cut_length (float): _description_
        gridsize (float): _description_
        tolerance (float): _description_
        diangonals_simplifying_angle (float): _description_
        bounding_box (Polygon): 특정 매스 각도로 생성하고 싶을 경우 mass angle 과 같이 넘겨줍니다..
        preset_mass_dict (dict): 같은 프리셋으로 알 수 있는 매스는 공유하기 위한 dict
        mass_angle (flooat): 특정 매스 각도로 생성하고 싶을 경우 사용합니다.

    Raises:
        Exception: _description_

    Returns:
        Tuple[Polygon, List[Polygon], Polygon, float]: _description_
    """

    # 필지 축 선택 (바운딩 박스 생성 및 mass_angle 결정)
    bounding_box: Polygon
    mass_angle: float

    if mass_angle is not None:
        # 정해진 bounding box 와 mass_angle 을 사용하고 싶을 경우 그대로 사용
        bounding_box = get_rotated_bb(each_floor_regulation, (np.cos(mass_angle), np.sin(mass_angle)))
    elif preset.bounding_box_config == 0:
        # 장변 기준 바운딩 박스 및 축 설정
        bounding_box, mass_angle = gen_obb_from_longest_segment(each_floor_regulation)
    elif preset.bounding_box_config == 1:
        # obb 기준 바운딩 박스 및 축 설정
        bounding_box, mass_angle = gen_obb_from_convex_hull(each_floor_regulation)
    else:
        raise Exception("FIXME: invaild input for bounding box creation")

    # 앞서 실행된 결과가 있다면 이를 활용
    preset_mass_key = (mass_angle, each_floor_regulation.wkt)
    result_set = preset_mass_dict.get(preset_mass_key)
    if result_set is not None:
        mass_polygon_wkt, intermediate_results = result_set
        mass_polygon = wkt.loads(mass_polygon_wkt)
    else:
        # 중간 결과 저장
        intermediate_results = []

        # 그리드 폴리곤 생성 (법규 내부에 포함된 그리드 셀로 매스 생성)
        mass_polygon = gen_grid_polygon(
            each_floor_regulation, mass_angle, gridsize, tolerance, time_counter_dict, regulation_bounds
        )
        intermediate_results.append(mass_polygon)  # 그리드 폴리곤 생성 결과 1층 매스

        if fill_gap:
            # 그리드 생성 이후 매스가 파이는 경우가 있으므로 gridsize 만큼 확장 및 축소 연산 실행
            possible_mass_polygon = simplify_polygon(buffer_dilation_and_erosion(mass_polygon, gridsize))

            # check if mass in contained inside regulation
            if each_floor_regulation.contains(possible_mass_polygon):
                mass_polygon = possible_mass_polygon

        # 1차 럼프 컷, 엠보스 컷
        mass_polygon = cut_extrude(mass_polygon, gridsize * 10000, mass_cut_length, tolerance, time_counter_dict)
        intermediate_results.append(mass_polygon)  # 럼프컷 결과 1층 매스

        mass_polygon = cut_emboss(
            mass_polygon,
            mass_cut_length,
            emboss_cut_policy,
            time_counter_dict,
            False,
            tolerance_angle,
            mass_cut_depth_divider=mass_cut_depth_divider,
            use_emboss_cut_length_sorting=use_emboss_cut_length_sorting,
            longest_length_baseline=longest_length_baseline,
            shortest_length_baseline=shortest_length_baseline,
        )
        intermediate_results.append(mass_polygon)  # 엠보스 컷 결과 1층 매스

        # 2차 럼프 컷, 엠보스 컷 (1칸짜리 삭제)
        mass_polygon = cut_extrude(mass_polygon, gridsize + tolerance, gridsize * 10000, tolerance, time_counter_dict)
        mass_polygon = cut_emboss(
            mass_polygon,
            gridsize + tolerance,
            1,
            time_counter_dict,
            False,
            tolerance_angle,
            mass_cut_depth_divider=mass_cut_depth_divider,
        )
        intermediate_results.append(mass_polygon)  # 1칸짜리 피쳐 제거 결과 1층 매스
        preset_mass_dict[preset_mass_key] = (mass_polygon.wkt, intermediate_results)

    start_pack = time.process_time()

    # far_cut 수행시간 합산
    time.process_time() - start_pack

    # 해당 시점에 사선이 생기면 안됩니다.
    no_diagonals_before_diagonalize(mass_polygon)

    if preset.diagonalize_config == 1:
        # 대각화 실행
        # 커팅 정책 0: 북쪽, 1: 장변, 2: 단변, 3: 대각선
        mass_polygon = diagonalize(each_floor_regulation, mass_polygon, angle_min, angle_max)
        mass_polygon = merge_diagonals(mass_polygon, diangonals_simplifying_angle, each_floor_regulation)

    # prevent invalid polygons
    mass_polygon = mass_polygon.buffer(0)

    intermediate_results.append(mass_polygon)  # 대각화 결과 1층 매스. 대각화하지 않는 경우 이전과 동일
    return mass_polygon, intermediate_results, bounding_box, mass_angle


def make_first_mass(
    archi_line,
    regulation,
    preset,
    mass_cut_length,
    gridsize,
    tolerance,
    time_counter_dict,
    preset_mass_dict,
    bcr,
    mass_config,
):
    if not mass_config.is_alt_ver:
        first_mass_polygon, intermediate_results, bounding_box, mass_angle = get_mass_each_floor(
            archi_line,
            regulation[0],
            preset,
            mass_cut_length,
            gridsize,
            tolerance,
            mass_config.tolerance_angle,
            mass_config.diangonals_simplifying_angle,
            mass_config.angle_min,
            mass_config.angle_max,
            mass_config.pack_after_cut,
            time_counter_dict,
            preset_mass_dict,
            mass_cut_depth_divider=mass_config.mass_cut_depth_divider,
            emboss_cut_policy=mass_config.emboss_cut_policy,
            use_emboss_cut_length_sorting=mass_config.use_emboss_cut_length_sorting,
            longest_length_baseline=mass_config.longest_length_baseline,
            shortest_length_baseline=mass_config.shortest_length_baseline,
        )

        # 건폐율을 맞출 때까지 커팅 실행
        first_mass_polygon = bcr_cut(
            archi_line,
            first_mass_polygon,
            bounding_box,
            bcr,
            preset.cutting_policy_config,
            mass_config.bcr_margin,
            mass_config.is_alt_ver,
        )
    else:
        regulation_cut = regulation[:]

        # NOTE: 1층에서 건폐율 먼저 맞추기
        target_area_reduce_num = 0
        while True:
            first_mass_polygon, intermediate_results, bounding_box, mass_angle = get_mass_each_floor(
                archi_line,
                regulation_cut[0],
                preset,
                mass_cut_length,
                gridsize,
                tolerance,
                mass_config.tolerance_angle,
                mass_config.diangonals_simplifying_angle,
                mass_config.angle_min,
                mass_config.angle_max,
                mass_config.pack_after_cut,
                time_counter_dict,
                preset_mass_dict,
                mass_cut_depth_divider=mass_config.mass_cut_depth_divider,
                emboss_cut_policy=mass_config.emboss_cut_policy,
                use_emboss_cut_length_sorting=mass_config.use_emboss_cut_length_sorting,
                longest_length_baseline=mass_config.longest_length_baseline,
                shortest_length_baseline=mass_config.shortest_length_baseline,
            )
            if (
                first_mass_polygon.area <= archi_line.area * bcr * mass_config.bcr_margin
                or target_area_reduce_num > int(1 / consts.SIMPLE_REDUCE_RATIO_INTERVAL)
            ):
                break
            else:
                target_area_reduce_num += 1
                archi_line_for_target_area = shapely.affinity.scale(
                    archi_line, (1 - target_area_reduce_num * consts.SIMPLE_REDUCE_RATIO_INTERVAL)
                )

                regulation_cut[0] = bcr_cut(
                    archi_line_for_target_area,
                    regulation_cut[0],
                    bounding_box,
                    bcr,
                    preset.cutting_policy_config,
                    mass_config.bcr_margin,
                    mass_config.is_alt_ver,
                )

                regulation_cut[0] = filter_polygon(regulation_cut[0])

        regulation_cut[1:] = [r.intersection(regulation_cut[0]) for r in regulation_cut[1:]]
        regulation_cut[1:] = [filter_polygon(r) for r in regulation_cut[1:]]
        regulation_cut = list(filter(lambda x: not x.is_empty, regulation_cut))

        mass = [first_mass_polygon]

        regulation_bounds = None
        if mass_config.use_same_grid:
            regulation_bounds = get_regulation_bounds(regulation_cut, mass_angle)

        for each_floor_regulation in regulation_cut[1:]:

            try:
                each_mass_polygon, _, _, _ = get_mass_each_floor(
                    archi_line,
                    each_floor_regulation,
                    preset,
                    mass_cut_length,
                    gridsize,
                    tolerance,
                    mass_config.tolerance_angle,
                    mass_config.diangonals_simplifying_angle,
                    mass_config.angle_min,
                    mass_config.angle_max,
                    mass_config.pack_after_cut,
                    time_counter_dict,
                    preset_mass_dict,
                    mass_angle,
                    mass_cut_depth_divider=mass_config.mass_cut_depth_divider,
                    regulation_bounds=regulation_bounds,
                    emboss_cut_policy=mass_config.emboss_cut_policy,
                    use_emboss_cut_length_sorting=mass_config.use_emboss_cut_length_sorting,
                    longest_length_baseline=mass_config.longest_length_baseline,
                    shortest_length_baseline=mass_config.shortest_length_baseline,
                )

                mass.append(each_mass_polygon)
            except Exception:  # pylint: disable=broad-except
                # 최상층 부근에서 실패하는 경우가 많음.
                pass

    return mass, first_mass_polygon, intermediate_results, bounding_box, mass_angle, regulation_cut, regulation_bounds


def cut_mass_far(
    archi_line,
    bounding_box,
    mass,
    max_far_with_margin,
    smallest_core_area,
    preset,
    has_piloti,
    building_purpose,
    regulation_cut,
    mass_angle,
    mass_cut_length,
    gridsize,
    tolerance,
    time_counter_dict,
    preset_mass_dict,
    regulation_bounds,
    mass_config,
    elev_area_for_advantage,
    use_small_core,
):

    # 용적률 컷 이전에 데드스페이스 한 번 제거
    # 여기서 한 번 제거해주지 않으면 데드스페이스 면적까지 용적률에 잡혀서 로스가 많이 생김
    mass_deadspace_cutted = []
    for each_mass in mass:
        deadspace_cutted = buffer_erosion_and_dilation(each_mass, mass_config.simple_deadspace_len)

        # 빈 층이 발생하면 그 이후는 모두 제거
        if deadspace_cutted.is_empty:
            break
        else:
            mass_deadspace_cutted.append(deadspace_cutted)

    mass = mass_deadspace_cutted

    mass, is_far_satisfied, top_floor_area_target = far_cut(
        archi_line,
        bounding_box,
        mass,
        max_far_with_margin,
        smallest_core_area,
        preset.cutting_policy_config,
        mass_config.min_mass_area,
        has_piloti,
        building_purpose,
        mass_config.is_alt_ver,
        elev_area_for_advantage,
        use_small_core,
    )

    if mass_config.is_alt_ver and not is_far_satisfied:
        # 용적률 컷 - 마지막 층 자르기
        last_floor_regulation_cut = regulation_cut[len(mass) - 1]
        left = 1  # 커팅이 필요한 경우이므로 최소 커팅 횟수는 1회
        right = (1 / consts.SIMPLE_REDUCE_RATIO_INTERVAL) - 1  # 최대 커팅 횟수. 100% 커팅은 의미가 없으므로 -1

        try:
            # 그리고 이 과정에서 잘못될 경우 마지막 층 삭제
            while True:

                if left < right:
                    mid = (left + right) // 2
                else:
                    # 이진탐색 결과 용적률이 목표보다 더 크게 나오는 경우
                    # 커팅을 한 칸 늘린다.
                    if mass[-1].area > top_floor_area_target:
                        mid = mid + 1
                    else:
                        break

                last_floor_regulation_cut_for_target_area = shapely.affinity.scale(
                    last_floor_regulation_cut,
                    (1 - mid * consts.SIMPLE_REDUCE_RATIO_INTERVAL),
                )

                regulation_cut_temp = bcr_cut(
                    last_floor_regulation_cut_for_target_area,
                    regulation_cut[len(mass) - 1],
                    bounding_box,
                    0,
                    preset.cutting_policy_config,
                    0,
                    mass_config.is_alt_ver,
                    mass_angle,
                )

                regulation_cut_temp = filter_polygon(regulation_cut_temp)

                mass[-1], _, _, _ = get_mass_each_floor(
                    archi_line,
                    regulation_cut_temp,
                    preset,
                    mass_cut_length,
                    gridsize,
                    tolerance,
                    mass_config.tolerance_angle,
                    mass_config.diangonals_simplifying_angle,
                    mass_config.angle_min,
                    mass_config.angle_max,
                    mass_config.pack_after_cut,
                    time_counter_dict,
                    preset_mass_dict,
                    mass_angle,
                    mass_cut_depth_divider=mass_config.mass_cut_depth_divider,
                    regulation_bounds=regulation_bounds,
                )

                if mass[-1].area > top_floor_area_target:
                    # 커팅을 늘려야 하는 경우
                    left = mid + 1
                else:
                    # 커팅을 줄여야 하는 경우
                    right = mid - 1

            regulation_cut[len(mass) - 1] = regulation_cut_temp

        except Exception:  # pylint: disable=broad-except
            pass

        # 충분히 커팅되지 않았을 경우 제거합니다.
        if mass[-1].area > top_floor_area_target:
            mass = mass[:-1]

        # 최상층이 코어를 배치하지 못하는 영역이라면 제거한다.
        elif top_floor_area_target < smallest_core_area:
            mass = mass[:-1]

        # 최소 면적 14m^2 + 가장 작은 코어 면적 6.72m^2 = 20.72m^2 보다 작은 최상층이 생성되었을 경우, 해당 층을 제거한다.
        elif mass[-1].area < mass_config.min_mass_area + smallest_core_area:
            mass = mass[:-1]

    return mass


def core_placement(
    mass,
    mass_angle,
    tolerance,
    engine_type,
    gridsize,
    refined_site,
    road_edge,
    is_commercial_area,
    use_small_core,
    has_piloti,
    archi_line,
    regulation,
    max_far_with_margin,
    bcr,
    mass_config,
):
    # 최상층 기준 코어 배치
    place_cores_results = place_cores(
        mass,
        mass_angle,
        tolerance,
        mass_config.simple_deadspace_len if engine_type == consts.ENGINE_TYPE_LIGHT else consts.TOLERANCE,
        gridsize,
        refined_site,
        MultiLineString([r["edge_geom"] for r in road_edge["edges"]]),
        is_commercial_area,
        use_small_core,
        mass_config,
        regulation,
    )

    core_placement_results = []
    for each_place_cores_result in place_cores_results:
        # pylint: disable=unbalanced-tuple-unpacking
        core, mass, core_type, sub_core, sub_core_type = each_place_cores_result
        # pylint: enable=unbalanced-tuple-unpacking

        if core.is_empty:
            continue

        # 필로티일 경우에는 packing 시 사용할 면적 계산을 위해 1층을 비워줍니다.
        if has_piloti:
            packed_unit_space_for_pack = [[Polygon()]] + [[each_floor_mass] for each_floor_mass in mass[1:]]
        else:
            packed_unit_space_for_pack = [[each_floor_mass] for each_floor_mass in mass]

        # 뒤에서 1층 매스를 대체하지만, 이 위치에서는 1층 필로티 정보를 주차 체크시 전달해줄 필요가 있음
        mass_after_pack = packed_unit_space_for_pack

        hall_list, stair_list, elev_list, core_list, _, _, close_seg, _, long_core_segs = gen_core(
            [core],
            core_type,
            mass,
            use_small_core,
            is_commercial_area,
            is_escape_core=mass_config.is_escape_core,
            is_center_core_placed=False,
            is_using_adjusted_core=False,
            is_last_gen_core_called=True,
        )

        core_orientation = LineString(np.array(close_seg[0].coords)).wkt

        # 피난계단 코어의 보이드 부분을 매스에 포함시킴
        if mass_config.is_escape_core:
            escape_core_void = buffer_erosion_and_dilation(core - core_list[0], consts.TOLERANCE_MARGIN)

            if not escape_core_void.is_empty:
                erosion_distance = min(explode_to_segments(escape_core_void.exterior), key=lambda s: s.length).length
                erosion_distance += consts.TOLERANCE_MARGIN
                erosion_distance /= 2

                for mi, m in enumerate(mass):
                    mass_with_void = buffer_dilation_and_erosion(
                        shapely.ops.unary_union([m, escape_core_void]), consts.TOLERANCE_MARGIN
                    )
                    mass_with_void = buffer_erosion_and_dilation(mass_with_void, erosion_distance)

                    mass[mi] = mass_with_void

                for mi, m in enumerate(mass_after_pack):
                    mass_with_void = buffer_dilation_and_erosion(
                        shapely.ops.unary_union([m[0], escape_core_void]), consts.TOLERANCE_MARGIN
                    )
                    mass_with_void = buffer_erosion_and_dilation(mass_with_void, erosion_distance)

                    mass_after_pack[mi][0] = mass_with_void

                core = core_list[0]

        sub_core_placement_result = [
            mass,
            mass_after_pack,
            [Polygon()],
            [Polygon()],
            [Polygon()],
            [Polygon()],
            [Polygon()],
            [Polygon()],
            Polygon(),
            LineString().wkt,
            None,
            None,
        ]

        if mass_config.is_sub_core_necessary:

            (
                sub_hall_list,
                sub_stair_list,
                sub_elev_list,
                sub_core_list,
                sub_core_attached_room_list,
                sub_core_emergency_elev_list,
                sub_close_seg,
                _,
                sub_long_core_segs,
            ) = gen_core(
                [sub_core],
                sub_core_type,
                mass,
                use_small_core,
                is_commercial_area,
                is_escape_core=mass_config.is_escape_core,
                is_center_core_placed=False,
                is_using_adjusted_core=False,
                is_specific_escape_sub_core=mass_config.is_specific_escape_sub_core,
                is_specific_escape_emgcy_elev_sub_core=mass_config.is_specific_escape_emgcy_elev_sub_core,
                is_last_gen_core_called=True,
            )

            sub_core_orientation = LineString(np.array(sub_close_seg[0].coords)).wkt

            sub_core_placement_result = [
                mass,
                mass_after_pack,
                sub_hall_list,
                sub_stair_list,
                sub_elev_list,
                sub_core_list,
                sub_core_attached_room_list,
                sub_core_emergency_elev_list,
                sub_core,
                sub_core_orientation,
                sub_core_type,
                sub_long_core_segs,
            ]

        core_placement_result = [
            mass,
            mass_after_pack,
            hall_list,
            stair_list,
            elev_list,
            [Polygon()],
            [Polygon()],
            core_list,
            core,
            core_orientation,
            core_type,
            long_core_segs,
        ]

        assert len(core_placement_result) == len(sub_core_placement_result)

        core_placement_results.append([core_placement_result, sub_core_placement_result])

    return core_placement_results


def adjust_mass_by_laws(
    mass_for_parklot_check: List[List[Polygon]],
    law_parklot_count: int,
    estimated_parklot_count: int,
    parklot_datas: List,
    underground_parking_boundaries: List[Polygon],
    regulation_cut: List[Polygon],
    bounding_box: Polygon,
    mass_generation_preset,
    mass_config,
    mass_angle: float,
    core: Polygon,
    hall_geom: Polygon,
    stair_geom: Polygon,
    elev_geom: Polygon,
    archi_line: Polygon,
    time_counter_dict: dict,
    preset_mass_dict: dict,
    regulation_bounds: List[float],
    engine_type: str,
    building_purpose: str,
    parking_commercial: dict,
    commercial_type: int,
    first_floor_reduce_area: float,
    has_piloti: bool,
    packed_unit_space_area_test_set_index: int,
    packed_unit_space_equal_division: int,
    packed_unit_space_sequantial: int,
    res,
    env_plan,
):

    target_area_reduce_num = 0
    buffered_core = core.buffer(consts.TOLERANCE_MACRO, join_style=JOIN_STYLE.mitre)
    last_floor_regulation_cut = regulation_cut[len(mass_for_parklot_check) - 1]

    is_sub_core_necessary = False

    mass_config.is_sub_core_necessary = is_sub_core_necessary

    core_count = len(polygon_or_multipolygon_to_list_of_polygon(core))

    # 다음 조건을 만족하지 못하면 층 제거
    # - 법정 주차대수를 만족하지 못하는 경우 제거
    # - 코어 2개소가 필요한 규모이지만 코어가 한 개 밖에 없는 경우 2개소가 필요하지 않은 규모까지 제거
    # - 다중, 다가구의 세대 수가 19세대를 초과하는 경우 제거(다중은 취사실 제외하고 19세대)

    max_households_num = np.inf
    if building_purpose == "dagagu":
        max_households_num = consts.MAX_HOUSEHOLDS_NUM_DAGAGU
    elif building_purpose == "dajung":
        max_households_num = consts.MAX_HOUSEHOLDS_NUM_DAJUNG

    while (
        (law_parklot_count > estimated_parklot_count)
        or (mass_config.is_sub_core_necessary and core_count == 1)
        or (
            building_purpose in ("dajung", "dagagu")
            and len([u for p in env_plan.packed_unit_space for u in p if not u.is_empty]) > max_households_num
        )
    ):

        if len(mass_for_parklot_check) <= 3:
            break

        last_floor_mass_before_cut = mass_for_parklot_check[-1][:]

        target_area_reduce_num += 1

        # 계산 결과 주차가 부족할 경우 추가 매스 깎음이 필요합니다.
        last_floor_regulation_cut_for_target_area = shapely.affinity.scale(
            last_floor_regulation_cut, (1 - target_area_reduce_num * consts.SIMPLE_REDUCE_RATIO_INTERVAL)
        )

        regulation_cut[len(mass_for_parklot_check) - 1] = bcr_cut(
            last_floor_regulation_cut_for_target_area,
            regulation_cut[len(mass_for_parklot_check) - 1],
            bounding_box,
            0,
            mass_generation_preset.cutting_policy_config,
            0,
            is_alt_ver=True,
            mass_angle=mass_angle,
            core=core,
        )

        regulation_cut[len(mass_for_parklot_check) - 1] = filter_polygon(
            regulation_cut[len(mass_for_parklot_check) - 1]
        )

        # 추가로 커팅한 법규선을 이용해 해당 층 폴리곤 생성
        last_floor_mass, _, _, _ = get_mass_each_floor(
            archi_line,
            regulation_cut[len(mass_for_parklot_check) - 1],
            mass_generation_preset,
            mass_generation_preset.mass_cut_length,
            mass_generation_preset.gridsize,
            mass_generation_preset.tolerance,
            mass_config.tolerance_angle,
            mass_config.diangonals_simplifying_angle,
            mass_config.angle_min,
            mass_config.angle_max,
            mass_config.pack_after_cut,
            time_counter_dict,
            preset_mass_dict,
            mass_angle,
            mass_cut_depth_divider=mass_config.mass_cut_depth_divider,
            regulation_bounds=regulation_bounds,
        )

        last_floor_mass = make_floor_mass_after_core(
            last_floor_mass,
            core,
            mass_config.simple_deadspace_len if engine_type == consts.ENGINE_TYPE_LIGHT else consts.TOLERANCE,
        )

        mass_for_parklot_check[-1] = [last_floor_mass]

        # 최소 면적 14m^2 + 가장 작은 코어 면적 6.72m^2 = 20.72m^2 보다 작은 최상층이 생성되었을 경우
        # 해당 층을 제거한다.

        core_iter = [core]
        if isinstance(core, MultiPolygon):
            core_iter = core.geoms

        entry_secured = True
        for c in core_iter:
            if not is_entry_secured_between_geoms(last_floor_mass, c, consts.UNITENTRY_MIN_WIDTH):
                entry_secured = False
                break

        elev_connection_valid = True
        if mass_config.has_elevator:
            for c in core_iter:
                if not is_elev_core_mass_connection_valid(
                    c,
                    last_floor_mass,
                    mass_generation_preset.tolerance,
                    mass_config.check_core_center_intersecting_mass,
                ):
                    elev_connection_valid = False
                    break

        if (
            last_floor_mass.area < mass_config.min_mass_area
            or target_area_reduce_num >= int(1 / consts.SIMPLE_REDUCE_RATIO_INTERVAL)
            or buffered_core.disjoint(last_floor_mass)
            or not entry_secured
            or (mass_config.has_elevator and not elev_connection_valid)
            or (  # 근생, 판매 업무의 경우 주차 차이가 층의 면적에 비해 매우 클 경우 층을 바로 날린다.
                consts.BUILDING_PURPOSE_MAP[building_purpose] >= 3
                and (law_parklot_count - estimated_parklot_count) * consts.PARKING_AREA_DIVISOR
                > sum(x.area for x in last_floor_mass_before_cut)
            )
        ):
            mass_for_parklot_check = mass_for_parklot_check[:-1]
            last_floor_regulation_cut = regulation_cut[len(mass_for_parklot_check) - 1]
            target_area_reduce_num = 0

            if commercial_type > 0:
                env_plan.commercial_type = max(
                    env_plan.commercial_type - 1, consts.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN + int(has_piloti)
                )

        packed_unit_space_equal_division, packed_unit_space_sequantial = mass_for_parklot_check, mass_for_parklot_check

        # 층수가 변경되었을 수 있어 core 및 다른 요소도 재정의
        env_plan.packed_unit_space = packed_unit_space_equal_division

        # 근생의 경우에는 commercial_type 을 전층으로 지정해줘야 함
        if consts.BUILDING_PURPOSE_MAP[building_purpose] in ["geunsaeng"]:
            env_plan.commercial_type = len(packed_unit_space_equal_division)

        law_parklot_count_equal_division = env_plan.law_parklot_count

        # 다른 건 동일. 세대만 갈아 끼워서 확인.
        env_plan.packed_unit_space = packed_unit_space_sequantial
        law_parklot_count_sequantial = env_plan.law_parklot_count

        # 법정 주차 대수는 둘 중에 작은 것으로 사용
        if law_parklot_count_equal_division <= law_parklot_count_sequantial:
            law_parklot_count = law_parklot_count_equal_division
            packed_unit_space_area_test_set_index = 0
        else:
            law_parklot_count = law_parklot_count_sequantial
            packed_unit_space_area_test_set_index = 1

        # 규모 변경하는 루프마다 is_sub_core_necessary 업데이트
        is_sub_core_necessary = False

        mass_config.is_sub_core_necessary = is_sub_core_necessary

    # 법정 주차대수를 이용해 깎을 때에는 아래 데이터를 추가해 줌
    packed_unit_space_equal_division_area_list_of_list = [[x.area for x in y] for y in packed_unit_space_equal_division]
    packed_unit_space_sequantial_area_list_of_list = [[x.area for x in y] for y in packed_unit_space_sequantial]
    packed_unit_space_area_test_set = [
        packed_unit_space_equal_division_area_list_of_list,
        packed_unit_space_sequantial_area_list_of_list,
    ]

    # 사용된 서비스 면적 표시하기 위해 마지막에 한번 더
    env_plan.packed_unit_space = [
        packed_unit_space_equal_division,
        packed_unit_space_sequantial,
    ][packed_unit_space_area_test_set_index]

    parklot_datas[0] = estimated_parklot_count
    parklot_datas[1] = law_parklot_count
    parklot_datas[2] = packed_unit_space_area_test_set
    parklot_datas[3].append(
        sum(x.area for x in flatten_list(mass_for_parklot_check)) + core.area * len(mass_for_parklot_check)
    )
    parklot_datas[4] = packed_unit_space_area_test_set_index

    return mass_for_parklot_check, parklot_datas, env_plan, law_parklot_count


def gen_parking(
    use_mech_parking,
    use_under_parking,
    core_list,
    hall_geom,
    stair_geom,
    elev_geom,
    parking_result_dict,
    refined_site,
    archi_line,
    road_edge,
    mass: List[Polygon],
    building_purpose,
    is_flag_lot,
    max_far,
    core,
    regulation_cut,
    bounding_box,
    mass_generation_preset,
    time_counter_dict,
    preset_mass_dict,
    mass_angle,
    engine_type,
    mass_after_pack: List[Polygon],
    first_floor_reduce_area,
    estimated_parklot_count,
    regulation_bounds,
    mass_config,
    commercial_type,
    sub_core_related_geoms,
    res,
):

    has_piloti = res["options"]["has_piloti"][0]
    res["regulations"]["max_bcr"]
    res["regulations"]["parking_residential"]
    parking_commercial = res["regulations"]["parking_commercial"]

    parking_cells_wkt_list: List[str] = []
    path = LineString()
    path_poly = None
    sub_path = LineString()
    sub_path_poly = None

    # 기계식 주차 관련 기본값
    mech_turn_table_circle = Polygon()  # interior, exterior boundary 를 둘다 가지고 있는 폴리곤
    Polygon()
    Polygon()
    Polygon()
    ramp_collection: List[Polygon] = []
    underground_parking_boundaries: List[Polygon] = []
    underground_parking_geoms: List[Polygon] = []
    underground_parking_spaces: List[Polygon] = []
    parking_objects_list_of_list: List[List[None]] = []

    (
        sub_core,
        sub_hall_geom,
        sub_stair_geom,
        sub_elev_geom,
        sub_attached_room,
        sub_emergency_elev,
    ) = sub_core_related_geoms

    core_geom_merged = shapely.ops.unary_union([core, sub_core])
    hall_geom_merged = shapely.ops.unary_union([hall_geom, sub_hall_geom, sub_attached_room])
    stair_geom_merged = shapely.ops.unary_union([stair_geom, sub_stair_geom])
    elev_geom_merged = shapely.ops.unary_union([elev_geom, sub_elev_geom, sub_emergency_elev])

    # 추정 주차 대수, 추정 법정 주차 대수, 추정 세대수 , 깎인 면적 정보
    parklot_datas = [
        estimated_parklot_count,
        0,
        [],
        [sum(x.area for x in flatten_list(mass_after_pack)) + core_geom_merged.area * len(mass_after_pack)],
        0,
        parking_cells_wkt_list,
    ]

    if mass_config.build_simple_check_parking:
        mass_for_parklot_check = mass_after_pack

        # 매스 덩어리를 가정한 unit area 를 가지고 가상의 packed_unit_space 생성
        packed_unit_space_equal_division, packed_unit_space_sequantial = mass_for_parklot_check, mass_for_parklot_check

        # 주차대수 만족 체크 위해 임시 env_plan 생성
        env_plan = EnvPlan(
            packed_unit_space_equal_division,
            [None] * estimated_parklot_count,
            consts.PARKING_AREA_DIVISOR,
            commercial_type,
        )
        law_parklot_count_equal_division = env_plan.law_parklot_count

        # 다른 건 동일. 세대만 갈아 끼워서 확인.
        env_plan.packed_unit_space = packed_unit_space_sequantial
        law_parklot_count_sequantial = env_plan.law_parklot_count

        # 법정 주차 대수는 둘 중에 작은 것으로 사용
        if law_parklot_count_equal_division <= law_parklot_count_sequantial:
            law_parklot_count = law_parklot_count_equal_division
            packed_unit_space_area_test_set_index = 0
        else:
            law_parklot_count = law_parklot_count_sequantial
            packed_unit_space_area_test_set_index = 1

        # 법정 주차대수에 따라 층 조절
        mass_after_pack, parklot_datas, env_plan, law_parklot_count = adjust_mass_by_laws(
            mass_for_parklot_check,
            law_parklot_count,
            estimated_parklot_count,
            parklot_datas,
            underground_parking_boundaries,
            regulation_cut,
            bounding_box,
            mass_generation_preset,
            mass_config,
            mass_angle,
            core_geom_merged,
            hall_geom_merged,
            stair_geom_merged,
            elev_geom_merged,
            archi_line,
            time_counter_dict,
            preset_mass_dict,
            regulation_bounds,
            engine_type,
            building_purpose,
            parking_commercial,
            commercial_type,
            first_floor_reduce_area,
            has_piloti,
            packed_unit_space_area_test_set_index,
            packed_unit_space_equal_division,
            packed_unit_space_sequantial,
            res,
            env_plan,
        )

        mass = mass_after_pack

    mech_park_visual_data = None
    under_parking_visul_data = None

    return (
        parklot_datas,
        mass_after_pack,
        mass,
        env_plan,
        path,
        path_poly,
        mech_park_visual_data,
        under_parking_visul_data,
        parking_objects_list_of_list,
        sub_path,
        sub_path_poly,
    )


def postprocess_mass(
    mass,
    has_piloti,
    min_mass_area,
    regulation,
    use_mass_intersection,
    engine_type,
    simple_deadspace_len,
    core,
    use_postprocess_emboss_cut,
    tolerance_angle,
    tolerance,
    postprocess_emboss_cut_length,
    time_counter_dict,
    mass_cut_depth_divider,
    use_deadspace_cut_with_exterior,
    first_floor_reduce_area,
    use_real_parking,
    mass_aspect_ratio_baseline,
    mass_bb_shortest_length_baseline,
    is_mech_park_weight_needed,
    env_plan,
):

    # packing 이후 최소면적 조건을 만족하지 못하는 경우, 층 제거
    mass = check_min_size(mass, has_piloti, regulation, min_mass_area)

    if use_mass_intersection:
        # 연속적으로 위층 매스에서 아래층 매스를 제거. 아래층보다 바깥으로 튀어나오는 매스를 방지함.
        mass = check_mass_intersection(mass, core, engine_type, regulation, simple_deadspace_len)

    if use_postprocess_emboss_cut:
        mass = postprocess_emboss_cut(
            mass,
            core,
            tolerance,
            tolerance_angle,
            regulation,
            postprocess_emboss_cut_length,
            time_counter_dict,
            mass_cut_depth_divider,
        )
    elif has_piloti:
        mass[0] = [wkt.loads("POLYGON EMPTY")]

    # 외곽선 기준 데드스페이스 제거, 사선 형태의 데드스페이스 제거
    if use_deadspace_cut_with_exterior:
        shortest_core_length = min(explode_to_segments(core.exterior), key=lambda s: s.length).length

        postprocess_cut_length = simple_deadspace_len
        if shortest_core_length <= simple_deadspace_len:
            postprocess_cut_length = shortest_core_length - consts.TOLERANCE

        mass = deadspacecut_with_exterior(
            mass, tolerance_angle, tolerance, core, engine_type, postprocess_cut_length, regulation
        )

    # 아래층 밖으로 튀어나오는 면적 및 데드스페이스 제거 후 최소면적 조건을 만족하지 못하는 경우, 층 제거
    mass = check_min_size(mass, has_piloti, regulation, min_mass_area)

    # 형상 점수 계산
    score = get_score(
        core, mass, first_floor_reduce_area, has_piloti, use_real_parking, engine_type == consts.ENGINE_TYPE_BASIC
    )

    # 기계식 주차 score 가중치 적용. 현재는 필요하지 않지만 일단 제거않고 가중치 1.0으로 사용
    # https://teamspacewalk.slack.com/archives/CCAN9MKRP/p1715152655174799?thread_ts=1714610173.934559&cid=CCAN9MKRP
    if is_mech_park_weight_needed:
        score *= consts.MECH_PARK_SCORE_WEIGHT_FACTOR_LIGHT

    # 주차가 모자란 설계안은 제외시키기 위해 score를 0으로 조정.
    # 제외하지 않을 경우 주차가 모자람에도 불구하고 더 높은 gfa를 가지게 되어 주차를 만족한 설계안이 선택되지 않는 경우 발생
    if env_plan.law_parklot_count > env_plan.parklot_count:
        score = consts.LIGHT_SCORE_FOR_PARKLOT_ERROR

    if engine_type == consts.ENGINE_TYPE_BASIC:
        mass = basic_final_postprocessing(mass, core, regulation)

    mass = get_final_mass(mass, core, mass_aspect_ratio_baseline, mass_bb_shortest_length_baseline)
    return mass, score


def create_mass_result(
    engine_type,
    res,
    score,
    core,
    hall_geom,
    stair_geom,
    elev_geom,
    sub_core,
    sub_hall_geom,
    sub_stair_geom,
    sub_elev_geom,
    sub_core_attached_room,
    sub_core_emergency_elev,
    sub_path,
    sub_path_poly,
    mass: List[List[Polygon]],
    mass_angle,
    intermediate_results,
    parklot_datas,
    first_floor_reduce_area,
    path,
    path_poly,
    road_edge,
    core_type,
    sub_core_type,
    core_orientation,
    mech_park_visual_data,
    under_parking_visul_data,
    error_type,
    elev_area_for_advantage,
    env_plan,
    summary_is_escape_core,
    use_small_core,
    has_elevator,
    is_commercial_area,
    has_commercial,
    is_specific_escape_sub_core,
    is_specific_escape_emgcy_elev_sub_core,
    regulation: List[Polygon],
    parking_objects_list_of_list,
    visualize_inside_get_mass,
):
    return {
        "score": score,
        "mass": mass,
        "core": core,
        "regulation": regulation,
        "hall_geom": hall_geom,
        "stair_geom": stair_geom,
        "elev_geom": elev_geom,
        "mass_angle": mass_angle,
        "intermediate_results": intermediate_results,
        "parklot_datas": parklot_datas,
        "first_floor_reduce_area": first_floor_reduce_area,
        "path": path,
        "path_poly": path_poly,
        "road_edge": road_edge,
        "legal_geom": regulation,
        "core_type": core_type,
        "core_orientation": core_orientation,
        "error_type": error_type,
        "elev_area_for_advantage": elev_area_for_advantage,
        "use_small_core": use_small_core,
    }


def get_score(core, mass, first_floor_reduce_area, has_piloti, use_real_parking, is_engine_type_basic):
    """aspect_ratio, ombr_ratio를 사용하여 결과의 점수를 계산

    Args:
        core (Polygon): 코어 폴리곤
        mass (List(List(Polygon))): 층별 매스 폴리곤. 세대구분이 있는 프리미엄과 동일한 형식 사용
        has_piloti (bool): 필로티 여부, 1층에서 용적 제외 용도
        use_real_parking (bool): 실제 주차 배치 사용 여부

    Returns:
        float: 해당 매스의 점수
    """
    if len(mass) == 0:
        raise Exception("매스가 존재하지 않습니다.")
    else:
        total_fa = get_gfa(core, mass, first_floor_reduce_area, has_piloti, use_real_parking, is_engine_type_basic)

        # 점수에서 코어에 해당하는 면적은 제외합니다.
        total_fa -= core.area * len(mass)

        # 실용적이 즉 점수입니다.
        score = total_fa

    return score


def get_gfa(
    core: Polygon,
    mass: List[List[Polygon]],
    first_floor_reduce_area: float,
    has_piloti: bool,
    use_real_parking: bool,
    is_engine_type_basic: bool,
) -> float:
    if mass is None or len(mass) == 0:
        return 0

    gfa = sum(sum(x.area for x in y) for y in mass)

    if not use_real_parking:
        # 1층 필로티 아닐 경우 1층 매스 면적에서 주차 때문에 빠질 영역을 추가 제거 - 필로티일 경우 추가 안하면 됨
        first_floor_mass_area_raw = sum(x.area for x in mass[0])

        if not has_piloti:
            first_floor_mass_area = max(0, first_floor_mass_area_raw - first_floor_reduce_area)

            # 1층 면적이 최소 기준을 만족할 때에만 추가
            if first_floor_mass_area >= consts.UNIT_MIN_AREA:
                gfa += first_floor_mass_area
        else:
            gfa -= first_floor_mass_area_raw

    if not is_engine_type_basic:
        gfa += core.area * len(mass)

    return gfa


def get_final_mass(
    mass: List[List[Polygon]],
    core: Polygon,
    mass_aspect_ratio_baseline: float,
    mass_bb_shortest_length_baseline: float,
) -> List[List[Polygon]]:
    """최종적으로 매스를 정돈한다

    Args:
        mass (List[List[Polygon]]): 층별 매스 도형
        mass_aspect_ratio_baseline (float): 가로 세로 비율 최대 허용값
        core (Polygon): 코어 도형

    Returns:
        List[List[Polygon]]: 최종 층별 매스 도형
    """

    core_segment_coords = np.array(explode_to_segments(core.exterior)[0].coords)
    core_segment_vector = core_segment_coords[1] - core_segment_coords[0]

    # 데드스페이스 제거 이후 1층을 제외한 층에 empty Polygon이 있는지 검사 후 있다면 제거
    # 바운딩박스의 aspect_ratio가 basline 미만인 매스만 허용
    # 바운딩박스의 단변 길이가 baseline 이상이면 aspect_ratio 무시하고 해당 매스는 허용
    final_mass = []
    for emi, each_mass in enumerate(mass):
        if emi == 0:
            final_mass.append(each_mass)
            continue

        each_mass_aspect_ratio, each_mass_bounding_box = get_aspect_ratio(
            each_mass[0], core_segment_vector, return_bb=True
        )

        shortest_bb_length = sorted([s.length for s in explode_to_segments(each_mass_bounding_box.exterior)])[0]

        is_satisfied_shortest_length = True
        is_satisfied_aspect_ratio = True

        is_satisfied_shortest_length = shortest_bb_length >= mass_bb_shortest_length_baseline
        is_satisfied_aspect_ratio = each_mass_aspect_ratio < mass_aspect_ratio_baseline

        if not each_mass[0].is_empty and (is_satisfied_aspect_ratio or is_satisfied_shortest_length):
            final_mass.append([simplify_polygon(each_mass[0])])

    return final_mass


def get_valid_mass_before_placing_core(
    original_mass: List[Polygon],
    regulation: List[Polygon],
    tolerance: float,
    tolerance_angle: float,
    simple_deadspace_len: float,
) -> List[Polygon]:
    """코어 배치 이전 단계에서 유효하지 않은 층별 매스 제거

    Args:
        original_mass (List[Polygon]): 정리 대상 매스
        regulation (List[Polygon]): 법규선
        tolerance (float): 데드스페이스 제거 관련 상수
        tolerance_angle (float): 데드스페이스 제거 관련 상수
        simple_deadspace_len (float): 데드스페이스 제거 관련 상수

    Returns:
        List[Polygon]: 정리 후 층별 매스
    """

    # 멀티폴리곤 및 sliver 제거
    valid_mass = []
    for floor in original_mass:
        floor = filter_polygon(floor)
        floor = buffer_erosion_and_dilation(
            polygon=floor,
            buffer_distance=tolerance,
            use_intersection=True,
            choose_biggest_polygon=True,
        )
        valid_mass.append(floor)

    mass = valid_mass

    # simplify
    simplified_mass = []
    for mfi, mass_floor in enumerate(mass):
        simplified_polygon = simplify_polygon(
            mass_floor, tol_angle=tolerance_angle, tol_length=consts.TOLERANCE, container_geometry=regulation[mfi]
        )
        simplified_mass.append(simplified_polygon)

    mass = simplified_mass

    # NOTE(pch): 코어 배치시 최상층 바운더리가 아래 층보다 튀어나간 경우 코어 배치 성공률이 낮아지므로 intersection 수행
    for i in range(1, len(mass)):
        intersected_mass = mass[i].intersection(mass[i - 1])
        deadspace_removed_mass = buffer_dilation_and_erosion(
            polygon=intersected_mass, buffer_distance=consts.SIMPLE_INTERSECTING_FILL_BUFFER_DISTANCE
        )

        # 데드스페이스 제거 이후 법규선을 초과하면 데드스페이스 제거한 도형 사용하지 않음
        if not deadspace_removed_mass.within(regulation[i]):
            mass[i] = simplify_polygon(intersected_mass)
            continue

        # 매스 외곽선들을 연장시켰을 때 데드스페이스가 있다면 모두 제거될 때까지 반복 실행
        # 1개는 매스 자기자신
        while (
            len(
                remove_deadspace_with_extended_exterior(
                    polygon=deadspace_removed_mass,
                    deadspace_len=simple_deadspace_len,
                    tolerance=tolerance,
                    return_only_splits=True,
                )
            )
            > 1
        ):
            deadspace_removed_mass = remove_deadspace_with_extended_exterior(
                polygon=deadspace_removed_mass,
                deadspace_len=simple_deadspace_len,
                tolerance=tolerance,
            )

        mass[i] = simplify_polygon(deadspace_removed_mass)

    return mass


def get_error_result(e, first_floor_reduce_area, road_edge, engine_type):
    e_message = str(e)

    if e_message == "주차 대수가 0대입니다.":
        error_type = "parking_failed"
    elif e_message == "매스가 존재하지 않습니다.":
        error_type = "mass_creation_failed"
    elif e_message == "기계식주차 배치 실패로 중복 결과가 생성됩니다.":
        error_type = "duplicate_result_mech_park"
    elif e_message == "저층상가 배치 실패로 중복 결과가 생성됩니다.":
        error_type = "duplicate_result_lower_commercial"
    else:
        error_type = e_message

    # Get the dict results
    get_mass_result = create_mass_result(
        engine_type=engine_type,
        res=None,
        score=-10000,
        core=None,
        hall_geom=None,
        stair_geom=None,
        elev_geom=None,
        sub_core=None,
        sub_hall_geom=None,
        sub_stair_geom=None,
        sub_elev_geom=None,
        sub_core_attached_room=None,
        sub_core_emergency_elev=None,
        sub_path=None,
        sub_path_poly=None,
        mass=None,
        mass_angle=None,
        intermediate_results=None,
        parklot_datas=None,
        first_floor_reduce_area=first_floor_reduce_area,
        path=None,
        path_poly=None,
        road_edge=road_edge,
        core_type=None,
        sub_core_type=None,
        core_orientation=None,
        mech_park_visual_data=None,
        under_parking_visul_data=None,
        error_type=error_type,
        elev_area_for_advantage=0,
        env_plan=None,
        summary_is_escape_core=False,
        use_small_core=False,
        has_elevator=False,
        is_commercial_area=False,
        has_commercial=False,
        is_specific_escape_sub_core=False,
        is_specific_escape_emgcy_elev_sub_core=False,
        regulation=None,
        parking_objects_list_of_list=None,
        visualize_inside_get_mass=False,
    )

    return get_mass_result


def get_mass(
    mass_generation_preset,
    refined_site,
    archi_line,
    regulation,
    building_purpose,
    time_counter_dict,
    postprocess_emboss_cut_length,
    estimated_parklot_count,
    first_floor_reduce_area,
    preset_mass_dict,
    parking_result_dict,
    road_edge,
    use_small_core,
    is_commercial_area,
    is_flag_lot,
    use_mech_parking,
    use_under_parking,
    custom_config,
    engine_type,
    mass_config,
    res,
    commercial_type,
    visualize_inside_get_mass,
):
    """매스를 생성합니다.

    Args:
        mass_generation_preset (List(int)): 필지 축 생성 방식, 대각화 여부, 커팅 정책을 결정하는 상수
        refined_site (Polygon): 사이트 도형
        archi_line (Polygon): 건축선 폴리곤
        regulation (List(Polygon)): 일조사선 적용된 층별 법규 폴리곤
        building_purpose (str): 설계 대상 건물 용도
        time_counter_dict (dict[str, float]): 함수별 시간 체크용 dict
        postprocess_emboss_cut_length (float), 최종 단계 엠보스 컷 길이
        estimated_parklot_count (int): 대지 면적으로 가늠한 예상 주차 대수
        first_floor_reduce_area (float): 1층 매스에서 제외해야 할 면적 - 가상 주차로 인해 깎이는 부분을 가정
        preset_mass_dict (dict): 같은 프리셋으로 알 수 있는 매스는 공유하기 위한 dict
        parking_result_dict (dict): 같은 프리셋으로 알 수 있는 주차를 공유하기 위한 dict
        road_edge (dict[str, Any]): 도로 정보
        use_small_core (bool): 소형코어 사용 여부 - 40평 이하인지 면적 확인 (라이트에서는 그럴 경우 둘다 체크)
        is_commercial_area (bool): 상업지역 여부
        is_flag_lot (bool): 자루형필지 여부
        use_mech_parking (bool): 기계식주차 사용 여부
        custom_config (dict): 교체할 config
        engine_type (str): 입력받은 엔진 타입
        mass_config (SimpleConfig): 매스 생성 config. custom_config를 덮어씌움
        res (dict): 엔진입력서비스 데이터
        commercial_type (int): 상가 층수
        visualize_inside_get_mass (bool): visualize 실행 여부
    Returns:
        mass (List(Polygon)): 조건에 따라 생성된 층별 매스 폴리곤
    """

    # save error type if one occurs
    error_type = ""
    get_mass_result_list = []

    try:

        max_far = res["regulations"]["max_far"]
        max_far_with_margin = max_far + mass_config.far_margin_for_commercial

        # 중간 결과 저장
        intermediate_results = []
        regulation = [simplify_polygon(floor, tol_length=consts.TOLERANCE) for floor in regulation]

        mass_length_before_processing = len(regulation)

        # Create the first mass
        make_first_mass_start = time.process_time()
        (
            mass,
            first_mass_polygon,
            intermediate_results,
            bounding_box,
            mass_angle,
            regulation_cut,
            regulation_bounds,
        ) = make_first_mass(
            archi_line,
            regulation,
            mass_generation_preset,
            mass_generation_preset.mass_cut_length,
            mass_generation_preset.gridsize,
            mass_generation_preset.tolerance,
            time_counter_dict,
            preset_mass_dict,
            res["regulations"]["max_bcr"],
            mass_config,
        )

        time.process_time() - make_first_mass_start

        intermediate_results.append(first_mass_polygon)  # BCR컷 결과 1층 매스

        # 나머지 층에서 1층 폴리곤 바깥으로 튀어나오는 면적을 제거 (층별 매스 생성)
        if not mass_config.is_alt_ver:
            mass = [first_mass_polygon]
            for regulation_polygon in regulation[1:]:
                mass.append(regulation_polygon.intersection(first_mass_polygon))

        mass_config.set_core_config(
            archi_line,
            mass,
            building_purpose,
            use_small_core,
            is_commercial_area,
            commercial_type,
            res,
            engine_type,
            use_sub_core=mass_generation_preset.use_sub_core,
        )

        # 건폐율 및 연면적 어드밴티지에 반영할 임시 엘레베이터 면적 생성
        test_core = box(0, 0, mass_config.core_size_list[0][0], mass_config.core_size_list[0][1])
        elev_area_for_advantage = gen_core(
            [test_core],
            mass_config.core_type_list[0],
            [test_core],  # mass - NOTE: 엘레베이터 면적만 확인하고자 하는 거고 방향이 중요하지 않아 임의 도형 삽입
            use_small_core,
            is_commercial_area,
            is_escape_core=mass_config.is_escape_core,
            is_center_core_placed=False,
            is_using_adjusted_core=False,
            is_last_gen_core_called=True,
        )[2][0].area

        # 가장 작은 코어의 크기 - 건폐율 및 연변적에 영향을 미치지 않는 엘레베이터를 제외합니다.
        smallest_core_area = (
            mass_config.core_size_list[0][0] * mass_config.core_size_list[0][1] - elev_area_for_advantage
        )

        # TODO replace this by a call to check_min_size?
        # 최상층부터 코어를 배치할 수 없는 층을 제거
        valid_mass = copy.deepcopy(mass)
        for top_mass in reversed(mass):
            # 최소 면적 14m^2 + 가장 작은 코어 면적 6.72m^2 = 20.72m^2 보다 작은 최상층이 생성되었을 경우, 해당 층을 제거한다.
            # multipolygon인 경우 면적 계산시에 가장 큰 면적의 도형만 사용한다.
            top_mass = filter_polygon(top_mass)
            if top_mass.area < mass_config.min_mass_area + smallest_core_area:
                valid_mass = valid_mass[:-1]
            else:
                break
        mass = valid_mass

        intermediate_results.append(mass)  # FAR컷 이전 전층 매스

        # 용적률 컷 - 알트 버전에서는 여기서는 층수만 컷
        start_far_cut = time.process_time()
        mass = cut_mass_far(
            archi_line,
            bounding_box,
            mass,
            max_far_with_margin,
            smallest_core_area,
            mass_generation_preset,
            res["options"]["has_piloti"][0],
            building_purpose,
            regulation_cut,
            mass_angle,
            mass_generation_preset.mass_cut_length,
            mass_generation_preset.gridsize,
            mass_generation_preset.tolerance,
            time_counter_dict,
            preset_mass_dict,
            regulation_bounds,
            mass_config,
            elev_area_for_advantage,
            use_small_core,
        )
        intermediate_results.append(mass)  # FAR컷 이후 전층 매스

        mass_config.set_core_config(
            archi_line,
            mass,
            building_purpose,
            use_small_core,
            is_commercial_area,
            commercial_type,
            res,
            engine_type,
            use_sub_core=mass_generation_preset.use_sub_core,
        )

        # far_cut 수행시간 합산
        time.process_time() - start_far_cut
        mass = get_valid_mass_before_placing_core(
            mass,
            regulation,
            mass_generation_preset.tolerance,
            mass_config.tolerance_angle,
            mass_config.simple_deadspace_len,
        )

        start_place_cores = time.process_time()
        # Place the core
        core_placement_results = core_placement(
            mass,
            mass_angle,
            mass_generation_preset.tolerance,
            engine_type,
            mass_generation_preset.gridsize,
            refined_site,
            road_edge,
            is_commercial_area,
            use_small_core,
            res["options"]["has_piloti"][0],
            archi_line,
            regulation,
            max_far_with_margin,
            res["regulations"]["max_bcr"],
            mass_config,
        )

        # 베이직은 코어 후보 중 가장 큰 1개만 사용합니다.
        if engine_type == consts.ENGINE_TYPE_BASIC or (mass_config.use_real_parking and use_mech_parking):
            core_placement_results = core_placement_results[:1]

        # core_placement_results 길이가 0인 경우 `finally` 부분에서 index error 발생.
        # 루프 자체를 돌지 않기 때문에 `except` 조건으로 넘어가지 못해서 실패처리 해줘야 함.
        if len(core_placement_results) == 0:
            raise ConstructionError("코어 배치 실패")

        for core_placement_result, sub_core_placement_result in core_placement_results:

            try:
                (
                    mass,
                    mass_after_pack,
                    hall_list,
                    stair_list,
                    elev_list,
                    _,
                    _,
                    core_list,
                    core,
                    core_orientation,
                    core_type,
                    long_core_segs,
                ) = core_placement_result

                (
                    _,
                    _,
                    sub_hall_list,
                    sub_stair_list,
                    sub_elev_list,
                    _,  # sub_core_list
                    sub_core_attached_room_list,
                    sub_core_emergency_elev_list,
                    sub_core,
                    _,  # sub_core_orientation
                    sub_core_type,
                    _,  # sub_long_core_segs
                ) = sub_core_placement_result

                if mass_config.commercial_type > 0 and mass_length_before_processing != len(mass):

                    mass_config.commercial_type = min(
                        mass_config.commercial_type,
                        max(
                            consts.LIGHT_LOWER_COMMERCIAL_FLOOR_MIN + res["options"]["has_piloti"][0],
                            len(mass) - consts.MAX_HOUSING_FLOOR_MAP[building_purpose],
                        ),
                    )

                hall_geom = hall_list[0]
                stair_geom = stair_list[0]
                elev_geom = elev_list[0]

                sub_hall_geom = sub_hall_list[0]
                sub_stair_geom = sub_stair_list[0]
                sub_elev_geom = sub_elev_list[0]
                sub_core_attached_room = sub_core_attached_room_list[0]
                sub_core_emergency_elev = sub_core_emergency_elev_list[0]

                sub_core_related_geoms = (
                    sub_core,
                    sub_hall_geom,
                    sub_stair_geom,  # stair[0]
                    sub_elev_geom,  # elev[0]
                    sub_core_attached_room,
                    sub_core_emergency_elev,
                )

                time.process_time() - start_place_cores

                # Generate the parkings
                start_parking_cut = time.process_time()
                (
                    parklot_datas,
                    mass_after_pack,
                    mass,
                    env_plan,
                    path,
                    path_poly,
                    mech_park_visual_data,
                    under_parking_visul_data,
                    parking_objects_list_of_list,
                    sub_path,
                    sub_path_poly,
                ) = gen_parking(
                    use_mech_parking,
                    use_under_parking,
                    core_list,
                    hall_geom,
                    stair_geom,
                    elev_geom,
                    parking_result_dict,
                    refined_site,
                    archi_line,
                    road_edge,
                    mass,
                    building_purpose,
                    is_flag_lot,
                    max_far,
                    core,
                    regulation_cut,
                    bounding_box,
                    mass_generation_preset,
                    time_counter_dict,
                    preset_mass_dict,
                    mass_angle,
                    engine_type,
                    mass_after_pack,
                    first_floor_reduce_area,
                    estimated_parklot_count,
                    regulation_bounds,
                    mass_config,
                    mass_config.commercial_type,
                    sub_core_related_geoms,
                    res,
                )

                # 코어가 배치되었지만 2개소가 필요하지 않은 규모인 경우 해당 설계안 제거
                if mass_generation_preset.use_sub_core and not mass_config.is_sub_core_necessary:
                    raise ConstructionError("코어 2개소가 배치되지 않아도 되는 설계안에서 코어 2개소가 배치되었습니다.")

                # parking_cut 수행시간 합산
                time.process_time() - start_parking_cut
                mass = mass_after_pack

                intermediate_results.append([x[0] for x in mass])  # packing 실행 이후 전층 매스

                is_mech_park_weight_needed = False

                # Post-process the mass
                mass, score = postprocess_mass(
                    mass,
                    res["options"]["has_piloti"][0],
                    mass_config.min_mass_area,
                    regulation,
                    mass_config.use_mass_intersection,
                    engine_type,
                    mass_config.simple_deadspace_len,
                    core,
                    mass_config.use_postprocess_emboss_cut,
                    mass_config.tolerance_angle,
                    mass_generation_preset.tolerance,
                    postprocess_emboss_cut_length,
                    time_counter_dict,
                    mass_config.mass_cut_depth_divider,
                    mass_config.use_deadspace_cut_with_exterior,
                    first_floor_reduce_area,
                    mass_config.use_real_parking,
                    mass_config.mass_aspect_ratio_baseline,
                    mass_config.mass_bb_shortest_length_baseline,
                    is_mech_park_weight_needed,
                    env_plan,
                )

                summary_is_escape_core = mass_config.is_escape_core

                packed_unit_space_equal_division, packed_unit_space_sequantial = mass, mass

                # 마지막으로 결과 생성 직전에 주차 대수를 한번 더 체크해봅니다.
                mass, parklot_datas, env_plan, _ = adjust_mass_by_laws(
                    mass,
                    parklot_datas[1],
                    parklot_datas[0],
                    parklot_datas,
                    [],  # underground_parking_boundaries
                    regulation_cut,
                    bounding_box,
                    mass_generation_preset,
                    mass_config,
                    mass_angle,
                    shapely.ops.unary_union([core, sub_core]),
                    shapely.ops.unary_union([hall_geom, sub_hall_geom]),
                    shapely.ops.unary_union([stair_geom, sub_stair_geom]),
                    shapely.ops.unary_union([elev_geom, sub_elev_geom]),
                    archi_line,
                    time_counter_dict,
                    preset_mass_dict,
                    regulation_bounds,
                    engine_type,
                    building_purpose,
                    res["regulations"]["parking_commercial"],
                    commercial_type,
                    first_floor_reduce_area,
                    res["options"]["has_piloti"][0],
                    parklot_datas[4],
                    packed_unit_space_equal_division,
                    packed_unit_space_sequantial,
                    res,
                    env_plan,
                )

                # 마지막에 score 업데이트
                score = get_score(
                    core,
                    mass,
                    first_floor_reduce_area,
                    res["options"]["has_piloti"][0],
                    mass_config.use_real_parking,
                    engine_type == consts.ENGINE_TYPE_BASIC,
                )

                # Get the dict results
                get_mass_result = create_mass_result(
                    engine_type,
                    res,
                    score,
                    core,
                    hall_geom,
                    stair_geom,
                    elev_geom,
                    sub_core,
                    sub_hall_geom,
                    sub_stair_geom,
                    sub_elev_geom,
                    sub_core_attached_room,
                    sub_core_emergency_elev,
                    sub_path,
                    sub_path_poly,
                    mass,
                    mass_angle,
                    intermediate_results,
                    parklot_datas,
                    first_floor_reduce_area,
                    path,
                    path_poly,
                    road_edge,
                    core_type,
                    sub_core_type,
                    core_orientation,
                    mech_park_visual_data,
                    under_parking_visul_data,
                    error_type,
                    elev_area_for_advantage,
                    env_plan,
                    summary_is_escape_core,
                    use_small_core,
                    res["options"]["has_elevator"][0],
                    is_commercial_area,
                    res["options"]["has_commercial"][0],
                    mass_config.is_specific_escape_sub_core,
                    mass_config.is_specific_escape_emgcy_elev_sub_core,
                    regulation,
                    parking_objects_list_of_list,
                    visualize_inside_get_mass,
                )

                get_mass_result_list.append(get_mass_result)
            except Exception as e:  # pylint: disable=broad-except
                get_mass_result = get_error_result(e, first_floor_reduce_area, road_edge, engine_type)
                get_mass_result_list.append(get_mass_result)

    except Exception as e:  # pylint: disable=broad-except
        print(e)
        get_mass_result = get_error_result(e, first_floor_reduce_area, road_edge, engine_type)
        get_mass_result_list.append(get_mass_result)

    finally:
        sorted_get_mass_result_list = sorted(get_mass_result_list, key=lambda x: x["score"], reverse=True)
        get_mass_result = sorted_get_mass_result_list[0]

    return get_mass_result


def run_basic(
    site_polygon,
    solar_setback_flag_polygon,
    openspace_buffer_len,
    estimated_parklot_count,
    floor_height,
    solar_setback_min_height,
    solar_setback_ratio_from_user_input,
    mass_generation_preset,
    mass_config,
    engine_input,
):
    refined_site = site_polygon
    archi_line = site_polygon
    max_floor_from_user_input = engine_input["regulations"]["max_floor"]

    regulation = [site_polygon.buffer(-openspace_buffer_len, join_style=JOIN_STYLE.mitre)] * max_floor_from_user_input
    for i, r in enumerate(regulation):
        current_floor_height = floor_height * (i + 1)
        if current_floor_height > solar_setback_min_height:
            regulation[i] = r.intersection(
                shapely.affinity.translate(
                    solar_setback_flag_polygon,
                    0,
                    -solar_setback_ratio_from_user_input * current_floor_height,
                )
            )

    building_purpose = "geunsaeng"
    time_counter_dict = {}
    postprocess_emboss_cut_length = 2.4
    estimated_parklot_count = estimated_parklot_count
    first_floor_reduce_area = 0
    preset_mass_dict = {}
    parking_result_dict = {}
    road_edge = {"edges": []}
    use_small_core = False
    is_commercial_area = solar_setback_ratio_from_user_input == 0.0
    is_flag_lot = False
    use_mech_parking = False
    use_under_parking = False
    engine_type = "basic"

    # Configs
    mass_generation_preset = CustomClassForAttrFromDict(mass_generation_preset)
    mass_config = CustomClassForAttrFromDict(mass_config)
    res = engine_input
    custom_config = {}

    commercial_type = max_floor_from_user_input
    visualize_inside_get_mass = False

    return get_mass(
        mass_generation_preset,
        refined_site,
        archi_line,
        regulation,
        building_purpose,
        time_counter_dict,
        postprocess_emboss_cut_length,
        estimated_parklot_count,
        first_floor_reduce_area,
        preset_mass_dict,
        parking_result_dict,
        road_edge,
        use_small_core,
        is_commercial_area,
        is_flag_lot,
        use_mech_parking,
        use_under_parking,
        custom_config,
        engine_type,
        mass_config,
        res,
        commercial_type,
        visualize_inside_get_mass,
    )


class BasicEngine:
    def __init__(
        self,
        site_polygon_from_user_input: Polygon,
        solar_setback_flag_polygon: Polygon,
        open_space_buffer_len: float,
        estimated_parklot_count: int,
        floor_height: float,
        parking_area_divisor: float,
        has_elevator: bool,
        has_piloti: bool,
        max_bcr: float,
        max_far: float,
        max_floor: int,
        max_height: float,
    ):
        self.site_polygon_from_user_input = site_polygon_from_user_input
        self.solar_setback_flag_polygon = solar_setback_flag_polygon
        self.open_space_buffer_len = open_space_buffer_len
        self.estimated_parklot_count = estimated_parklot_count
        self.floor_height = floor_height
        self.parking_area_divisor = parking_area_divisor
        self.has_elevator = has_elevator
        self.has_piloti = has_piloti
        self.max_bcr = max_bcr
        self.max_far = max_far
        self.max_floor = max_floor
        self.max_height = max_height

    def run(self):
        custom_input_from_user_input = {
            "open_space_buffer_len": self.open_space_buffer_len,
            "estimated_parklot_count": self.estimated_parklot_count,
            "floor_height": self.floor_height,
            "parking_area_divisor": self.parking_area_divisor,
            "has_elevator": self.has_elevator,
            "has_piloti": self.has_piloti,
            "max_bcr": self.max_bcr,
            "max_far": self.max_far,
            "max_floor": self.max_floor,
            "max_height": self.max_height,
        }
        custom_input.update(custom_input_from_user_input)

        estimated_parklot_count_from_user_input = custom_input["estimated_parklot_count"]
        openspace_buffer_len_from_user_input = custom_input["open_space_buffer_len"]
        solar_setback_ratio_from_user_input = custom_input["solar_setback_ratio"]
        floor_height_from_user_input = custom_input["floor_height"]
        solar_setback_min_height_from_user_input = custom_input["solar_setback_min_height"]
        consts.PARKING_AREA_DIVISOR = custom_input["parking_area_divisor"]

        mass_generation_preset_default.update(custom_input)
        mass_config_default.update(custom_input)
        engine_input_default["options"]["has_elevator"] = [custom_input["has_elevator"]]
        engine_input_default["options"]["has_piloti"] = [custom_input["has_piloti"]]
        engine_input_default["options"]["has_commercial"] = [not custom_input["has_piloti"]]
        engine_input_default["regulations"]["max_bcr"] = custom_input["max_bcr"]
        engine_input_default["regulations"]["max_far"] = custom_input["max_far"]
        engine_input_default["regulations"]["max_floor"] = custom_input["max_floor"]
        engine_input_default["regulations"]["max_height"] = custom_input["max_height"]

        # parse
        estimated_parklot_count_from_user_input = int(estimated_parklot_count_from_user_input)
        site_polygon_from_user_input = shapely.ops.orient(self.site_polygon_from_user_input)
        solar_setback_flag_polygon = shapely.ops.orient(self.solar_setback_flag_polygon)

        basic_result = run_basic(
            site_polygon_from_user_input,
            solar_setback_flag_polygon,
            openspace_buffer_len_from_user_input,
            estimated_parklot_count_from_user_input,
            floor_height_from_user_input,
            solar_setback_min_height_from_user_input,
            solar_setback_ratio_from_user_input,
            mass_generation_preset_default,
            mass_config_default,
            engine_input_default,
        )

        basic_result["mass"] = [[shapely.ops.orient(x) for x in y] for y in basic_result["mass"]]
        basic_result["core"] = shapely.ops.orient(basic_result["core"])

        return basic_result
