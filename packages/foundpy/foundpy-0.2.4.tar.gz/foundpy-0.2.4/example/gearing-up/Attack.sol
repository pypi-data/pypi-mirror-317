// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "./GearingUp.sol";

contract Attack {
    GearingUp public GU;

    constructor(address _GU) payable{
        GU = GearingUp(_GU);
        GU.callThis();
        GU.sendMoneyHere{value: 5 ether}();
        GU.withdrawReward();
        GU.sendSomeData("GearNumber1", 687221, bytes4(0x1a2b3c4d), address(this));
        GU.completedGearingUp();
    }

    function isSolved() public view returns(bool){
        return GU.allFinished();
    }

}
