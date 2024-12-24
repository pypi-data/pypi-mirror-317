from datetime import datetime
import calendar
from typing import List, Dict, Tuple
import pandas as pd
import re

# Lookup Tables
order_status_descriptions = {
    1: "Pending",
    2: "Accepted",
    3: "Open",
    4: "Cancelled",
    5: "Rejected",
    6: "Suspended",
    8: "Yellow Card",
    9: "Closed",
    10: "Red Card",
    11: "Triggered"
}


order_status_reason_descriptions = {
    1: "OK",
    2: "Market does not allow Guaranteed Stop Loss Protection",
    3: "This Market is currently not available on the Trading Platform.",
    4: "Market is Limit Down",
    5: "Market is Limit Up",
    6: "Over Size",
    7: "Oversize",
    8: "Quantity is less than allowed Minimum",
    9: "Market does not allow Orders to be placed",
    10: "Market is Closed",
    11: "Market is Phone Only",
    12: "The Quantity, when divided by the market lot size, should be a whole number.",
    13: "Market is Suspended",
    14: "Trades on this market can not have linked Stop and/or Limit orders.",
    15: "Market does not allow Stop or Stop Loss Protection",
    16: "Market does not allow orders to trigger against Our Price.",
    17: "Market is not available to this Product",
    18: "Market does not allow Orders to be placed",
    19: "Guaranteed Stop Loss Protection exceeds allowed Maximum",
    20: "Quantity Precision is greater than allowed decimal places",
    21: "Expiry Date Time must not be provided",
    22: "A Guaranteed Stop Loss order must always be set to Good Till Cancelled.",
    23: "Guaranteed Stop Loss Protection is not allowed",
    24: "Stop Loss order must be guaranteed.",
    25: "Level is wrong side of price for Order Type and Direction",
    26: "Order must be set to trigger against Our Price.",
    27: "Oversize trade for Binary market.",
    28: "When the order Quantity is within our size, the target type must be set to Our Price.",
    29: "Market does not allow Orders to be placed",
    30: "Market is Long Only",
    31: "This account is not allowed to trade in the supplied currency.",
    32: "Trading Account is Suspended",
    33: "Trading Account is Closed",
    34: "Guaranteed Stop is not allowed",
    35: "The Quantity is below the minimum allowed for the Trading Academy account.",
    36: "Cannot accept order that is not on yellow card.",
    37: "Order is no longer active",
    38: "Order cannot be amended",
    39: "Order is no longer active",
    40: "An Order in an If Done relationship must be of type trade.",
    41: "An Order in an If Done relationship must be of type stop or limit.",
    42: "Orders in OCO Pair must be either Stop or Limit",
    43: "Order Currency must match Market Currency",
    44: "The Market does not allow limited risk guaranteed orders to be placed.",
    45: "A Guaranteed Order cannot be set to trigger against external price.",
    46: "Stop Loss or Take Profit Direction must be opposite to parent Order or Position",
    47: "Cannot trade against market that has a bet per of zero.",
    48: "Stop Loss or Take Profit Quantity must be less than or equal to parent Order or Position",
    49: "Level is not allowed inside Minimum Distance",
    50: "Position with triggered Stop Loss or Take Profit order cannot be closed",
    51: "Order is no longer active",
    52: "Order is no longer active",
    53: "Equity Commission settings could not be determined",
    54: "Order can be only be linked to one Order or Position",
    55: "Unable to calculate the guaranteed order premium due to missing or incorrect settings.",
    56: "The Market must be of type: Binary.",
    57: "All orders must be associated with the same trading account.",
    58: "Position is closed",
    59: "Insufficient Liquidity",
    60: "The Market must be of type: Cash.",
    61: "The bid/offer price entered does not overlap the current bid/offer price.",
    62: "The bid/offer price entered is not valid within the last three seconds.",
    63: "Insufficient Funds",
    64: "The Market underlying currency is not supported by the trading account.",
    65: "Market is not available to this Product",
    66: "Unable to add guaranteed stop loss order as the market does not have the necessary settings.",
    67: "Market State is Indicative",
    68: "Supplied price is in an unavailable state.",
    69: "Client is not allowed to place Orders",
    70: "This Market does not allow orders to be linked in an OCO relationship.",
    71: "Market does not allow Limit or Take Profit Orders",
    72: "This Market does not allow orders to trigger against external price.",
    73: "Stop Loss Protection must be less than or equal to parent Order Quantity",
    74: "Take Profit must be less than or equal to parent Order Quantity",
    75: "The total quantity of guaranteed stop orders must be equal to trade order quantity.",
    76: "Market is Close Only",
    77: "New Open Position is not allowed when closing existing open Positions",
    78: "Total Margin Requirement Limit has been exceeded",
    79: "The quantity will cause the account to exceed the market maximum limited risk order exposure.",
    80: "The order target is set to trigger off the external price but the market prices out of hours.",
    81: "Remaining Position Quantity is less than allowed Minimum",
    82: "Level Precision is greater than allowed decimal places",
    83: "The Bid price is not valid for the market pricing rules.",
    84: "Insufficient Funds",
    85: "Insufficient Funds",
    86: "Insufficient Funds",
    87: "Insufficient Funds",
    88: "Order has Expired",
    89: "Insufficient Funds",
    90: "Closing Price Used For Margin",
    91: "Closing Price Used For Margin",
    92: "ALERT! OBMS has triggered order as it was being loaded.",
    93: "Closing Price Used For Margin",
    94: "Closing Price Used For Margin",
    95: "The Offer price is not valid for the market pricing rules.",
    96: "Expiry Date Time must be provided and set in the future",
    97: "Closing Price Used For Margin",
    98: "Closing Price Used For Margin",
    99: "Closing Price Used For Margin",
    100: "Position Closed",
    101: "Client Cancelled Order",
    102: "Order Rejected",
    103: "OCO Order Completed",
    104: "Client Account Id must match value against Order or Position",
    105: "The trade was placed at an incorrect price.",
    106: "Market Id must match value against Order or Position",
    107: "The trade was placed twice.",
    108: "The trade was placed with an incorrect quantity.",
    109: "Expiry Date Time must be provided",
    110: "The Guaranteed order must always be set to trigger out of hours.",
    111: "Guaranteed Stop Loss Protection Quantity cannot be increased",
    112: "The expiry date/time cannot be changed if order is Good For Day.",
    113: "Cannot cancel a guaranteed stop loss order on a Limited Risk trade.",
    114: "The order status must be set to one of the following: Triggered",
    115: "Unable to calculate non-equity CFD commission due to missing or incorrect settings.",
    116: "Dealing Desk has Triggered Order",
    117: "Unable to determine a price when performing margin simulation for this instruction.",
    118: "Unable to determine a price when performing margin simulation for this instruction.",
    119: "Unable to determine a price when performing margin simulation for this instruction.",
    120: "Unable to determine a price when performing margin simulation for this instruction.",
    121: "Unable to determine a price when performing margin simulation for this instruction.",
    122: "Unable to determine a price when performing margin simulation for this instruction.",
    123: "Unable to determine a price when performing margin simulation for this instruction.",
    124: "DMA Unhandled Exception",
    125: "Total Margin Requirement Limit has been exceeded.",
    126: "Total Margin Requirement Limit has been exceeded.",
    127: "Total Margin Requirement Limit has been exceeded.",
    128: "Total Margin Requirement Limit has been exceeded.",
    129: "Total Margin Requirement Limit has been exceeded.",
    130: "Market does not support Hedge Position",
    131: "This account is not allowed to trade against this market via the hedge ticket.",
    132: "Referral Spread",
    133: "This Market does not support the trading client type.",
    134: "OCO Pair is restricted to Buy Limit/Stop, Buy/Sell Limit, Sell Limit/Sell Stop or Buy/Sell Stop",
    135: "Academy Status is set to New Account",
    136: "Market Roll Date Time has expired",
    137: "Market Last Trading Date Time has expired",
    138: "Quantity is greater than allowed Maximum",
    139: "Market has Expired",
    140: "Watch List Client",
    141: "Watch List Client",
    142: "Client is Close Only",
    143: "Client is not allowed to place Orders",
    144: "Client is not allowed to place Orders",
    145: "Account is currently not allowed to accept new business.",
    146: "Account is currently not allowed online access.",
    147: "Account is currently not allowed to trade online.",
    148: "Gap Tolerance Exceeded",
    149: "Cannot close existing positions on different books",
    150: "Trigger prices of orders in If Done link must be valid.",
    151: "Market Quote Order",
    152: "Orders must be filled in the same order they were Triggered",
    153: "ALERT! OBMS has triggered order at different level to current.",
    154: "Other OCO Order Rejected",
    155: "Order sent to Approval due to Unexpected Error",
    156: "Order cannot be Rejected",
    157: "Auto Closeout",
    158: "Price Tolerance Exceeded",
    159: "Client is not able to place Orders",
    160: "Market is unavailable due to local regulations or account restrictions",
    161: "Order structure is not supported for MetaTrader enabled accounts.",
    162: "Order Quantity does not match Increment Size",
    163: "Unable to calculate FX commission due to missing or incorrect settings.",
    164: "Unable to calculate CFD commission due to missing or incorrect settings.",
    165: "Trading Advisor Allocation Profile contains no managed accounts",
    166: "Market Increment Size is Incorrect",
    167: "An existing managed trade allocation is required.",
    168: "Trading Advisor Order result in managed account rejections",
    169: "Watch List Client",
    170: "Watch List Client",
    171: "Unable to calculate US Dollar Notional commission due to missing or incorrect arguments.",
    172: "Cannot place associated order with no net position.",
    173: "Position cannot be closed with triggered Stop Loss or Take Profit",
    174: "Net Position Quantity exceeds allowed Maximum",
    175: "US Standard Lot settings are missing.",
    176: "Step Margin Bands could not be determined",
    177: "Order is Released to Venue",
    178: "Order is Released to Venue",
    179: "Order is Released to Venue",
    180: "Order is Released to Venue",
    181: "Stop must be provided when opening Position",
    182: "Stop must not be provided when closing Position",
    183: "Close By Position Method is not supported",
    184: "Knockout Stop Level Basis Type can only be specified for Stop Order Type",
    185: "More than one knockout specified",
    186: "Level is wrong side of price",
    187: "Knockout Stop must be guaranteed",
    188: "Level must be set to zero",
    189: "Knockout trigger level is not valid",
    190: "Knockout level is on the wrong side of price",
    191: "Expiry Type must be set to Good Till Cancelled",
    192: "Knockout stop quantity is not same as order quantity",
    193: "Knockout min distance type must be points",
    194: "Level is not allowed inside the Minimum Distance",
    195: "Cannot reject knockout stop approval",
    1000: "Order Id must be provided",
    1001: "Comments can be up to 255 characters",
    1002: "Currency is not supported",
    1003: "Order Direction is not supported",
    1004: "Execution Policy is not supported",
    1005: "Level must be between -9999999 and 9999999",
    1006: "Expiry Type is not supported",
    1007: "Level must be between -9999999 and 9999999",
    1008: "Level Basis must be between 0 and 9999999",
    1009: "Level Basis Type is not supported",
    1010: "OCO Order Request Token must be provided in GUID Format",
    1011: "OCO Order Request Token must refer to Order Request Token of different Order Request",
    1012: "Order Request Token must be provided in GUID Format",
    1013: "Order Type is not supported",
    1014: "Parent Order Request Token must be provided in GUID Format",
    1015: "Parent Order Request Token must refer to Order Request Token of different Order Request",
    1016: "Position Method is not supported",
    1017: "Positions must all be greater than zero",
    1018: "Quantity must be between 0 and 9999999999",
    1019: "Order Reason is not supported",
    1020: "Reference can be up to 100 characters",
    1021: "Risk Book is not supported",
    1022: "Order Request Token must be unique within Request",
    1023: "Associate to Positions must be false",
    1024: "Position Method must not be set to Close By",
    1025: "Currency must match that specified against parent Order",
    1026: "Risk Book must not be provided",
    1027: "Execution Policy is not supported for given Service",
    1028: "Execution Policy must be set to Balance",
    1029: "Expiry Date Time must not be provided",
    1030: "Expiry Type must not be provided",
    1031: "Reference must not be provided",
    1032: "Quantity must not be provided",
    1033: "Order Type must be set to Trade",
    1034: "Execution Policy must be set to Confirmation",
    1035: "Market must not be provided",
    1036: "Position Method must be set to Long And Short",
    1037: "Position Method must be set to FIFO",
    1038: "OCO Order Id is not an active Order",
    1039: "Level must not be provided",
    1040: "Parent Order Id is not an active Order",
    1041: "Position Id is not linked to an open Position",
    1042: "Execution Policy must not be provided where Order Type is Stop or Limit",
    1043: "Level cannot be amended",
    1044: "Position is Closed",
    1045: "Trailing Distance Level Basis Type must only be provided where Order Type is Stop",
    1046: "Level Basis And Level Basis Type must both be provided",
    1047: "OCO Order Id must not be provided",
    1048: "OCO Order Request Token must not be provided",
    1049: "Parent Order Id must not be provided",
    1050: "Parent Order Request Token must not be provided",
    1051: "Position Id must not be provided",
    1052: "Positions must not be provided",
    1053: "Parent Order Status must be Working",
    1054: "Level Basis must not be provided",
    1055 : "Level Basis Type must not be provided",
    1056 : "Parent Order Id and Parent Order Request Token must not both be provided",
    1057 : "Position Id must not be provided if Parent Order Id or Parent Order Request Token is provided",
    1058 : "Position Id must not be provided if OCO Order Id or OCO Order Request Token is provided",
    1059 : "OCO Order Id and OCO Order Request Token must be provided but not both",
    1060 : "Order Request Token must not be provided",
    1061 : "CannotLinkExistingStopLimitOrderToExistingOrderAsStopLossOrTakeProfit",
    1062 : "CannotLinkExistingStopLimitOrderToNewOrderAsStopLossOrTakeProfit",
    1063 : "Protecting Quantity must be less than or equal to parent Position Quantity",
    1064 : "Order Type must be set to Stop or Limit",
    1065 : "Positions must contain a minimum of one Position",
    1066 : "Cannot close Position that has triggered Stop Loss or Take Profit",
    1067 : "Order Id must not be provided",
    1068 : "Positions must be closed in oldest to newest order",
    1069 : "Positions must contain at least one open Position from each side of the market",
    1070 : "Risk Book must be provided",
    1071 : "Position Id must be provided",
    1072 : "Order Reason must not be provided",
    1073 : "Currency must not be provided",
    1074 : "Direction must not be provided",
    1075 : "Order Type must not be provided",
    1076 : "Position Method must not be provided",
    1077 : "Positions must not be provided",
    1078 : "Balance must be between -9999999999 and 9999999999",
    1079 : "Stop Loss And Take Profit must have same parent Order",
    1080 : "Stop Loss And Take Profit must have same parent Position",
    1081 : "Order Id must be unique with Request",
    1082 : "OcoOrderRequestTokenOfStopOrderMustReferToOrderTokenOfLimitOrder",
    1083 : "OcoOrderRequestTokenOfLimitOrderMustReferToOrderTokenOfStopOrder",
    1084 : "Comments must not be provided",
    1085 : "Level Basis Type must not be set to Knockout Stop",
    1086 : "Auto Rollover must be false",
    1087 : "Take Profit Quantity must be less than or equal to parent Position Quantity",
    1088 : "Order could not be completed by matching process",
    1089 : "Parent Order is Cancelled",
    1090 : "Position is Closed",
    1091 : "Position is Cancelled",
    1092 : "Currency must be provided",
    1093 : "Positions must all be on the same side of the market",
    1094 : "Could not complete Order due to Limit breach",
    1095 : "Conversion Rate could not be retrieved",
    1096 : "Margin Check Portfolio prices could not be retrieved",
    1097 : "Entry order not allowed on other side of knockout market",
    1098 : "Risk Book Assignment could not be retrieved",
    1099 : "Execution Rules could not be retrieved",
    1100 : "Fees And Charges Settings could not be retrieved",
    1101 : "Margin Rules Settings could not be retrieved",
    1102 : "Price could not be retrieved",
    1103 : "Bid/Ask Spread would result in new open Position being closed at a Loss",
    1104 : "Step Margin Bands could not be determined",
    1105 : "Unexpected Problem",
    1106 : "knockouts have different knockout levels",
    1107 : "Stop Loss and/or Take Profit Order is already in place",
    1108 : "Converted to Entering Order",
    1109 : "Positions are Closed",
    1110 : "Potential Stale Price",
    1111 : "Unexpected Service Failover",
    1112 : "Firm Reference must refer to Approved Quote",
    1113 : "Trading Account Id must not be provided",
    1114 : "Order is already Released to Venue",
    1115 : "Market Id must be greater than zero",
    1116 : "Trading Account Id must be greater than zero",
    1117 : "Trading Account Id must match value stored against Order or Position",
    1118 : "OCO Order Id is already linked to another Order in OCO relationship",
    1119 : "Market does not allow Negative Price",
    1120 : "Venue Bid must not be less than zero",
    1121 : "Position Method must not be set to Targeted Closure",
    1122 : "Market is Short Only"

}

instruction_status_descriptions = {

    1 : "Accepted",
    2 : "Red Card",
    3 : "Yellow Card",
    4 : "Error",
    5 : "Pending",
    2 : "Red Card",
    3 : "Yellow Card",
    4 : "Error",
    5 : "Pending"

  }

instruction_status_reason_descriptions = {

    1 : "OK",
    2 : "Request Type Id is not supported",
    3 : "Risk Process identifier does not exist",
    4 : "Channel Id must be provided",
    5 : "Session Id must be provided in GUID Format",
    6 : "Instruction source identifier does not exist",
    7 : "Unexpected Error",
    8 : "Underlying bid price must be provided",
    9 : "Underlying offer price must be provided",
    10 : "Additional narrative must be less than or equal to 2500 characters",
    11 : "Price Id must be provided",
    12 : "Bid must be less than or equal to Ask",
    13 : "Order is currently being Approved",
    14 : "Previous Request has already changed the same Orders and/or Positions",
    15 : "Level Basis Type Id is not supported",
    16 : "Level Basis Type Id must be provided",
    17 : "Trigger level calculation value must not be set.",
    18 : "Level Basis must be between 0 and 9999999",
    19 : "Client Reference can be up to 50 characters",
    20 : "Client user identifier does not exist.",
    21 : "Channel Id is not recognised",
    22 : "Invalid Posting Narrative Value",
    23 : "Market Id must be provided",
    24 : "Trading Account Id must be provided",
    25 : "Order of type StopLimitOrderDTO must be provided.",
    26 : "Order of type TradeOrderDTO must be provided.",
    27 : "Position Method Id is not supported",
    28 : "Order Request must be provided",
    29 : "At least one Order Request must be provided",
    30 : "Quantity must be greater than zero",
    32 : "Counter party identifier must be provided.",
    33 : "Currency Id is not supported",
    34 : "Direction identifier does not exist.",
    38 : "Order Id must be provided",
    39 : "Instance of the type IfDoneDTO must be provided.",
    42 : "Decision Price Request must be provided",
    43 : "Bid must be between -9999999 and 9999999",
    45 : "Ask must be between -9999999 and 9999999",
    46 : "Order must be of type Stop or Limit.",
    47 : "Order applicability identifier does not exist.",
    48 : "Order expiry date/time must not be less than the current UTC date/time.",
    50 : "Order target identifier does not exist.",
    51 : "Level must be greater than zero",
    55 : "Market Id is not recognised",
    56 : "Trading Account Id is not recognised",
    60 : "Counter party identifier does not exist.",
    61 : "Order Id or Position Id must reference active Order or open Position",
    68 : "Firm Reference must be provided",
    69 : "Quote is not Pending",
    70 : "Quote Breath Time Seconds must be greater than zero",
    71 : "Bid Adjust must be greater than or equal to zero",
    72 : "Ask Adjust must be greater than or equal to zero",
    73 : "Instruction type is not available via the ITP.",
    75 : "Venue Rejection",
    81 : "Quote must be provided.",
    82 : "Bid AMP adjust must be less than or equal to zero.",
    84 : "Offer AMP adjust must be greater than or equal to zero.",
    87 : "Quote status reason identifier does not exist.",
    89 : "Order status reason identifier does not exist.",
    90 : "Quote type does not exist.",
    91 : "Quantity must be between 0 and 99999999",
    92 : "Child Orders have not been specified",
    93 : "Stop or Limit Order does not support targeted closure",
    95 : "Final Approval Rules",
    96 : "Price Discovery And Execution",
    97 : "Desk source new instruction to trade must have an associated quote.",
    98 : "Hedge instruction does not support quotes.",
    99 : "New stop/limt order must not have an associated quote.",
    100 : "Order type must be set to Limit.",
    101 : "Order type must be set to Stop.",
    102 : "TradeOrderDTO cannot be provided with the UpdateInstructionDTO.",
    103 : "IfDoneDTO Limit order cannot have instance of the type IfDoneDTO.",
    104 : "IfDoneDTO Stop order cannot have instance of the type IfDoneDTO.",
    105 : "Order cannot have an associated instance of the type IfDoneDTO.",
    106 : "Order cannot have an associated OCO order.",
    107 : "Risk process identifier must be provided.",
    108 : "Tolerance must be greater than or equal to zero",
    109 : "Execution broker identifier does not exist",
    110 : "Managed orders may not be cancelled directly. Please cancel the advisory order.",
    111 : "NFA FIFO Account - Stop/Limit restricted",
    112 : "Positions must be closed in oldest to newest order",
    113 : "OBMS cannot update Trigger Price as Trailing Stop has been updated by another process",
    114 : "Simultaneous Long and Short Positions are not allowed",
    115 : "NFA FIFO Account - Cannot place associated order with no net position.",
    116 : "NFA FIFO Account - Associated order of same type already exists.",
    117 : "NFA FIFO Account - Associated order quantity must match net position.",
    118 : "NFA FIFO Account - Can only update order for single position.",
    119 : "Fixed Margin Account - Cannot place Entry Orders",
    120 : "Trade failed fill-or-kill price adjustment",
    121 : "Cannot close Positions with different Stop Levels",
    122 : "Knockout - Targeted closure quantity is more than original order",
    123 : "Knockout - Trigger Level different from original order",
    124 : "Stop cannot be amended",
    125 : "Positions to Close must not be provided",
    126 : "Positions to Close must be provided",
    1000 : "Client Group Id is not supported",
    1001 : "Service Id is not supported",
    1002 : "Venue Type is not supported",
    1003 : "Date Time UTC must be in recognised format",
    1004 : "Firm Reference can be up to 50 characters",
    1005 : "Request Id must be provided in GUID format",
    1006 : "Venue Request Token is not in a valid format",
    1007 : "Span Id can be up to 100 characters",
    1008 : "Span Id is not in a valid format",
    1009 : "Trace Id can be up to 100 characters",
    1010 : "Trace Id is not in a valid format",
    1011 : "Transaction Id must be provided in GUID format",
    1012 : "User Name can be up to 50 characters",
    1013 : "Trading account identifier and username mismatch",
    1014 : "Request Validation",
    1015 : "Oco Request token must match an order request token in request",
    1016 : "Valid order request token must be provided",
    1017 : "Valid Order Type must be specified",
    1018 : "One Order Request Only must be provided",
    1023 : "Order request token must be unique",
    1025 : "Order request token and order id cannot both be specified",
    1029 : "Stop request needs to be sent with new/existing order/position",
    1030 : "Limit request needs to be sent with new/existing order/position",
    1035 : "New Limit order unspecified in the OCO pair",
    1036 : "New Stop order unspecified in the OCO pair",
    1040 : "New order request cannot have existing parent/oco orderid",
    1042 : "Single action must be specified in each execution request",
    1049 : "Expiry Reason Id must be specified",
    1050 : "Request Type Id is not supported for given Service Id",
    1051 : "Invalid metric report provided in request",
    1052 : "Unsupported execution type",
    1053 : "Order must be of type market",
    1054 : "Guaranteed is only applicable to Stop order",
    1055 : "Associated flag must be set",
    1058 : "Client account identifier not recognized",
    1059 : "Client Account Id must be provided",
    1060 : "Two Order Requests must be provided",
    1061 : "Price Request must not be provided",
    1062 : "Service Id must be within Cash Flow Range (201-300)",
    1063 : "Service Id must be within Execution Client Range (1-100)",
    1064 : "Price Type Id is not supported",
    1065 : "Metric Report Type Id is not supported",
    1066 : "Price Type Id must be set to Decision",
    1067 : "KnockoutOptionPlaceOrderMustContainSingleImmediateOrder",
    1068 : "KnockoutOptionPlaceOrderMustNotContainStopLimitOrders",
    1069 : "Level must be equal to Decision Price Request Ask",
    1070 : "Level must be equal to Decision Price Request Bid",
    1071 : "Pre Execution Preparation",
    1072 : "Trading account identifier does not belong to the client",
    1073 : "Request to Report Mapping",
    1074 : "Client And Symbol Rules",
    1075 : "Market State And Order Rules",
    1076 : "Price Discovery And Execution",
    1077 : "Post Execution Rules",
    1078 : "Fees And Charges",
    1079 : "Realised Profit or Loss",
    1080 : "Margin Check",
    1081 : "Final Approval Rules",
    1082 : "Commit And Publish",
    1083 : "Initialization",
    1084 : "Duplicate Request Id",
    1085 : "Request Processing did not start before specified Timeout Date Time UTC",
    1086 : "Ledger Transaction Requests must not be provided",
    1087 : "Timeout Date Time UTC must not be provided",
    1088 : "Custom Settings Request Key must be unique",
    1089 : "Custom Settings Request Key must not be greater than 20 characters",
    1090 : "Custom Settings Request Value must not be greater than 20 characters",
    1092 : "Firm Reference must be set to Quote Id",
    1093 : "Firm Reference must refer to Approved Quote",
    1094 : "Quote Reason Id must be greater than zero",
    1095 : "Post Execution Preparation",
    1096 : "Execution Rules cannot be retrieved",
    1097 : "Price cannot be retrieved",
    1098 : "FX Rate cannot be retrieved",
    1099 : "Margin Rules cannot be retrieved"
}

order_action_type_descriptions = {

    1 : "Opening Order",
    2 : "Full Close",
    3 : "Part Close",
    4 : "Quantity Decrease",
    5 : "Quantity Increase",
    6 : "Add Order",
    7 : "Rolled Order",
    8 : "Cancelled Order"
  }

# Functions
def get_instruction_status_description(status_code: int) -> str:
    """
    Retrieve the description of an instruction status code.
    """
    return instruction_status_descriptions.get(status_code, "Unknown status code")

def get_instruction_status_reason_description(reason_code: int) -> str:
    """
    Retrieve the description of an instruction status reason code.
    """
    return instruction_status_reason_descriptions.get(reason_code, "Unknown reason code")

def get_order_status_description(status_code: int) -> str:
    """
    Retrieve the description of an order status code.
    """
    return order_status_descriptions.get(status_code, "Unknown status code")

def get_order_status_reason_description(reason_code: int) -> str:
    """
    Retrieve the description of an order status reason code.
    """
    return order_status_reason_descriptions.get(reason_code, "Unknown reason code")

def get_order_action_type_description(action_type_code: int) -> str:
    """
    Retrieve the description of an order action type code.
    """
    return order_action_type_descriptions.get(action_type_code, "Unknown action type code")

def extract_every_nth(n_months: int = 6, by_time: str = '15min', n: int = 3900):
    """
    Generate start and stop Unix UTC timestamps for API requests.
    """
    end_time = datetime.utcnow()
    start_time = end_time - pd.DateOffset(months=n_months)

    # Generate date range in UTC
    time_seq = pd.date_range(start=start_time, end=end_time, freq=by_time, tz="UTC")

    intervals = []
    for i in range(0, len(time_seq), n):
        start_dt = time_seq[i]
        if i + n < len(time_seq):
            end_dt = time_seq[i + n]
        else:
            end_dt = time_seq[-1]

        # Use .timestamp() to get POSIX timestamp in UTC
        start_utc = int(start_dt.timestamp())
        end_utc = int(end_dt.timestamp())

        intervals.append((start_utc, end_utc))

    return intervals



def convert_to_dataframe(data: list) -> pd.DataFrame:
    """
    Convert a list of dictionaries with a '/Date(...)' timestamp into a pandas DataFrame
    with a nicely formatted datetime column.
    
    :param data: A list of dictionaries, each containing 'BarDate' or 'TickDate' keys with '/Date(...)' format.
    :return: A pandas DataFrame with a 'Date' column as a datetime and other columns as numeric data.
    """
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Extract the timestamp in milliseconds from the '/Date(...)' format.
    # For example: '/Date(1732075200000)/' -> '1732075200000'
    df['BarDate'] = df['BarDate'].apply(lambda x: int(re.findall(r'\d+', x)[0]))
    
    # Convert milliseconds to datetime
    df['Date'] = pd.to_datetime(df['BarDate'], unit='ms', utc=True)
    
    # Drop the old 'BarDate' column or rename it
    df.drop(columns=['BarDate'], inplace=True)
    
    # Optionally, convert to local timezone if desired:
    # df['Date'] = df['Date'].dt.tz_convert('Asia/Singapore')
    
    # Reorder columns so that Date is first
    cols = ['Date'] + [col for col in df.columns if col != 'Date']
    df = df[cols]
    
    return df


def convert_orders_to_dataframe(data):
    """
    Convert nested order data to a Pandas DataFrame.
    
    Args:
        data (dict): Nested dictionary containing ActiveOrders data.
    
    Returns:
        pd.DataFrame: Flattened DataFrame with relevant fields.
    """
    def convert_date(date_str):
        """Convert '/Date(timestamp)/' to datetime."""
        if date_str and date_str.startswith('/Date('):
            timestamp = int(date_str[6:-2])
            return pd.to_datetime(timestamp, unit='ms')
        return None

    # Flatten and extract relevant fields
    orders = [
        {
            **order['TradeOrder'],
            'StopLimitOrder': order.get('StopLimitOrder'),
            'OuterTypeId': order.get('TypeId')  # Renaming outer TypeId to avoid overwriting
        }
        for order in data.get('ActiveOrders', [])
    ]

    # Create DataFrame
    df = pd.DataFrame(orders)

    # Convert date fields to datetime
    for date_field in ['CreatedDateTimeUTC', 'LastChangedDateTimeUTC', 'ExecutedDateTimeUTC']:
        if date_field in df.columns:
            df[date_field] = df[date_field].apply(convert_date)

    return df
