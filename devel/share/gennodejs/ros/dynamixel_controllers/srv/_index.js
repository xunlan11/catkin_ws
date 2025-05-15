
"use strict";

let TorqueEnable = require('./TorqueEnable.js')
let StartController = require('./StartController.js')
let SetComplianceSlope = require('./SetComplianceSlope.js')
let SetCompliancePunch = require('./SetCompliancePunch.js')
let SetComplianceMargin = require('./SetComplianceMargin.js')
let SetSpeed = require('./SetSpeed.js')
let RestartController = require('./RestartController.js')
let StopController = require('./StopController.js')
let SetTorqueLimit = require('./SetTorqueLimit.js')

module.exports = {
  TorqueEnable: TorqueEnable,
  StartController: StartController,
  SetComplianceSlope: SetComplianceSlope,
  SetCompliancePunch: SetCompliancePunch,
  SetComplianceMargin: SetComplianceMargin,
  SetSpeed: SetSpeed,
  RestartController: RestartController,
  StopController: StopController,
  SetTorqueLimit: SetTorqueLimit,
};
