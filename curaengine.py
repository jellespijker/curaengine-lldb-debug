import lldb


def __lldb_init_module(debugger, internal_dict):
    lldb.formatters.Logger._lldb_formatters_debug_level = 2
    logger = lldb.formatters.Logger.Logger()
    logger >> "curaengine lldb tools init"

    simpleValues = ['Temperature',
                    'Velocity',
                    'Acceleration',
                    'LayerIndex',
                    'Ratio',
                    'AngleDegrees']
    for sv in simpleValues:
        debugger.HandleCommand("type summary add -F {}.getSimpleValueSummary cura::{}".format(__name__, sv))

    debugger.HandleCommand("type summary add -F " + __name__ + ".PointSummary cura::Point3")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ClipperLibIntPointSummary cura::Point")
    debugger.HandleCommand("type summary add -F " + __name__ + ".AABB3DSummary cura::AABB3D")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ExtruderTrainSummary cura::ExtruderTrain")
    debugger.HandleCommand("type summary add -F " + __name__ + ".LayerPlanSummary cura::LayerPlan")


def getSimpleValueSummary(value, internal_dict):
    return "<{} = {}>".format(value.GetDisplayTypeName(), value.GetChildMemberWithName("value").GetValueAsSigned())


def getAxisValues(value, axes='xyz'):
    return {
        axis: value.GetChildMemberWithName("x").GetValueAsSigned()
        for axis in axes
    }


def PointSummary(value, internal_dict):
    return "<{} = [x: {x}, y: {y}, z: {z}]>".format(value.GetDisplayTypeName(), **getAxisValues(value))


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
                                 value.GetChildMemberWithName("extruder_nr").GetValueAsUnsigned())
