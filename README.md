# ION-Update (DEPRECATED)
Keeps IONOS Public (A)Records updated with your current Public IP
**Please use the new version, rewritten in Rust. [Link](https://hub.docker.com/r/jimurrito/ionupdate_rs)**

https://hub.docker.com/r/jimurrito/ionupdate

Enviromental variables
  
  [Required]
  
  SCOPE -- Defines the domain names the application should monitor. One domain per call of Scope.
  
  PUBKEY -- Public key Prefix provided when private key was generated.
  
  PRVKEY -- The private key generated from IONOS.
  
  
  [Optional]
  
  Both the following are used for the idle interval. This sets the interval that the application will check for a change to your IP address.
  Value defaults to "1 Day", if these are not provided
  
  UNIT -- Idle interval unit ("days" or "hours").
  
  AMOUNT -- Amount of units to idle.
