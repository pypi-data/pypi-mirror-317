from __future__ import annotations
from typing import Literal, Optional, List

from enum import Enum

from aas_pydantic import (
    AAS,
    Submodel,
    SubmodelElementCollection,
)
from sdm_reference_model.processes import ProcessAttributes
from sdm_reference_model.distribution import (
    ABSTRACT_REAL_DISTRIBUTION,
    DistributionTypeEnum,
)

ProcessAttributes.model_rebuild()


class ProcedureTypeEnum(str, Enum):
    """
    Enum to describe the type of a procedure.
    """

    PRODUCTION = "Production"
    TRANSPORT = "Transport"
    LOADING = "Loading"
    SETUP = "Setup"
    BREAKDOWN = "Breakdown"
    MAINTENANCE = "Maintenance"
    STAND_BY = "StandBy"
    WAITING = "Waiting"
    OFF = "Off"
    NON_SCHEDULED = "NonScheduled"
    ORDER_RELEASE = "OrderRelease"
    ORDER_SHIPPING = "OrderShipping"


class ActivityTypeEnum(str, Enum):
    """
    Enum to describe the type of an activity.
    """

    START = "Start"
    END = "End"
    START_INTERUPT = "StartInterupt"
    END_INTERUPT = "EndInterupt"


class Event(SubmodelElementCollection):
    """
    The Event class represents an event in the execution of a procedure. It contains the time of the event, the resource that executed the event, the procedure that was executed, the activity that was executed, the product that was produced, and whether the event was successful or not.

    Args:
        time (float): The time of the event.
        resource_id (str): The id of the resource that executed the event.
        procedure_id (str): The id of the procedure that was executed.
        procedure_type (ProcedureTypeEnum): The type of the procedure that was executed.
        activity (str): The activity that was executed.
        product_id (Optional[str]): The id of the product that was produced.
        expected_end_time (Optional[float]): The expected end time of the event.
        actual_end_time (Optional[float]): The actual end time of the event.
        success (Optional[bool]): Whether the event was successful or not.
    """

    time: str
    resource_id: str
    procedure_id: str
    procedure_type: ProcedureTypeEnum
    activity: ActivityTypeEnum
    product_id: Optional[str] = None
    expected_end_time: Optional[str] = None
    actual_end_time: Optional[str] = None
    success: Optional[bool] = None


class ExecutionModel(Submodel):
    """
    The ExecutionModel represents all planned (scheduled) and performed (executed) execution of a process. It contains the schedule of the process, and the execution log of the process.

    Args:
        id (str): The id of the execution model.
        description (Optional[str]): The description of the execution model.
        id_short (Optional[str]): The short id of the execution model.
        semantic_id (Optional[str]): The semantic id of the execution model.
        schedule (List[Event]): The schedule of the procedure.
        execution_log (List[Event]): The execution log of the procedure.
    """

    schedule: Optional[List[Event]] = None
    execution_log: Optional[List[Event]] = None


class TransportTime(SubmodelElementCollection):
    """
    This class represents a transport time where the required time for transport between and origin and a target is specified.

    Args:
        origin_id (str): Id of the resource where the transport starts
        target_id (str): Id of the resource where the transport ends
        transport_time (float): Time needed for the transport in seconds.
    """

    origin_id: str
    target_id: str
    transport_time: float


class TimeModel(Submodel):
    """
    Submodel containing parameters to represent the timely duration of a procedure. All times are specified in minutes unless otherwise stated.

    Args:
        id (str): The id of the time model.
        description (Optional[str]): The description of the time model.
        id_short (Optional[str]): The short id of the time model.
        semantic_id (Optional[str]): The semantic id of the time model.
        type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time model.
        sequence (Optional[List[float]]): The sequence of timely values (only for sequential time models).
        repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential time models).
        distribution_type (Optional[str]): The name of the distribution (e.g. "normal", "exponential", "weibull", "lognormal", "gamma", "beta", "uniform", "triangular", "discrete") (only for distribution time models).
        distribution_parameters (Optional[List[float]]): The parameters of the distribution (1: location, 2: scale, 3 and 4: shape) (only for distribution time models).
        speed (Optional[float]): The speed of the resource (only for distance-based time models) in m / s.
        rotation_speed (Optional[float]): The rotation speed of the resource (only for distance-based time models) in degree / s.
        reaction_time (Optional[float]): The reaction time of the resource (only for distance-based time models) in s.
        acceleration (Optional[float]): The acceleration of the resource (only for distance-based time models) in m^2/s.
        deceleration (Optional[float]): The deceleration of the resource (only for distance-based time models) in m^2/s.
    """

    type_: Literal["sequential", "distribution", "distance_based"]
    sequence: Optional[List[float]] = None
    repeat: Optional[bool] = None
    distribution_type: Optional[DistributionTypeEnum] = None
    distribution_parameters: Optional[ABSTRACT_REAL_DISTRIBUTION] = None
    speed: Optional[float] = None
    rotation_speed: Optional[float] = None
    reaction_time: Optional[float] = None
    acceleration: Optional[float] = None
    deceleration: Optional[float] = None
    transport_times: Optional[List[TransportTime]] = None


class ProcedureInformation(Submodel):
    """
    Submodel containing general information about the procedure.

    Args:
        procedure_type (ProcedureTypeEnum): The type of the procedure.
        name (Optional[str]): The name of the procedure.
    """

    procedure_type: ProcedureTypeEnum
    name: Optional[str] = None


class ProcedureConsumption(Submodel):
    """
    Submodel containing the specification of a procedure.

    Args:
        power_consumption (Optional[float]): The power consumption of the procedure.
        water_consumption (Optional[float]): The water consumption of the procedure.

    """

    power_consumption: Optional[float] = None
    water_consumption: Optional[float] = None


class Procedure(AAS):
    """
    The Procedure class represents a procedure that is executed by a resource. It contains the process
    attributes, the execution model, and the time model of the procedure.

    Args:
        id (str): The id of the procedure.
        description (Optional[str]): The description of the procedure.
        id_short (Optional[str]): The short id of the procedure.
        process_attributes (processes.ProcessAttributes): Parameters that describe what the procedure does and how it does it.
        execution (ExecutionModel): The execution model of the procedure containing planned and performed executions of this procedure.
        time_model (TimeModel): The time model of the procedure containing parameters to represent the timely duration of the procedure.

    """

    procedure_information: ProcedureInformation
    process_attributes: Optional[ProcessAttributes] = None
    execution_model: Optional[ExecutionModel] = None
    time_model: Optional[TimeModel] = None
    procedure_consumption: Optional[ProcedureConsumption] = None
