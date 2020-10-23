import lldb


def __lldb_init_module(debugger, internal_dict):
    lldb.formatters.Logger._lldb_formatters_debug_level = 2
    logger = lldb.formatters.Logger.Logger()
    logger >> "curaengine lldb tools init"

    simpleValues = ['Temperature',
                    'Velocity',
                    'Acceleration',
                    'LayerIndex',
                    'AngleDegrees',
                    'Ratio']
    for sv in simpleValues:
        debugger.HandleCommand("type summary add -F {}.getSimpleValueSummary cura::{}".format(__name__, sv))

    debugger.HandleCommand("type summary add -F " + __name__ + ".PointSummary cura::Point")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ClipperLibIntPointSummary cura::Point")
    debugger.HandleCommand("type summary add -F " + __name__ + ".AABB3DSummary cura::AABB3D")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ExtruderTrainSummary cura::ExtruderTrain")
    debugger.HandleCommand("type summary add -F " + __name__ + ".LayerPlanSummary cura::LayerPlan")
    debugger.HandleCommand("type summary add -F " + __name__ + ".PolygonsSummary cura::Polygons")
    debugger.HandleCommand("type summary add -F " + __name__ + ".WallToolPathsSummary cura::WallToolPaths")


def getSimpleValueSummary(value, internal_dict):
    return "<{} = {}>".format(value.GetDisplayTypeName(), value.GetChildMemberWithName("value").GetValue())


def getAxisValues(value, axes='xyz'):
    return {
        axis: value.GetChildMemberWithName("x").GetValueAsSigned()
        for axis in axes
    }


def PointSummary(value, internal_dict):
    return "<{} = [x: {}, y: {}]>".format(value.GetDisplayTypeName(), value.GetChildMemberWithName("X").GetValueAsSigned(), value.GetChildMemberWithName("X").GetValueAsSigned())


def AABB3DSummary(value, internal_dict):
    kwret = {}
    for bound in ['min', 'max']:
        axes = getAxisValues(value.GetChildMemberWithName(bound))
        kwret.update(dict(zip(['{}_{}'.format(k, bound) for k in axes.keys()], axes.values())))
    return "<{} = min[x: {x_min}, y: {y_min}, z: {z_min} ... max[x: {x_max}, y: {y_max}, z: {z_max}>".format(
        value.GetDisplayTypeName(), **kwret)


def ClipperLibIntPointSummary(value, internal_dict):
    return "<{} = [x: {X}, y: {Y}]>".format(value.GetDisplayTypeName(), **getAxisValues(value, axes='XY'))


def ExtruderTrainSummary(value, internal_dict):
    return "<{} nr = {}>".format(value.GetDisplayTypeName(),
                                 value.GetChildMemberWithName("extruder_nr").GetValueAsUnsigned())


def LayerPlanSummary(value, internal_dict):
    # todo: make better
    return "<{} nr = {}>".format(value.GetDisplayTypeName(),
                                 value.GetChildMemberWithName("layer_nr").GetChildMemberWithName("value").GetValueAsSigned())

def PolygonsSummary(value, internal_dict):
    paths = value.GetChildMemberWithName("paths")
    summary = ""
    if paths is None:
        return
    for i in range(paths.GetNumChildren()):
        path = paths.GetChildAtIndex(i)
        if path is None:
            return
        polypath = []
        for j in range(path.GetNumChildren()):
            line = path.GetChildAtIndex(j)
            if line is None:
                return
            polypath.append([line.GetChildMemberWithName("X").GetValueAsSigned(), line.GetChildMemberWithName("Y").GetValueAsSigned()])
        summary += "{}, ".format(polypath)
    return "[{}]".format(summary[:-2])

def WallToolPathsSummary(value, internal_dict):
    return "<{} = no walls: {} with a width of 0th: {}, xth: {}, strategy type: {}>".format(value.GetDisplayTypeName(), value.GetChildMemberWithName("inset_count").GetValueAsSigned(), value.GetChildMemberWithName("bead_width_0").GetValueAsSigned(), value.GetChildMemberWithName("bead_width_x").GetValueAsSigned(), value.GetChildMemberWithName("strategy_type") )