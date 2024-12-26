# Auto Hack
* note the professional version is being beta tested.

## This does automated vulnerability enumeration and recommends exploits.<br><br>

### How to Run

* [Install Docker](https://docs.docker.com/engine/install/)


* Create AutoHack Docker container
  ```
  docker run -it --net=host -v ${PWD}/portal:/root/portal hdizzle/autohack 
  ```
  Command above does the following:
  * creates Docker container based on the [AutoHack image](https://registry.hub.docker.com/r/hdizzle/autohack)
  * mounts a folder named `portal` in current directory
    * this allows us to persist the AutoHack results once the <br>container is destroyed
  * allows us to access the terminal of the AutoHack container


* Run AutoHack
  ```
  autohack -i <some ip address>
  ```
