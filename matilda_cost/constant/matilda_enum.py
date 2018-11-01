import enum


class Field(enum.Enum):
    granularity = "Granularity"
    group_by = "GroupBy"
    tag = "Tag"
    dimension = "Dimension"
    filter = "Filter"
    time_period = "TimePeriod"
    metrics = "Metrics"


class Granularity(enum.Enum):
    daily = "DAILY"
    monthly = "MONTHLY"

class GroupByConstants(enum.Enum):
    default_group_by_type = "DIMENSION"
    default_group_by_key = "SERVICE"
    group_by_tag = "TAG"
    group_by_dimension = "DIMENSION"
    group_by_component_name = "GroupBy"
    max_group_by = 2

class FilterByConstants(enum.Enum):
    input_dimension = "Dimensions"
    input_tag = "Tags"

class FormatterConstants(enum.Enum):
    # input params
    time_period = "TimePeriod"
    # date = "date"
    #kendo date
    date = "category"
    start_date = "Start"
    end_date = "End"
    input_metrics = "Metrics"
    groups = "Groups"
    input_keys = "Keys"
    amount = "Amount"
    input_total = "Total"

    # output params
    # output_metrics = "metrics"
    #kendo metrics
    output_metrics = "bar_stack_data"
    response = "response"
    # kendo value
    # value = "value"
    value = "values"
    total = "total"
    metric = "metric"
    key = "key"
    # kendo
    # cost = "cost"
    cost = "value"
    y_axis = "yaxis"
    title = "Title"
    unit = "unit"
    type = "type"
    pie_data = "pie_data"