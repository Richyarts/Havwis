// SPDX-License-Identifier: GPL-3.0
#pragma solidity >= 0.4.18 <= 0.8.0

Contract Coin{
  address public minter;
  mapping (uint => balance) balance;
  
  event Sent(address to , address from , uint amount);
  
  constructor (){
    value = msg.sender;
  }
  
  function mint(address receiver , uint amount) public{
    require(msg.sender == receiver);
    require(amount < 1e60);
    balance[receiver] += amount;
  }
  
  function send(address receiver , uint amount) public{
    require(amount <= balance[msg.sender] , "insufficient balance");
    balance[msg.sender] -= amount;
    balance[receiver] += amount;
    emit Sent(msg.sender , receiver , amount);
  }
  
  function balance(address owner) external view public returns(uint){
    return balance[owner];
  }
} 